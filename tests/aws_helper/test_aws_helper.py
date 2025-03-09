"""
Tests for the AWS helper module.

This module contains tests for the S3Helper class, which provides a clean interface
for S3 operations. It uses pytest for testing and moto for mocking AWS services.

Note: These tests require the following packages:
    - pytest
    - moto
    - boto3
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock
import boto3
from botocore.exceptions import ClientError
from moto import mock_aws
from cws_helpers.aws_helper import S3Helper
from cws_helpers.aws_helper import AWSConfigError, S3UploadError, S3DownloadError, S3Error

# Test constants
TEST_BUCKET = "test-bucket"
TEST_REGION = "us-east-1"
TEST_KEY = "test/key.txt"
TEST_JSON_KEY = "test/data.json"
TEST_CONTENT = b"Test content"
TEST_JSON_DATA = {"key": "value", "nested": {"data": 123}}

@pytest.fixture(scope="function")
def aws_credentials():
    """
    Mocked AWS Credentials for moto.
    
    This fixture sets up mock AWS credentials for testing purposes.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = TEST_REGION

@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    """
    Mocked S3 client.
    
    This fixture creates a mocked S3 client and test bucket.
    """
    with mock_aws():
        s3_client = boto3.client("s3", region_name=TEST_REGION)
        s3_client.create_bucket(Bucket=TEST_BUCKET)
        yield s3_client

