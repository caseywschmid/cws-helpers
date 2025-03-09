"""
AWS Helper Module

This module provides a clean, type-safe interface for AWS S3 operations.
All AWS credentials are handled through either direct parameters or environment variables.

Required Environment Variables:
    - AWS_ACCESS_KEY_ID: Your AWS access key ID
    - AWS_SECRET_ACCESS_KEY: Your AWS secret access key
    - AWS_DEFAULT_REGION: (optional) Default AWS region

Example:
    from cws_helpers.aws_helper import S3Helper
    
    # Initialize S3 helper
    s3 = S3Helper(bucket_name='my-bucket')
    
    # Store JSON data
    data = {"key": "value"}
    s3.put_object("path/to/file.json", data)
    
    # Read JSON data
    content = s3.get_json("path/to/file.json")
"""

import os
import json
from typing import Optional, List, Union, Any, Dict

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel

from .errors.aws_errors import AWSConfigError, S3UploadError, S3DownloadError, S3Error

class S3Config(BaseModel):
    """
    Configuration for S3 operations.
    
    This model ensures type safety for S3 configuration and provides
    validation for required fields.
    
    Attributes:
        bucket_name: Name of the S3 bucket
        region_name: AWS region name
        access_key_id: AWS access key ID
        secret_access_key: AWS secret access key
    """
    bucket_name: str
    region_name: str = "us-east-1"
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None

