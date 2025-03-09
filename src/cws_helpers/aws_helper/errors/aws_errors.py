"""
AWS-specific exceptions for the application.

This module contains custom exceptions for AWS-related operations. These exceptions
provide more specific error handling and better error messages for AWS operations
compared to using generic exceptions.

Usage:
    from errors.aws_errors import AWSConfigError, S3UploadError, S3DownloadError

    try:
        # AWS operation
        pass
    except AWSConfigError as e:
        # Handle AWS configuration errors
        pass
    except S3UploadError as e:
        # Handle S3 upload errors
        pass
    except S3DownloadError as e:
        # Handle S3 download errors
        pass
"""

class AWSError(Exception):
    """
    Base exception class for all AWS-related errors.
    
    This class serves as the parent class for all AWS-specific exceptions
    in the application. It inherits from the built-in Exception class.
    
    Attributes:
        message (str): The error message.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class AWSConfigError(AWSError):
    """
    Exception raised when there are AWS configuration issues.
    
    This exception is raised when there are problems with AWS credentials,
    region configuration, or other AWS-related settings.
    
    Example:
        >>> raise AWSConfigError("AWS credentials not found in environment variables")
    """
    pass

class S3Error(AWSError):
    """
    Base exception class for all S3-related errors.
    
    This class serves as the parent class for more specific S3 exceptions.
    It should be used for general S3 operations that don't fit into more
    specific categories.
    
    Example:
        >>> raise S3Error("Failed to list objects in bucket")
    """
    pass

class S3UploadError(S3Error):
    """
    Exception raised when an S3 upload operation fails.
    
    This exception is raised for any errors that occur during file uploads
    to AWS S3, including network issues, permission errors, or invalid
    bucket names.
    
    Example:
        >>> raise S3UploadError("Failed to upload file: Network timeout")
    """
    pass

class S3DownloadError(S3Error):
    """
    Exception raised when an S3 download operation fails.
    
    This exception is raised for any errors that occur during file downloads
    from AWS S3, including missing files, network issues, or permission errors.
    
    Example:
        >>> raise S3DownloadError("Failed to download file: Object does not exist")
    """
    pass 