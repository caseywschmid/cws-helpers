"""
OpenAI Helper module for interacting with OpenAI's API.

This module provides a simplified interface for making requests to OpenAI's API,
with support for text completions, image inputs, JSON mode, structured outputs,
and streaming responses.

Usage:
    from cws_helpers.openai_helper import OpenAIHelper
    
    helper = OpenAIHelper(api_key="your_api_key", organization="your_org_id")
    response = helper.create_chat_completion(prompt="Hello, world!")
    
    # You can also access the AIModel enum for model-specific logic
    from cws_helpers.openai_helper import AIModel
    
    # Check if a model supports structured outputs
    supports_structured = AIModel.supports_structured_outputs("gpt-4o")
    
    # Get the appropriate token parameter name for a model
    token_param = AIModel.get_token_param_name("o3-mini")  # Returns "max_completion_tokens"
"""

from .openai_helper import OpenAIHelper
from .enums import AIModel, AIProvider

__all__ = ["OpenAIHelper", "AIModel", "AIProvider"]
