# Google Helper

A comprehensive helper for interacting with Google APIs including Sheets, Drive, and Docs. This helper handles authentication and provides methods for common operations across different Google services.

## Features

- **Authentication Management**: Handles OAuth2 authentication flow and token refresh
- **Google Sheets**: Read, write, and manipulate spreadsheet data
- **Google Drive**: List, search, create, and manage files and folders
- **Google Docs**: Create, read, and manage documents
- **Recursive Operations**: Recursively list files and folders in Drive
- **Error Handling**: Comprehensive error handling and logging

## Installation

This helper is included in the cws-helpers package:

```bash
pip install git+https://github.com/caseywschmid/cws-helpers.git
```

You'll also need to install the required Google API dependencies:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Authentication Setup

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the APIs you need (Drive API, Sheets API, Docs API, etc.)
3. Create OAuth 2.0 credentials (Desktop application)
4. Download the credentials JSON file and save it as `credentials.json` in your project directory

The first time you use the helper, it will open a browser window for you to authenticate with your Google account. After authentication, a `token.json` file will be created to store your credentials for future use.

## Usage

### Basic Initialization

```python
from cws_helpers import GoogleHelper

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
```

### Working with Google Sheets

#### Reading Data

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

# Simplified reading with default parameters
data = google.sheets.read_sheet(
    spreadsheet_id='your_spreadsheet_id',
    range_name='Sheet1!A1:D10'
)
```

#### Writing Data

```python
# Write data to a specific range
values = [
    ['Name', 'Email', 'Phone'],
    ['John Doe', 'john@example.com', '555-1234'],
    ['Jane Smith', 'jane@example.com', '555-5678']
]
google.sheets.write_range(
    spreadsheet_id='your_spreadsheet_id',
    values=values,
    sheet_name='Sheet1',
    start_cell='A1'
)

# Write data using a range name
google.sheets.write_range(
    spreadsheet_id='your_spreadsheet_id',
    values=values,
    range_name='Sheet1!A1'
)

# Simplified writing with default parameters
google.sheets.write_sheet(
    spreadsheet_id='your_spreadsheet_id',
    values=values,
    range_name='Sheet1!A1'
)
```

#### Clearing Data

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

# Simplified clearing of an output sheet while preserving headers
google.sheets.clear_output_sheet(
    spreadsheet_id='your_spreadsheet_id',
    sheet_name='output'
)
```

#### Finding Empty Rows

```python
# Find the next empty row in a column
next_row = google.sheets.get_next_empty_row(
    spreadsheet_id='your_spreadsheet_id',
    sheet_name='Sheet1',
    column='A'
)
```

#### Getting Sheet Information

```python
# Get the name of the first sheet in a spreadsheet
first_sheet = google.sheets.get_first_sheet_name(
    spreadsheet_id='your_spreadsheet_id'
)
```

### Working with Google Drive

#### Listing Files

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

#### Creating Folders

```python
# Create a folder in the root directory
folder = google.drive.create_folder(name='My New Folder')

# Create a folder inside another folder
folder = google.drive.create_folder(
    name='Subfolder',
    parent_id='parent_folder_id'
)
```

#### Recursive File and Folder Operations

```python
# List all files recursively from the root
all_files = google.drive.list_all_files_recursive()

# List all files recursively from a specific folder
all_files = google.drive.list_all_files_recursive(folder_id='folder_id')

# List all files of a specific type recursively
all_docs = google.drive.list_all_files_recursive(
    file_type='application/vnd.google-apps.document'
)

# List all folders recursively
all_folders = google.drive.list_all_folders_recursive()

# List all folders recursively from a specific folder
all_subfolders = google.drive.list_all_folders_recursive(folder_id='folder_id')
```

#### Finding Files and Folders

```python
# Get a folder ID by name
folder_id = google.drive.get_folder_id(folder_name='My Folder')

# Get a folder ID by name, creating it if it doesn't exist
folder_id = google.drive.get_folder_id(
    folder_name='My Folder',
    create_if_missing=True
)

# Get a file ID by name in a specific folder
file_id = google.drive.get_file_id(
    file_name='My Document',
    folder_name='My Folder'
)

# Get a file ID by name in a specific folder with a specific type
file_id = google.drive.get_file_id(
    file_name='My Document',
    folder_id='folder_id',
    file_type='application/vnd.google-apps.document'
)

# List all files in a folder
folder_id, files = google.drive.list_files_in_folder(folder_name='My Folder')

# List all files of a specific type in a folder
folder_id, docs = google.drive.list_files_in_folder(
    folder_name='My Folder',
    file_type='application/vnd.google-apps.document'
)
```

#### Deleting Files

```python
# Delete a file or folder
success = google.drive.delete_file(file_id='file_id')
```

### Working with Google Docs

#### Getting Documents

```python
# Get a document by ID
document = google.docs.get_document(document_id='your_document_id')
```