class S3Helper:
    """
    Helper class for S3 operations.
    
    This class provides a clean interface for common S3 operations with
    strong type safety and error handling. It supports both direct data
    operations and JSON serialization/deserialization.
    
    Attributes:
        bucket_name: Name of the S3 bucket
        region_name: AWS region name
        s3_client: Boto3 S3 client instance
    """
    
    def __init__(
        self,
        bucket_name: str,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        """
        Initialize the S3Helper with credentials and bucket information.
        
        Args:
            bucket_name: Name of the S3 bucket
            region_name: AWS region name (default: from env or "us-east-1")
            aws_access_key_id: Optional AWS access key ID
            aws_secret_access_key: Optional AWS secret access key
        
        Raises:
            AWSConfigError: If AWS credentials are not provided and not in env vars
        """
        # Build config with environment fallbacks
        config = S3Config(
            bucket_name=bucket_name,
            region_name=region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            access_key_id=aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID"),
            secret_access_key=aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        
        if not config.access_key_id or not config.secret_access_key:
            raise AWSConfigError(
                "AWS credentials not found. Please provide them as parameters or set "
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
            )
        
        self.bucket_name = config.bucket_name
        self.region_name = config.region_name
        
        # Initialize S3 client
        self.s3_client = boto3.client(
            "s3",
            region_name=config.region_name,
            aws_access_key_id=config.access_key_id,
            aws_secret_access_key=config.secret_access_key,
        )
    
    def get_object(self, key: str) -> bytes:
        """
        Get an object from S3.
        
        Args:
            key: S3 object key
            
        Returns:
            bytes: The object's content
            
        Raises:
            S3DownloadError: If the object cannot be retrieved
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise S3DownloadError(f"Object not found: {key}")
            raise S3DownloadError(f"Failed to get object {key}: {str(e)}")
        except Exception as e:
            raise S3DownloadError(f"Unexpected error getting object {key}: {str(e)}")
    
    def get_json(self, key: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Get and parse a JSON object from S3.
        
        Args:
            key: S3 object key
            
        Returns:
            Union[Dict[str, Any], List[Any]]: Parsed JSON data
            
        Raises:
            S3DownloadError: If the object cannot be retrieved or parsed
        """
        try:
            content = self.get_object(key)
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise S3DownloadError(f"Failed to parse JSON from {key}: {str(e)}")
    
    def put_object(
        self, 
        key: str, 
        data: Union[str, bytes, dict, list],
        content_type: Optional[str] = None
    ) -> None:
        """
        Put an object into S3.
        
        Args:
            key: S3 object key
            data: Content to store (string, bytes, or JSON-serializable object)
            content_type: Optional MIME type for the object
            
        Raises:
            S3UploadError: If the object cannot be uploaded
        """
        try:
            # Handle different input types
            if isinstance(data, (dict, list)):
                body = json.dumps(data, default=str)
                content_type = content_type or 'application/json'
            elif isinstance(data, str):
                body = data.encode('utf-8')
                content_type = content_type or 'text/plain'
            else:
                body = data
                content_type = content_type or 'application/octet-stream'
            
            # Upload with content type if specified
            args = {
                'Bucket': self.bucket_name,
                'Key': key,
                'Body': body
            }
            if content_type:
                args['ContentType'] = content_type
                
            self.s3_client.put_object(**args)
            
        except Exception as e:
            raise S3UploadError(f"Failed to upload object {key}: {str(e)}")
    
    def object_exists(self, key: str) -> bool:
        """
        Check if an object exists in S3.
        
        Args:
            key: S3 object key
            
        Returns:
            bool: True if object exists, False otherwise
            
        Raises:
            S3DownloadError: For unexpected S3 errors during object check
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise S3DownloadError(f"Error checking object existence {key}: {str(e)}")
    
    def _calculate_max_keys(self, max_keys: int, result_length: int) -> int:
        """
        Calculate the MaxKeys parameter for list_objects_v2.
        
        This is a helper method to make testing easier.
        
        Args:
            max_keys: The maximum number of keys to return
            result_length: The current length of the result list
            
        Returns:
            int: The calculated MaxKeys parameter
        """
        return max_keys - result_length

    def list_objects(
        self, 
        prefix: str = "", 
        max_keys: Optional[int] = None
    ) -> List[str]:
        """
        List objects in S3 with the given prefix.
        
        This method handles pagination automatically, retrieving all objects
        that match the prefix up to the max_keys limit if specified.
        
        Args:
            prefix: S3 key prefix to filter by
            max_keys: Maximum number of keys to return (if None, returns all keys)
            
        Returns:
            List[str]: List of object keys
            
        Raises:
            S3Error: If the objects cannot be listed
        """
        try:
            result = []
            continuation_token = None
            
            # Early return if max_keys is 0
            if max_keys == 0:
                return []
                
            while True:
                args = {
                    'Bucket': self.bucket_name,
                    'Prefix': prefix
                }
                
                # Add continuation token if we're paginating
                if continuation_token:
                    args['ContinuationToken'] = continuation_token
                
                # Add max_keys if specified and adjust for pagination
                if max_keys is not None:
                    # If we've already collected some results, adjust the max_keys
                    if len(result) >= max_keys:
                        # We've already reached or exceeded max_keys
                        break
                    
                    # Calculate remaining keys needed
                    remaining = max_keys - len(result)
                    args['MaxKeys'] = remaining
                
                # Make the API call
                response = self.s3_client.list_objects_v2(**args)
                
                # Add the contents to our result
                if 'Contents' in response:
                    result.extend([obj['Key'] for obj in response['Contents']])
                
                # Check if there are more results
                if not response.get('IsTruncated', False):
                    break
                
                # Get the continuation token for the next request
                continuation_token = response.get('NextContinuationToken')
                
                # If we have a max_keys and we've reached it, stop
                if max_keys is not None and len(result) >= max_keys:
                    # Truncate to exactly max_keys if we went over
                    result = result[:max_keys]
                    break
            
            return result
            
        except Exception as e:
            raise S3Error(f"Failed to list objects with prefix {prefix}: {str(e)}")
    
    def delete_object(self, key: str) -> None:
        """
        Delete an object from S3.
        
        Args:
            key: S3 object key
            
        Raises:
            S3UploadError: If the object cannot be deleted
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except Exception as e:
            raise S3UploadError(f"Failed to delete object {key}: {str(e)}") 