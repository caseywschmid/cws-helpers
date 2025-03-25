import pytest
from cws_helpers.openai_helper import AIModel, AIProvider


class TestAIProvider:
    """Tests for the AIProvider enum."""
    
    def test_from_string(self):
        """Test converting string representations to AIProvider enum values."""
        assert AIProvider.from_string("openai") == AIProvider.OPENAI
        assert AIProvider.from_string("OPENAI") == AIProvider.OPENAI
        assert AIProvider.from_string("gpt") == AIProvider.OPENAI
        
        assert AIProvider.from_string("anthropic") == AIProvider.ANTHROPIC
        assert AIProvider.from_string("ANTHROPIC") == AIProvider.ANTHROPIC
        assert AIProvider.from_string("claude") == AIProvider.ANTHROPIC
        
        # Test invalid provider
        with pytest.raises(ValueError):
            AIProvider.from_string("invalid_provider")


class TestAIModel:
    """Tests for the AIModel enum."""
    
    def test_from_string(self):
        """Test converting string representations to AIModel enum values."""
        assert AIModel.from_string("gpt-4-turbo") == AIModel.GPT_4_TURBO
        assert AIModel.from_string("gpt-4o") == AIModel.GPT_4O
        assert AIModel.from_string("o3-mini") == AIModel.O3_MINI
        
        # Test invalid model
        with pytest.raises(ValueError):
            AIModel.from_string("invalid_model")
    
    def test_get_provider(self):
        """Test getting the provider for a model."""
        # Test OpenAI models
        assert AIModel.get_provider(AIModel.GPT_4_TURBO) == AIProvider.OPENAI
        assert AIModel.get_provider("gpt-4") == AIProvider.OPENAI
        assert AIModel.get_provider("o3-mini") == AIProvider.OPENAI
        assert AIModel.get_provider("o1") == AIProvider.OPENAI
        
        # Test invalid model - should still return OpenAI provider for unknown models
        assert AIModel.get_provider("unknown-model") == AIProvider.OPENAI
    
    def test_supports_structured_outputs(self):
        """Test checking if a model supports structured outputs."""
        # Test models that support structured outputs
        assert AIModel.supports_structured_outputs("gpt-4.5-preview") is True
        assert AIModel.supports_structured_outputs("o3-mini") is True
        assert AIModel.supports_structured_outputs(AIModel.O1) is True
        
        # Test models that don't support structured outputs
        assert AIModel.supports_structured_outputs("gpt-3.5-turbo") is False
        assert AIModel.supports_structured_outputs(AIModel.GPT_4) is False
    
    def test_get_token_param_name(self):
        """Test getting the token parameter name for a model."""
        # Test models that use max_completion_tokens
        assert AIModel.get_token_param_name("o3-mini") == "max_completion_tokens"
        assert AIModel.get_token_param_name("o1") == "max_completion_tokens"
        assert AIModel.get_token_param_name("o1-mini") == "max_completion_tokens"
        assert AIModel.get_token_param_name("gpt-4o") == "max_completion_tokens"
        assert AIModel.get_token_param_name(AIModel.GPT_4O_MINI) == "max_completion_tokens"
        
        # Test models that use max_tokens
        assert AIModel.get_token_param_name("gpt-4") == "max_tokens"
        assert AIModel.get_token_param_name("gpt-3.5-turbo") == "max_tokens"
        assert AIModel.get_token_param_name(AIModel.GPT_4_TURBO) == "max_tokens"
        
        # Test models that aren't in our enum but should still work
        assert AIModel.get_token_param_name("gpt-3.5-turbo-16k") == "max_tokens"
        assert AIModel.get_token_param_name("o3") == "max_completion_tokens"
        assert AIModel.get_token_param_name("gpt-4o-2024-05-13") == "max_completion_tokens"
        
        # Test passing an actual enum
        assert AIModel.get_token_param_name(AIModel.O3_MINI) == "max_completion_tokens"
        assert AIModel.get_token_param_name(AIModel.GPT_4) == "max_tokens"

    def test_get_unsupported_parameters(self):
        """Test getting unsupported parameters for different models."""
        # Test models with known unsupported parameters
        assert "temperature" in AIModel.get_unsupported_parameters("o3-mini")
        assert "top_p" in AIModel.get_unsupported_parameters("o1")
        assert "parallel_tool_calls" in AIModel.get_unsupported_parameters("o1-mini")
        
        # Test using enum values
        assert "temperature" in AIModel.get_unsupported_parameters(AIModel.O3_MINI)
        assert "top_p" in AIModel.get_unsupported_parameters(AIModel.O1)
        
        # Test models with pattern matching (o-series)
        assert "temperature" in AIModel.get_unsupported_parameters("o3-2024-05-13")
        assert "top_p" in AIModel.get_unsupported_parameters("o1-preview")
        
        # Test models that should support all parameters
        assert len(AIModel.get_unsupported_parameters("gpt-4")) == 0
        assert len(AIModel.get_unsupported_parameters("gpt-3.5-turbo")) == 0
        assert len(AIModel.get_unsupported_parameters(AIModel.GPT_4_TURBO)) == 0 