"""
Tests for the Google helper module.

These tests verify the functionality of the GoogleHelper class and its handlers.
Note: Most tests are mocked to avoid requiring actual Google API credentials.
"""

import pytest
import os
from unittest.mock import MagicMock, patch, mock_open
from cws_helpers import GoogleHelper


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


class TestGoogleHelper:
    """Test cases for the GoogleHelper class."""

    @patch('cws_helpers.google_helper.google_helper.Credentials')
    @patch('cws_helpers.google_helper.google_helper.InstalledAppFlow')
    @patch('cws_helpers.google_helper.google_helper.build')
    @patch('cws_helpers.google_helper.google_helper.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init(self, mock_file_open, mock_path_exists, mock_build, mock_flow, mock_credentials_class, mock_credentials):
        """Test initialization of GoogleHelper."""
        # Arrange
        mock_path_exists.return_value = True
        mock_credentials_class.from_authorized_user_file.return_value = mock_credentials
        mock_credentials.valid = True
        
        # Act
        helper = GoogleHelper()
        
        # Assert
        assert helper is not None
        assert hasattr(helper, 'sheets')
        assert hasattr(helper, 'drive')
        assert hasattr(helper, 'docs')
        mock_credentials_class.from_authorized_user_file.assert_called_once_with("token.json", helper.scopes)

    @patch('cws_helpers.google_helper.google_helper.build')
    @patch('cws_helpers.google_helper.google_helper.os.path.exists')
    def test_get_service(self, mock_path_exists, mock_build, mock_credentials):
        """Test _get_service method."""
        # Arrange
        mock_path_exists.return_value = True
        mock_build.return_value = "mock_service"
        mock_build.reset_mock()  # Reset the mock to clear previous calls
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)  # Skip initializing services
            service = helper._get_service('sheets', 'v4')
        
        # Assert
        assert service == "mock_service"
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials)


