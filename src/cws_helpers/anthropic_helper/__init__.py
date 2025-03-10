"""
Anthropic Helper module for interacting with Anthropic's Claude API.

This module provides a simplified interface for making requests to Anthropic's Claude API,
with support for text completions, system prompts, streaming responses, and cost calculation.

Usage:
    from cws_helpers.anthropic_helper import AnthropicHelper
    
    helper = AnthropicHelper(api_key="your_api_key")
    response = helper.create_message(prompt="Hello, world!")
"""

from .anthropic_helper import AnthropicHelper, ClaudeModel, ClaudeCostCalculator

__all__ = ["AnthropicHelper", "ClaudeModel", "ClaudeCostCalculator"]
