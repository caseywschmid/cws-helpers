# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# ------------------ Imports ------------------ #
import os
import time
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Tuple, Dict, Optional, Union, Any


class GoogleHelper:
    """
    Comprehensive helper class for interacting with Google APIs.
    
    This class provides a unified interface for working with various Google services
    including Sheets, Drive, and Docs. It handles authentication, token refresh,
    and provides methods for common operations across different Google services.
    
    Features:
    - Authentication Management: Handles OAuth2 authentication flow and token refresh
    - Google Sheets: Read, write, and manipulate spreadsheet data
    - Google Drive: List, search, create, and manage files and folders
    - Google Docs: Create, read, and manage documents
    - Recursive Operations: Recursively list files and folders in Drive
    - Error Handling: Comprehensive error handling and logging
    
    Authentication:
    The first time you use the helper, it will open a browser window for you to
    authenticate with your Google account. After authentication, a `token.json`
    file will be created to store your credentials for future use.
    
    Usage:
        # Initialize with default scopes (Sheets, Drive, and Docs)
        google = GoogleHelper()
        
        # Or initialize with specific scopes
        google = GoogleHelper(scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ])
        
        # Access different service handlers
        sheets = google.sheets
        drive = google.drive
        docs = google.docs
        
        # Work with sheets
        data = google.sheets.read_range("spreadsheet_id", "Sheet1!A1:B10")
        
        # Work with drive
        files = google.drive.list_files(query="name contains 'Report'")
        
        # Work with docs
        doc = google.docs.get_document("document_id")
    """

    def __init__(self, scopes: list = None, initialize_services: bool = True):
        """
        Initialize the Google Helper.
        
        This constructor sets up the Google API client with the specified scopes,
        handles authentication, and initializes service handlers for Sheets, Drive,
        and Docs APIs.
        
        Args:
            scopes: Optional list of Google API scopes. If None, default scopes for 
                   Sheets, Drive, and Docs will be used. Common scopes include:
                   - 'https://www.googleapis.com/auth/spreadsheets'
                   - 'https://www.googleapis.com/auth/drive'
                   - 'https://www.googleapis.com/auth/documents'
            initialize_services: Whether to initialize service handlers during construction.
                                 Set to False for testing purposes.
        
        Note:
            Authentication requires a 'credentials.json' file in the current directory.
            The first time you run this, it will open a browser window for authentication.
            After authentication, a 'token.json' file will be created to store credentials.
        """
        self.scopes = scopes or [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/documents",
        ]
        self._credentials = self._get_credentials()
        
        # Initialize service handlers
        if initialize_services:
            self.sheets_service = self._get_service("sheets", "v4")
            self.drive_service = self._get_service("drive", "v3")
            self.docs_service = self._get_service("docs", "v1")
            
            self.sheets = self.SheetsHandler(self.sheets_service)
            self.drive = self.DriveHandler(self.drive_service)
            self.docs = self.DocsHandler(self.docs_service)
        else:
            # For testing purposes
            self.sheets_service = None
            self.drive_service = None
            self.docs_service = None
            
            # Initialize handlers with None, they'll be set in tests
            self.sheets = self.SheetsHandler(None)
            self.drive = self.DriveHandler(None)
            self.docs = self.DocsHandler(None)

    def _get_credentials(self):
        """
        Get and refresh Google OAuth2 credentials.
        
        This method handles the OAuth2 authentication flow for Google APIs:
        1. Checks for existing credentials in 'token.json'
        2. Validates and refreshes expired credentials if possible
        3. Initiates a new authentication flow if needed
        4. Saves new credentials to 'token.json'
        
        The authentication flow requires a 'credentials.json' file containing
        OAuth client configuration from the Google Cloud Console.
        
        Returns:
            Google OAuth2 credentials object that can be used to authenticate API requests.
            
        Raises:
            FileNotFoundError: If credentials.json is missing.
            RefreshError: If token refresh fails and re-authentication is needed.
        """
        credentials = None
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", self.scopes)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except RefreshError:
                    log.info("Token refresh failed. Please re-authenticate.")
                    credentials = None
            
            if not credentials:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                credentials = flow.run_local_server(port=0)
            
            with open("token.json", "w") as token:
                token.write(credentials.to_json())
        
        return credentials

    def _get_service(self, kind: str, version: str):
        """
        Get an authenticated Google API service.
        
        This method creates and returns an authenticated service client for the
        specified Google API using the credentials obtained from _get_credentials().
        
        Args:
            kind: The API service to get (e.g., "sheets", "drive", "docs")
            version: The API version to use (e.g., "v4", "v3")
            
        Returns:
            Authenticated Google API service client that can be used to make API requests.
            
        Raises:
            Exception: If service creation fails for any reason (e.g., invalid API,
                      network issues, authentication problems).
        """
        try:
            service = build(kind, version, credentials=self._credentials)
            return service
        except Exception as e:
            log.error(f"Error creating {kind} service: {str(e)}")
            raise

    class SheetsHandler:
        """
        Handler for Google Sheets operations.
        
        This handler provides methods for reading, writing, and managing Google Sheets data.
        It includes functionality for reading and writing ranges, finding empty rows,
        clearing sheets, and working with sheet metadata.
        
        All methods include comprehensive error handling and logging to help with debugging.
        Most methods return sensible defaults (like empty lists) when errors occur, rather
        than raising exceptions, to prevent application crashes.
        """
        
        def __init__(self, service):
            """
            Initialize with an authenticated Google Sheets service.
            
            Args:
                service: Authenticated Google Sheets service from googleapiclient.discovery.build()
            """
            self.service = service

        def read_range(self, spreadsheet_id: str, range_name: str = None, sheet_name: str = None, 
                      start_cell: str = "A1", end_cell: str = None) -> list:
            """
            Read data from a specified range in a spreadsheet.
            
            This method retrieves data from a Google Sheet. You can specify the range
            either as a full A1 notation range (e.g., "Sheet1!A1:D10") or by providing
            the sheet name, start cell, and end cell separately.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                range_name: Full range to read (e.g., "Sheet1!A1:B10"). If provided, 
                           other range params are ignored.
                sheet_name: Name of sheet to read from. If None, reads from first sheet.
                start_cell: Starting cell (e.g., "A1", "B2"). Defaults to "A1".
                end_cell: Ending cell (e.g., "E10", "Z100"). If None, reads to last used cell.
                
            Returns:
                A list of rows, where each row is a list of values. Returns an empty list
                if the range is empty or an error occurs.
                
            Example:
                ```python
                # Read data from a specific range
                data = google.sheets.read_range(
                    spreadsheet_id='your_spreadsheet_id',
                    sheet_name='Sheet1',
                    start_cell='A1',
                    end_cell='D10'
                )
                
                # Read data using a range name
                data = google.sheets.read_range(
                    spreadsheet_id='your_spreadsheet_id',
                    range_name='Sheet1!A1:D10'
                )
                ```
            """
            try:
                if not range_name:
                    # Construct range from components
                    sheet_prefix = f"{sheet_name}!" if sheet_name else ""
                    range_suffix = f"{start_cell}" if not end_cell else f"{start_cell}:{end_cell}"
                    range_name = f"{sheet_prefix}{range_suffix}"

                result = (
                    self.service.spreadsheets()
                    .values()
                    .get(spreadsheetId=spreadsheet_id, range=range_name)
                    .execute()
                )
                return result.get("values", [])
            except Exception as e:
                log.error(f"Error reading sheet: {str(e)}")
                return []

        def write_range(self, spreadsheet_id: str, values: list, range_name: str = None,
                       sheet_name: str = None, start_cell: str = "A1", 
                       input_option: str = "RAW", rate_limit: float = 1.0):
            """
            Write data to a specified range in a spreadsheet.
            
            This method writes data to a Google Sheet. You can specify the range
            either as a full A1 notation range (e.g., "Sheet1!A1") or by providing
            the sheet name and start cell separately.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                values: The data to write as a list of rows, where each row is a list of values.
                range_name: Full range to write to (e.g., "Sheet1!A1"). If provided, 
                           other range params are ignored.
                sheet_name: Name of sheet to write to. If None, writes to first sheet.
                start_cell: Starting cell for write operation (e.g., "A1", "B2").
                input_option: How input should be interpreted:
                             - "RAW": Values are stored as-is
                             - "USER_ENTERED": Values are parsed as if typed by a user
                rate_limit: Seconds to wait after write (for rate limiting).
                
            Raises:
                Exception: If the write operation fails.
                
            Example:
                ```python
                # Write data to a specific range
                values = [
                    ['Name', 'Email', 'Phone'],
                    ['John Doe', 'john@example.com', '555-1234']
                ]
                google.sheets.write_range(
                    spreadsheet_id='your_spreadsheet_id',
                    values=values,
                    sheet_name='Sheet1',
                    start_cell='A1'
                )
                ```
            """
            try:
                if not range_name:
                    # Construct range from components
                    sheet_prefix = f"{sheet_name}!" if sheet_name else ""
                    range_name = f"{sheet_prefix}{start_cell}"

                body = {"values": values}
                self.service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption=input_option,
                    body=body,
                ).execute()
                
                if rate_limit > 0:
                    time.sleep(rate_limit)
                    
            except Exception as e:
                log.error(f"Error writing to sheet: {e}")
                raise

        def clear_range(self, spreadsheet_id: str, range_name: str = None,
                       sheet_name: str = None, start_cell: str = None, 
                       end_cell: str = None, preserve_headers: bool = False):
            """
            Clear data from a specified range in a spreadsheet.
            
            This method clears data from a Google Sheet. You can specify the range
            either as a full A1 notation range (e.g., "Sheet1!A1:D10") or by providing
            the sheet name, start cell, and end cell separately. The preserve_headers
            option allows you to keep the first row (headers) while clearing the rest.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                range_name: Full range to clear (e.g., "Sheet1!A1:B10"). If provided, 
                           other range params are ignored.
                sheet_name: Name of sheet to clear. If None, uses first sheet.
                start_cell: Starting cell (e.g., "A1", "B2").
                end_cell: Ending cell (e.g., "E10", "Z100").
                preserve_headers: Whether to preserve the first row (headers).
                
            Raises:
                Exception: If the clear operation fails.
                
            Example:
                ```python
                # Clear a specific range
                google.sheets.clear_range(
                    spreadsheet_id='your_spreadsheet_id',
                    sheet_name='Sheet1',
                    start_cell='A1',
                    end_cell='D10'
                )
                
                # Clear a range while preserving headers
                google.sheets.clear_range(
                    spreadsheet_id='your_spreadsheet_id',
                    sheet_name='Sheet1',
                    start_cell='A2',  # Start from row 2 to preserve headers
                    end_cell='D10',
                    preserve_headers=True
                )
                ```
            """
            try:
                if not range_name:
                    # Construct range from components
                    sheet_prefix = f"{sheet_name}!" if sheet_name else ""
                    if start_cell and end_cell:
                        range_suffix = f"{start_cell}:{end_cell}"
                    elif start_cell:
                        range_suffix = start_cell
                    else:
                        range_suffix = "A1"
                    range_name = f"{sheet_prefix}{range_suffix}"
                
                if preserve_headers:
                    # Get the current range data
                    values = self.read_range(spreadsheet_id, range_name)
                    if values and len(values) > 1:
                        # Keep the header row and clear the rest
                        header = values[0]
                        self.service.spreadsheets().values().clear(
                            spreadsheetId=spreadsheet_id,
                            range=range_name,
                        ).execute()
                        # Write back the header row
                        self.write_range(
                            spreadsheet_id=spreadsheet_id,
                            values=[header],
                            range_name=range_name,
                        )
                else:
                    # Clear the entire range
                    self.service.spreadsheets().values().clear(
                        spreadsheetId=spreadsheet_id,
                        range=range_name,
                    ).execute()
            except Exception as e:
                log.error(f"Error clearing range: {e}")
                raise

        def get_first_sheet_name(self, spreadsheet_id: str) -> str:
            """
            Get the name of the first sheet in a spreadsheet.
            
            This method retrieves the name of the first sheet in a Google Spreadsheet.
            This is useful when you need to reference a sheet by name but don't know
            what sheets are available in the spreadsheet.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                
            Returns:
                The name of the first sheet as a string. Returns an empty string if
                an error occurs or if the spreadsheet has no sheets.
                
            Example:
                ```python
                # Get the name of the first sheet in a spreadsheet
                first_sheet = google.sheets.get_first_sheet_name(
                    spreadsheet_id='your_spreadsheet_id'
                )
                ```
            """
            try:
                spreadsheet = self.service.spreadsheets().get(
                    spreadsheetId=spreadsheet_id
                ).execute()
                
                if spreadsheet and "sheets" in spreadsheet and len(spreadsheet["sheets"]) > 0:
                    return spreadsheet["sheets"][0]["properties"]["title"]
                return ""
            except Exception as e:
                log.error(f"Error getting first sheet name: {str(e)}")
                return ""

        def get_next_empty_row(self, spreadsheet_id: str, sheet_name: str = None, 
                             column: str = "A") -> int:
            """
            Find the next empty row in a specified column.
            
            This method is useful for appending data to a sheet without overwriting
            existing data. It finds the first empty row in a specified column, which
            can then be used as the starting point for writing new data.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                sheet_name: Name of the sheet to check. If None, uses the first sheet.
                column: Column to check (e.g., "A", "B"). Defaults to "A".
                
            Returns:
                The row number of the next empty row (1-indexed). Returns 1 if the
                column is empty or if an error occurs.
                
            Example:
                ```python
                # Find the next empty row in column A of Sheet1
                next_row = google.sheets.get_next_empty_row(
                    spreadsheet_id='your_spreadsheet_id',
                    sheet_name='Sheet1',
                    column='A'
                )
                
                # Use the next empty row to append data
                google.sheets.write_range(
                    spreadsheet_id='your_spreadsheet_id',
                    values=[['New', 'Data', 'Row']],
                    sheet_name='Sheet1',
                    start_cell=f'A{next_row}'
                )
                ```
            """
            try:
                # If no sheet name provided, get the first sheet
                if not sheet_name:
                    sheet_name = self.get_first_sheet_name(spreadsheet_id)
                
                # Get all values in the specified column
                range_name = f"{sheet_name}!{column}:{column}"
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id,
                    range=range_name
                ).execute()
                
                values = result.get("values", [])
                return len(values) + 1  # 1-indexed row number
            except Exception as e:
                log.error(f"Error finding next empty row: {e}")
                return 1  # Default to first row if error

        def read_sheet(self, spreadsheet_id: str, range_name: str = None) -> list:
            """
            Alias for read_range with simpler parameters.
            
            This is a convenience method that provides a simpler interface to read_range
            when you only need to specify the spreadsheet ID and range name.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                range_name: Range to read (e.g., "Sheet1!A1:D10").
                
            Returns:
                A list of rows, where each row is a list of values.
                
            Example:
                ```python
                # Simplified reading with default parameters
                data = google.sheets.read_sheet(
                    spreadsheet_id='your_spreadsheet_id',
                    range_name='Sheet1!A1:D10'
                )
                ```
            """
            return self.read_range(spreadsheet_id, range_name)

        def write_sheet(self, spreadsheet_id: str, values: list, range_name: str = None):
            """
            Alias for write_range with simpler parameters.
            
            This is a convenience method that provides a simpler interface to write_range
            when you only need to specify the spreadsheet ID, values, and range name.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                values: The data to write as a list of rows, where each row is a list of values.
                range_name: Range to write to (e.g., "Sheet1!A1").
                
            Example:
                ```python
                # Simplified writing with default parameters
                google.sheets.write_sheet(
                    spreadsheet_id='your_spreadsheet_id',
                    values=[['Name', 'Email'], ['John', 'john@example.com']],
                    range_name='Sheet1!A1'
                )
                ```
            """
            return self.write_range(spreadsheet_id, values, range_name)

        def clear_output_sheet(self, spreadsheet_id: str, sheet_name: str = "output"):
            """
            Clear a sheet while preserving headers.
            
            This is a convenience method that clears all data in a sheet except for
            the first row (headers). It's particularly useful for output sheets that
            need to be cleared before writing new data.
            
            Args:
                spreadsheet_id: ID of the spreadsheet (the long string in the sheet URL).
                sheet_name: Name of the sheet to clear. Defaults to "output".
                
            Example:
                ```python
                # Clear the "output" sheet while preserving headers
                google.sheets.clear_output_sheet(
                    spreadsheet_id='your_spreadsheet_id'
                )
                
                # Clear a different sheet while preserving headers
                google.sheets.clear_output_sheet(
                    spreadsheet_id='your_spreadsheet_id',
                    sheet_name='results'
                )
                ```
            """
            return self.clear_range(
                spreadsheet_id, sheet_name=sheet_name, preserve_headers=True
            )

    class DriveHandler:
        """
        Handler for Google Drive operations.
        
        This handler provides methods for working with Google Drive files and folders.
        It includes functionality for listing, creating, finding, and managing files
        and folders, including recursive operations.
        
        All methods include comprehensive error handling and logging to help with debugging.
        Most methods return sensible defaults (like empty lists or None) when errors occur,
        rather than raising exceptions, to prevent application crashes.
        """
        
        def __init__(self, service):
            """
            Initialize with an authenticated Google Drive service.
            
            Args:
                service: Authenticated Google Drive service from googleapiclient.discovery.build()
            """
            self.service = service

        def list_files(self, query: str = None, page_size: int = 10, fields: str = None):
            """
            List files in Google Drive.
            
            This method searches for files in Google Drive based on a query string.
            The query syntax follows the Google Drive API search syntax, which allows
            for complex queries based on file properties.
            
            Args:
                query: Search query string (e.g., "name contains 'Report'", 
                      "mimeType='application/vnd.google-apps.spreadsheet'").
                      See https://developers.google.com/drive/api/guides/search-files
                      for the full query syntax.
                page_size: Maximum number of files to return. Defaults to 10.
                fields: Fields to include in the response. Defaults to "id, name, mimeType".
                       Use "files(id, name, mimeType, createdTime)" to include more fields.
                
            Returns:
                List of file metadata dictionaries. Each dictionary contains the requested
                fields for each file. Returns an empty list if no files are found or an
                error occurs.
                
            Example:
                ```python
                # List files with a query
                files = google.drive.list_files(
                    query="name contains 'Report'",
                    page_size=20
                )
                
                # List files with custom fields
                files = google.drive.list_files(
                    query="mimeType='application/vnd.google-apps.spreadsheet'",
                    fields="files(id, name, createdTime, modifiedTime)"
                )
                ```
            """
            try:
                fields = fields or "nextPageToken, files(id, name, mimeType)"
                results = self.service.files().list(
                    q=query,
                    pageSize=page_size,
                    fields=fields
                ).execute()
                
                return results.get("files", [])
            except Exception as e:
                log.error(f"Error listing files: {str(e)}")
                return []

        def create_folder(self, name: str, parent_id: str = None):
            """
            Create a new folder in Google Drive.
            
            This method creates a new folder in Google Drive. You can specify a parent
            folder ID to create the folder inside another folder, or omit it to create
            the folder in the root of your Drive.
            
            Args:
                name: Name of the folder to create.
                parent_id: ID of the parent folder. If None, creates the folder in the root.
                
            Returns:
                A dictionary containing metadata of the created folder, including:
                - id: The unique ID of the created folder
                - name: The name of the folder
                - mimeType: The MIME type (always "application/vnd.google-apps.folder")
                
            Raises:
                Exception: If the folder creation fails.
                
            Example:
                ```python
                # Create a folder in the root directory
                folder = google.drive.create_folder(name='My New Folder')
                
                # Create a folder inside another folder
                folder = google.drive.create_folder(
                    name='Subfolder',
                    parent_id='parent_folder_id'
                )
                
                # Use the returned folder ID for further operations
                folder_id = folder['id']
                ```
            """
            try:
                file_metadata = {
                    "name": name,
                    "mimeType": "application/vnd.google-apps.folder"
                }
                
                if parent_id:
                    file_metadata["parents"] = [parent_id]
                
                folder = self.service.files().create(
                    body=file_metadata,
                    fields="id, name, mimeType"
                ).execute()
                
                return folder
            except Exception as e:
                log.error(f"Error creating folder: {str(e)}")
                raise

        def list_all_files_recursive(self, folder_id: str = "root", file_type: str = None) -> List[Tuple[str, str]]:
            """
            Recursively list all files in a Google Drive folder.
            
            This method traverses a folder and all its subfolders to find all files.
            It's useful for creating a complete inventory of files in a folder structure.
            You can optionally filter by file type using the MIME type.
            
            Args:
                folder_id: ID of the folder to start the search from. Defaults to "root"
                          (the root of your Google Drive).
                file_type: Optional MIME type filter (e.g., "application/vnd.google-apps.document").
                          If provided, only files of this type will be included.
                
            Returns:
                A list of tuples, each containing the ID and name of a file. Returns an
                empty list if no files are found or an error occurs.
                
            Example:
                ```python
                # List all files recursively from the root
                all_files = google.drive.list_all_files_recursive()
                
                # List all files recursively from a specific folder
                all_files = google.drive.list_all_files_recursive(folder_id='folder_id')
                
                # List all Google Docs recursively
                all_docs = google.drive.list_all_files_recursive(
                    file_type='application/vnd.google-apps.document'
                )
                
                # Process the results
                for file_id, file_name in all_files:
                    print(f"File: {file_name}, ID: {file_id}")
                ```
            """
            try:
                # Query for all files in the current folder
                file_query = f"'{folder_id}' in parents"
                if file_type:
                    file_query += f" and mimeType='{file_type}'"
                else:
                    file_query += f" and mimeType!='application/vnd.google-apps.folder'"
                
                files = self.service.files().list(
                    q=file_query,
                    fields="files(id, name, mimeType)"
                ).execute().get("files", [])
                
                all_files = [(file["id"], file["name"]) for file in files]
                
                # Query for all subfolders in the current folder
                folder_query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
                folders = self.service.files().list(
                    q=folder_query,
                    fields="files(id, name)"
                ).execute().get("files", [])
                
                # Recursively list all files in each subfolder
                for folder in folders:
                    all_files.extend(self.list_all_files_recursive(folder_id=folder["id"], file_type=file_type))
                
                return all_files
            except Exception as e:
                log.error(f"Error listing files recursively: {str(e)}")
                return []

        def list_all_folders_recursive(self, folder_id: str = "root") -> List[Tuple[str, str]]:
            """
            Recursively list all folders in Google Drive.
            
            This method traverses a folder and all its subfolders to find all folders.
            It's useful for creating a complete inventory of the folder structure.
            
            Args:
                folder_id: ID of the folder to start the search from. Defaults to "root"
                          (the root of your Google Drive).
                
            Returns:
                A list of tuples, each containing the ID and name of a folder. Returns an
                empty list if no folders are found or an error occurs.
                
            Example:
                ```python
                # List all folders recursively from the root
                all_folders = google.drive.list_all_folders_recursive()
                
                # List all folders recursively from a specific folder
                all_subfolders = google.drive.list_all_folders_recursive(folder_id='folder_id')
                
                # Process the results
                for folder_id, folder_name in all_folders:
                    print(f"Folder: {folder_name}, ID: {folder_id}")
                ```
            """
            try:
                # Query for all folders in the current folder
                folder_query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
                folders = self.service.files().list(
                    q=folder_query,
                    fields="files(id, name)"
                ).execute().get("files", [])
                
                all_folders = [(folder["id"], folder["name"]) for folder in folders]
                
                # Recursively list all folders in each subfolder
                for folder in folders:
                    all_folders.extend(self.list_all_folders_recursive(folder_id=folder["id"]))
                
                return all_folders
            except Exception as e:
                log.error(f"Error listing folders recursively: {str(e)}")
                return []

        def get_folder_id(self, folder_name: str, parent_id: str = "root", create_if_missing: bool = False) -> str:
            """
            Get the ID of a folder by name, optionally creating it if it doesn't exist.
            
            This method searches for a folder with the specified name in a parent folder.
            If the folder is not found, it can optionally create it. This is useful for
            ensuring that a folder exists before trying to use it.
            
            Args:
                folder_name: Name of the folder to find.
                parent_id: ID of the parent folder to search in. Defaults to "root"
                          (the root of your Google Drive).
                create_if_missing: Whether to create the folder if it doesn't exist.
                                  If True and the folder is not found, it will be created.
                
            Returns:
                The ID of the folder as a string. Returns None if the folder is not found
                and create_if_missing is False, or if an error occurs.
                
            Example:
                ```python
                # Get a folder ID by name
                folder_id = google.drive.get_folder_id(folder_name='My Folder')
                
                # Get a folder ID by name, creating it if it doesn't exist
                folder_id = google.drive.get_folder_id(
                    folder_name='My Folder',
                    create_if_missing=True
                )
                
                # Get a folder ID in a specific parent folder
                folder_id = google.drive.get_folder_id(
                    folder_name='Subfolder',
                    parent_id='parent_folder_id'
                )
                ```
            """
            try:
                # Check if the folder exists
                folder_query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"
                folders = self.service.files().list(
                    q=folder_query,
                    fields="files(id, name)"
                ).execute().get("files", [])
                
                if folders:
                    return folders[0]["id"]
                
                # Create the folder if requested and not found
                if create_if_missing:
                    folder = self.create_folder(folder_name, parent_id)
                    return folder["id"]
                
                return None
            except Exception as e:
                log.error(f"Error getting folder ID: {str(e)}")
                return None

        def get_file_id(self, file_name: str, folder_name: str = None, folder_id: str = None, file_type: str = None) -> str:
            """
            Get the ID of a file by name in a specific folder.
            
            This method searches for a file with the specified name in a folder.
            You can specify the folder either by name or by ID, and optionally
            filter by file type.
            
            Args:
                file_name: Name of the file to find.
                folder_name: Name of the folder to search in (mutually exclusive with folder_id).
                folder_id: ID of the folder to search in (mutually exclusive with folder_name).
                file_type: Optional MIME type filter (e.g., "application/vnd.google-apps.document").
                          If provided, only files of this type will be considered.
                
            Returns:
                The ID of the file as a string. Returns None if the file is not found
                or if an error occurs.
                
            Example:
                ```python
                # Get a file ID by name in a specific folder
                file_id = google.drive.get_file_id(
                    file_name='My Document',
                    folder_name='My Folder'
                )
                
                # Get a file ID by name in a specific folder using folder ID
                file_id = google.drive.get_file_id(
                    file_name='My Document',
                    folder_id='folder_id'
                )
                
                # Get a Google Doc by name
                doc_id = google.drive.get_file_id(
                    file_name='My Document',
                    folder_name='My Folder',
                    file_type='application/vnd.google-apps.document'
                )
                ```
            """
            try:
                # Get folder ID if folder name is provided
                if folder_name and not folder_id:
                    folder_id = self.get_folder_id(folder_name)
                    if not folder_id:
                        log.error(f"Folder '{folder_name}' not found.")
                        return None
                
                # Default to root if no folder specified
                if not folder_id:
                    folder_id = "root"
                
                # Build query
                file_query = f"name='{file_name}' and '{folder_id}' in parents"
                if file_type:
                    file_query += f" and mimeType='{file_type}'"
                
                # Search for the file
                files = self.service.files().list(
                    q=file_query,
                    fields="files(id, name)"
                ).execute().get("files", [])
                
                if not files:
                    log.error(f"File '{file_name}' not found in the specified folder.")
                    return None
                
                return files[0]["id"]
            except Exception as e:
                log.error(f"Error getting file ID: {str(e)}")
                return None

        def list_files_in_folder(self, folder_name: str = None, folder_id: str = None, 
                                file_type: str = None) -> Tuple[str, List[Tuple[str, str]]]:
            """
            Get a list of files in a specific folder.
            
            This method retrieves a list of files in a folder. You can specify the folder
            either by name or by ID, and optionally filter by file type.
            
            Args:
                folder_name: Name of the folder to search in (mutually exclusive with folder_id).
                folder_id: ID of the folder to search in (mutually exclusive with folder_name).
                file_type: Optional MIME type filter (e.g., "application/vnd.google-apps.document").
                          If provided, only files of this type will be included.
                
            Returns:
                A tuple containing:
                - The folder ID as a string
                - A list of tuples, each containing the ID and name of a file
                
                Returns (None, []) if the folder is not found or if an error occurs.
                
            Example:
                ```python
                # List all files in a folder
                folder_id, files = google.drive.list_files_in_folder(folder_name='My Folder')
                
                # List all files in a folder using folder ID
                folder_id, files = google.drive.list_files_in_folder(folder_id='folder_id')
                
                # List all Google Docs in a folder
                folder_id, docs = google.drive.list_files_in_folder(
                    folder_name='My Folder',
                    file_type='application/vnd.google-apps.document'
                )
                
                # Process the results
                for file_id, file_name in files:
                    print(f"File: {file_name}, ID: {file_id}")
                ```
            """
            try:
                # Get folder ID if folder name is provided
                if folder_name and not folder_id:
                    folder_id = self.get_folder_id(folder_name)
                    if not folder_id:
                        log.error(f"Folder '{folder_name}' not found.")
                        return None, []
                
                # Default to root if no folder specified
                if not folder_id:
                    folder_id = "root"
                
                # Build query
                file_query = f"'{folder_id}' in parents"
                if file_type:
                    file_query += f" and mimeType='{file_type}'"
                
                # Get files in the folder
                files = self.service.files().list(
                    q=file_query,
                    fields="files(id, name, mimeType)"
                ).execute().get("files", [])
                
                file_list = [(file["id"], file["name"]) for file in files]
                
                return folder_id, file_list
            except Exception as e:
                log.error(f"Error listing files in folder: {str(e)}")
                return None, []

        def delete_file(self, file_id: str) -> bool:
            """
            Delete a file or folder from Google Drive.
            
            This method permanently deletes a file or folder from Google Drive.
            Use with caution as this operation cannot be undone.
            
            Args:
                file_id: ID of the file or folder to delete.
                
            Returns:
                True if the deletion was successful, False otherwise.
                
            Example:
                ```python
                # Delete a file
                success = google.drive.delete_file(file_id='file_id')
                
                # Delete a folder
                success = google.drive.delete_file(file_id='folder_id')
                
                if success:
                    print("File/folder deleted successfully")
                else:
                    print("Failed to delete file/folder")
                ```
            """
            try:
                self.service.files().delete(fileId=file_id).execute()
                return True
            except Exception as e:
                log.error(f"Error deleting file: {str(e)}")
                return False

    class DocsHandler:
        """
        Handler for Google Docs operations.
        
        This handler provides methods for working with Google Docs documents.
        It includes functionality for creating, reading, and managing documents.
        
        All methods include comprehensive error handling and logging to help with debugging.
        """
        
        def __init__(self, service):
            """
            Initialize with an authenticated Google Docs service.
            
            Args:
                service: Authenticated Google Docs service from googleapiclient.discovery.build()
            """
            self.service = service

        def get_document(self, document_id: str):
            """
            Get a Google Doc's content.
            
            This method retrieves the full content and metadata of a Google Doc.
            The returned document includes the document's structure, content, and formatting.
            
            Args:
                document_id: ID of the document to retrieve.
                
            Returns:
                A dictionary containing the document's content and metadata. The structure
                follows the Google Docs API document resource format.
                
            Raises:
                Exception: If the document retrieval fails.
                
            Example:
                ```python
                # Get a document by ID
                document = google.docs.get_document(document_id='your_document_id')
                
                # Access document properties
                title = document.get('title')
                content = document.get('body', {}).get('content', [])
                ```
            """
            try:
                return self.service.documents().get(
                    documentId=document_id
                ).execute()
            except Exception as e:
                log.error(f"Error getting document: {str(e)}")
                raise

        def create_document(self, title: str, folder_id: str = None):
            """
            Create a new Google Doc.
            
            This method creates a new Google Doc with the specified title.
            You can optionally specify a folder ID to create the document in a specific folder.
            
            Args:
                title: Title of the document to create.
                folder_id: Optional ID of the folder to create the document in.
                          If None, the document is created in the root of your Drive.
                
            Returns:
                A dictionary containing the created document's content and metadata.
                The structure follows the Google Docs API document resource format.
                
            Raises:
                Exception: If the document creation fails.
                
            Example:
                ```python
                # Create a new document
                document = google.docs.create_document(title='My New Document')
                
                # Create a new document in a specific folder
                document = google.docs.create_document(
                    title='My New Document',
                    folder_id='folder_id'
                )
                
                # Get the ID of the created document
                doc_id = document['documentId']
                ```
            """
            try:
                body = {
                    'title': title
                }
                
                # If folder_id is provided, we need to use the Drive API to create the document
                if folder_id:
                    # We need to access the drive service from the parent GoogleHelper
                    # This is a bit of a hack, but it works
                    drive_service = build('drive', 'v3', credentials=self.service._http.credentials)
                    
                    doc_metadata = {
                        'name': title,
                        'mimeType': 'application/vnd.google-apps.document',
                        'parents': [folder_id]
                    }
                    
                    doc = drive_service.files().create(
                        body=doc_metadata,
                        fields='id'
                    ).execute()
                    
                    # Now get the document content
                    return self.get_document(doc.get('id'))
                else:
                    # Create document without specifying a folder
                    doc = self.service.documents().create(body=body).execute()
                    return doc
            except Exception as e:
                log.error(f"Error creating document: {str(e)}")
                raise

        def create_or_replace_document(self, title: str, folder_name: str = None, folder_id: str = None):
            """
            Create a new Google Doc with a given title inside a specific folder.
            
            This method creates a new Google Doc with the specified title in a specific folder.
            If a file with the same name already exists in the folder, it gets deleted and replaced.
            This is useful for ensuring that a document exists with a clean state.
            
            Args:
                title: Title of the document to create.
                folder_name: Name of the folder to create the document in (mutually exclusive with folder_id).
                folder_id: ID of the folder to create the document in (mutually exclusive with folder_name).
                
            Returns:
                The ID of the created document as a string.
                
            Raises:
                Exception: If the document creation fails.
                
            Example:
                ```python
                # Create or replace a document in a folder
                doc_id = google.docs.create_or_replace_document(
                    title='My Document',
                    folder_name='My Folder'
                )
                
                # Create or replace a document in a folder using folder ID
                doc_id = google.docs.create_or_replace_document(
                    title='My Document',
                    folder_id='folder_id'
                )
                
                # Use the returned document ID
                document = google.docs.get_document(document_id=doc_id)
                ```
            """
            try:
                # We need to access the drive service from the parent GoogleHelper
                # This is a bit of a hack, but it works
                drive_service = build('drive', 'v3', credentials=self.service._http.credentials)
                
                # Get or create the folder
                if folder_name and not folder_id:
                    # Check if the folder exists
                    folder_query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
                    folders = drive_service.files().list(q=folder_query).execute().get("files", [])
                    
                    if not folders:
                        # Create the folder if it doesn't exist
                        folder_metadata = {
                            "name": folder_name,
                            "mimeType": "application/vnd.google-apps.folder",
                        }
                        folder = drive_service.files().create(
                            body=folder_metadata, 
                            fields="id"
                        ).execute()
                        folder_id = folder.get("id")
                    else:
                        folder_id = folders[0]["id"]
                
                # Check if a document with this name already exists in the folder
                if folder_id:
                    file_query = f"name='{title}' and '{folder_id}' in parents and mimeType='application/vnd.google-apps.document'"
                    files = drive_service.files().list(q=file_query).execute().get("files", [])
                    
                    # Delete existing files with the same name
                    for file in files:
                        drive_service.files().delete(fileId=file["id"]).execute()
                
                # Create the new document
                doc_metadata = {
                    "name": title,
                    "mimeType": "application/vnd.google-apps.document",
                }
                
                if folder_id:
                    doc_metadata["parents"] = [folder_id]
                
                doc = drive_service.files().create(
                    body=doc_metadata, 
                    fields="id"
                ).execute()
                
                return doc.get("id")
            except Exception as e:
                log.error(f"Error creating or replacing document: {str(e)}")
                raise
