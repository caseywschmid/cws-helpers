"""
Tests for the AWS error classes.

This module contains tests for the custom AWS error classes used in the AWS helper.
"""

import pytest
from cws_helpers.aws_helper import (
    AWSError,
    AWSConfigError,
    S3Error,
    S3UploadError,
    S3DownloadError
)

class TestAWSErrors:
    """
    Tests for the AWS error classes.
    
    This class contains tests for all the custom AWS error classes.
    """
    
    def test_aws_error_base_class(self):
        """
        Test the base AWSError class.
        
        This test verifies that:
        1. The error message is stored correctly
        2. The error can be converted to a string
        3. The error inherits from Exception
        """
        error_message = "Test AWS error"
        error = AWSError(error_message)
        
        assert error.message == error_message
        assert str(error) == error_message
        assert isinstance(error, Exception)
    
    def test_aws_config_error(self):
        """
        Test the AWSConfigError class.
        
        This test verifies that:
        1. The error message is stored correctly
        2. The error inherits from AWSError
        """
        error_message = "AWS credentials not found"
        error = AWSConfigError(error_message)
        
        assert error.message == error_message
        assert isinstance(error, AWSError)
    
    def test_s3_error_base_class(self):
        """
        Test the base S3Error class.
        
        This test verifies that:
        1. The error message is stored correctly
        2. The error inherits from AWSError
        """
        error_message = "Test S3 error"
        error = S3Error(error_message)
        
        assert error.message == error_message
        assert isinstance(error, AWSError)
    
    def test_s3_upload_error(self):
        """
        Test the S3UploadError class.
        
        This test verifies that:
        1. The error message is stored correctly
        2. The error inherits from S3Error
        """
        error_message = "Failed to upload object"
        error = S3UploadError(error_message)
        
        assert error.message == error_message
        assert isinstance(error, S3Error)
    
    def test_s3_download_error(self):
        """
        Test the S3DownloadError class.
        
        This test verifies that:
        1. The error message is stored correctly
        2. The error inherits from S3Error
        """
        error_message = "Failed to download object"
        error = S3DownloadError(error_message)
        
        assert error.message == error_message
        assert isinstance(error, S3Error)
    
    def test_error_inheritance_chain(self):
        """
        Test the error inheritance chain.
        
        This test verifies that the error inheritance chain is correct:
        Exception -> AWSError -> S3Error -> S3UploadError/S3DownloadError
        """
        upload_error = S3UploadError("Upload error")
        download_error = S3DownloadError("Download error")
        
        # Test S3UploadError inheritance
        assert isinstance(upload_error, S3Error)
        assert isinstance(upload_error, AWSError)
        assert isinstance(upload_error, Exception)
        
        # Test S3DownloadError inheritance
        assert isinstance(download_error, S3Error)
        assert isinstance(download_error, AWSError)
        assert isinstance(download_error, Exception)
    
    def test_error_catching(self):
        """
        Test catching errors at different levels of the inheritance chain.
        
        This test verifies that errors can be caught at any level of the
        inheritance chain.
        """
        # Create an error
        error = S3UploadError("Test error")
        
        # Test catching as S3UploadError
        try:
            raise error
        except S3UploadError as e:
            assert e is error
        
        # Test catching as S3Error
        try:
            raise error
        except S3Error as e:
            assert e is error
        
        # Test catching as AWSError
        try:
            raise error
        except AWSError as e:
            assert e is error
        
        # Test catching as Exception
        try:
            raise error
        except Exception as e:
            assert e is error 