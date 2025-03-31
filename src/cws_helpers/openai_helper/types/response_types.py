"""
Response type definitions for OpenAI API interactions.

This module provides type definitions and helpers for handling
various response formats from the OpenAI API.
"""

from typing import TypeVar, Type, Generic
from openai.types.chat import ChatCompletion

# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# Define a type variable for response format types
ResponseFormatT = TypeVar('ResponseFormatT')

# Try to import beta chat completions for structured outputs
try:
    from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
    HAS_PARSED_COMPLETION = True
    log.debug("Using ParsedChatCompletion for structured outputs")
except ImportError:
    # Define a fallback for older versions
    class ParsedChatCompletion(ChatCompletion, Generic[ResponseFormatT]):
        pass
    HAS_PARSED_COMPLETION = False
    log.debug("ParsedChatCompletion not available, using fallback")

def get_parsed_chat_completion():
    """
    Return the appropriate ParsedChatCompletion class based on availability.
    
    This function handles compatibility with different versions of the
    OpenAI Python package.
    
    Returns
    -------
    Type
        The ParsedChatCompletion class or a fallback
    """
    # Check if the genuine ParsedChatCompletion is available
    if HAS_PARSED_COMPLETION:
        try:
            from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
            return ParsedChatCompletion
        except ImportError:
            log.warning("Failed to import ParsedChatCompletion despite earlier success")
    
    # Return our fallback implementation
    return ParsedChatCompletion 