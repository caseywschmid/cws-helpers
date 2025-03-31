"""
Model feature support collections.

This module contains the collections of model features supported 
by different AI models, such as structured outputs and token parameters.
"""

from typing import Dict, Set

# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__, log_level="INFO")

# Collection of models that support structured outputs
STRUCTURED_OUTPUT_MODELS: Set[str] = {
    "gpt-4.5-preview",
    "o3-mini",
    "o1",
    "gpt-4o-mini",
    "gpt-4o"
}

# Collection of models that use max_completion_tokens instead of max_tokens
COMPLETION_TOKEN_MODELS: Set[str] = {
    "o3-mini",
    "o1",
    "o1-mini",
    "gpt-4o",
    "gpt-4o-mini"
}

# Dictionary mapping models to their unsupported parameters
UNSUPPORTED_PARAMETERS: Dict[str, Set[str]] = {
    "o3-mini": {"temperature", "top_p", "parallel_tool_calls"},
    "o1": {"temperature", "top_p", "parallel_tool_calls"},
    "o1-mini": {"temperature", "top_p", "parallel_tool_calls"},
} 