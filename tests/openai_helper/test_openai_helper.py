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
from unittest.mock import patch, MagicMock, ANY, create_autospec
from openai._types import NOT_GIVEN
from cws_helpers.openai_helper import OpenAIHelper, AIModel
import json
import base64
from openai import OpenAI


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
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai:
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        mock_openai.assert_called_once_with(api_key="test_key", organization="test_org")


# Test version check
def test_version_check():
    """Test that the version check works correctly."""
    # First, import the actual OPENAI_VERSION constant to ensure we mock a different version
    from cws_helpers.openai_helper.utils.model_utils import OPENAI_VERSION
    
    # Create a custom version function for mocking
    def mock_version_func(package_name):
        if package_name == "openai":
            return "0.0.1"  # Return a version different from OPENAI_VERSION
        return "1.0.0"  # Default for other packages
    
    with patch('cws_helpers.openai_helper.core.base.OpenAI'), \
            patch('cws_helpers.openai_helper.utils.model_utils.version', side_effect=mock_version_func), \
            patch('cws_helpers.openai_helper.utils.model_utils.log') as mock_log, \
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
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create messages using the helper's create_messages method
        messages = helper.create_messages(prompt="Hello")
        
        # Call create_chat_completion with the messages
        response = helper.create_chat_completion(messages=messages)
        
        assert response == "Test response"
        mock_completions.create.assert_called_once()
        
        # Verify the parameters passed to the API
        call_args = mock_completions.create.call_args[1]
        assert call_args["model"] == "gpt-4-turbo-preview"
        assert len(call_args["messages"]) == 1
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == "Hello"


# Test with system message
def test_create_chat_completion_with_system_message(mock_openai_response):
    """Test chat completion with a system message."""
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create messages using the helper's create_messages method
        messages = helper.create_messages(
            prompt="Hello",
            system_message="You are a helpful assistant."
        )
        
        # Call create_chat_completion with the messages
        response = helper.create_chat_completion(messages=messages)
        
        assert response == "Test response"
        
        # Verify the system message was included
        call_args = mock_completions.create.call_args[1]
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0]["role"] == "system"
        assert call_args["messages"][0]["content"] == "You are a helpful assistant."
        assert call_args["messages"][1]["role"] == "user"
        assert call_args["messages"][1]["content"] == "Hello"


# Test JSON mode
def test_json_mode(mock_openai_response):
    """Test chat completion with JSON mode enabled."""
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
    
        # Set up the response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"result": "success"}'
        mock_completions.create.return_value = mock_response
    
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create messages using the helper's create_messages method
        messages = helper.create_messages(prompt="List three colors as a JSON array")
        
        # Call create_chat_completion with JSON mode enabled
        response = helper.create_chat_completion(
            messages=messages,
            json_mode=True
        )
    
        assert response is not None
        assert isinstance(response, dict) or isinstance(response, list)
        print(f"\nJSON response: {response}")


# Test Pydantic model schema
def test_pydantic_model_schema(mock_openai_response):
    """Test chat completion with a Pydantic model schema."""
    from pydantic import BaseModel
    
    class TestModel(BaseModel):
        name: str
        age: int
    
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
    
        # Set up the response with valid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"name": "Test", "age": 30}'
        mock_completions.create.return_value = mock_response
    
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create messages using the helper's create_messages method
        messages = helper.create_messages(prompt="Generate a person")
        
        # Call create_chat_completion with the Pydantic model
        response = helper.create_chat_completion(
            messages=messages,
            response_format=TestModel
        )
    
        # Verify the response was parsed as JSON
        assert isinstance(response, dict)
        assert response["name"] == "Test"
        assert response["age"] == 30
        
        # Verify response_format was set correctly
        call_args = mock_completions.create.call_args[1]
        assert call_args["response_format"]["type"] == "json_object"
        assert "schema" in call_args["response_format"]
        schema = call_args["response_format"]["schema"]
        assert schema["type"] == "object"
        assert schema["title"] == "TestModel"
        assert "name" in schema["properties"]
        assert "age" in schema["properties"]
        assert schema["properties"]["name"]["type"] == "string"
        assert schema["properties"]["age"]["type"] == "integer"
        assert set(schema["required"]) == {"name", "age"}


