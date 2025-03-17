"""
Tests for the OpenAI helper module.

This module contains tests for the OpenAIHelper class, including:
- Initialization
- Basic chat completion
- JSON mode
- Image encoding
- Error handling
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from cws_helpers.openai_helper import OpenAIHelper
import json
import base64


# Mock OpenAI API responses
@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI API response for testing."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    return mock_response


# Test initialization
def test_init():
    """Test that the OpenAIHelper initializes correctly."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai:
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        mock_openai.assert_called_once_with(api_key="test_key", organization="test_org")


# Test version check
def test_version_check():
    """Test that the version check works correctly."""
    # First, import the actual OPENAI_VERSION constant to ensure we mock a different version
    from cws_helpers.openai_helper.openai_helper import OPENAI_VERSION
    
    # Create a custom version function for mocking
    def mock_version_func(package_name):
        if package_name == "openai":
            return "0.0.1"  # Return a version different from OPENAI_VERSION
        return "1.0.0"  # Default for other packages
    
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI'), \
            patch('cws_helpers.openai_helper.openai_helper.version', side_effect=mock_version_func), \
            patch('cws_helpers.openai_helper.openai_helper.log') as mock_log, \
            patch.dict(os.environ, {"MUTE_OPENAI_HELPER_WARNING": "False"}):
        
        # Initialize the helper, which should trigger the version check
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Verify that a warning was logged
        mock_log.warning.assert_called_once()
        
        # Test with muted warnings
        mock_log.reset_mock()
        with patch.dict(os.environ, {"MUTE_OPENAI_HELPER_WARNING": "True"}):
            helper = OpenAIHelper(api_key="test_key", organization="test_org")
            mock_log.warning.assert_not_called()


# Test basic chat completion
def test_create_chat_completion(mock_openai_response):
    """Test basic chat completion functionality."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(prompt="Hello")
        
        assert response == "Test response"
        mock_completions.create.assert_called_once()
        
        # Verify the parameters passed to the API
        call_args = mock_completions.create.call_args[1]
        assert call_args["model"] == "gpt-4-turbo-preview"
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"][0]["type"] == "text"
        assert call_args["messages"][0]["content"][0]["text"] == "Hello"


# Test with system message
def test_create_chat_completion_with_system_message(mock_openai_response):
    """Test chat completion with a system message."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(
            prompt="Hello",
            system_message="You are a helpful assistant."
        )
        
        assert response == "Test response"
        
        # Verify the system message was included
        call_args = mock_completions.create.call_args[1]
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0]["role"] == "system"
        assert call_args["messages"][0]["content"] == "You are a helpful assistant."


# Test JSON mode
def test_json_mode(mock_openai_response):
    """Test chat completion with JSON mode enabled."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class, \
            patch('cws_helpers.openai_helper.openai_helper.ResponseFormatJSONObject') as mock_json_format:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        # Set up the mock JSON format
        mock_json_format_instance = MagicMock()
        mock_json_format.return_value = mock_json_format_instance
        
        # Set up the response
        mock_openai_response.choices[0].message.content = '{"result": "success"}'
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(prompt="Hello", json_mode=True)
        
        assert response == '{"result": "success"}'
        
        # Verify JSON format was created correctly
        mock_json_format.assert_called_once_with(type="json_object")
        
        # Verify response_format was set correctly
        call_args = mock_completions.create.call_args[1]
        assert call_args["response_format"] == mock_json_format_instance


# Test Pydantic model schema
def test_pydantic_model_schema(mock_openai_response):
    """Test chat completion with a Pydantic model schema."""
    from pydantic import BaseModel
    
    class TestModel(BaseModel):
        name: str
        age: int
        
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class, \
            patch('cws_helpers.openai_helper.openai_helper.ResponseFormatJSONSchema') as mock_schema_format:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        
        # Set up the mock schema format
        mock_schema_format_instance = MagicMock()
        mock_schema_format_instance.type = "json_schema"  # Add type attribute
        mock_schema_format.return_value = mock_schema_format_instance
        
        # Set up the response with valid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"name": "Test", "age": 30}'
        mock_completions.create.return_value = mock_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(
            prompt="Generate a person",
            response_format=TestModel,
            use_beta_parse=False  # Disable beta parse endpoint to use legacy approach
        )
        
        # Verify the response was parsed as JSON
        assert isinstance(response, dict)
        assert response["name"] == "Test"
        assert response["age"] == 30
        
        # Verify schema format was created correctly
        mock_schema_format.assert_called_once()
        
        # Verify response_format was set correctly
        call_args = mock_completions.create.call_args[1]
        assert call_args["response_format"] == mock_schema_format_instance


# Test streaming
def test_streaming(mock_openai_response):
    """Test streaming responses."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(prompt="Hello", stream=True)
        
        # For streaming, the response object should be returned directly
        assert response == mock_openai_response
        
        # Verify stream parameter was set
        call_args = mock_completions.create.call_args[1]
        assert call_args["stream"] is True


