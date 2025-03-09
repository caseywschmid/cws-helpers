"""
AWS Helper Package

This package provides helpers for AWS services like S3.
It includes classes for S3 operations and custom exceptions for AWS-related errors.

Example:
    from cws_helpers.aws_helper import S3Helper
    
    s3 = S3Helper(bucket_name='my-bucket')
    s3.put_object('path/to/file.txt', 'Hello, World!')
"""

from .aws_helper import S3Helper, S3Config
from .errors.aws_errors import (
    AWSError,
    AWSConfigError,
    S3Error,
    S3UploadError,
    S3DownloadError
)

__all__ = [
    'S3Helper',
    'S3Config',
    'AWSError',
    'AWSConfigError',
    'S3Error',
    'S3UploadError',
    'S3DownloadError'
]