# Test streaming
def test_streaming(mock_openai_response):
    """Test streaming responses."""
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response
    
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create messages using the helper's create_messages method
        messages = helper.create_messages(prompt="Hello")
        
        # Call create_chat_completion with streaming enabled
        response = helper.create_chat_completion(
            messages=messages,
            stream=True
        )
    
        assert response == mock_openai_response
    
        # Verify stream parameter was True
        call_args = mock_completions.create.call_args[1]
        assert call_args["stream"] is True


# Test image encoding
def test_encode_image(tmp_path):
    """Test encoding images to base64."""
    # Create a temporary test image
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"test image content")
    
    # Mock base64 encoding
    with patch('base64.b64encode', return_value=b"encoded_data"):
        from cws_helpers.openai_helper.utils.image import encode_image
        result = encode_image(str(test_image))
        
        assert result == "data:image/jpeg;base64,encoded_data"


# Test chat completion with images
def test_create_chat_completion_with_images(mock_openai_response, tmp_path):
    """Test chat completion with image inputs."""
    # Create a temporary test image
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"test image content")

    # We need to patch at the module level where it's imported, not where it's defined
    with patch('cws_helpers.openai_helper.utils.image.encode_image') as mock_encode_image:
        # Set up the mock to return a consistent value
        mock_encode_image.return_value = "data:image/jpeg;base64,dGVzdCBpbWFnZSBjb250ZW50"

        with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
            # Set up the mock chain
            mock_openai = MagicMock()
            mock_openai_class.return_value = mock_openai
            mock_chat = MagicMock()
            mock_openai.chat = mock_chat
            mock_completions = MagicMock()
            mock_chat.completions = mock_completions
            mock_completions.create.return_value = mock_openai_response

            helper = OpenAIHelper(api_key="test_key", organization="test_org")

            # Create messages using the helper's create_messages method
            messages = helper.create_messages(
                prompt="Describe this image",
                images=[str(test_image)]
            )

            # Call create_chat_completion with the messages
            response = helper.create_chat_completion(messages=messages)

            assert response == "Test response"

            # Verify the image was included in the messages
            call_args = mock_completions.create.call_args[1]
            assert len(call_args["messages"]) == 1
            assert call_args["messages"][0]["role"] == "user"
            assert isinstance(call_args["messages"][0]["content"], list)
            assert len(call_args["messages"][0]["content"]) == 2
            assert call_args["messages"][0]["content"][0]["type"] == "text"
            assert call_args["messages"][0]["content"][0]["text"] == "Describe this image"
            assert call_args["messages"][0]["content"][1]["type"] == "image_url"
            assert call_args["messages"][0]["content"][1]["image_url"]["url"] == "data:image/jpeg;base64,dGVzdCBpbWFnZSBjb250ZW50"


# Test chat completion with URL images
def test_create_chat_completion_with_url_images(mock_openai_response):
    """Test chat completion with URL images."""
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class, \
            patch('cws_helpers.openai_helper.core.messages.utils.log') as mock_log:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response

        # Set up the image URL
        image_url = "https://example.com/image.jpg"
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create messages using the helper's create_messages method
        messages = helper.create_messages(
            prompt="Describe this image",
            images=[image_url]
        )
        
        # Call create_chat_completion with the messages and vision model
        response = helper.create_chat_completion(
            messages=messages,
            model="gpt-4-vision-preview"  # Explicitly set vision model
        )
        
        assert response == "Test response"
        mock_completions.create.assert_called_once()
        
        # Verify the parameters passed to the API
        call_args = mock_completions.create.call_args[1]
        assert call_args["model"] == "gpt-4-vision-preview"
        assert len(call_args["messages"]) == 1
        assert call_args["messages"][0]["role"] == "user"
        
        # Verify the content structure for multimodal message
        content = call_args["messages"][0]["content"]
        assert isinstance(content, list)
        assert len(content) == 2  # Text prompt and image URL
        
        # Verify text part
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "Describe this image"
        
        # Verify image part
        assert content[1]["type"] == "image_url"
        assert content[1]["image_url"]["url"] == image_url


