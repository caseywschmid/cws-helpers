"""
Tests for error handling in the Google helper module.

These tests focus on error handling paths to improve coverage.
"""

import pytest
from unittest.mock import MagicMock, patch, mock_open
from cws_helpers import GoogleHelper
from google.auth.exceptions import RefreshError


@pytest.fixture
def mock_credentials():
    """Mock Google credentials for testing."""
    mock_creds = MagicMock()
    mock_creds.valid = True
    mock_creds.to_json.return_value = '{"token": "mock_token"}'
    return mock_creds


@pytest.fixture
def mock_sheets_service():
    """Mock Google Sheets service for testing."""
    mock_service = MagicMock()
    mock_values = MagicMock()
    mock_service.spreadsheets.return_value.values.return_value = mock_values
    mock_service.spreadsheets.return_value.get = MagicMock()
    return mock_service


@pytest.fixture
def mock_drive_service():
    """Mock Google Drive service for testing."""
    mock_service = MagicMock()
    mock_files = MagicMock()
    mock_service.files.return_value = mock_files
    return mock_service


@pytest.fixture
def mock_docs_service():
    """Mock Google Docs service for testing."""
    mock_service = MagicMock()
    mock_documents = MagicMock()
    mock_service.documents.return_value = mock_documents
    return mock_service