class TestSheetsHandler:
    """Test cases for the SheetsHandler class."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_read_range(self, mock_build, mock_credentials, mock_sheets_service):
        """Test read_range method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.get = mock_get
        mock_get.return_value.execute.return_value = {"values": [["A1", "B1"], ["A2", "B2"]]}
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            # Create a new SheetsHandler with the mock service
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            result = helper.sheets.read_range(
                spreadsheet_id="test_id",
                sheet_name="Sheet1",
                start_cell="A1",
                end_cell="B2"
            )
        
        # Assert
        assert result == [["A1", "B1"], ["A2", "B2"]]
        mock_get.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_write_range(self, mock_build, mock_credentials, mock_sheets_service):
        """Test write_range method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_update = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.update = mock_update
        mock_update.return_value.execute.return_value = {"updatedCells": 4}
        test_values = [["A1", "B1"], ["A2", "B2"]]
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            # Create a new SheetsHandler with the mock service
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            helper.sheets.write_range(
                spreadsheet_id="test_id",
                values=test_values,
                sheet_name="Sheet1",
                start_cell="A1"
            )
        
        # Assert
        mock_update.assert_called_once()
        # Verify the body parameter contains our test values
        call_args = mock_update.call_args[1]
        assert call_args["body"]["values"] == test_values


class TestDriveHandler:
    """Test cases for the DriveHandler class."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_files(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_files method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.return_value = {
            "files": [{"id": "file1", "name": "File 1"}, {"id": "file2", "name": "File 2"}]
        }
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            # Create a new DriveHandler with the mock service
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.list_files(query="name contains 'File'")
        
        # Assert
        assert len(result) == 2
        assert result[0]["name"] == "File 1"
        assert result[1]["name"] == "File 2"
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_all_files_recursive(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_all_files_recursive method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        
        # Mock first call for files in root
        first_call_result = {
            "files": [
                {"id": "file1", "name": "File 1"},
                {"id": "file2", "name": "File 2"}
            ]
        }
        
        # Mock second call for folders in root
        second_call_result = {
            "files": [
                {"id": "folder1", "name": "Folder 1"}
            ]
        }
        
        # Mock third call for files in subfolder
        third_call_result = {
            "files": [
                {"id": "file3", "name": "File 3"}
            ]
        }
        
        # Mock fourth call for folders in subfolder (empty)
        fourth_call_result = {
            "files": []
        }
        
        # Set up the mock to return different results for different calls
        mock_list.return_value.execute.side_effect = [
            first_call_result,  # Files in root
            second_call_result,  # Folders in root
            third_call_result,   # Files in subfolder
            fourth_call_result   # Folders in subfolder (empty)
        ]
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.list_all_files_recursive(folder_id="root")
        
        # Assert
        assert len(result) == 3
        assert result[0] == ("file1", "File 1")
        assert result[1] == ("file2", "File 2")
        assert result[2] == ("file3", "File 3")
        assert mock_list.call_count == 4

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_folder_id(self, mock_build, mock_credentials, mock_drive_service):
        """Test get_folder_id method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_list.return_value.execute.return_value = {
            "files": [{"id": "folder1", "name": "Test Folder"}]
        }
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.get_folder_id(folder_name="Test Folder")
        
        # Assert
        assert result == "folder1"
        mock_list.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_folder_id_create_if_missing(self, mock_build, mock_credentials, mock_drive_service):
        """Test get_folder_id method with create_if_missing=True."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_create = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        mock_drive_service.files.return_value.create = mock_create
        
        # Empty result for the list call (folder not found)
        mock_list.return_value.execute.return_value = {"files": []}
        
        # Result for the create call
        mock_create.return_value.execute.return_value = {"id": "new_folder", "name": "New Folder", "mimeType": "application/vnd.google-apps.folder"}
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.get_folder_id(folder_name="New Folder", create_if_missing=True)
        
        # Assert
        assert result == "new_folder"
        mock_list.assert_called_once()
        mock_create.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_file_id(self, mock_build, mock_credentials, mock_drive_service):
        """Test get_file_id method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        
        # First call for folder lookup
        first_call_result = {
            "files": [{"id": "folder1", "name": "Test Folder"}]
        }
        
        # Second call for file lookup
        second_call_result = {
            "files": [{"id": "file1", "name": "Test File"}]
        }
        
        mock_list.return_value.execute.side_effect = [first_call_result, second_call_result]
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.get_file_id(file_name="Test File", folder_name="Test Folder")
        
        # Assert
        assert result == "file1"
        assert mock_list.call_count == 2

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_files_in_folder(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_files_in_folder method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        
        # First call for folder lookup
        first_call_result = {
            "files": [{"id": "folder1", "name": "Test Folder"}]
        }
        
        # Second call for files in folder
        second_call_result = {
            "files": [
                {"id": "file1", "name": "File 1", "mimeType": "application/vnd.google-apps.document"},
                {"id": "file2", "name": "File 2", "mimeType": "application/vnd.google-apps.document"}
            ]
        }
        
        mock_list.return_value.execute.side_effect = [first_call_result, second_call_result]
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            folder_id, files = helper.drive.list_files_in_folder(folder_name="Test Folder")
        
        # Assert
        assert folder_id == "folder1"
        assert len(files) == 2
        assert files[0] == ("file1", "File 1")
        assert files[1] == ("file2", "File 2")
        assert mock_list.call_count == 2


class TestDocsHandler:
    """Test cases for the DocsHandler class."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_document(self, mock_build, mock_credentials, mock_docs_service):
        """Test get_document method."""
        # Arrange
        mock_build.return_value = mock_docs_service
        mock_get = MagicMock()
        mock_docs_service.documents.return_value.get = mock_get
        mock_get.return_value.execute.return_value = {"documentId": "doc1", "title": "Test Document"}
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            # Create a new DocsHandler with the mock service
            helper.docs = GoogleHelper.DocsHandler(mock_docs_service)
            result = helper.docs.get_document(document_id="doc1")
        
        # Assert
        assert result["documentId"] == "doc1"
        assert result["title"] == "Test Document"
        mock_get.assert_called_once_with(documentId="doc1")

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_document(self, mock_build, mock_credentials, mock_docs_service):
        """Test create_document method."""
        # Arrange
        mock_build.return_value = mock_docs_service
        mock_create = MagicMock()
        mock_docs_service.documents.return_value.create = mock_create
        mock_create.return_value.execute.return_value = {"documentId": "new_doc", "title": "New Document"}
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.docs = GoogleHelper.DocsHandler(mock_docs_service)
            result = helper.docs.create_document(title="New Document")
        
        # Assert
        assert result["documentId"] == "new_doc"
        assert result["title"] == "New Document"
        mock_create.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_document_in_folder(self, mock_build, mock_credentials, mock_docs_service):
        """Test create_document method with folder_id."""
        # Arrange
        # Mock the Drive service
        mock_drive_service = MagicMock()
        mock_drive_files = MagicMock()
        mock_drive_create = MagicMock()
        mock_drive_service.files.return_value = mock_drive_files
        mock_drive_files.create = mock_drive_create
        mock_drive_create.return_value.execute.return_value = {"id": "new_doc"}
        
        # Mock the Docs service
        mock_get = MagicMock()
        mock_docs_service.documents.return_value.get = mock_get
        mock_get.return_value.execute.return_value = {"documentId": "new_doc", "title": "New Document"}
        
        # Set up the build function to return different services based on arguments
        def side_effect(service_type, version, credentials=None):
            if service_type == 'drive':
                return mock_drive_service
            return mock_docs_service
        
        mock_build.side_effect = side_effect
        
        # Mock the credentials access
        mock_docs_service._http = MagicMock()
        mock_docs_service._http.credentials = mock_credentials
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.docs = GoogleHelper.DocsHandler(mock_docs_service)
            result = helper.docs.create_document(title="New Document", folder_id="folder1")
        
        # Assert
        assert result["documentId"] == "new_doc"
        assert result["title"] == "New Document"
        mock_drive_create.assert_called_once()
        mock_get.assert_called_once_with(documentId="new_doc")

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_or_replace_document(self, mock_build, mock_credentials, mock_docs_service):
        """Test create_or_replace_document method."""
        # Arrange
        # Mock the Drive service
        mock_drive_service = MagicMock()
        mock_drive_files = MagicMock()
        mock_list = MagicMock()
        mock_delete = MagicMock()
        mock_create = MagicMock()
        
        mock_drive_service.files.return_value = mock_drive_files
        mock_drive_files.list = mock_list
        mock_drive_files.delete = mock_delete
        mock_drive_files.create = mock_create
        
        # First call to list (folder lookup)
        first_list_result = {"files": [{"id": "folder1", "name": "Test Folder"}]}
        
        # Second call to list (existing file lookup)
        second_list_result = {"files": [{"id": "old_doc", "name": "Test Document"}]}
        
        # Set up the list mock to return different results for different calls
        mock_list.return_value.execute.side_effect = [first_list_result, second_list_result]
        
        # Create call result
        mock_create.return_value.execute.return_value = {"id": "new_doc"}
        
        # Set up the build function to return different services based on arguments
        def side_effect(service_type, version, credentials=None):
            if service_type == 'drive':
                return mock_drive_service
            return mock_docs_service
        
        mock_build.side_effect = side_effect
        
        # Mock the credentials access
        mock_docs_service._http = MagicMock()
        mock_docs_service._http.credentials = mock_credentials
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.docs = GoogleHelper.DocsHandler(mock_docs_service)
            result = helper.docs.create_or_replace_document(title="Test Document", folder_name="Test Folder")
        
        # Assert
        assert result == "new_doc"
        assert mock_list.call_count == 2
        mock_delete.assert_called_once_with(fileId="old_doc")
        mock_create.assert_called_once() 