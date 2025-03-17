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
    
    # Create mock beta module
    mock_beta = MagicMock()
    mock_beta.chat.completions.parse.return_value = MockParsedChatCompletion(parsed_data)
    
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        
        # Set up the beta property
        type(mock_openai).beta = PropertyMock(return_value=mock_beta)
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
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
        
        # Verify the result
        assert result.choices[0].message.parsed == parsed_data
        
        # Verify the parse method was called with correct parameters
        mock_beta.chat.completions.parse.assert_called_once()
        call_args = mock_beta.chat.completions.parse.call_args[1]
        assert call_args["messages"] == messages
        assert call_args["model"] == "gpt-4o"
        assert call_args["response_format"] == TestMathResponse


# Test beta parse endpoint integration in create_chat_completion
def test_create_chat_completion_with_beta_parse():
    """Test that create_chat_completion uses the beta parse endpoint when appropriate."""
    # Create mock parsed data
    parsed_data = TestMathResponse(
        steps=[
            TestStep(explanation="First step", output="2x = 10"),
            TestStep(explanation="Second step", output="x = 5")
        ],
        final_answer="x = 5"
    )
    
    # Create mock beta module
    mock_beta = MagicMock()
    mock_beta.chat.completions.parse.return_value = MockParsedChatCompletion(parsed_data)
    
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        
        # Set up the beta property
        type(mock_openai).beta = PropertyMock(return_value=mock_beta)
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Call create_chat_completion with a Pydantic model
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10",
            response_format=TestMathResponse,
            model="gpt-4o"
        )
        
        # Verify the result
        assert result.choices[0].message.parsed == parsed_data
        
        # Verify the parse method was called
        mock_beta.chat.completions.parse.assert_called_once()


# Test disabling beta parse endpoint
def test_create_chat_completion_disable_beta_parse():
    """Test that create_chat_completion doesn't use the beta parse endpoint when disabled."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class, \
            patch('cws_helpers.openai_helper.openai_helper.ResponseFormatJSONSchema') as mock_schema_format:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        
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
        
        # Call create_chat_completion with use_beta_parse=False
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10",
            response_format=TestMathResponse,
            model="gpt-4o",
            use_beta_parse=False
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
    """Test that create_chat_completion falls back to standard endpoint when beta is not available."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class, \
            patch('cws_helpers.openai_helper.openai_helper.ResponseFormatJSONSchema') as mock_schema_format, \
            patch('cws_helpers.openai_helper.openai_helper.log') as mock_log:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        
        # Set up the beta property to raise an exception when accessed
        mock_beta = MagicMock()
        mock_beta.chat = MagicMock()
        mock_beta.chat.completions = MagicMock()
        mock_beta.chat.completions.parse = MagicMock(side_effect=Exception("Beta parse endpoint failed"))
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
        
        # Call create_chat_completion with a Pydantic model
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10",
            response_format=TestMathResponse,
            model="gpt-4o"
        )
        
        # Verify the result is a dictionary (fallback to standard endpoint)
        assert isinstance(result, dict)
        assert "steps" in result
        assert "final_answer" in result
        
        # Verify the standard completions.create method was called
        mock_completions.create.assert_called_once()
        
        # Verify the warning was logged
        mock_log.warning.assert_called_once()


# Test error handling in create_structured_chat_completion
def test_create_structured_chat_completion_error():
    """Test error handling in create_structured_chat_completion."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        
        # Set up the beta property to not have the parse method
        mock_beta = MagicMock()
        mock_beta.chat = MagicMock()
        mock_beta.chat.completions = MagicMock()
        # Remove the parse attribute to simulate it not being available
        delattr(mock_beta.chat.completions, 'parse')
        
        type(mock_openai).beta = PropertyMock(return_value=mock_beta)
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Create test messages
        messages = [
            {"role": "user", "content": [{"type": "text", "text": "Solve 2x = 10"}]}
        ]
        
        # Should raise ImportError
        with pytest.raises(ImportError):
            helper.create_structured_chat_completion(
                messages=messages,
                model="gpt-4o",
                response_format=TestMathResponse
            )


# Test _create_messages helper method
def test_create_messages():
    """Test the _create_messages helper method."""
    with patch('cws_helpers.openai_helper.openai_helper.OpenAI') as mock_openai_class:
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        
        # Test with just prompt
        messages = helper._create_messages(prompt="Hello")
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"][0]["type"] == "text"
        assert messages[0]["content"][0]["text"] == "Hello"
        
        # Test with system message
        messages = helper._create_messages(prompt="Hello", system_message="You are a helpful assistant.")
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a helpful assistant."
        assert messages[1]["role"] == "user"
        
        # Test with images
        with patch.object(OpenAIHelper, 'encode_image', return_value="encoded_image_data"):
            with patch('os.path.exists', return_value=True):
                messages = helper._create_messages(
                    prompt="What's in this image?",
                    images=["image.jpg", "https://example.com/image.jpg"]
                )
                assert len(messages) == 1
                content = messages[0]["content"]
                assert len(content) == 3  # Text + 2 images
                assert content[0]["type"] == "text"
                assert content[1]["type"] == "image_url"
                assert "data:image/jpeg;base64,encoded_image_data" in content[1]["image_url"]["url"]
                assert content[2]["type"] == "image_url"
                assert content[2]["image_url"]["url"] == "https://example.com/image.jpg" 