@pytest.fixture(scope="function")
def s3_helper(aws_credentials):
    """
    S3Helper instance for testing.
    
    This fixture creates an S3Helper instance with mock credentials.
    """
    with mock_aws():
        # Create the bucket first
        s3_client = boto3.client(
            "s3", 
            region_name=TEST_REGION,
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        s3_client.create_bucket(Bucket=TEST_BUCKET)
        
        # Create and return the helper
        helper = S3Helper(
            bucket_name=TEST_BUCKET,
            region_name=TEST_REGION
        )
        yield helper

class TestS3Helper:
    """
    Tests for the S3Helper class.
    
    This class contains tests for all the methods in the S3Helper class.
    """
    
    def test_init_with_credentials(self):
        """
        Test initialization with explicit credentials.
        """
        helper = S3Helper(
            bucket_name=TEST_BUCKET,
            region_name=TEST_REGION,
            aws_access_key_id="test_key",
            aws_secret_access_key="test_secret"
        )
        assert helper.bucket_name == TEST_BUCKET
        assert helper.region_name == TEST_REGION
        
    def test_init_missing_credentials(self):
        """
        Test initialization with missing credentials.
        """
        # Clear environment variables
        os.environ.pop("AWS_ACCESS_KEY_ID", None)
        os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
        
        with pytest.raises(AWSConfigError) as exc_info:
            S3Helper(bucket_name=TEST_BUCKET)
        
        assert "AWS credentials not found" in str(exc_info.value)
    
    def test_put_and_get_object(self, s3_helper):
        """
        Test putting and getting an object.
        
        This test verifies that:
        1. An object can be uploaded successfully
        2. The same object can be retrieved with the correct content
        """
        # Put the object
        s3_helper.put_object(TEST_KEY, TEST_CONTENT)
        
        # Get the object
        content = s3_helper.get_object(TEST_KEY)
        
        # Verify content
        assert content == TEST_CONTENT
    
    def test_put_and_get_json(self, s3_helper):
        """
        Test putting and getting JSON data.
        
        This test verifies that:
        1. JSON data can be uploaded successfully
        2. The same data can be retrieved and parsed correctly
        """
        # Put the JSON data
        s3_helper.put_object(TEST_JSON_KEY, TEST_JSON_DATA)
        
        # Get the JSON data
        data = s3_helper.get_json(TEST_JSON_KEY)
        
        # Verify data
        assert data == TEST_JSON_DATA
    
    def test_object_exists(self, s3_helper):
        """
        Test checking if an object exists.
        """
        # Initially the object should not exist
        assert not s3_helper.object_exists(TEST_KEY)
        
        # Put the object
        s3_helper.put_object(TEST_KEY, TEST_CONTENT)
        
        # Now it should exist
        assert s3_helper.object_exists(TEST_KEY)
    
    def test_list_objects(self, s3_helper):
        """
        Test listing objects with a prefix.
        """
        # Create multiple objects with different prefixes
        prefix = "test/list/"
        keys = [f"{prefix}file{i}.txt" for i in range(5)]
        
        for key in keys:
            s3_helper.put_object(key, TEST_CONTENT)
        
        # Also create an object with a different prefix
        s3_helper.put_object("other/file.txt", TEST_CONTENT)
        
        # List objects with the prefix
        result = s3_helper.list_objects(prefix=prefix)
        
        # Verify all expected keys are returned
        assert sorted(result) == sorted(keys)
        
        # Test with max_keys
        result_limited = s3_helper.list_objects(prefix=prefix, max_keys=2)
        assert len(result_limited) == 2
        assert all(key in keys for key in result_limited)
    
    def test_delete_object(self, s3_helper):
        """
        Test deleting an object.
        """
        # Put the object
        s3_helper.put_object(TEST_KEY, TEST_CONTENT)
        
        # Verify it exists
        assert s3_helper.object_exists(TEST_KEY)
        
        # Delete the object
        s3_helper.delete_object(TEST_KEY)
        
        # Verify it no longer exists
        assert not s3_helper.object_exists(TEST_KEY)
    
    def test_get_nonexistent_object(self, s3_helper):
        """
        Test getting a non-existent object.
        """
        with pytest.raises(S3DownloadError) as exc_info:
            s3_helper.get_object("nonexistent.txt")
        
        assert "Object not found" in str(exc_info.value)
    
    def test_get_invalid_json(self, s3_helper):
        """
        Test getting invalid JSON data.
        """
        # Put invalid JSON
        s3_helper.put_object(TEST_KEY, "Not valid JSON")
        
        with pytest.raises(S3DownloadError) as exc_info:
            s3_helper.get_json(TEST_KEY)
        
        assert "Failed to parse JSON" in str(exc_info.value)
        
    def test_put_object_with_string(self, s3_helper):
        """
        Test putting a string object.
        
        This test verifies that a string can be uploaded correctly.
        """
        # Put a string
        test_string = "Hello, World!"
        s3_helper.put_object(TEST_KEY, test_string)
        
        # Get the object
        content = s3_helper.get_object(TEST_KEY)
        
        # Verify content (should be bytes)
        assert content == test_string.encode('utf-8')
        
    def test_put_object_with_content_type(self, s3_helper, s3_client):
        """
        Test putting an object with a specific content type.
        
        This test verifies that the content type is set correctly.
        """
        # Put an object with content type
        content_type = "application/xml"
        s3_helper.put_object(TEST_KEY, TEST_CONTENT, content_type=content_type)
        
        # Verify content type using the S3 client directly
        response = s3_client.head_object(Bucket=TEST_BUCKET, Key=TEST_KEY)
        assert response.get('ContentType') == content_type
        
    def test_list_objects_pagination(self, s3_helper):
        """
        Test pagination in list_objects.
        
        This test verifies that pagination works correctly when there are
        more objects than can be returned in a single response.
        """
        # Create many objects (more than default pagination limit)
        prefix = "test/pagination/"
        keys = [f"{prefix}file{i}.txt" for i in range(1005)]  # More than 1000 (default limit)
        
        # Mock the pagination by patching the list_objects_v2 method
        # Since creating 1005 objects is slow, we'll simulate pagination
        original_list_objects = s3_helper.s3_client.list_objects_v2
        
        def mock_list_objects_v2(**kwargs):
            """Mock implementation that simulates pagination."""
            prefix = kwargs.get('Prefix', '')
            max_keys = kwargs.get('MaxKeys', 1000)
            continuation_token = kwargs.get('ContinuationToken')
            
            # Filter keys by prefix
            matching_keys = [k for k in keys if k.startswith(prefix)]
            
            # Handle pagination
            if continuation_token == "token1":
                # Second page
                start_idx = 1000
                is_truncated = False
                next_token = None
            else:
                # First page
                start_idx = 0
                is_truncated = True
                next_token = "token1"
            
            # Get the slice of keys for this page
            end_idx = min(start_idx + max_keys, len(matching_keys))
            page_keys = matching_keys[start_idx:end_idx]
            
            # Build response
            contents = [{'Key': key} for key in page_keys]
            response = {
                'Contents': contents,
                'IsTruncated': is_truncated
            }
            if next_token:
                response['NextContinuationToken'] = next_token
                
            return response
        
        # Replace the method with our mock
        s3_helper.s3_client.list_objects_v2 = mock_list_objects_v2
        
        try:
            # Test listing all objects
            result = s3_helper.list_objects(prefix=prefix)
            
            # Should return all keys
            assert len(result) == len(keys)
            assert sorted(result) == sorted(keys)
            
            # Test with max_keys
            result_limited = s3_helper.list_objects(prefix=prefix, max_keys=500)
            assert len(result_limited) == 500
            
        finally:
            # Restore the original method
            s3_helper.s3_client.list_objects_v2 = original_list_objects
            
    def test_delete_nonexistent_object(self, s3_helper):
        """
        Test deleting a non-existent object.
        
        This test verifies that deleting a non-existent object doesn't raise an error.
        """
        # Delete a non-existent object
        s3_helper.delete_object("nonexistent.txt")
        
        # No assertion needed - the test passes if no exception is raised
        
    def test_put_object_with_empty_content(self, s3_helper):
        """
        Test putting an object with empty content.
        
        This test verifies that an empty object can be uploaded and retrieved.
        """
        # Put an empty object
        s3_helper.put_object(TEST_KEY, b"")
        
        # Get the object
        content = s3_helper.get_object(TEST_KEY)
        
        # Verify content
        assert content == b""
        
    def test_list_objects_empty_result(self, s3_helper):
        """
        Test listing objects with a prefix that doesn't match any objects.
        
        This test verifies that an empty list is returned when no objects match.
        """
        # List objects with a prefix that doesn't exist
        result = s3_helper.list_objects(prefix="nonexistent/")
        
        # Should return an empty list
        assert result == []
        
    def test_put_object_upload_error(self, s3_helper):
        """
        Test handling of upload errors.
        
        This test verifies that S3UploadError is raised when the upload fails.
        """
        # Mock the put_object method to raise an exception
        with patch.object(s3_helper.s3_client, 'put_object', side_effect=Exception("Upload failed")):
            with pytest.raises(S3UploadError) as exc_info:
                s3_helper.put_object(TEST_KEY, TEST_CONTENT)
            
            assert "Failed to upload object" in str(exc_info.value)
            
    def test_get_object_download_error(self, s3_helper):
        """
        Test handling of download errors.
        
        This test verifies that S3DownloadError is raised when the download fails
        with an error other than NoSuchKey.
        """
        # Create a ClientError with a non-NoSuchKey error code
        error_response = {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}}
        client_error = ClientError(error_response, 'GetObject')
        
        # Mock the get_object method to raise the client error
        with patch.object(s3_helper.s3_client, 'get_object', side_effect=client_error):
            with pytest.raises(S3DownloadError) as exc_info:
                s3_helper.get_object(TEST_KEY)
            
            assert "Failed to get object" in str(exc_info.value)
            
    def test_object_exists_error(self, s3_helper):
        """
        Test handling of errors in object_exists.
        
        This test verifies that S3DownloadError is raised when head_object fails
        with an error other than 404.
        """
        # Create a ClientError with a non-404 error code
        error_response = {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}}
        client_error = ClientError(error_response, 'HeadObject')
        
        # Mock the head_object method to raise the client error
        with patch.object(s3_helper.s3_client, 'head_object', side_effect=client_error):
            with pytest.raises(S3DownloadError) as exc_info:
                s3_helper.object_exists(TEST_KEY)
            
            assert "Error checking object existence" in str(exc_info.value)
            
    def test_list_objects_error(self, s3_helper):
        """
        Test handling of errors in list_objects.
        
        This test verifies that S3Error is raised when list_objects_v2 fails.
        """
        # Mock the list_objects_v2 method to raise an exception
        with patch.object(s3_helper.s3_client, 'list_objects_v2', side_effect=Exception("Listing failed")):
            with pytest.raises(S3Error) as exc_info:
                s3_helper.list_objects(prefix="test/")
            
            assert "Failed to list objects" in str(exc_info.value)
            
    def test_complex_json_serialization(self, s3_helper):
        """
        Test handling of complex JSON data with custom types.
        
        This test verifies that complex JSON data with custom types
        can be serialized and deserialized correctly.
        """
        from datetime import datetime
        
        # Create complex data with a datetime (not directly JSON serializable)
        complex_data = {
            "name": "Test",
            "created_at": datetime(2023, 1, 1, 12, 0, 0),
            "nested": {
                "updated_at": datetime(2023, 1, 2, 12, 0, 0)
            }
        }
        
        # Put the complex data
        s3_helper.put_object(TEST_JSON_KEY, complex_data)
        
        # Get the data
        result = s3_helper.get_json(TEST_JSON_KEY)
        
        # Verify the data (datetimes should be converted to strings)
        assert result["name"] == "Test"
        assert "created_at" in result
        assert "nested" in result
        assert "updated_at" in result["nested"]

    def test_get_object_unexpected_error(self, s3_helper):
        """
        Test handling of unexpected errors in get_object.
        
        This test verifies that S3DownloadError is raised when get_object
        encounters an unexpected error.
        """
        # Mock the get_object method to raise an unexpected exception
        with patch.object(s3_helper.s3_client, 'get_object', side_effect=RuntimeError("Unexpected error")):
            with pytest.raises(S3DownloadError) as exc_info:
                s3_helper.get_object(TEST_KEY)
            
            assert "Unexpected error getting object" in str(exc_info.value)
    
    def test_list_objects_max_keys_already_reached(self, s3_helper):
        """
        Test list_objects when max_keys is already reached.
        
        This test verifies that the method handles the case where max_keys
        is already reached before making another API call.
        """
        # Create a few objects
        prefix = "test/max_keys/"
        keys = [f"{prefix}file{i}.txt" for i in range(3)]
        
        for key in keys:
            s3_helper.put_object(key, TEST_CONTENT)
        
        # Mock the list_objects_v2 method to simulate pagination
        original_list_objects = s3_helper.s3_client.list_objects_v2
        
        call_count = 0
        
        def mock_list_objects_v2(**kwargs):
            """Mock implementation that forces a second call with max_keys already reached."""
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                # First call returns all keys and indicates there are more
                return {
                    'Contents': [{'Key': key} for key in keys],
                    'IsTruncated': True,
                    'NextContinuationToken': 'token1'
                }
            else:
                # Second call should not be made if max_keys is already reached
                # But if it is, return an empty result
                return {
                    'Contents': [],
                    'IsTruncated': False
                }
        
        # Replace the method with our mock
        s3_helper.s3_client.list_objects_v2 = mock_list_objects_v2
        
        try:
            # Test with max_keys exactly matching the number of keys we already have
            result = s3_helper.list_objects(prefix=prefix, max_keys=3)
            
            # Should return all keys and not make a second API call
            assert len(result) == 3
            assert call_count == 1
            
        finally:
            # Restore the original method
            s3_helper.s3_client.list_objects_v2 = original_list_objects
    
    def test_delete_object_error(self, s3_helper):
        """
        Test handling of errors in delete_object.
        
        This test verifies that S3UploadError is raised when delete_object fails.
        """
        # Mock the delete_object method to raise an exception
        with patch.object(s3_helper.s3_client, 'delete_object', side_effect=Exception("Delete failed")):
            with pytest.raises(S3UploadError) as exc_info:
                s3_helper.delete_object(TEST_KEY)
            
            assert "Failed to delete object" in str(exc_info.value)

    def test_list_objects_max_keys_zero(self, s3_helper):
        """
        Test list_objects with max_keys=0.
        
        This test verifies that the method handles the case where max_keys is 0,
        which should result in an early return without making an API call.
        """
        # Mock the list_objects_v2 method to track if it's called
        original_list_objects = s3_helper.s3_client.list_objects_v2
        mock_list_objects = MagicMock()
        s3_helper.s3_client.list_objects_v2 = mock_list_objects
        
        try:
            # Test with max_keys=0
            result = s3_helper.list_objects(prefix="test/", max_keys=0)
            
            # Should return an empty list without making an API call
            assert result == []
            mock_list_objects.assert_not_called()
            
        finally:
            # Restore the original method
            s3_helper.s3_client.list_objects_v2 = original_list_objects 

    def test_list_objects_max_keys_less_than_result(self, s3_helper):
        """
        Test list_objects when max_keys is less than the number of results.
        
        This test verifies that the method handles the case where max_keys is less
        than the number of results already collected.
        """
        # Create a few objects
        prefix = "test/max_keys_less/"
        keys = [f"{prefix}file{i}.txt" for i in range(5)]
        
        for key in keys:
            s3_helper.put_object(key, TEST_CONTENT)
        
        # Mock the list_objects_v2 method to simulate pagination with more results than max_keys
        original_list_objects = s3_helper.s3_client.list_objects_v2
        
        call_count = 0
        
        def mock_list_objects_v2(**kwargs):
            """Mock implementation that forces a second call with max_keys already reached."""
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                # First call returns 3 keys and indicates there are more
                return {
                    'Contents': [{'Key': keys[i]} for i in range(3)],
                    'IsTruncated': True,
                    'NextContinuationToken': 'token1'
                }
            else:
                # Second call should not be made if max_keys is already reached
                # But if it is, return the remaining keys
                return {
                    'Contents': [{'Key': keys[i]} for i in range(3, 5)],
                    'IsTruncated': False
                }
        
        # Replace the method with our mock
        s3_helper.s3_client.list_objects_v2 = mock_list_objects_v2
        
        try:
            # Test with max_keys exactly matching the number of keys in the first response
            result = s3_helper.list_objects(prefix=prefix, max_keys=3)
            
            # Should return exactly max_keys objects and not make a second API call
            assert len(result) == 3
            assert call_count == 1
            
            # Test with max_keys less than the number of keys in the first response
            call_count = 0
            result = s3_helper.list_objects(prefix=prefix, max_keys=2)
            
            # Should return exactly max_keys objects and not make a second API call
            assert len(result) == 2
            assert call_count == 1
            
        finally:
            # Restore the original method
            s3_helper.s3_client.list_objects_v2 = original_list_objects 

    def test_list_objects_max_keys_calculation(self, s3_helper):
        """
        Test that MaxKeys is calculated correctly in list_objects.
        
        This test specifically targets the line where MaxKeys is calculated
        as max_keys - len(result).
        """
        # Create a few objects
        prefix = "test/max_keys_calc/"
        keys = [f"{prefix}file{i}.txt" for i in range(5)]
        
        for key in keys:
            s3_helper.put_object(key, TEST_CONTENT)
        
        # Mock the list_objects_v2 method to track the MaxKeys parameter
        original_list_objects = s3_helper.s3_client.list_objects_v2
        
        max_keys_values = []
        
        def mock_list_objects_v2(**kwargs):
            """Mock implementation that tracks MaxKeys values."""
            # Record the MaxKeys value
            if 'MaxKeys' in kwargs:
                max_keys_values.append(kwargs['MaxKeys'])
            
            # First call returns 2 keys and indicates there are more
            return {
                'Contents': [{'Key': keys[i]} for i in range(2)],
                'IsTruncated': False
            }
        
        # Replace the method with our mock
        s3_helper.s3_client.list_objects_v2 = mock_list_objects_v2
        
        try:
            # Test with max_keys=4
            result = s3_helper.list_objects(prefix=prefix, max_keys=4)
            
            # Verify that MaxKeys was set to 4
            assert max_keys_values[0] == 4
            
        finally:
            # Restore the original method
            s3_helper.s3_client.list_objects_v2 = original_list_objects 

    def test_calculate_max_keys(self, s3_helper):
        """
        Test the _calculate_max_keys helper method.
        
        This test directly tests the helper method that calculates the MaxKeys
        parameter for list_objects_v2.
        """
        # Test with various inputs
        assert s3_helper._calculate_max_keys(10, 0) == 10
        assert s3_helper._calculate_max_keys(10, 5) == 5
        assert s3_helper._calculate_max_keys(10, 9) == 1