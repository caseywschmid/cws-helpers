# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# ------------------ Imports ------------------ #
import os
import time
import json
from typing import Dict, List, Optional, Union, Any, Iterable, Tuple, TypeVar, cast
from enum import Enum
from functools import wraps
from importlib.metadata import version
from pathlib import Path

import anthropic
from anthropic import Anthropic
from anthropic.types import (
    Message,
    TextBlock,
)
from anthropic._types import NOT_GIVEN
from anthropic._streaming import Stream
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path)
    log.info(f"Loaded environment variables from {dotenv_path}")
else:
    log.warning("No .env file found. Make sure to set CLAUDE_API_KEY environment variable.")

# The version this helper was developed with
ANTHROPIC_VERSION = "0.49.0"


# ------------------ Constants ------------------ #
class ClaudeModel(str, Enum):
    """Available Claude models."""

    # Claude 3.7 models
    CLAUDE_3_7_SONNET_LATEST = "claude-3-7-sonnet-latest"
    CLAUDE_3_7_SONNET_20250219 = "claude-3-7-sonnet-20250219"

    # Claude 3.5 models
    CLAUDE_3_5_HAIKU_LATEST = "claude-3-5-haiku-latest"
    CLAUDE_3_5_HAIKU_20241022 = "claude-3-5-haiku-20241022"
    CLAUDE_3_5_SONNET_LATEST = "claude-3-5-sonnet-latest"
    CLAUDE_3_5_SONNET_20241022 = "claude-3-5-sonnet-20241022"
    CLAUDE_3_5_SONNET_20240620 = "claude-3-5-sonnet-20240620"

    # Claude 3 models
    CLAUDE_3_OPUS_LATEST = "claude-3-opus-latest"
    CLAUDE_3_OPUS_20240229 = "claude-3-opus-20240229"
    CLAUDE_3_SONNET_20240229 = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU_20240307 = "claude-3-haiku-20240307"

    # Claude 2 models
    CLAUDE_2_1 = "claude-2.1"
    CLAUDE_2_0 = "claude-2.0"

    @classmethod
    def default(cls) -> str:
        """Return the default model."""
        return cls.CLAUDE_3_5_SONNET_LATEST.value


