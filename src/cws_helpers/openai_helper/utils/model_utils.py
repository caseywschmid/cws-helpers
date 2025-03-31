"""
Model utility functions for OpenAI API interactions.

This module provides utility functions for working with different
AI models, managing model-specific parameters, and compatibility.
"""

import os
from typing import Dict, Any, Set, Union
from importlib.metadata import version

# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__, log_level="INFO")

# The version this helper was developed with
OPENAI_VERSION = "1.68.2"

# Try to import AIModel enum if available
try:
    from ..enums.ai_models import AIModel
    USE_AI_MODEL_ENUM = True
    log.debug("Using AIModel enum for model-specific logic")
except ImportError:
    USE_AI_MODEL_ENUM = False
    log.debug("AIModel enum not available, falling back to hardcoded model checks")

def check_dependency_versions():
    """
    Check if the installed OpenAI package version is compatible with this helper.
    Logs a warning if the versions aren't compatible.
    
    Returns
    -------
    bool
        True if versions are compatible, False otherwise
    """
    current_openai_version = version("openai")
    # Check if the warning should be muted
    mute_warning = os.getenv("MUTE_OPENAI_HELPER_WARNING", "False").lower() in (
        "true",
        "1",
        "t",
    )
    
    # Use version comparison to check for compatibility
    # This assumes versions following semantic versioning (major.minor.patch)
    current_parts = [int(p) for p in current_openai_version.split(".")]
    base_parts = [int(p) for p in OPENAI_VERSION.split(".")]
    
    # Compare major version - must be the same
    is_compatible = current_parts[0] == base_parts[0]
    # For minor version, current should be >= base version
    if is_compatible and len(current_parts) > 1 and len(base_parts) > 1:
        is_compatible = current_parts[1] >= base_parts[1]

    if not mute_warning and not is_compatible:
        log.warning(
            f"The 'OpenAIHelper' tool was created using openai version {OPENAI_VERSION}. "
            f"The version you have installed in this project ({current_openai_version}) "
            f"may not be compatible with this tool. If you encounter any issues, either "
            f"downgrade your OpenAI version to {OPENAI_VERSION} or email the creator "
            f"at caseywschmid@gmail.com to have the package updated."
        )
        log.info(
            "This warning can be muted by setting the MUTE_OPENAI_HELPER_WARNING "
            "environment variable to 'True'."
        )
    
    return is_compatible

def get_token_param_name(model: str) -> str:
    """
    Determine which token parameter to use based on the model.
    Uses AIModel enum if available, otherwise falls back to hardcoded checks.
    
    Parameters
    ----------
    model : str
        The model name to check
        
    Returns
    -------
    str
        Either 'max_tokens' or 'max_completion_tokens' depending on the model
    """
    if USE_AI_MODEL_ENUM:
        # Use AIModel enum's logic
        return AIModel.get_token_param_name(model)
    else:
        # Fallback to hardcoded checks
        is_o_model = model.startswith("o") or "o1-" in model or "o3-" in model or "o-" in model or "gpt-4o" in model
        return "max_completion_tokens" if is_o_model else "max_tokens"

def filter_unsupported_parameters(params: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Filter out parameters that are not supported by the specified model.
    
    Parameters
    ----------
    params : Dict[str, Any]
        Dictionary of parameters to filter
    model : str
        The model name to check against
        
    Returns
    -------
    Dict[str, Any]
        Filtered parameters dictionary with unsupported parameters removed
    """
    if USE_AI_MODEL_ENUM:
        # Use AIModel enum to get unsupported parameters
        unsupported_params = AIModel.get_unsupported_parameters(model)
    else:
        # Fallback for when AIModel enum is not available
        unsupported_params = set()
        # Simple check for o-series models
        is_o_model = model.startswith("o") or "o1-" in model or "o3-" in model or "o-" in model
        if is_o_model:
            # These parameters are known to be unsupported by o-series models
            unsupported_params = {"temperature", "top_p", "parallel_tool_calls"}
    
    # Remove unsupported parameters
    filtered_params = params.copy()
    for param in unsupported_params:
        if param in filtered_params:
            # Log a warning that we're removing an unsupported parameter
            log.debug(f"Parameter '{param}' is not supported by model '{model}'. Removing it from the request.")
            filtered_params.pop(param)
    
    return filtered_params 