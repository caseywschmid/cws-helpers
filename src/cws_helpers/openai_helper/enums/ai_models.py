from enum import Enum, auto
from typing import Dict, Set, Union

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


class AIModel(Enum):
    """
    Enum representing different AI models supported by the OpenAIHelper.
    
    This enum is used to specify which AI model to use when generating text.
    Each model is associated with a specific provider.
    The API will automatically use the latest version of each model.

    List of models:
    - gpt-4.5-preview
    - o3-mini
    - o1
    - o1-mini
    - gpt-4o
    - gpt-4o-mini
    - gpt-4-turbo
    - gpt-4
    - gpt-3.5-turbo

    Structured Output Support:
    The following models support structured outputs (using their latest versions):
    - gpt-4.5-preview
    - o3-mini
    - o1
    - gpt-4o-mini
    - gpt-4o

    Token Parameter Support:
    The following models require max_completion_tokens instead of max_tokens:
    - o3-mini
    - o1
    - o1-mini
    - gpt-4o
    - gpt-4o-mini
    """
    
    # OpenAI GPT models
    GPT_4_5_PREVIEW = "gpt-4.5-preview"
    O3_MINI = "o3-mini"
    O1 = "o1"
    O1_MINI = "o1-mini"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    
    @classmethod
    def get_provider(cls, model_name: Union[str, 'AIModel'] = None) -> AIProvider:
        """
        Get the provider for a specific model.
        
        Args:
            model_name: The AIModel or model name string to get the provider for
            
        Returns:
            The AIProvider for the model
        """
        # All models in this enum are from OpenAI
        return AIProvider.OPENAI
    
    @classmethod
    def from_string(cls, model_name: str) -> 'AIModel':
        """
        Convert a string representation to an AIModel enum value.
        
        Args:
            model_name: String name of the model
            
        Returns:
            AIModel enum value
            
        Raises:
            ValueError: If the model name is not recognized
        """
        try:
            return cls(model_name)
        except ValueError:
            # Try some common aliases
            name_map = {
                'gpt-4.5-preview': cls.GPT_4_5_PREVIEW,
                'o3-mini': cls.O3_MINI,
                'o1': cls.O1,
                'o1-mini': cls.O1_MINI,
                'gpt-4o': cls.GPT_4O,
                'gpt-4o-mini': cls.GPT_4O_MINI,
                'gpt-4': cls.GPT_4,
                'gpt-4-turbo': cls.GPT_4_TURBO,
                'gpt-3.5-turbo': cls.GPT_3_5_TURBO,
            }
            
            if model_name in name_map:
                return name_map[model_name]
            
            raise ValueError(f"Unknown AI model: {model_name}")

    @classmethod
    def supports_structured_outputs(cls, model_name: Union[str, 'AIModel']) -> bool:
        """
        Check if a model supports structured outputs.
        
        Args:
            model_name: Name of the model to check (string or AIModel enum)
            
        Returns:
            bool: True if the model supports structured outputs, False otherwise
        """
        # Convert to string if it's an enum
        if isinstance(model_name, AIModel):
            model_str = model_name.value
        elif isinstance(model_name, Enum):
            try:
                model_str = model_name.value
            except AttributeError:
                model_str = str(model_name)
        else:
            model_str = str(model_name)
            
        return model_str in cls.STRUCTURED_OUTPUT_MODELS

    @classmethod
    def get_token_param_name(cls, model_name: Union[str, 'AIModel']) -> str:
        """
        Determine which token parameter name to use based on the model.
        
        Args:
            model_name: Name of the model (string or AIModel enum)
            
        Returns:
            str: Either 'max_tokens' or 'max_completion_tokens' depending on the model
        """
        # Debug information about the input
        log.debug(f"get_token_param_name called with: {model_name}, type: {type(model_name)}")
        
        # Convert AIModel to string if needed
        if isinstance(model_name, AIModel):
            model_str = model_name.value
            log.debug(f"Converted AIModel enum to string: {model_str}")
        elif isinstance(model_name, Enum):
            try:
                model_str = model_name.value
                log.debug(f"Converted enum to string: {model_str}")
            except AttributeError:
                # In case it's an enum but doesn't have value attribute
                model_str = str(model_name)
                log.debug(f"Used str() for enum: {model_str}")
        else:
            model_str = str(model_name)
            log.debug(f"Input is not an enum, using as string: {model_str}")
        
        # Check if it's in our known list of models requiring max_completion_tokens
        if model_str in cls.COMPLETION_TOKEN_MODELS:
            log.debug(f"Model {model_str} is in COMPLETION_TOKEN_MODELS list")
            return "max_completion_tokens"
        
        # Explicit check for 'o' series models as a fallback
        if any(o_model in model_str for o_model in ["o3-", "o1-", "gpt-4o"]) or model_str in ["o1", "o3"]:
            log.debug(f"Model {model_str} is in the 'o' series, using max_completion_tokens")
            return "max_completion_tokens"
        else:
            log.debug(f"Model {model_str} is not in the 'o' series, using max_tokens")
            return "max_tokens"
            
    @classmethod
    def get_unsupported_parameters(cls, model_name: Union[str, 'AIModel']) -> Set[str]:
        """
        Get the set of parameters that are unsupported by a specific model.
        
        Args:
            model_name: Name of the model (string or AIModel enum)
            
        Returns:
            Set[str]: Set of parameter names that are unsupported by the model
        """
        # Convert to string if it's an enum
        if isinstance(model_name, AIModel):
            model_str = model_name.value
        elif isinstance(model_name, Enum):
            try:
                model_str = model_name.value
            except AttributeError:
                model_str = str(model_name)
        else:
            model_str = str(model_name)
        
        # Check our dictionary of known unsupported parameters
        if model_str in cls.UNSUPPORTED_PARAMETERS:
            return cls.UNSUPPORTED_PARAMETERS[model_str]
        
        # For O-series models not explicitly in our dictionary, check by name pattern
        if any(o_model in model_str for o_model in ["o3-", "o1-"]) or model_str in ["o1", "o3"]:
            # By default, assume o-series reasoning models don't support temperature and top_p
            return {"temperature", "top_p", "parallel_tool_calls"}
        
        # Default for models we don't have specific information about
        return set()

# Initialize class variables for AIModel
AIModel.STRUCTURED_OUTPUT_MODELS = {
    "gpt-4.5-preview",
    "o3-mini",
    "o1",
    "gpt-4o-mini",
    "gpt-4o"
}

AIModel.COMPLETION_TOKEN_MODELS = {
    "o3-mini",
    "o1",
    "o1-mini",
    "gpt-4o",
    "gpt-4o-mini"
}

# Dictionary mapping models to their unsupported parameters
AIModel.UNSUPPORTED_PARAMETERS = {
    "o3-mini": {"temperature", "top_p", "parallel_tool_calls"},
    "o1": {"temperature", "top_p", "parallel_tool_calls"},
    "o1-mini": {"temperature", "top_p", "parallel_tool_calls"},
}