#### Creating Documents

```python
# Create a new document
document = google.docs.create_document(title='My New Document')

# Create a new document in a specific folder
document = google.docs.create_document(
    title='My New Document',
    folder_id='folder_id'
)

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
```

## API Reference

### `GoogleHelper`

#### `__init__(scopes: list = None, initialize_services: bool = True)`

Initialize the Google Helper.

- **Parameters:**
  - `scopes`: Optional list of Google API scopes. If None, default scopes for Sheets, Drive, and Docs will be used.
  - `initialize_services`: Whether to initialize service handlers during construction. Set to False for testing purposes.

#### `_get_credentials()`

Get and refresh Google OAuth2 credentials.

- **Returns:**
  - Google OAuth2 credentials object

#### `_get_service(kind: str, version: str)`

Get an authenticated Google API service.

- **Parameters:**
  - `kind`: The API service to get (e.g., "sheets", "drive", "docs")
  - `version`: The API version to use (e.g., "v4", "v3")
- **Returns:**
  - Authenticated Google API service

### `SheetsHandler`

#### `__init__(service)`

Initialize with an authenticated Google Sheets service.

- **Parameters:**
  - `service`: Authenticated Google Sheets service

#### `read_range(spreadsheet_id: str, range_name: str = None, sheet_name: str = None, start_cell: str = "A1", end_cell: str = None) -> list`

Read data from a specified range in a spreadsheet.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
  - `range_name`: Full range to read (e.g., "Sheet1!A1:B10"). If provided, other range params are ignored.
  - `sheet_name`: Name of sheet to read from. If None, reads from first sheet.
  - `start_cell`: Starting cell (e.g., "A1", "B2"). Defaults to "A1".
  - `end_cell`: Ending cell (e.g., "E10", "Z100"). If None, reads to last used cell.
- **Returns:**
  - A list of rows, where each row is a list of values.

#### `write_range(spreadsheet_id: str, values: list, range_name: str = None, sheet_name: str = None, start_cell: str = "A1", input_option: str = "RAW", rate_limit: float = 1.0)`

Write data to a specified range in a spreadsheet.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
  - `values`: The data to write.
  - `range_name`: Full range to write to. If provided, other range params are ignored.
  - `sheet_name`: Name of sheet to write to. If None, writes to first sheet.
  - `start_cell`: Starting cell for write operation (e.g., "A1", "B2").
  - `input_option`: How input should be interpreted ("RAW" or "USER_ENTERED").
  - `rate_limit`: Seconds to wait after write (for rate limiting).

#### `clear_range(spreadsheet_id: str, range_name: str = None, sheet_name: str = None, start_cell: str = None, end_cell: str = None, preserve_headers: bool = False)`

Clear data from a specified range in a spreadsheet.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
  - `range_name`: Full range to clear (e.g., "Sheet1!A1:B10"). If provided, other range params are ignored.
  - `sheet_name`: Name of sheet to clear. If None, uses first sheet.
  - `start_cell`: Starting cell (e.g., "A1", "B2").
  - `end_cell`: Ending cell (e.g., "E10", "Z100").
  - `preserve_headers`: Whether to preserve the first row (headers).

#### `get_first_sheet_name(spreadsheet_id: str) -> str`

Get the name of the first sheet in a spreadsheet.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
- **Returns:**
  - The name of the first sheet.

#### `get_next_empty_row(spreadsheet_id: str, sheet_name: str = None, column: str = "A") -> int`

Find the next empty row in a specified column.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
  - `sheet_name`: Name of the sheet to check.
  - `column`: Column to check (e.g., "A", "B").
- **Returns:**
  - The row number of the next empty row (1-indexed).

#### `read_sheet(spreadsheet_id: str, range_name: str = None) -> list`

Alias for read_range with simpler parameters.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
  - `range_name`: Range to read.
- **Returns:**
  - A list of rows, where each row is a list of values.

#### `write_sheet(spreadsheet_id: str, values: list, range_name: str = None)`

Alias for write_range with simpler parameters.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
  - `values`: The data to write.
  - `range_name`: Range to write to.

#### `clear_output_sheet(spreadsheet_id: str, sheet_name: str = "output")`

Clear a sheet while preserving headers.

- **Parameters:**
  - `spreadsheet_id`: ID of the spreadsheet.
  - `sheet_name`: Name of the sheet to clear. Defaults to "output".

### `DriveHandler`

#### `__init__(service)`

Initialize with an authenticated Google Drive service.

- **Parameters:**
  - `service`: Authenticated Google Drive service.

#### `list_files(query: str = None, page_size: int = 10, fields: str = None)`

List files in Google Drive.

- **Parameters:**
  - `query`: Search query string (e.g., "name contains 'Report'").
  - `page_size`: Maximum number of files to return.
  - `fields`: Fields to include in the response (default: id, name, mimeType).
- **Returns:**
  - List of file metadata.

