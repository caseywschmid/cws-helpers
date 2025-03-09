# AWS Helper

This module provides a clean, type-safe interface for AWS S3 operations. It handles AWS credentials through either direct parameters or environment variables.

## Features

- Type-safe S3 operations with Pydantic models
- Comprehensive error handling with custom exceptions
- Support for both raw data and JSON operations
- Automatic pagination for listing objects
- Environment variable fallbacks for credentials

## Requirements

- boto3
- pydantic

## Usage

### Basic Usage

```python
from cws_helpers import S3Helper

# Initialize S3 helper with bucket name
# Credentials will be read from environment variables
s3 = S3Helper(bucket_name='my-bucket')

# Store a string
s3.put_object('path/to/file.txt', 'Hello, World!')

# Store JSON data
data = {"key": "value", "nested": {"data": 123}}
s3.put_object('path/to/data.json', data)

# Read raw data
content = s3.get_object('path/to/file.txt')
print(content)  # b'Hello, World!'

# Read and parse JSON data
json_data = s3.get_json('path/to/data.json')
print(json_data)  # {"key": "value", "nested": {"data": 123}}

# Check if an object exists
if s3.object_exists('path/to/file.txt'):
    print('File exists!')

# List objects with a prefix
files = s3.list_objects(prefix='path/to/')
for file in files:
    print(file)

# Delete an object
s3.delete_object('path/to/file.txt')
```

### With Explicit Credentials

```python
s3 = S3Helper(
    bucket_name='my-bucket',
    region_name='us-west-2',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)
```

## Environment Variables

The following environment variables are used if credentials are not provided explicitly:

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
- `AWS_DEFAULT_REGION`: Default AWS region (defaults to "us-east-1" if not set)

## Error Handling

The module provides custom exceptions for better error handling:

```python
from cws_helpers.aws_helper import S3DownloadError, S3UploadError

try:
    data = s3.get_json('non-existent-file.json')
except S3DownloadError as e:
    print(f"Download error: {e}")

try:
    s3.put_object('path/to/file.txt', 'content')
except S3UploadError as e:
    print(f"Upload error: {e}")
``` 