class TestGoogleHelperInitialization:
    """Test cases for GoogleHelper initialization and credential handling."""

    @patch('cws_helpers.google_helper.google_helper.Credentials')
    @patch('cws_helpers.google_helper.google_helper.InstalledAppFlow')
    @patch('cws_helpers.google_helper.google_helper.build')
    @patch('cws_helpers.google_helper.google_helper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_no_token_file(self, mock_file_open, mock_path_exists, mock_build, mock_flow, mock_credentials_class):
        """Test initialization when token.json doesn't exist."""
        # Arrange
        mock_path_exists.side_effect = lambda path: path != "token.json"  # Only token.json doesn't exist
        mock_flow_instance = MagicMock()
        mock_flow.from_client_secrets_file.return_value = mock_flow_instance
        
        # Mock credentials properly
        mock_creds = MagicMock()
        mock_creds.to_json.return_value = '{"token": "mock_token"}'
        mock_flow_instance.run_local_server.return_value = mock_creds
        
        # Act
        with patch.object(GoogleHelper, '_get_service', return_value=MagicMock()):
            helper = GoogleHelper()
        
        # Assert
        assert helper is not None
        mock_flow.from_client_secrets_file.assert_called_once()
        mock_flow_instance.run_local_server.assert_called_once()
        mock_file_open.assert_called()

    @patch('cws_helpers.google_helper.google_helper.Credentials')
    @patch('cws_helpers.google_helper.google_helper.InstalledAppFlow')
    @patch('cws_helpers.google_helper.google_helper.build')
    @patch('cws_helpers.google_helper.google_helper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_invalid_token(self, mock_file_open, mock_path_exists, mock_build, mock_flow, mock_credentials_class):
        """Test initialization when token exists but is invalid."""
        # Arrange
        mock_path_exists.return_value = True
        mock_creds = MagicMock()
        mock_credentials_class.from_authorized_user_file.return_value = mock_creds
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "refresh_token"
        
        # Act
        with patch.object(GoogleHelper, '_get_service', return_value=MagicMock()):
            helper = GoogleHelper()
        
        # Assert
        assert helper is not None
        mock_credentials_class.from_authorized_user_file.assert_called_once()
        mock_creds.refresh.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.Credentials')
    @patch('cws_helpers.google_helper.google_helper.InstalledAppFlow')
    @patch('cws_helpers.google_helper.google_helper.build')
    @patch('cws_helpers.google_helper.google_helper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_refresh_error(self, mock_file_open, mock_path_exists, mock_build, mock_flow, mock_credentials_class):
        """Test initialization when token refresh fails."""
        # Arrange
        mock_path_exists.return_value = True
        mock_creds = MagicMock()
        mock_credentials_class.from_authorized_user_file.return_value = mock_creds
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "refresh_token"
        mock_creds.refresh.side_effect = RefreshError("Token refresh failed")
        
        mock_flow_instance = MagicMock()
        mock_flow.from_client_secrets_file.return_value = mock_flow_instance
        
        # Mock credentials properly
        new_creds = MagicMock()
        new_creds.to_json.return_value = '{"token": "mock_token"}'
        mock_flow_instance.run_local_server.return_value = new_creds
        
        # Act
        with patch.object(GoogleHelper, '_get_service', return_value=MagicMock()):
            helper = GoogleHelper()
        
        # Assert
        assert helper is not None
        mock_flow.from_client_secrets_file.assert_called_once()
        mock_flow_instance.run_local_server.assert_called_once()


class TestSheetsHandlerErrorHandling:
    """Test cases for error handling in SheetsHandler."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_read_range_error(self, mock_build, mock_credentials, mock_sheets_service):
        """Test read_range method with error."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.get = mock_get
        mock_get.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            result = helper.sheets.read_range(
                spreadsheet_id="test_id",
                sheet_name="Sheet1",
                start_cell="A1",
                end_cell="B10"
            )
        
        # Assert
        assert result == []  # Should return empty list on error
        mock_get.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_write_range_error(self, mock_build, mock_credentials, mock_sheets_service):
        """Test write_range method with error."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_update = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.update = mock_update
        mock_update.return_value.execute.side_effect = Exception("API Error")
        test_values = [["A1", "B1"], ["A2", "B2"]]
        
        # Act & Assert
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            
            # Should raise exception
            with pytest.raises(Exception):
                helper.sheets.write_range(
                    spreadsheet_id="test_id",
                    values=test_values,
                    sheet_name="Sheet1",
                    start_cell="A1"
                )
        
        mock_update.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_clear_range_error(self, mock_build, mock_credentials, mock_sheets_service):
        """Test clear_range method with error."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_clear = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.clear = mock_clear
        mock_clear.return_value.execute.side_effect = Exception("API Error")
        
        # Act & Assert
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            
            # Should raise exception
            with pytest.raises(Exception):
                helper.sheets.clear_range(
                    spreadsheet_id="test_id",
                    sheet_name="Sheet1",
                    start_cell="A1",
                    end_cell="B10"
                )
        
        mock_clear.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_first_sheet_name_error(self, mock_build, mock_credentials, mock_sheets_service):
        """Test get_first_sheet_name method with error."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = mock_sheets_service.spreadsheets.return_value.get
        mock_get.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            result = helper.sheets.get_first_sheet_name(spreadsheet_id="test_id")
        
        # Assert
        assert result == ""  # Should return empty string on error
        mock_get.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_first_sheet_name_no_sheets(self, mock_build, mock_credentials, mock_sheets_service):
        """Test get_first_sheet_name method with no sheets."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = mock_sheets_service.spreadsheets.return_value.get
        mock_get.return_value.execute.return_value = {
            "sheets": []  # Empty sheets array
        }
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            result = helper.sheets.get_first_sheet_name(spreadsheet_id="test_id")
        
        # Assert
        assert result == ""  # Should return empty string when no sheets
        mock_get.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_next_empty_row_error(self, mock_build, mock_credentials, mock_sheets_service):
        """Test get_next_empty_row method with error."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.get = mock_get
        mock_get.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            result = helper.sheets.get_next_empty_row(
                spreadsheet_id="test_id",
                sheet_name="Sheet1",
                column="A"
            )
        
        # Assert
        assert result == 1  # Should return 1 on error
        mock_get.assert_called_once()


class TestDriveHandlerErrorHandling:
    """Test cases for error handling in DriveHandler."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_files_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_files method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.list_files(query="name contains 'File'")
        
        # Assert
        assert result == []  # Should return empty list on error
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_folder_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test create_folder method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_create = MagicMock()
        mock_drive_service.files.return_value.create = mock_create
        mock_create.return_value.execute.side_effect = Exception("API Error")
        
        # Act & Assert
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            
            # Should raise exception
            with pytest.raises(Exception):
                helper.drive.create_folder(name="New Folder")
        
        mock_create.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_all_files_recursive_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_all_files_recursive method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.list_all_files_recursive(folder_id="root")
        
        # Assert
        assert result == []  # Should return empty list on error
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_all_folders_recursive_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_all_folders_recursive method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.list_all_folders_recursive(folder_id="root")
        
        # Assert
        assert result == []  # Should return empty list on error
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_folder_id_not_found(self, mock_build, mock_credentials, mock_drive_service):
        """Test get_folder_id method when folder not found."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.return_value = {"files": []}  # Empty result
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.get_folder_id(folder_name="Nonexistent Folder")
        
        # Assert
        assert result is None  # Should return None when folder not found
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_folder_id_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test get_folder_id method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.get_folder_id(folder_name="Test Folder")
        
        # Assert
        assert result is None  # Should return None on error
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_file_id_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test get_file_id method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.get_file_id(file_name="Test File", folder_id="folder_id")
        
        # Assert
        assert result is None  # Should return None on error
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_files_in_folder_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_files_in_folder method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.side_effect = Exception("API Error")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            folder_id, files = helper.drive.list_files_in_folder(folder_name="Test Folder")
        
        # Assert
        assert folder_id is None  # Should return None on error
        assert files == []  # Should return empty list on error
        mock_list.assert_called_once()


class TestDocsHandlerErrorHandling:
    """Test cases for error handling in DocsHandler."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_document_error(self, mock_build, mock_credentials, mock_docs_service):
        """Test get_document method with error."""
        # Arrange
        mock_build.return_value = mock_docs_service
        mock_get = MagicMock()
        mock_docs_service.documents.return_value.get = mock_get
        
        # Set up the execute method to raise an exception
        mock_execute = MagicMock(side_effect=Exception("API Error"))
        mock_get.return_value.execute = mock_execute
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.docs = GoogleHelper.DocsHandler(mock_docs_service)
            
            # Use try/except to handle the exception
            try:
                result = helper.docs.get_document(document_id="doc1")
            except Exception:
                result = None
        
        # Assert
        assert result is None  # Should return None on error
        mock_get.assert_called_once()
        mock_execute.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_document_error(self, mock_build, mock_credentials, mock_docs_service):
        """Test create_document method with error."""
        # Arrange
        mock_build.return_value = mock_docs_service
        mock_create = MagicMock()
        mock_docs_service.documents.return_value.create = mock_create
        mock_create.return_value.execute.side_effect = Exception("API Error")
        
        # Act & Assert
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.docs = GoogleHelper.DocsHandler(mock_docs_service)
            
            # Should raise exception
            with pytest.raises(Exception):
                helper.docs.create_document(title="New Document")
        
        mock_create.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_or_replace_document_folder_error(self, mock_build, mock_credentials, mock_docs_service):
        """Test create_or_replace_document method with folder error."""
        # Arrange
        # Mock the Drive service
        mock_drive_service = MagicMock()
        mock_drive_files = MagicMock()
        mock_list = MagicMock()
        
        mock_drive_service.files.return_value = mock_drive_files
        mock_drive_files.list = mock_list
        mock_list.return_value.execute.side_effect = Exception("API Error")
        
        # Set up the build function to return different services based on arguments
        def side_effect(service_type, version, credentials=None):
            if service_type == 'drive':
                return mock_drive_service
            return mock_docs_service
        
        mock_build.side_effect = side_effect
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.docs = GoogleHelper.DocsHandler(mock_docs_service)
            
            # Should raise exception
            with pytest.raises(Exception):
                helper.docs.create_or_replace_document(title="Test Document", folder_name="Test Folder")
        
        mock_list.assert_called_once() 