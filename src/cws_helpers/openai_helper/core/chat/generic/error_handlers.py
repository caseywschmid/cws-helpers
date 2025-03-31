"""
Error handlers for the OpenAI chat completions.

This module contains functions that handle various errors that can occur
during chat completion API calls.
"""

from typing import Dict, Any
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)


def handle_token_parameter_error(
    self,
    error: ValueError,
    params: Dict[str, Any]
) -> Any:
    """
    Handle errors related to token parameters in chat completion requests.
    
    Parameters
    ----------
    self : OpenAIHelper
        The OpenAIHelper instance
    error : ValueError
        The error that occurred
    params : Dict[str, Any]
        The parameters that were used in the request
        
    Returns
    -------
    Any
        The response from the API after fixing the token parameter
    """
    # Check if the error is related to max_tokens vs max_completion_tokens
    error_str = str(error)
    if "max_tokens" in error_str and "max_completion_tokens" in error_str:
        log.debug("Detected error related to token parameter. Attempting to fix...")
        
        # Swap the token parameter
        if "max_tokens" in params:
            tokens_value = params.pop("max_tokens")
            params["max_completion_tokens"] = tokens_value
            log.debug(f"Retrying with max_completion_tokens={tokens_value}")
        elif "max_completion_tokens" in params:
            tokens_value = params.pop("max_completion_tokens")
            params["max_tokens"] = tokens_value
            log.debug(f"Retrying with max_tokens={tokens_value}")
            
        # Retry the API call with the fixed parameters
        return self.client.chat.completions.create(**params)
    
    # If it's not a token parameter error, re-raise the exception
    raise error 