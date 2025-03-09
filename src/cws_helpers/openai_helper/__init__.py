"""
OpenAI Helper module for interacting with OpenAI's API.

This module provides a simplified interface for making requests to OpenAI's API,
with support for text completions, image inputs, JSON mode, structured outputs,
and streaming responses.

Usage:
    from cws_helpers.openai_helper import OpenAIHelper
    
    helper = OpenAIHelper(api_key="your_api_key", organization="your_org_id")
    response = helper.create_chat_completion(prompt="Hello, world!")
"""

from .openai_helper import OpenAIHelper

__all__ = ["OpenAIHelper"]
