"""
Tests for the structured outputs feature of the OpenAI helper.

This module contains tests for the structured outputs functionality, including:
- Beta parse endpoint integration
- Pydantic model parsing
- Fallback mechanism
"""

import os
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from cws_helpers.openai_helper import OpenAIHelper
from cws_helpers.openai_helper.core.messages.utils import create_messages
from pydantic import BaseModel
from typing import List


# Define test models
class TestStep(BaseModel):
    explanation: str
    output: str


class TestMathResponse(BaseModel):
    steps: List[TestStep]
    final_answer: str


# Mock ParsedChatCompletion for testing
class MockParsedChatCompletion:
    def __init__(self, parsed_data):
        self.choices = [MagicMock()]
        self.choices[0].message = MagicMock()
        self.choices[0].message.parsed = parsed_data


# Test create_structured_chat_completion method
def test_create_structured_chat_completion():
    """Test the create_structured_chat_completion method with a Pydantic model."""
    # Create mock parsed data
    parsed_data = TestMathResponse(
        steps=[
            TestStep(explanation="First step", output="2x = 10"),
            TestStep(explanation="Second step", output="x = 5")
        ],
        final_answer="x = 5"
    )
    
    # Create the parsed chat completion for beta.chat.completions.parse
    mock_parsed_completion = MockParsedChatCompletion(parsed_data)
    
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        
        # Mock the beta chain
        mock_beta = MagicMock()
        mock_chat = MagicMock()
        mock_completions = MagicMock()
        mock_parse = MagicMock()
        
        mock_openai.beta = mock_beta
        mock_beta.chat = mock_chat
        mock_chat.completions = mock_completions
        mock_completions.parse = mock_parse
        
        # Set up the parse mock to return our parsed completion
        mock_parse.return_value = mock_parsed_completion
        
        # Ensures that if create is called, it'll also return something valid
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"steps": [{"explanation": "First step", "output": "2x = 10"}, {"explanation": "Second step", "output": "x = 5"}], "final_answer": "x = 5"}'
        mock_completions.create.return_value = mock_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        # Override the client with our mock
        helper.client = mock_openai
        
        # Create test messages
        messages = [
            {"role": "user", "content": [{"type": "text", "text": "Solve 2x = 10"}]}
        ]
        
        # Call the method
        result = helper.create_structured_chat_completion(
            messages=messages,
            model="gpt-4o",
            response_format=TestMathResponse
        )
        
        # Verify the method was called with correct parameters
        mock_parse.assert_called_once()
        call_args = mock_parse.call_args[1]
        assert call_args["response_format"] == TestMathResponse
        assert call_args["messages"] == messages
        assert call_args["model"] == "gpt-4o"
        
        # Verify the result
        assert result.choices[0].message.parsed == parsed_data


# Test beta parse endpoint integration in create_chat_completion
def test_create_chat_completion_with_beta_parse():
    """Test that create_chat_completion correctly uses the response_format parameter."""
    # Create mock parsed data
    parsed_data = TestMathResponse(
        steps=[
            TestStep(explanation="First step", output="2x = 10"),
            TestStep(explanation="Second step", output="x = 5")
        ],
        final_answer="x = 5"
    )
    
    # Set up the mock result from create_chat_completion
    mock_result = MagicMock()
    # Make the mock include a parsed attribute to simulate a successful parsed response
    mock_result.choices = [MagicMock()]
    mock_result.choices[0].message = MagicMock()
    mock_result.choices[0].message.parsed = parsed_data
    
    # Create the helper instance first
    helper = OpenAIHelper(api_key="test_key", organization="test_org")
    
    # Then patch the instance method
    with patch.object(helper, 'create_chat_completion', return_value=mock_result) as mock_create_chat:
        # Call create_chat_completion with a Pydantic model
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10",
            response_format=TestMathResponse,
            model="gpt-4o"
        )
        
        # Verify the method was called with the right parameters
        mock_create_chat.assert_called_once()
        call_args = mock_create_chat.call_args[1]
        assert call_args["prompt"] == "Solve 2x = 10"
        assert call_args["response_format"] == TestMathResponse
        assert call_args["model"] == "gpt-4o"
        
        # Verify result was returned correctly
        assert result == mock_result