# Test missing image error handling
def test_missing_image_error_handling():
    """Test error handling when an image file is missing."""
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
        # Set up the mock chain for OpenAI
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        # Set up a mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_completions.create.return_value = mock_response

        helper = OpenAIHelper(api_key="test_key", organization="test_org")

        # Create messages using the helper's create_messages method
        messages = helper.create_messages(
            prompt="Describe this image",
            images=["nonexistent.jpg"]
        )

        # Call create_chat_completion with the messages
        response = helper.create_chat_completion(messages=messages)

        # Verify the response is still returned even if image encoding failed
        assert response == "Test response"

        # Verify that the message only contains the text prompt since image encoding failed
        call_args = mock_completions.create.call_args[1]
        assert len(call_args["messages"]) == 1
        assert call_args["messages"][0]["role"] == "user"
        assert isinstance(call_args["messages"][0]["content"], list)
        assert len(call_args["messages"][0]["content"]) == 1
        assert call_args["messages"][0]["content"][0]["type"] == "text"
        assert call_args["messages"][0]["content"][0]["text"] == "Describe this image"


# Test JSON parsing error
def test_json_parsing_error():
    """Test error handling for JSON parsing errors."""
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class, \
            patch('cws_helpers.openai_helper.core.chat.generic.generic_completion.log') as mock_log:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        
        # Set up the response with invalid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "Invalid JSON"
        mock_completions.create.return_value = mock_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create messages using the helper's create_messages method
        messages = helper.create_messages(prompt="Generate JSON")
        
        # Call create_chat_completion with JSON mode enabled
        response = helper.create_chat_completion(
            messages=messages,
            json_mode=True
        )
        
        # Verify error was logged
        mock_log.error.assert_called_once()
        
        # Verify response is still returned as string
        assert isinstance(response, str)
        assert response == "Invalid JSON"


