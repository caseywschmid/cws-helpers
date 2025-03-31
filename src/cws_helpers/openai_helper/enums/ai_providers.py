"""
Enum for AI providers supported by the OpenAI Helper.

This module contains the AIProvider enum for identifying 
different providers of AI models.
"""

from enum import Enum, auto

# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__, log_level="INFO")


class AIProvider(Enum):
    """
    Enum representing different AI providers supported by the system.
    
    This enum is used to specify which AI provider to use when generating text.
    As new providers are added to the system, they should be added to this enum.
    
    Used in the OpenAIHelper class to identify the provider for a given model.
    """
    ANTHROPIC = auto()  # Claude models from Anthropic
    OPENAI = auto()     # GPT models from OpenAI
    
    @classmethod
    def from_string(cls, provider_name: str) -> 'AIProvider':
        """
        Convert a string representation to an AIProvider enum value.
        
        Args:
            provider_name: String name of the provider (case-insensitive)
            
        Returns:
            AIProvider enum value
            
        Raises:
            ValueError: If the provider name is not recognized
        """
        name_map = {
            'anthropic': cls.ANTHROPIC,
            'claude': cls.ANTHROPIC,
            'openai': cls.OPENAI,
            'gpt': cls.OPENAI,
        }
        
        normalized_name = provider_name.lower()
        if normalized_name not in name_map:
            raise ValueError(f"Unknown AI provider: {provider_name}")
        
        return name_map[normalized_name] 