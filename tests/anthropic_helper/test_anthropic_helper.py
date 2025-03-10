"""
Tests for the AnthropicHelper module.

These tests use mocking to avoid making actual API calls.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from typing import Dict, Any, List

from cws_helpers.anthropic_helper import AnthropicHelper, ClaudeModel, ClaudeCostCalculator

# ------------------ Test Fixtures ------------------ #

@pytest.fixture
def mock_anthropic_client():
    """Create a mock Anthropic client for testing."""
    with patch('anthropic.Anthropic') as mock_client:
        # Mock the messages.create method
        mock_messages = MagicMock()
        mock_client.return_value.messages = mock_messages
        
        # Mock the response for messages.create
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="This is a test response")]
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20
        mock_response.model = ClaudeModel.CLAUDE_3_5_SONNET_LATEST.value
        mock_messages.create.return_value = mock_response
        
        # Mock the response for messages.count_tokens
        mock_token_response = MagicMock()
        mock_token_response.tokens = 15
        mock_messages.count_tokens.return_value = mock_token_response
        
        yield mock_client

# ------------------ Tests ------------------ #

class TestAnthropicHelper:
    """Tests for the AnthropicHelper class."""
    
    def test_init_with_api_key(self):
        """Test initialization with an API key."""
        helper = AnthropicHelper(api_key="test_api_key")
        assert helper.api_key == "test_api_key"
        assert helper.model == ClaudeModel.default()
    
    def test_init_with_env_var(self, monkeypatch):
        """Test initialization with an environment variable."""
        monkeypatch.setenv("CLAUDE_API_KEY", "env_api_key")
        helper = AnthropicHelper()
        assert helper.api_key == "env_api_key"
    
    def test_init_missing_api_key(self, monkeypatch):
        """Test initialization with no API key."""
        monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
        with pytest.raises(ValueError) as excinfo:
            AnthropicHelper()
        
        # Check that the error message contains helpful instructions
        error_msg = str(excinfo.value)
        assert "API key must be provided" in error_msg
        assert "Create a .env file" in error_msg
        assert "Set the environment variable" in error_msg
        assert "Pass the API key directly" in error_msg
        assert "https://console.anthropic.com/" in error_msg
    
    def test_create_message(self):
        """Test creating a message."""
        # Create mock client
        mock_client = MagicMock()
        mock_messages = MagicMock()
        mock_client.messages = mock_messages
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="This is a test response")]
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20
        mock_response.model = ClaudeModel.CLAUDE_3_5_SONNET_LATEST.value
        mock_messages.create.return_value = mock_response
        
        # Create the helper with the mock client
        helper = AnthropicHelper(client=mock_client)
        response = helper.create_message("Test prompt")
        
        # Check that the client was called correctly
        mock_messages.create.assert_called_once()
        call_kwargs = mock_messages.create.call_args.kwargs
        assert call_kwargs["model"] == ClaudeModel.default()
        assert call_kwargs["messages"][0]["content"] == "Test prompt"
        
        # Check the response
        assert response == "This is a test response"
    
    def test_create_message_with_system(self):
        """Test creating a message with a system prompt."""
        # Create mock client
        mock_client = MagicMock()
        mock_messages = MagicMock()
        mock_client.messages = mock_messages
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="This is a test response")]
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20
        mock_response.model = ClaudeModel.CLAUDE_3_5_SONNET_LATEST.value
        mock_messages.create.return_value = mock_response
        
        # Create the helper with the mock client
        helper = AnthropicHelper(client=mock_client)
        response = helper.create_message("Test prompt", system="System prompt")
        
        # Check that the system prompt was passed correctly
        call_kwargs = mock_messages.create.call_args.kwargs
        assert call_kwargs["system"] == "System prompt"
    
    def test_count_tokens(self):
        """Test counting tokens."""
        # Create mock client
        mock_client = MagicMock()
        mock_messages = MagicMock()
        mock_client.messages = mock_messages
        
        # Mock the response
        mock_token_response = MagicMock()
        mock_token_response.tokens = 15
        mock_messages.count_tokens.return_value = mock_token_response
        
        # Create the helper with the mock client
        helper = AnthropicHelper(client=mock_client)
        token_count = helper.count_tokens("Test text")
        
        # Check that the client was called correctly
        mock_messages.count_tokens.assert_called_once()
        call_kwargs = mock_messages.count_tokens.call_args.kwargs
        assert call_kwargs["model"] == ClaudeModel.default()
        assert call_kwargs["messages"][0]["content"] == "Test text"
        
        # Check the response
        assert token_count == 15

class TestClaudeCostCalculator:
    """Tests for the ClaudeCostCalculator class."""
    
    def test_calculate_cost_opus(self):
        """Test calculating cost for Claude 3 Opus."""
        cost = ClaudeCostCalculator.calculate_cost(
            ClaudeModel.CLAUDE_3_OPUS_LATEST.value, 1000, 500
        )
        expected_cost = (1000 / 1000 * (15.0 / 1000)) + (500 / 1000 * (75.0 / 1000))
        assert cost == expected_cost
    
    def test_calculate_cost_sonnet(self):
        """Test calculating cost for Claude 3 Sonnet."""
        cost = ClaudeCostCalculator.calculate_cost(
            ClaudeModel.CLAUDE_3_SONNET_20240229.value, 1000, 500
        )
        expected_cost = (1000 / 1000 * (3.0 / 1000)) + (500 / 1000 * (15.0 / 1000))
        assert cost == expected_cost
    
    def test_calculate_cost_haiku(self):
        """Test calculating cost for Claude 3 Haiku."""
        cost = ClaudeCostCalculator.calculate_cost(
            ClaudeModel.CLAUDE_3_HAIKU_20240307.value, 1000, 500
        )
        expected_cost = (1000 / 1000 * (0.25 / 1000)) + (500 / 1000 * (1.25 / 1000))
        assert cost == expected_cost
    
    def test_calculate_cost_claude_3_5_sonnet(self):
        """Test calculating cost for Claude 3.5 Sonnet."""
        cost = ClaudeCostCalculator.calculate_cost(
            ClaudeModel.CLAUDE_3_5_SONNET_LATEST.value, 1000, 500
        )
        expected_cost = (1000 / 1000 * (3.0 / 1000)) + (500 / 1000 * (15.0 / 1000))
        assert cost == expected_cost
    
    def test_calculate_cost_claude_3_5_haiku(self):
        """Test calculating cost for Claude 3.5 Haiku."""
        cost = ClaudeCostCalculator.calculate_cost(
            ClaudeModel.CLAUDE_3_5_HAIKU_LATEST.value, 1000, 500
        )
        expected_cost = (1000 / 1000 * (0.80 / 1000)) + (500 / 1000 * (4.0 / 1000))
        assert cost == expected_cost
    
    def test_calculate_cost_claude_3_7_sonnet(self):
        """Test calculating cost for Claude 3.7 Sonnet."""
        cost = ClaudeCostCalculator.calculate_cost(
            ClaudeModel.CLAUDE_3_7_SONNET_LATEST.value, 1000, 500
        )
        expected_cost = (1000 / 1000 * (3.0 / 1000)) + (500 / 1000 * (15.0 / 1000))
        assert cost == expected_cost
    
    def test_calculate_cost_claude_2(self):
        """Test calculating cost for Claude 2."""
        cost = ClaudeCostCalculator.calculate_cost(
            ClaudeModel.CLAUDE_2_1.value, 1000, 500
        )
        expected_cost = (1000 / 1000 * 0.008) + (500 / 1000 * 0.024)
        assert cost == expected_cost
    
    def test_calculate_cost_unknown_model(self):
        """Test calculating cost for an unknown model."""
        cost = ClaudeCostCalculator.calculate_cost(
            "unknown-model", 1000, 500
        )
        # Should default to Claude 3.5 Sonnet pricing
        expected_cost = (1000 / 1000 * (3.0 / 1000)) + (500 / 1000 * (15.0 / 1000))
        assert cost == expected_cost
    
    def test_calculate_prompt_cache_write_cost_claude_3_7_sonnet(self):
        """Test calculating prompt cache write cost for Claude 3.7 Sonnet."""
        cost = ClaudeCostCalculator.calculate_prompt_cache_cost(
            ClaudeModel.CLAUDE_3_7_SONNET_LATEST.value, 1000, "write"
        )
        expected_cost = (1000 / 1000) * (3.75 / 1000)
        assert cost == expected_cost
    
    def test_calculate_prompt_cache_read_cost_claude_3_7_sonnet(self):
        """Test calculating prompt cache read cost for Claude 3.7 Sonnet."""
        cost = ClaudeCostCalculator.calculate_prompt_cache_cost(
            ClaudeModel.CLAUDE_3_7_SONNET_LATEST.value, 1000, "read"
        )
        expected_cost = (1000 / 1000) * (0.30 / 1000)
        assert cost == expected_cost
    
    def test_calculate_prompt_cache_write_cost_claude_3_5_haiku(self):
        """Test calculating prompt cache write cost for Claude 3.5 Haiku."""
        cost = ClaudeCostCalculator.calculate_prompt_cache_cost(
            ClaudeModel.CLAUDE_3_5_HAIKU_LATEST.value, 1000, "write"
        )
        expected_cost = (1000 / 1000) * (1.0 / 1000)
        assert cost == expected_cost
    
    def test_calculate_prompt_cache_read_cost_claude_3_5_haiku(self):
        """Test calculating prompt cache read cost for Claude 3.5 Haiku."""
        cost = ClaudeCostCalculator.calculate_prompt_cache_cost(
            ClaudeModel.CLAUDE_3_5_HAIKU_LATEST.value, 1000, "read"
        )
        expected_cost = (1000 / 1000) * (0.08 / 1000)
        assert cost == expected_cost
    
    def test_calculate_prompt_cache_invalid_operation(self):
        """Test calculating prompt cache cost with invalid operation."""
        with pytest.raises(ValueError, match="Operation must be either 'write' or 'read'"):
            ClaudeCostCalculator.calculate_prompt_cache_cost(
                ClaudeModel.CLAUDE_3_5_SONNET_LATEST.value, 1000, "invalid"
            )