# Test image encoding
def test_encode_image(tmp_path):
    """Test the image encoding functionality."""
    # Create a test image file
    test_image = tmp_path / "test.jpg"
    test_image.write_bytes(b"test image content")
    
    encoded = OpenAIHelper.encode_image(str(test_image))
    assert isinstance(encoded, str)
    assert len(encoded) > 0
    
    # Verify it's valid base64
    decoded = base64.b64decode(encoded)
    assert decoded == b"test image content"


# Test with images
def test_create_chat_completion_with_images(mock_openai_response, tmp_path):
    """Test chat completion with image inputs."""
    # Create a test image file
    test_image = tmp_path / "test.jpg"
    test_image.write_bytes(b"test image content")
    
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class, \
            patch.object(OpenAIHelper, 'encode_image', return_value="encoded_image_data"):
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(
            prompt="What's in this image?",
            images=[str(test_image)]
        )
        
        assert response == "Test response"
        
        # Verify the image was included in the request
        call_args = mock_completions.create.call_args[1]
        content_parts = call_args["messages"][0]["content"]
        assert len(content_parts) == 2  # Text prompt and image
        assert content_parts[1]["type"] == "image_url"
        assert "data:image/jpeg;base64,encoded_image_data" in content_parts[1]["image_url"]["url"]


# Test with URL images
def test_create_chat_completion_with_url_images(mock_openai_response):
    """Test chat completion with image URLs."""
    image_url = "https://example.com/image.jpg"
    
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(
            prompt="What's in this image?",
            images=[image_url]
        )
        
        assert response == "Test response"
        
        # Verify the image URL was included in the request
        call_args = mock_completions.create.call_args[1]
        content_parts = call_args["messages"][0]["content"]
        assert len(content_parts) == 2  # Text prompt and image
        assert content_parts[1]["type"] == "image_url"
        assert content_parts[1]["image_url"]["url"] == image_url


# Test error handling for missing images
def test_missing_image_error_handling(mock_openai_response):
    """Test error handling for missing image files."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class, \
            patch('os.path.exists', return_value=False), \
            patch('cws_helpers.openai_helper.openai_helper.log') as mock_log:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(
            prompt="What's in this image?",
            images=["nonexistent_image.jpg"]
        )
        
        # Should still work, just log an error and continue without the image
        assert response == "Test response"
        mock_log.error.assert_called_once_with("Image file not found: nonexistent_image.jpg")
        
        # Verify only the text prompt was included
        call_args = mock_completions.create.call_args[1]
        content_parts = call_args["messages"][0]["content"]
        assert len(content_parts) == 1
        assert content_parts[0]["type"] == "text"


# Test JSON parsing error handling
def test_json_parsing_error():
    """Test error handling for JSON parsing errors."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class, \
            patch('cws_helpers.openai_helper.openai_helper.log') as mock_log:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        
        # Set up the mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"invalid": json}'
        mock_completions.create.return_value = mock_response
        
        # Create a mock response format with type="json_schema"
        mock_response_format = MagicMock()
        mock_response_format.type = "json_schema"
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Should raise a JSONDecodeError
        with pytest.raises(json.JSONDecodeError):
            helper.create_chat_completion(
                prompt="Generate JSON",
                response_format=mock_response_format
            )
        
        # Verify errors were logged
        assert mock_log.error.call_count == 2
