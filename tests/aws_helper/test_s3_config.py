"""
Tests for the S3Config class.

This module contains tests for the S3Config Pydantic model used in the AWS helper.
"""

import pytest
from pydantic import ValidationError
from cws_helpers.aws_helper import S3Config

class TestS3Config:
    """
    Tests for the S3Config class.
    
    This class contains tests for the S3Config Pydantic model.
    """
    
    def test_s3_config_with_required_fields(self):
        """
        Test creating an S3Config with only required fields.
        
        This test verifies that an S3Config can be created with just the
        required bucket_name field, and default values are used for other fields.
        """
        config = S3Config(bucket_name="test-bucket")
        
        assert config.bucket_name == "test-bucket"
        assert config.region_name == "us-east-1"  # Default value
        assert config.access_key_id is None  # Default value
        assert config.secret_access_key is None  # Default value
    
    def test_s3_config_with_all_fields(self):
        """
        Test creating an S3Config with all fields.
        
        This test verifies that an S3Config can be created with all fields
        specified, and the values are stored correctly.
        """
        config = S3Config(
            bucket_name="test-bucket",
            region_name="us-west-2",
            access_key_id="test-key",
            secret_access_key="test-secret"
        )
        
        assert config.bucket_name == "test-bucket"
        assert config.region_name == "us-west-2"
        assert config.access_key_id == "test-key"
        assert config.secret_access_key == "test-secret"
    
    def test_s3_config_missing_required_field(self):
        """
        Test creating an S3Config without the required bucket_name field.
        
        This test verifies that a ValidationError is raised when the required
        bucket_name field is missing.
        """
        with pytest.raises(ValidationError) as exc_info:
            S3Config()
        
        # Check that the error message mentions the missing field
        error_message = str(exc_info.value)
        assert "bucket_name" in error_message
        assert "Field required" in error_message
    
    def test_s3_config_with_invalid_type(self):
        """
        Test creating an S3Config with an invalid type for a field.
        
        This test verifies that a ValidationError is raised when a field
        has an invalid type.
        """
        with pytest.raises(ValidationError) as exc_info:
            S3Config(bucket_name=123)  # bucket_name should be a string
        
        # Check that the error message mentions the invalid type
        error_message = str(exc_info.value)
        assert "bucket_name" in error_message
        assert "Input should be a valid string" in error_message
    
    def test_s3_config_dict_conversion(self):
        """
        Test converting an S3Config to a dictionary.
        
        This test verifies that an S3Config can be converted to a dictionary
        with the correct keys and values.
        """
        config = S3Config(
            bucket_name="test-bucket",
            region_name="us-west-2",
            access_key_id="test-key",
            secret_access_key="test-secret"
        )
        
        config_dict = config.model_dump()
        
        assert config_dict["bucket_name"] == "test-bucket"
        assert config_dict["region_name"] == "us-west-2"
        assert config_dict["access_key_id"] == "test-key"
        assert config_dict["secret_access_key"] == "test-secret" 