class TestOpenAIHelper:
    """Test class for OpenAIHelper parameter filtering."""
    
    def test_filter_unsupported_parameters(self):
        """Test that unsupported parameters are automatically filtered out when making API calls."""
        with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class, \
                patch('cws_helpers.openai_helper.core.chat.generic.generic_completion.filter_unsupported_parameters') as mock_filter_params:
            # Set up the mock chain
            mock_openai = MagicMock()
            mock_openai_class.return_value = mock_openai
            mock_chat = MagicMock()
            mock_openai.chat = mock_chat
            mock_completions = MagicMock()
            mock_chat.completions = mock_completions
    
            # Set up a mock response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "Test response"
            mock_completions.create.return_value = mock_response
            
            # Setup mock filter to remove parameters
            def filter_params(params, model):
                filtered = params.copy()
                if "temperature" in filtered:
                    filtered.pop("temperature")
                if "top_p" in filtered:
                    filtered.pop("top_p")
                return filtered
            
            mock_filter_params.side_effect = filter_params
    
            # Initialize helper and make request with unsupported parameters
            helper = OpenAIHelper(api_key="test_key", organization="test_org")
            
            # Create messages using the helper's create_messages method
            messages = helper.create_messages(prompt="Hello")
            
            # Call create_chat_completion with unsupported parameters
            response = helper.create_chat_completion(
                messages=messages,
                model="o3-mini",
                temperature=0.7,  # This should be filtered out
                top_p=0.9,  # This should be filtered out
                max_completion_tokens=100
            )
    
            # Verify response was returned
            assert response == "Test response"
    
            # Verify the filter function was called with the right parameters
            mock_filter_params.assert_called_once()
            call_args = mock_filter_params.call_args[0]
            assert "temperature" in call_args[0]
            assert "top_p" in call_args[0]
            assert call_args[1] == "o3-mini"
    
            # Verify unsupported parameters were filtered out in the API call
            api_call_args = mock_completions.create.call_args[1]
            assert "temperature" not in api_call_args
            assert "top_p" not in api_call_args
            assert "max_completion_tokens" in api_call_args
    
    def test_create_chat_completion_with_unsupported_parameters(self):
        """Test that unsupported parameters are automatically filtered out when making API calls."""
        with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class, \
                patch('cws_helpers.openai_helper.core.chat.generic.generic_completion.filter_unsupported_parameters') as mock_filter_params:
            # Set up the mock chain
            mock_openai = MagicMock()
            mock_openai_class.return_value = mock_openai
            mock_chat = MagicMock()
            mock_openai.chat = mock_chat
            mock_completions = MagicMock()
            mock_chat.completions = mock_completions
    
            # Set up a mock response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "Test response"
            mock_completions.create.return_value = mock_response
            
            # Setup mock filter to remove parameters
            def filter_params(params, model):
                filtered = params.copy()
                if "temperature" in filtered:
                    filtered.pop("temperature")
                if "top_p" in filtered:
                    filtered.pop("top_p")
                return filtered
            
            mock_filter_params.side_effect = filter_params
    
            # Initialize helper and make request with unsupported parameters
            helper = OpenAIHelper(api_key="test_key", organization="test_org")
            
            # Create messages using the helper's create_messages method
            messages = helper.create_messages(prompt="Hello")
            
            # Call create_chat_completion with unsupported parameters
            response = helper.create_chat_completion(
                messages=messages,
                model="o3-mini",
                temperature=0.7,  # This should be filtered out
                top_p=0.9,  # This should be filtered out
                max_completion_tokens=100
            )
    
            # Verify response was returned
            assert response == "Test response"
    
            # Verify the filter function was called with the right parameters
            mock_filter_params.assert_called_once()
            call_args = mock_filter_params.call_args[0]
            assert "temperature" in call_args[0]
            assert "top_p" in call_args[0]
            assert call_args[1] == "o3-mini"
    
            # Verify unsupported parameters were filtered out in the API call
            api_call_args = mock_completions.create.call_args[1]
            assert "temperature" not in api_call_args
            assert "top_p" not in api_call_args
            assert "max_completion_tokens" in api_call_args

    def test_structured_chat_completion_with_unsupported_parameters(self):
        """Test structured chat completion with unsupported parameters."""
        from pydantic import BaseModel
        from openai.types.chat import (
            ParsedChatCompletion,
            ParsedChatCompletionMessage,
            ParsedChoice,
        )
        from unittest.mock import create_autospec, MagicMock
        from openai import OpenAI

        class TestModel(BaseModel):
            result: str

        with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class, \
                patch('cws_helpers.openai_helper.core.chat.structured.structured_completion.filter_unsupported_parameters') as mock_filter_params:
            # Set up the mock chain
            mock_openai = MagicMock()
            mock_openai_class.return_value = mock_openai
    
            # Create the beta.chat.completions chain
            mock_beta = MagicMock()
            mock_chat = MagicMock()
            mock_completions = MagicMock()
            mock_parse = MagicMock()
    
            mock_openai.beta = mock_beta
            mock_beta.chat = mock_chat
            mock_chat.completions = mock_completions
            mock_completions.parse = mock_parse
            
            # Setup mock filter to remove parameters
            def filter_params(params, model):
                filtered = params.copy()
                if "temperature" in filtered:
                    filtered.pop("temperature")
                if "top_p" in filtered:
                    filtered.pop("top_p")
                return filtered
            
            mock_filter_params.side_effect = filter_params
    
            # Create a proper mock response
            parsed_message = ParsedChatCompletionMessage(
                role="assistant",
                content='{"result": "success"}',
                parsed=TestModel(result="success")
            )
            choice = ParsedChoice(
                index=0,
                message=parsed_message,
                finish_reason="stop"
            )
            mock_response = ParsedChatCompletion[TestModel](
                id="test_id",
                choices=[choice],
                created=1234567890,
                model="gpt-4",
                object="chat.completion",
                usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
            )
    
            # Configure the mock chain to return the response
            mock_parse.return_value = mock_response
    
            # Create test messages
            messages = [
                {"role": "user", "content": "Test message"}
            ]
    
            # Create the helper instance
            helper = OpenAIHelper(api_key="test_key", organization="test_org")
    
            # Call the method with unsupported parameters
            result = helper.create_structured_chat_completion(
                messages=messages,
                model="gpt-4",
                response_format=TestModel,
                temperature=0.7,
                top_p=0.9
            )
    
            # Verify the result
            assert isinstance(result, ParsedChatCompletion)
            assert result.choices[0].message.parsed.result == "success"
    
            # Verify the filter function was called
            mock_filter_params.assert_called_once()
            call_args = mock_filter_params.call_args[0]
            assert "temperature" in call_args[0]
            assert "top_p" in call_args[0]
            assert call_args[1] == "gpt-4"
    
            # Verify unsupported parameters were filtered out
            api_call_args = mock_parse.call_args[1]
            assert "temperature" not in api_call_args
            assert "top_p" not in api_call_args