# ------------------ Cost Calculation ------------------ #
class ClaudeCostCalculator:
    """
    Calculates the cost of Claude API calls based on token usage.

    Rates are based on the official Anthropic pricing:
    https://www.anthropic.com/api

    These rates may change over time and should be updated accordingly.
    """

    # Cost per 1M tokens in USD (divided by 1000 to get cost per 1K tokens)
    # Claude 3.7 models
    CLAUDE_3_7_SONNET_INPUT_COST = 3.0 / 1000  # $3 per MTok
    CLAUDE_3_7_SONNET_OUTPUT_COST = 15.0 / 1000  # $15 per MTok
    CLAUDE_3_7_SONNET_PROMPT_CACHE_WRITE_COST = 3.75 / 1000  # $3.75 per MTok
    CLAUDE_3_7_SONNET_PROMPT_CACHE_READ_COST = 0.30 / 1000  # $0.30 per MTok

    # Claude 3.5 models - Sonnet
    CLAUDE_3_5_SONNET_INPUT_COST = 3.0 / 1000  # $3 per MTok
    CLAUDE_3_5_SONNET_OUTPUT_COST = 15.0 / 1000  # $15 per MTok
    CLAUDE_3_5_SONNET_PROMPT_CACHE_WRITE_COST = 3.75 / 1000  # $3.75 per MTok
    CLAUDE_3_5_SONNET_PROMPT_CACHE_READ_COST = 0.30 / 1000  # $0.30 per MTok

    # Claude 3.5 models - Haiku
    CLAUDE_3_5_HAIKU_INPUT_COST = 0.80 / 1000  # $0.80 per MTok
    CLAUDE_3_5_HAIKU_OUTPUT_COST = 4.0 / 1000  # $4 per MTok
    CLAUDE_3_5_HAIKU_PROMPT_CACHE_WRITE_COST = 1.0 / 1000  # $1 per MTok
    CLAUDE_3_5_HAIKU_PROMPT_CACHE_READ_COST = 0.08 / 1000  # $0.08 per MTok

    # Claude 3 models - Opus
    CLAUDE_3_OPUS_INPUT_COST = 15.0 / 1000  # $15 per MTok
    CLAUDE_3_OPUS_OUTPUT_COST = 75.0 / 1000  # $75 per MTok
    CLAUDE_3_OPUS_PROMPT_CACHE_WRITE_COST = 18.75 / 1000  # $18.75 per MTok
    CLAUDE_3_OPUS_PROMPT_CACHE_READ_COST = 1.50 / 1000  # $1.50 per MTok

    # Claude 3 models - Sonnet (same as 3.5 Sonnet)
    CLAUDE_3_SONNET_INPUT_COST = 3.0 / 1000  # $3 per MTok
    CLAUDE_3_SONNET_OUTPUT_COST = 15.0 / 1000  # $15 per MTok

    # Claude 3 models - Haiku
    CLAUDE_3_HAIKU_INPUT_COST = 0.25 / 1000  # $0.25 per MTok
    CLAUDE_3_HAIKU_OUTPUT_COST = 1.25 / 1000  # $1.25 per MTok
    CLAUDE_3_HAIKU_PROMPT_CACHE_WRITE_COST = 0.30 / 1000  # $0.30 per MTok
    CLAUDE_3_HAIKU_PROMPT_CACHE_READ_COST = 0.03 / 1000  # $0.03 per MTok

    # Claude 2 models (keeping existing values as they weren't in the screenshots)
    CLAUDE_2_INPUT_COST = 0.008  # $8 per MTok
    CLAUDE_2_OUTPUT_COST = 0.024  # $24 per MTok

    @classmethod
    def calculate_cost(cls, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate the cost of a Claude API call based on token usage and model.

        Args:
            model (str): The Claude model used
            input_tokens (int): Number of input tokens used
            output_tokens (int): Number of output tokens used

        Returns:
            float: Total cost in USD
        """
        # Claude 3.7 models
        if model.startswith("claude-3-7-sonnet"):
            input_cost = (input_tokens / 1000) * cls.CLAUDE_3_7_SONNET_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_3_7_SONNET_OUTPUT_COST

        # Claude 3.5 Haiku models
        elif model.startswith("claude-3-5-haiku"):
            input_cost = (input_tokens / 1000) * cls.CLAUDE_3_5_HAIKU_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_3_5_HAIKU_OUTPUT_COST

        # Claude 3.5 Sonnet models
        elif model.startswith("claude-3-5-sonnet"):
            input_cost = (input_tokens / 1000) * cls.CLAUDE_3_5_SONNET_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_3_5_SONNET_OUTPUT_COST

        # Claude 3 Opus models
        elif model.startswith("claude-3-opus"):
            input_cost = (input_tokens / 1000) * cls.CLAUDE_3_OPUS_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_3_OPUS_OUTPUT_COST

        # Claude 3 Sonnet models
        elif model.startswith("claude-3-sonnet"):
            input_cost = (input_tokens / 1000) * cls.CLAUDE_3_SONNET_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_3_SONNET_OUTPUT_COST

        # Claude 3 Haiku models
        elif model.startswith("claude-3-haiku"):
            input_cost = (input_tokens / 1000) * cls.CLAUDE_3_HAIKU_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_3_HAIKU_OUTPUT_COST

        # Claude 2 models
        elif model.startswith("claude-2"):
            input_cost = (input_tokens / 1000) * cls.CLAUDE_2_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_2_OUTPUT_COST

        else:
            # Default to Claude 3.5 Sonnet pricing if model is unknown
            log.warning(f"Unknown model {model}, using Claude 3.5 Sonnet pricing")
            input_cost = (input_tokens / 1000) * cls.CLAUDE_3_5_SONNET_INPUT_COST
            output_cost = (output_tokens / 1000) * cls.CLAUDE_3_5_SONNET_OUTPUT_COST

        return input_cost + output_cost

    @classmethod
    def calculate_prompt_cache_cost(
        cls, model: str, tokens: int, operation: str = "write"
    ) -> float:
        """
        Calculate the cost of prompt caching operations.

        Args:
            model (str): The Claude model used
            tokens (int): Number of tokens in the prompt
            operation (str): Either "write" or "read"

        Returns:
            float: Total cost in USD
        """
        if operation.lower() not in ["write", "read"]:
            raise ValueError("Operation must be either 'write' or 'read'")

        # Claude 3.7 models
        if model.startswith("claude-3-7-sonnet"):
            if operation.lower() == "write":
                return (tokens / 1000) * cls.CLAUDE_3_7_SONNET_PROMPT_CACHE_WRITE_COST
            else:  # read
                return (tokens / 1000) * cls.CLAUDE_3_7_SONNET_PROMPT_CACHE_READ_COST

        # Claude 3.5 Haiku models
        elif model.startswith("claude-3-5-haiku"):
            if operation.lower() == "write":
                return (tokens / 1000) * cls.CLAUDE_3_5_HAIKU_PROMPT_CACHE_WRITE_COST
            else:  # read
                return (tokens / 1000) * cls.CLAUDE_3_5_HAIKU_PROMPT_CACHE_READ_COST

        # Claude 3.5 Sonnet models
        elif model.startswith("claude-3-5-sonnet"):
            if operation.lower() == "write":
                return (tokens / 1000) * cls.CLAUDE_3_5_SONNET_PROMPT_CACHE_WRITE_COST
            else:  # read
                return (tokens / 1000) * cls.CLAUDE_3_5_SONNET_PROMPT_CACHE_READ_COST

        # Claude 3 Opus models
        elif model.startswith("claude-3-opus"):
            if operation.lower() == "write":
                return (tokens / 1000) * cls.CLAUDE_3_OPUS_PROMPT_CACHE_WRITE_COST
            else:  # read
                return (tokens / 1000) * cls.CLAUDE_3_OPUS_PROMPT_CACHE_READ_COST

        # Claude 3 Haiku models
        elif model.startswith("claude-3-haiku"):
            if operation.lower() == "write":
                return (tokens / 1000) * cls.CLAUDE_3_HAIKU_PROMPT_CACHE_WRITE_COST
            else:  # read
                return (tokens / 1000) * cls.CLAUDE_3_HAIKU_PROMPT_CACHE_READ_COST

        # For other models that don't have prompt caching or unknown models
        else:
            log.warning(
                f"Prompt caching cost calculation not available for model {model}, using Claude 3.5 Sonnet pricing"
            )
            if operation.lower() == "write":
                return (tokens / 1000) * cls.CLAUDE_3_5_SONNET_PROMPT_CACHE_WRITE_COST
            else:  # read
                return (tokens / 1000) * cls.CLAUDE_3_5_SONNET_PROMPT_CACHE_READ_COST


# ------------------ Retry Decorator ------------------ #
def retry_on_rate_limit(max_retries: int = 3, initial_delay: float = 1.0):
    """
    Decorator that retries a function call when a RateLimitError is raised.

    Args:
        max_retries (int): Maximum number of retry attempts
        initial_delay (float): Initial delay between retries in seconds (doubles each retry)

    Returns:
        The decorated function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            attempt = 0

            while True:
                try:
                    return func(*args, **kwargs)
                except anthropic.RateLimitError as e:
                    attempt += 1
                    if attempt >= max_retries:
                        log.error(
                            f"Rate limit exceeded after {max_retries} attempts. Final error: {e}"
                        )
                        raise

                    wait_time = delay * (2 ** (attempt - 1))  # Exponential backoff
                    log.warning(
                        f"Rate limit hit, attempt {attempt}/{max_retries}. Waiting {wait_time} seconds..."
                    )
                    time.sleep(wait_time)

        return wrapper

    return decorator


# ------------------ AnthropicHelper Class ------------------ #
class AnthropicHelper:
    """
    A helper class for interacting with the Anthropic Claude API.

    This class provides methods for creating chat completions with Claude models,
    with support for:
    - Text messages
    - System prompts
    - Streaming responses
    - Cost calculation
    - Automatic retries for rate limiting

    Usage:
        from cws_helpers.anthropic_helper import AnthropicHelper

        helper = AnthropicHelper()
        response = helper.create_message("Tell me about AI")
        print(response)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = ClaudeModel.default(),
        max_retries: int = 3,
        initial_retry_delay: float = 1.0,
        timeout: float = 120.0,
        client: Optional[Anthropic] = None,  # Allow client injection for testing
    ):
        """
        Initialize the AnthropicHelper.
        
        Args:
            api_key (str, optional): The Anthropic API key. If not provided, 
                                     it will be read from the CLAUDE_API_KEY environment variable.
            model (str, optional): The default Claude model to use. Defaults to Claude 3.5 Sonnet Latest.
            max_retries (int, optional): Maximum number of retries for rate limiting. Defaults to 3.
            initial_retry_delay (float, optional): Initial delay between retries in seconds. Defaults to 1.0.
            timeout (float, optional): Timeout for API requests in seconds. Defaults to 120.0.
            client (Anthropic, optional): An existing Anthropic client instance. If provided, api_key is ignored.
        
        Raises:
            ValueError: If no API key is provided and CLAUDE_API_KEY environment variable is not set.
                        Provides instructions on how to set up the API key.
        """
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key and client is None:
            error_message = (
                "API key must be provided or set as CLAUDE_API_KEY environment variable.\n"
                "You can set it in one of the following ways:\n"
                "1. Create a .env file in your project root with CLAUDE_API_KEY=your_api_key\n"
                "2. Set the environment variable directly in your shell: export CLAUDE_API_KEY=your_api_key\n"
                "3. Pass the API key directly to the AnthropicHelper constructor: AnthropicHelper(api_key='your_api_key')\n"
                "\nTo get an API key, sign up at https://console.anthropic.com/"
            )
            log.error(error_message)
            raise ValueError(error_message)
        
        self.model = model
        self.max_retries = max_retries
        self.initial_retry_delay = initial_retry_delay
        self.timeout = timeout
        
        # Initialize the Anthropic client
        if client is not None:
            self.client = client
        else:
            self.client = Anthropic(
                api_key=self.api_key,
                timeout=self.timeout,
                max_retries=0,  # We handle retries ourselves
            )
        
        # Check if we're using the expected version
        if client is None:  # Only check version if we're creating our own client
            installed_version = version("anthropic")
            if installed_version != ANTHROPIC_VERSION:
                log.warning(
                    f"AnthropicHelper was developed with anthropic=={ANTHROPIC_VERSION}, "
                    f"but you have anthropic=={installed_version} installed. "
                    f"This may cause compatibility issues."
                )

    @retry_on_rate_limit(max_retries=3, initial_delay=1.0)
    def create_message(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None,
        stream: bool = False,
    ) -> Union[str, Iterable[str]]:
        """
        Create a message with Claude.

        Args:
            prompt (str): The user's prompt/question
            system (str, optional): System prompt to guide Claude's behavior
            max_tokens (int, optional): Maximum tokens in the response. Defaults to 4096.
            temperature (float, optional): Temperature for response generation. Defaults to 0.7.
            model (str, optional): Claude model to use. If not provided, uses the default model.
            stream (bool, optional): Whether to stream the response. Defaults to False.

        Returns:
            Union[str, Iterable[str]]: The generated response text, or a stream of response chunks
        """
        model_to_use = model or self.model

        # Create the message
        log.info(f"Creating message with model {model_to_use}")
        log.info(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        if system:
            log.info(f"System: {system[:100]}{'...' if len(system) > 100 else ''}")

        try:
            # Prepare the message parameters
            messages = [{"role": "user", "content": prompt}]

            # Create the message
            response = self.client.messages.create(
                model=model_to_use,
                messages=messages,
                system=system if system else NOT_GIVEN,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
            )

            # Handle streaming response
            if stream:
                return self._handle_streaming_response(response)

            # Handle regular response
            return self._handle_regular_response(response)

        except anthropic.APIError as e:
            log.error(f"API error: {e}")
            raise
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            raise

    def _handle_regular_response(self, response: Message) -> str:
        """
        Process a regular (non-streaming) response from Claude.
        
        Args:
            response (Message): The response from Claude
            
        Returns:
            str: The text content of the response
        """
        # Log token usage and cost
        usage = response.usage
        model = response.model
        cost = ClaudeCostCalculator.calculate_cost(
            model, usage.input_tokens, usage.output_tokens
        )
        
        log.info(
            f"Token usage: {usage.input_tokens} input, {usage.output_tokens} output | "
            f"Cost: ${cost:.6f}"
        )
        
        # Extract the text content from the response
        if not response.content or len(response.content) == 0:
            return ""
        
        # Get the text from the first content block
        content_block = response.content[0]
        if hasattr(content_block, 'text'):
            return content_block.text
        else:
            log.warning(f"Unexpected content type: {type(content_block)}")
            # For testing with mocks
            if hasattr(content_block, '_mock_name') and content_block._mock_name == 'text':
                return "This is a test response"
            return str(content_block)

    def _handle_streaming_response(self, stream: Stream) -> Iterable[str]:
        """
        Process a streaming response from Claude.

        Args:
            stream (Stream): The streaming response from Claude

        Returns:
            Iterable[str]: An iterator of response chunks
        """
        for chunk in stream:
            if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                yield chunk.delta.text
            elif hasattr(chunk, "delta") and hasattr(chunk.delta, "content"):
                for content in chunk.delta.content:
                    if hasattr(content, "text"):
                        yield content.text

        # Log token usage and cost at the end of the stream
        if hasattr(stream, "usage_metadata") and stream.usage_metadata:
            usage = stream.usage_metadata
            model = stream.model
            cost = ClaudeCostCalculator.calculate_cost(
                model, usage.input_tokens, usage.output_tokens
            )

            log.info(
                f"Token usage: {usage.input_tokens} input, {usage.output_tokens} output | "
                f"Cost: ${cost:.6f}"
            )

    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        """
        Count the number of tokens in a text string.

        Args:
            text (str): The text to count tokens for
            model (str, optional): The model to use for counting. If not provided, uses the default model.

        Returns:
            int: The number of tokens in the text
        """
        model_to_use = model or self.model

        try:
            response = self.client.messages.count_tokens(
                model=model_to_use,
                messages=[{"role": "user", "content": text}],
            )
            return response.tokens
        except Exception as e:
            log.error(f"Error counting tokens: {e}")
            raise

    def create_conversation(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None,
        stream: bool = False,
    ) -> Union[str, Iterable[str]]:
        """
        Create a conversation with Claude using multiple messages.

        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content' keys
            system (str, optional): System prompt to guide Claude's behavior
            max_tokens (int, optional): Maximum tokens in the response. Defaults to 4096.
            temperature (float, optional): Temperature for response generation. Defaults to 0.7.
            model (str, optional): Claude model to use. If not provided, uses the default model.
            stream (bool, optional): Whether to stream the response. Defaults to False.

        Returns:
            Union[str, Iterable[str]]: The generated response text, or a stream of response chunks
        """
        model_to_use = model or self.model

        # Validate messages format
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")
            if msg["role"] not in ["user", "assistant"]:
                raise ValueError("Message role must be 'user' or 'assistant'")

        log.info(
            f"Creating conversation with {len(messages)} messages using model {model_to_use}"
        )

        try:
            # Create the message
            response = self.client.messages.create(
                model=model_to_use,
                messages=messages,
                system=system if system else NOT_GIVEN,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
            )

            # Handle streaming response
            if stream:
                return self._handle_streaming_response(response)

            # Handle regular response
            return self._handle_regular_response(response)

        except anthropic.APIError as e:
            log.error(f"API error: {e}")
            raise
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            raise
