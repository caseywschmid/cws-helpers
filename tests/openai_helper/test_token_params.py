import pytest
from unittest.mock import MagicMock, patch
from cws_helpers.openai_helper import OpenAIHelper, AIModel


class TestTokenParams:
    """Tests for handling of token parameters in OpenAIHelper."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock OpenAI client with mocked methods."""
        # Create a mock response with a choices attribute containing a message with content
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock() 
        mock_response.choices[0].message.content = "test response"
        
        # Create a mock completion object
        mock_completions = MagicMock()
        mock_completions.create.return_value = mock_response
        
        # Create a mock chat object
        mock_chat = MagicMock()
        mock_chat.completions = mock_completions
        
        # Create a mock client
        mock_client = MagicMock()
        mock_client.chat = mock_chat
        return mock_client
    
    @pytest.fixture
    def helper(self, mock_client):
        """Create an OpenAIHelper instance with a mocked client."""
        with patch('cws_helpers.openai_helper.core.base.OpenAI'):
            helper = OpenAIHelper(api_key="fake_key", organization="fake_org")
            helper.client = mock_client
            return helper
    
    def test_standard_model_uses_max_tokens(self, helper):
        """Test that standard models use max_tokens parameter."""
        helper.create_chat_completion(messages=[{"role": "user", "content": "Hello"}], model="gpt-4-turbo", max_tokens=100)
        
        # Check the create call
        args, kwargs = helper.client.chat.completions.create.call_args
        
        # Verify max_tokens was used
        assert "max_tokens" in kwargs
        assert kwargs["max_tokens"] == 100
        assert "max_completion_tokens" not in kwargs
    
    def test_o_model_uses_max_completion_tokens(self, helper):
        """Test that 'o' models use max_completion_tokens parameter."""
        helper.create_chat_completion(messages=[{"role": "user", "content": "Hello"}], model="o3-mini", max_tokens=100)
        
        # Check the create call
        args, kwargs = helper.client.chat.completions.create.call_args
        
        # Verify max_completion_tokens was used
        assert "max_completion_tokens" in kwargs
        assert kwargs["max_completion_tokens"] == 100
        assert "max_tokens" not in kwargs
    
    def test_explicitly_provided_max_completion_tokens(self, helper):
        """Test that explicitly provided max_completion_tokens is used for 'o' models."""
        helper.create_chat_completion(
            messages=[{"role": "user", "content": "Hello"}], 
            model="o3-mini", 
            max_tokens=100,
            max_completion_tokens=200
        )
        
        # Check the create call
        args, kwargs = helper.client.chat.completions.create.call_args
        
        # Verify max_completion_tokens was used with the explicitly provided value
        assert "max_completion_tokens" in kwargs
        assert kwargs["max_completion_tokens"] == 200
        assert "max_tokens" not in kwargs
    
    def test_error_recovery(self, helper):
        """Test that errors related to token parameters are handled correctly."""
        # Create a second mock response for the retry
        second_mock_response = MagicMock()
        second_mock_response.choices = [MagicMock()]
        second_mock_response.choices[0].message = MagicMock()
        second_mock_response.choices[0].message.content = "test response after recovery"
        
        # Mock the handle_token_parameter_error function to return a simple string
        # This simulates what happens after error handling where process_chat_completion_response
        # extracts the message content
        with patch('cws_helpers.openai_helper.core.chat.generic.error_handlers.handle_token_parameter_error') as mock_handler:
            # Set up the mock handler to return the content directly
            mock_handler.return_value = "test response after recovery"
            
            # Set up the original error
            helper.client.chat.completions.create.side_effect = ValueError(
                "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead."
            )
            
            # This should trigger the error and call our mocked handler
            response = helper.create_chat_completion(
                messages=[{"role": "user", "content": "Hello"}], 
                model="o3-mini", 
                max_tokens=100
            )
            
            # Verify that we got the expected response
            assert response == "test response after recovery"
            
            # Verify that the handler was called
            assert mock_handler.called
    
    def test_custom_model_detection(self, helper):
        """Test detection of custom model names that should use max_completion_tokens."""
        # Test with a custom model name that starts with 'o'
        helper.create_chat_completion(messages=[{"role": "user", "content": "Hello"}], model="o3-something-custom", max_tokens=100)
        
        # Check the create call
        args, kwargs = helper.client.chat.completions.create.call_args
        
        # Verify max_completion_tokens was used
        assert "max_completion_tokens" in kwargs
        assert kwargs["max_completion_tokens"] == 100
        assert "max_tokens" not in kwargs
        
        # Reset the mock
        helper.client.chat.completions.create.reset_mock()
        
        # Test with a custom gpt-4o model
        helper.create_chat_completion(messages=[{"role": "user", "content": "Hello"}], model="gpt-4o-custom", max_tokens=100)
        
        # Check the create call
        args, kwargs = helper.client.chat.completions.create.call_args
        
        # Verify max_completion_tokens was used
        assert "max_completion_tokens" in kwargs
        assert kwargs["max_completion_tokens"] == 100
        assert "max_tokens" not in kwargs 