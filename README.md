# CWS Helpers

A collection of helper utilities for personal Python projects, providing enhanced functionality and convenience features.

## Available Packages

- **[Logger](src/cws_helpers/logger/README.md)**: Enhanced logging system with custom levels, colored output, and file logging capabilities
- **[OpenAI Helper](src/cws_helpers/openai_helper/README.md)**: Simplified interface for interacting with OpenAI's API, supporting text completions, image inputs, JSON mode, and structured outputs
- **[AWS Helper](src/cws_helpers/aws_helper/README.md)**: Type-safe interface for AWS S3 operations with comprehensive error handling and automatic pagination
- **[YouTube Helper](src/cws_helpers/youtube_helper/README.md)**: Utilities for interacting with YouTube videos, extracting video information, validating URLs, and working with captions
- **[Google Helper](src/cws_helpers/google_helper/README.md)**: Comprehensive helper for interacting with Google APIs including Sheets, Drive, and Docs with authentication handling
- **[PowerPath Helper](src/cws_helpers/powerpath_helper/README.md)**: Complete interface for the PowerPath API with models, clients, and utility functions for educational content management
- *(More packages to be added)*

Each helper includes its own documentation in its respective directory.

## Installation

### For Users

You can install this package directly from GitHub using pip without needing Poetry:

```bash
# Install the latest version
pip install git+https://github.com/caseywschmid/cws-helpers.git

# Install a specific version using a tag
pip install git+https://github.com/caseywschmid/cws-helpers.git@v0.1.0
```

For requirements.txt:
```
# Always get the latest version
git+https://github.com/caseywschmid/cws-helpers.git

# Or pin to a specific version tag
git+https://github.com/caseywschmid/cws-helpers.git@v0.1.0
```

### Versioning and Updates

This package uses semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR version for incompatible API changes
- MINOR version for added functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes

When you install the package, you can control how updates are handled:

1. **Latest version** (will update when you run `pip install --upgrade`):
   ```
   pip install git+https://github.com/caseywschmid/cws-helpers.git
   ```

2. **Specific version tag** (stable, won't automatically update):
   ```
   pip install git+https://github.com/caseywschmid/cws-helpers.git@v0.1.0
   ```

3. **Specific commit** (exact version, won't automatically update):
   ```
   pip install git+https://github.com/caseywschmid/cws-helpers.git@8d3b355fd90b0f5326e21942790ba063fb77e9c9
   ```

Check the [releases page](https://github.com/caseywschmid/cws-helpers/releases) for the latest version information and the [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

### For Developers

This package uses Poetry for development and dependency management. To contribute or modify the package:

```bash
# Clone the repository
git clone https://github.com/caseywschmid/cws-helpers.git

# Navigate to the project directory
cd cws-helpers

# Install dependencies using Poetry
poetry install
```

### Package Structure

This project uses a `src` layout, which means the actual package code is in the `src/cws_helpers` directory. When you install the package (either via Poetry or pip), the package will be available as `cws_helpers` in your Python environment.

```
cws-helpers/
├── src/
│   └── cws_helpers/  # This becomes the importable package
│       ├── __init__.py
│       ├── logger/
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   └── README.md
│       ├── openai_helper/
│       │   ├── __init__.py
│       │   ├── openai_helper.py
│       │   └── README.md
│       └── ...
└── ...
```

## Quick Examples

### Logger

```python
from cws_helpers.logger import configure_logging

logger = configure_logging(logger_name="my_app")
logger.info("Application started")
logger.success("Operation completed successfully!")
```

### OpenAI Helper

```python
from cws_helpers import OpenAIHelper
import os

helper = OpenAIHelper(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORGANIZATION")
)

response = helper.create_chat_completion(
    prompt="What is the capital of France?",
    model="gpt-3.5-turbo"
)
```

### AWS Helper

```python
from cws_helpers import S3Helper

# Initialize with bucket name (credentials from environment variables)
s3 = S3Helper(bucket_name='my-bucket')

# Store JSON data
data = {"key": "value"}
s3.put_object("path/to/file.json", data)

# Read JSON data
content = s3.get_json("path/to/file.json")
```

### YouTube Helper

```python
from cws_helpers import YoutubeHelper

# Initialize the helper
youtube = YoutubeHelper()

# Check if a URL is a valid YouTube URL
is_valid = youtube.is_valid_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Get detailed information about a video
video_info = youtube.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

### Google Helper

```python
from cws_helpers import GoogleHelper

# Initialize with specific scopes
google = GoogleHelper(scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Read data from a spreadsheet
data = google.sheets.read_range(
    spreadsheet_id='your_spreadsheet_id',
    sheet_name='Sheet1',
    start_cell='A1',
    end_cell='D10'
)

# List files in Drive
files = google.drive.list_files(query="name contains 'Report'")
```

### PowerPath Helper

```python
from cws_helpers.powerpath_helper import PowerPathClient, get_all_courses, get_user

# Initialize the client (base URL is set by default)
client = PowerPathClient()

# Get all courses
courses = get_all_courses(client)
print(f"Found {len(courses)} courses")

# Get a specific user
user = get_user(client, "123")
print(f"User: {user.given_name} {user.family_name}")
```

For detailed usage instructions and API documentation for each helper, see the README.md file in the helper's directory.

## Dependencies

- Python ^3.9
- python-dotenv ^1.0.1
- openai ^1.65.5
- pydantic ^2.10.6
- boto3 ^1.37.9
- yt-dlp ^2025.2.19
- google-auth ^2.32.0
- google-auth-oauthlib ^1.2.0
- google-auth-httplib2 ^0.2.0
- google-api-python-client ^2.133.0
- pytest ^8.3.5 (dev dependency)
- moto ^5.1.1 (dev dependency)

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Install development dependencies: `poetry install`
4. Run tests: `poetry run pytest`
5. Submit a pull request

For guidance on adding a new helper, see [How to add a new helper](docs/How_to_add_a_new_helper.md).

## License

MIT License

## Author

Casey Schmid (caseywschmid@gmail.com)

