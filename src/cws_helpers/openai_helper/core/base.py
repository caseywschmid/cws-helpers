"""
Base OpenAIHelper class for interacting with the OpenAI API.

This module contains the main OpenAIHelper class which provides
a simplified interface to OpenAI's API.
"""

from openai import OpenAI
from typing import Annotated
from cws_helpers.logger import configure_logging
from ..utils.model_utils import check_dependency_versions
from .messages import MessageMixin
from .chat.structured import StructuredCompletionMixin
from .chat.generic import GenericChatCompletionMixin

# Configure logging for this module
log = configure_logging(__name__)

class OpenAIHelper(MessageMixin, StructuredCompletionMixin, GenericChatCompletionMixin):
    """
    A helper class for interacting with the OpenAI API.
    
    Provides methods for creating chat completions with support for:
    - Basic text responses
    - Image inputs
    - JSON mode
    - Structured outputs using JSON schema
    - Pydantic model parsing
    - Beta structured outputs with automatic parsing
    
    This class initializes the OpenAI client with your API key and
    organization, and provides methods to interact with the API.
    """

    def __init__(
        self,
        api_key: Annotated[str, "The OpenAI API Key you wish to use"],
        organization: str,
    ):
        """
        Initialize the OpenAI helper with your API key and organization.
        
        Parameters
        ----------
        api_key : str
            Your OpenAI API key
        organization : str
            Your OpenAI organization ID
        """
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=api_key, organization=organization)
        
        # Check if the OpenAI package version is compatible
        check_dependency_versions() 