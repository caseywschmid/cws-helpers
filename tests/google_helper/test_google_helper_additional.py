"""
Additional tests for the Google helper module to improve coverage.

These tests focus on methods that were not covered in the main test file.
"""

import pytest
from unittest.mock import MagicMock, patch
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
    mock_service.spreadsheets.return_value.get = MagicMock()
    return mock_service


@pytest.fixture
def mock_drive_service():
    """Mock Google Drive service for testing."""
    mock_service = MagicMock()
    mock_files = MagicMock()
    mock_service.files.return_value = mock_files
    return mock_service


class TestSheetsHandlerAdditional:
    """Additional test cases for the SheetsHandler class."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_clear_range(self, mock_build, mock_credentials, mock_sheets_service):
        """Test clear_range method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_clear = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.clear = mock_clear
        mock_clear.return_value.execute.return_value = {"clearedRange": "Sheet1!A1:B10"}
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            helper.sheets.clear_range(
                spreadsheet_id="test_id",
                sheet_name="Sheet1",
                start_cell="A1",
                end_cell="B10"
            )
        
        # Assert
        mock_clear.assert_called_once()
        call_args = mock_clear.call_args[1]
        assert call_args["spreadsheetId"] == "test_id"
        assert call_args["range"] == "Sheet1!A1:B10"

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_clear_range_with_preserve_headers(self, mock_build, mock_credentials, mock_sheets_service):
        """Test clear_range method with preserve_headers=True."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = MagicMock()
        mock_clear = MagicMock()
        mock_update = MagicMock()
        
        mock_sheets_service.spreadsheets.return_value.values.return_value.get = mock_get
        mock_sheets_service.spreadsheets.return_value.values.return_value.clear = mock_clear
        mock_sheets_service.spreadsheets.return_value.values.return_value.update = mock_update
        
        # Mock the read_range response
        mock_get.return_value.execute.return_value = {"values": [["Header1", "Header2"], ["Data1", "Data2"]]}
        mock_clear.return_value.execute.return_value = {"clearedRange": "Sheet1!A1:B10"}
        mock_update.return_value.execute.return_value = {"updatedCells": 2}
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            helper.sheets.clear_range(
                spreadsheet_id="test_id",
                sheet_name="Sheet1",
                start_cell="A1",
                end_cell="B10",
                preserve_headers=True
            )
        
        # Assert
        mock_get.assert_called_once()
        mock_clear.assert_called_once()
        mock_update.assert_called_once()
        
        # Verify the update call contains the header row
        update_call_args = mock_update.call_args[1]
        assert update_call_args["body"]["values"] == [["Header1", "Header2"]]

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_first_sheet_name(self, mock_build, mock_credentials, mock_sheets_service):
        """Test get_first_sheet_name method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = mock_sheets_service.spreadsheets.return_value.get
        mock_get.return_value.execute.return_value = {
            "sheets": [
                {"properties": {"title": "FirstSheet"}},
                {"properties": {"title": "SecondSheet"}}
            ]
        }
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            result = helper.sheets.get_first_sheet_name(spreadsheet_id="test_id")
        
        # Assert
        assert result == "FirstSheet"
        mock_get.assert_called_once()
        # The actual implementation doesn't specify fields parameter
        assert mock_get.call_args[1]["spreadsheetId"] == "test_id"

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_next_empty_row(self, mock_build, mock_credentials, mock_sheets_service):
        """Test get_next_empty_row method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.get = mock_get
        
        # Mock response with data in first 3 rows
        mock_get.return_value.execute.return_value = {
            "values": [["data"], ["data"], ["data"]]
        }
        
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
        assert result == 4  # Should be row 4 (1-indexed)
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]
        assert call_args["spreadsheetId"] == "test_id"
        assert call_args["range"] == "Sheet1!A:A"

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_get_next_empty_row_empty_sheet(self, mock_build, mock_credentials, mock_sheets_service):
        """Test get_next_empty_row method with empty sheet."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.get = mock_get
        
        # Mock response with no data
        mock_get.return_value.execute.return_value = {}
        
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
        assert result == 1  # Should be row 1 for empty sheet
        mock_get.assert_called_once()

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_read_sheet(self, mock_build, mock_credentials, mock_sheets_service):
        """Test read_sheet method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_get = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.get = mock_get
        mock_get.return_value.execute.return_value = {"values": [["A1", "B1"], ["A2", "B2"]]}
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            result = helper.sheets.read_sheet(
                spreadsheet_id="test_id",
                range_name="Sheet1!A1:B2"
            )
        
        # Assert
        assert result == [["A1", "B1"], ["A2", "B2"]]
        mock_get.assert_called_once_with(spreadsheetId="test_id", range="Sheet1!A1:B2")

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_write_sheet(self, mock_build, mock_credentials, mock_sheets_service):
        """Test write_sheet method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        mock_update = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value.update = mock_update
        mock_update.return_value.execute.return_value = {"updatedCells": 4}
        test_values = [["A1", "B1"], ["A2", "B2"]]
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            helper.sheets.write_sheet(
                spreadsheet_id="test_id",
                values=test_values,
                range_name="Sheet1!A1"
            )
        
        # Assert
        mock_update.assert_called_once()
        call_args = mock_update.call_args[1]
        assert call_args["spreadsheetId"] == "test_id"
        assert call_args["range"] == "Sheet1!A1"
        assert call_args["body"]["values"] == test_values

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_clear_output_sheet(self, mock_build, mock_credentials, mock_sheets_service):
        """Test clear_output_sheet method."""
        # Arrange
        mock_build.return_value = mock_sheets_service
        
        # Since clear_output_sheet calls clear_range, we need to patch that method
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.sheets = GoogleHelper.SheetsHandler(mock_sheets_service)
            
            # Mock the clear_range method
            helper.sheets.clear_range = MagicMock()
            
            # Act
            helper.sheets.clear_output_sheet(spreadsheet_id="test_id")
        
        # Assert
        helper.sheets.clear_range.assert_called_once_with(
            "test_id", sheet_name="output", preserve_headers=True
        )