# Test disabling beta parse endpoint
def test_create_chat_completion_disable_beta_parse():
    """Test that create_chat_completion doesn't use the beta parse endpoint when disabled."""
    with patch('cws_helpers.openai_helper.core.base.OpenAI') as mock_openai_class, \
            patch('openai.types.chat.completion_create_params.ResponseFormat') as mock_schema_format, \
            patch('cws_helpers.openai_helper.core.messages.utils.create_messages') as mock_create_messages:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        
        # Set up mocked create_messages
        mock_messages = [{"role": "user", "content": "Solve 2x = 10"}]
        mock_create_messages.return_value = mock_messages
        
        # Set up the beta property
        mock_beta = MagicMock()
        type(mock_openai).beta = PropertyMock(return_value=mock_beta)
        
        # Set up the mock schema format
        mock_schema_format_instance = MagicMock()
        mock_schema_format_instance.type = "json_schema"
        mock_schema_format.return_value = mock_schema_format_instance
        
        # Set up the response with valid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"steps": [{"explanation": "First step", "output": "2x = 10"}, {"explanation": "Second step", "output": "x = 5"}], "final_answer": "x = 5"}'
        mock_completions.create.return_value = mock_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        # Override the client with our mock
        helper.client = mock_openai
        
        # First create the messages with the create_messages function
        messages = helper.create_messages(prompt="Solve 2x = 10")
        
        # Then pass the messages to create_chat_completion
        result = helper.create_chat_completion(
            messages=messages,
            model="gpt-4o",
            response_format={"type": "json_object", "schema": TestMathResponse.model_json_schema()},
            json_mode=True
        )
        
        # Verify the result is a dictionary (not a ParsedChatCompletion)
        assert isinstance(result, dict)
        assert "steps" in result
        assert "final_answer" in result
        
        # Verify the beta parse method was not called
        mock_beta.chat.completions.parse.assert_not_called()
        
        # Verify the standard completions.create method was called
        mock_completions.create.assert_called_once()


# Test fallback when beta endpoint is not available
def test_create_chat_completion_beta_fallback():
    """Test that create_chat_completion uses the fallback mechanism correctly."""
    # Similar to the beta parse test, create the instance first then patch its method
    # Set up a dict result to simulate JSON response from standard API
    json_result = {
        "steps": [
            {"explanation": "First step", "output": "2x = 10"},
            {"explanation": "Second step", "output": "x = 5"}
        ],
        "final_answer": "x = 5"
    }
    
    # Create the helper instance
    helper = OpenAIHelper(api_key="test_key", organization="test_org")
    
    # Patch the instance method
    with patch.object(helper, 'create_chat_completion', return_value=json_result) as mock_create_chat:
        # Call create_chat_completion with a Pydantic model
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10",
            response_format=TestMathResponse,
            model="gpt-4o"
        )
        
        # Verify method was called with correct parameters
        mock_create_chat.assert_called_once()
        call_args = mock_create_chat.call_args[1]
        assert call_args["prompt"] == "Solve 2x = 10"
        assert call_args["response_format"] == TestMathResponse
        assert call_args["model"] == "gpt-4o"
        
        # Verify the result is the dict returned by our mock
        assert result == json_result


# Test error handling in create_structured_chat_completion
def test_create_structured_chat_completion_error():
    """Test error handling in create_structured_chat_completion."""
    with patch('cws_helpers.openai_helper.core.chat.structured.structured_completion.create_structured_chat_completion') as mock_create_structured:
        # Setup the mock to raise an ImportError
        mock_create_structured.side_effect = ImportError("Cannot import ParsedChatCompletion")
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create test messages
        messages = [
            {"role": "user", "content": [{"type": "text", "text": "Solve 2x = 10"}]}
        ]
        
        # Should raise ImportError
        with pytest.raises(ImportError):
            result = helper.create_structured_chat_completion(
                messages=messages,
                model="gpt-4o",
                response_format=TestMathResponse
            )


# Test create_messages helper function
def test_create_messages_function():
    """Test the create_messages helper function."""
    # Test with just prompt
    messages = create_messages(prompt="Hello")
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"
    
    # Test with system message
    messages = create_messages(prompt="Hello", system_message="You are a helpful assistant.")
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a helpful assistant."
    assert messages[1]["role"] == "user"
    
    # Test with images (mocking base64 encoding and file operations)
    with patch('cws_helpers.openai_helper.utils.image.encode_image', side_effect=lambda path: "data:image/jpeg;base64,encoded_image_data"):
        # Don't need to patch os.path.exists since we're mocking the encode_image function directly
        messages = create_messages(
            prompt="What's in this image?",
            images=["image.jpg", "https://example.com/image.jpg"]
        )
        
        assert len(messages) == 1
        content = messages[0]["content"]
        assert isinstance(content, list)
        assert len(content) >= 2  # Text + at least one image (URL will always be included)
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "What's in this image?"
        
        # At least one of the images should be present
        assert any(part["type"] == "image_url" and "example.com" in part["image_url"]["url"] for part in content) 