#### `create_folder(name: str, parent_id: str = None)`

Create a new folder in Google Drive.

- **Parameters:**
  - `name`: Name of the folder.
  - `parent_id`: ID of the parent folder. If None, creates in root.
- **Returns:**
  - Metadata of the created folder.

#### `list_all_files_recursive(folder_id: str = "root", file_type: str = None) -> List[Tuple[str, str]]`

Recursively list all files in a Google Drive folder.

- **Parameters:**
  - `folder_id`: ID of the folder to start the search from.
  - `file_type`: Optional MIME type filter (e.g., "application/vnd.google-apps.document").
- **Returns:**
  - List of tuples, each containing the ID and name of a file.

#### `list_all_folders_recursive(folder_id: str = "root") -> List[Tuple[str, str]]`

Recursively list all folders in Google Drive.

- **Parameters:**
  - `folder_id`: ID of the folder to start the search from.
- **Returns:**
  - List of tuples, each containing the ID and name of a folder.

#### `get_folder_id(folder_name: str, parent_id: str = "root", create_if_missing: bool = False) -> str`

Get the ID of a folder by name, optionally creating it if it doesn't exist.

- **Parameters:**
  - `folder_name`: Name of the folder to find.
  - `parent_id`: ID of the parent folder to search in.
  - `create_if_missing`: Whether to create the folder if it doesn't exist.
- **Returns:**
  - ID of the folder, or None if not found and not created.

#### `get_file_id(file_name: str, folder_name: str = None, folder_id: str = None, file_type: str = None) -> str`

Get the ID of a file by name in a specific folder.

- **Parameters:**
  - `file_name`: Name of the file to find.
  - `folder_name`: Name of the folder to search in (mutually exclusive with folder_id).
  - `folder_id`: ID of the folder to search in (mutually exclusive with folder_name).
  - `file_type`: Optional MIME type filter (e.g., "application/vnd.google-apps.document").
- **Returns:**
  - ID of the file, or None if not found.

#### `list_files_in_folder(folder_name: str = None, folder_id: str = None, file_type: str = None) -> Tuple[str, List[Tuple[str, str]]]`

Get a list of files in a specific folder.

- **Parameters:**
  - `folder_name`: Name of the folder to search in (mutually exclusive with folder_id).
  - `folder_id`: ID of the folder to search in (mutually exclusive with folder_name).
  - `file_type`: Optional MIME type filter (e.g., "application/vnd.google-apps.document").
- **Returns:**
  - Tuple containing the folder ID and a list of tuples (file_id, file_name).

#### `delete_file(file_id: str) -> bool`

Delete a file or folder from Google Drive.

- **Parameters:**
  - `file_id`: ID of the file or folder to delete.
- **Returns:**
  - True if successful, False otherwise.

### `DocsHandler`

#### `__init__(service)`

Initialize with an authenticated Google Docs service.

- **Parameters:**
  - `service`: Authenticated Google Docs service.

#### `get_document(document_id: str)`

Get a Google Doc's content.

- **Parameters:**
  - `document_id`: ID of the document.
- **Returns:**
  - Document content.

#### `create_document(title: str, folder_id: str = None)`

Create a new Google Doc.

- **Parameters:**
  - `title`: Title of the document.
  - `folder_id`: Optional ID of the folder to create the document in.
- **Returns:**
  - Document resource of the created document.

#### `create_or_replace_document(title: str, folder_name: str = None, folder_id: str = None)`

Create a new Google Doc with a given title inside a specific folder. If a file with the same name already exists, it gets deleted and replaced.

- **Parameters:**
  - `title`: Title of the document.
  - `folder_name`: Name of the folder (mutually exclusive with folder_id).
  - `folder_id`: ID of the folder (mutually exclusive with folder_name).
- **Returns:**
  - ID of the created document.

## Common MIME Types

- Google Document: `application/vnd.google-apps.document`
- Google Spreadsheet: `application/vnd.google-apps.spreadsheet`
- Google Presentation: `application/vnd.google-apps.presentation`
- Google Folder: `application/vnd.google-apps.folder`
- PDF: `application/pdf`
- Text: `text/plain`
- CSV: `text/csv`
- Excel: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Word: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

## Error Handling

All methods include comprehensive error handling and logging. Errors are logged with detailed information to help with debugging. Most methods return sensible defaults (like empty lists or None) when errors occur, rather than raising exceptions, to prevent application crashes.

## Best Practices

1. **Rate Limiting**: Be mindful of Google API quotas. The `write_range` method includes a `rate_limit` parameter to help avoid quota issues.
2. **Authentication**: Store your `credentials.json` file securely and never commit it to version control.
3. **Scopes**: Only request the scopes you need to minimize security risks.
4. **Error Handling**: Always check return values for None or empty lists, which may indicate errors.
5. **Folder Operations**: When working with folders, prefer using folder IDs over folder names when possible for better performance. 