class TestDriveHandlerAdditional:
    """Additional test cases for the DriveHandler class."""

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_folder(self, mock_build, mock_credentials, mock_drive_service):
        """Test create_folder method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_create = MagicMock()
        mock_drive_service.files.return_value.create = mock_create
        mock_create.return_value.execute.return_value = {
            "id": "new_folder",
            "name": "New Folder",
            "mimeType": "application/vnd.google-apps.folder"
        }
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.create_folder(name="New Folder")
        
        # Assert
        assert result["id"] == "new_folder"
        assert result["name"] == "New Folder"
        mock_create.assert_called_once()
        call_args = mock_create.call_args[1]
        assert call_args["body"]["name"] == "New Folder"
        assert call_args["body"]["mimeType"] == "application/vnd.google-apps.folder"

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_create_folder_with_parent(self, mock_build, mock_credentials, mock_drive_service):
        """Test create_folder method with parent_id."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_create = MagicMock()
        mock_drive_service.files.return_value.create = mock_create
        mock_create.return_value.execute.return_value = {
            "id": "new_subfolder",
            "name": "New Subfolder",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": ["parent_folder"]
        }
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.create_folder(name="New Subfolder", parent_id="parent_folder")
        
        # Assert
        assert result["id"] == "new_subfolder"
        assert result["name"] == "New Subfolder"
        mock_create.assert_called_once()
        call_args = mock_create.call_args[1]
        assert call_args["body"]["name"] == "New Subfolder"
        assert call_args["body"]["parents"] == ["parent_folder"]

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_delete_file(self, mock_build, mock_credentials, mock_drive_service):
        """Test delete_file method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_delete = MagicMock()
        mock_drive_service.files.return_value.delete = mock_delete
        mock_delete.return_value.execute.return_value = None  # Delete returns empty response
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.delete_file(file_id="file_to_delete")
        
        # Assert
        assert result is True
        mock_delete.assert_called_once_with(fileId="file_to_delete")

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_delete_file_error(self, mock_build, mock_credentials, mock_drive_service):
        """Test delete_file method with error."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_delete = MagicMock()
        mock_drive_service.files.return_value.delete = mock_delete
        mock_delete.return_value.execute.side_effect = Exception("File not found")
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.delete_file(file_id="nonexistent_file")
        
        # Assert
        assert result is False
        mock_delete.assert_called_once_with(fileId="nonexistent_file")

    @patch('cws_helpers.google_helper.google_helper.build')
    def test_list_all_folders_recursive(self, mock_build, mock_credentials, mock_drive_service):
        """Test list_all_folders_recursive method."""
        # Arrange
        mock_build.return_value = mock_drive_service
        mock_list = MagicMock()
        mock_drive_service.files.return_value.list = mock_list
        
        # Mock first call for folders in root
        first_call_result = {
            "files": [
                {"id": "folder1", "name": "Folder 1"}
            ]
        }
        
        # Mock second call for subfolders in folder1
        second_call_result = {
            "files": [
                {"id": "subfolder1", "name": "Subfolder 1"}
            ]
        }
        
        # Mock third call for subfolders in subfolder1 (empty)
        third_call_result = {
            "files": []
        }
        
        # Set up the mock to return different results for different calls
        mock_list.return_value.execute.side_effect = [
            first_call_result,   # Folders in root
            second_call_result,  # Subfolders in folder1
            third_call_result    # Subfolders in subfolder1 (empty)
        ]
        
        # Act
        with patch.object(GoogleHelper, '_get_credentials', return_value=mock_credentials):
            helper = GoogleHelper(initialize_services=False)
            helper.drive = GoogleHelper.DriveHandler(mock_drive_service)
            result = helper.drive.list_all_folders_recursive(folder_id="root")
        
        # Assert
        assert len(result) == 2
        assert result[0] == ("folder1", "Folder 1")
        assert result[1] == ("subfolder1", "Subfolder 1")
        assert mock_list.call_count == 3 