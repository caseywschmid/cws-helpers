"""
This is the orginal OpenAIHelper class from the OpenAI Helper package.
It has been refactored to use smaller files. 
"""

# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# ------------------ Imports ------------------ #
import os
from importlib.metadata import version

if os.getenv("OPENAI_HELPER_PACKAGE_TEST", "False").lower() in ("true", "1", "t"):
    log.info("Running in test mode.")

import json
from openai import OpenAI
from typing import List, Optional, Annotated, Dict, Any, Union, Iterable, Type, TypeVar, Generic
import base64
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
    ChatCompletionStreamOptionsParam,
    ChatCompletionModality,
)
from openai._types import NotGiven, NOT_GIVEN
from openai._streaming import Stream
from pydantic import BaseModel

# Import AIModel enum if available, with fallback if not
try:
    from ..enums.ai_models import AIModel
    USE_AI_MODEL_ENUM = True
    log.debug("Using AIModel enum for model-specific logic")
except ImportError:
    USE_AI_MODEL_ENUM = False
    log.debug("AIModel enum not available, falling back to hardcoded model checks")

# Import beta chat completions for structured outputs
try:
    from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
except ImportError:
    # Define a fallback for older versions
    class ParsedChatCompletion(ChatCompletion):
        pass

# Define a type variable for response format types
ResponseFormatT = TypeVar('ResponseFormatT')

# The version this helper was developed with
OPENAI_VERSION = "1.68.2"

class OpenAIHelper:
    """
    A helper class for interacting with the OpenAI API.
    Provides methods for creating chat completions with support for:
    - Basic text responses
    - Image inputs
    - JSON mode
    - Structured outputs using JSON schema
    - Pydantic model parsing
    - Beta structured outputs with automatic parsing
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
        self.client = OpenAI(api_key=api_key, organization=organization)
        self.check_dependency_versions()

    def check_dependency_versions(self):
        """
        Check if the installed OpenAI package version is compatible with this helper.
        Logs a warning if the versions aren't compatible.
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
                f"The 'OpenAIHelper' tool was created using openai version {OPENAI_VERSION}. The version you have installed in this project ({current_openai_version}) may not be compatible with this tool. If you encounter any issues, either downgrade your OpenAI version to {OPENAI_VERSION} or email the creator at caseywschmid@gmail.com to have the package updated."
            )
            log.info(
                "This warning can be muted by setting the MUTE_OPENAI_HELPER_WARNING environment variable to 'True'."
            )
            
    def _get_token_param_name(self, model: str) -> str:
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

    def _filter_unsupported_parameters(self, params: Dict[str, Any], model: str) -> Dict[str, Any]:
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
                log.warning(f"Parameter '{param}' is not supported by model '{model}'. Removing it from the request.")
                filtered_params.pop(param)
        
        return filtered_params

    def create_chat_completion(
        self,
        prompt: str,
        images: Optional[
            List[str]
        ] = None,
        system_message: Optional[
            str
        ] = None,
        model: str = "gpt-4-turbo-preview",
        stream: bool = False,
        json_mode: bool = False,
        max_tokens: Optional[int] | None = 4096,
        max_completion_tokens: Optional[int] | None = None,
        temperature: Optional[float] | None = 0.7,
        n: Optional[int] | None = 1,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: Union[Dict[str, Any], Type[BaseModel], NotGiven] = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        stream_options: Optional[ChatCompletionStreamOptionsParam] = None,
        modalities: Optional[List[ChatCompletionModality]] = None,
        use_beta_parse: bool = True,
    ) -> Union[Dict[str, Any], str, ChatCompletion, Stream[ChatCompletionChunk]]:
        """
        Create a chat completion using OpenAI's API.
        
        This method handles various input types and configurations:
        - Simple text prompts
        - Image inputs (multimodal)
        - JSON mode
        - Response format control
        - Stream mode
        - Structured output parsing
        
        Parameters
        ----------
        prompt : str
            The text prompt to send to the model
        images : Optional[List[str]]
            Optional list of image paths to include as multimodal input
        system_message : Optional[str]
            Optional system message to set context for the model
        model : str
            The OpenAI model to use (default: "gpt-4-turbo-preview")
        stream : bool
            Whether to stream the response (default: False)
        json_mode : bool
            Whether to force the model to return valid JSON (default: False)
        max_tokens : Optional[int]
            Maximum tokens in the response for applicable models
        max_completion_tokens : Optional[int]
            Maximum tokens in the response for O-series models
        temperature : Optional[float]
            Controls randomness in the response (default: 0.7)
        n : Optional[int]
            Number of completions to generate (default: 1)
        frequency_penalty : Optional[float]
            Controls repetition penalty (default: NOT_GIVEN)
        logit_bias : Optional[Dict[str, int]]
            Modifies token probabilities (default: NOT_GIVEN)
        logprobs : Optional[bool]
            Whether to return log probabilities (default: NOT_GIVEN)
        presence_penalty : Optional[float]
            Penalty for new tokens (default: NOT_GIVEN)
        response_format : Union[Dict[str, Any], Type[BaseModel], NotGiven]
            Controls response format, can be a Pydantic model for structure
        seed : Optional[int]
            Seed for deterministic outputs (default: NOT_GIVEN)
        stop : Union[Optional[str], List[str]]
            Token(s) to stop generation (default: NOT_GIVEN)
        tool_choice : ChatCompletionToolChoiceOptionParam
            Controls tool selection (default: NOT_GIVEN)
        tools : Iterable[ChatCompletionToolParam]
            Tools to make available (default: NOT_GIVEN)
        top_logprobs : Optional[int]
            Number of most likely tokens to return (default: NOT_GIVEN)
        top_p : Optional[float]
            Controls diversity via nucleus sampling (default: NOT_GIVEN)
        user : str
            User identifier (default: NOT_GIVEN)
        stream_options : Optional[ChatCompletionStreamOptionsParam]
            Additional streaming options (default: None)
        modalities : Optional[List[ChatCompletionModality]]
            Modalities of the input (default: None)
        use_beta_parse : bool
            Whether to use the beta structured output parsing (default: True)
            
        Returns
        -------
        Union[Dict[str, Any], str, ChatCompletion, Stream[ChatCompletionChunk]]
            The model's response in the appropriate format
        """
        from ..core import create_chat_completion
        return create_chat_completion(
            self,
            prompt=prompt,
            images=images,
            system_message=system_message,
            model=model,
            stream=stream,
            json_mode=json_mode,
            max_tokens=max_tokens,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            n=n,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            logprobs=logprobs,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            stop=stop,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            stream_options=stream_options,
            modalities=modalities,
            use_beta_parse=use_beta_parse,
        )

    def create_structured_chat_completion(
        self,
        messages: List[ChatCompletionMessageParam],
        model: str,
        response_format: Type[ResponseFormatT],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | None = 4096,
        max_completion_tokens: Optional[int] | None = None,
        n: Optional[int] | None = 1,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | None = 0.7,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
    ) -> ParsedChatCompletion[ResponseFormatT]:
        """
        Creates a structured chat completion using the beta.chat.completions.parse endpoint.
        This method provides enhanced support for Pydantic models with automatic parsing.
        
        Parameters
        ----------
        messages: List of message objects to send to the API.
        
        model: ID of the model to use.
        
        response_format: A Pydantic model class that defines the structure of the response.
        
        frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens
          based on their existing frequency in the text so far.
          
        logit_bias: Modify the likelihood of specified tokens appearing in the completion.
        
        logprobs: Whether to return log probabilities of the output tokens or not.
        
        max_tokens: The maximum number of tokens that can be generated in the chat completion.
          Note: Not supported by o-series models.
          
        max_completion_tokens: The maximum number of tokens to generate in the chat completion.
          Required for o-series models (o1, o3-mini).
        
        n: How many chat completion choices to generate for each input message.
        
        presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens
          based on whether they appear in the text so far.
          
        seed: If specified, our system will make a best effort to sample deterministically.
        
        stop: Up to 4 sequences where the API will stop generating further tokens.
        
        temperature: What sampling temperature to use, between 0 and 2.
        
        tool_choice: Controls which (if any) function is called by the model.
        
        tools: A list of tools the model may call.
        
        top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens
          to return at each token position.
          
        top_p: An alternative to sampling with temperature, called nucleus sampling.
        
        user: A unique identifier representing your end-user.
        
        Returns
        -------
        ParsedChatCompletion[ResponseFormatT]
            A ParsedChatCompletion object containing the structured response.
            The parsed data can be accessed via completion.choices[0].message.parsed
        """
        log.debug("create_structured_chat_completion")
        
        # Ensure the beta module is available
        if not (hasattr(self.client, 'beta') and 
                hasattr(self.client.beta, 'chat') and 
                hasattr(self.client.beta.chat, 'completions') and
                hasattr(self.client.beta.chat.completions, 'parse')):
            raise ImportError("The beta.chat.completions.parse endpoint is not available in your OpenAI SDK version. "
                             f"Current version: {version('openai')}. Please upgrade to a newer version.")
        
        # Determine which token parameter to use based on the model
        token_param_name = self._get_token_param_name(model)
        tokens_value = max_completion_tokens if token_param_name == "max_completion_tokens" and max_completion_tokens is not None else max_tokens
        log.debug(f"Using {token_param_name}={tokens_value} for model: {model}")
        
        # Prepare parameters for the parse endpoint
        parse_params = {
            "messages": messages,
            "model": model,
            "response_format": response_format,
            "frequency_penalty": frequency_penalty,
            "logit_bias": logit_bias,
            "logprobs": logprobs,
            "n": n,
            "presence_penalty": presence_penalty,
            "seed": seed,
            "stop": stop,
            "temperature": temperature,
            "tool_choice": tool_choice,
            "tools": tools,
            "top_logprobs": top_logprobs,
            "top_p": top_p,
            "user": user,
            token_param_name: tokens_value,  # Use the appropriate token parameter
        }
        
        # Filter out None values
        parse_params = {k: v for k, v in parse_params.items() if v is not None}
        
        # Filter out NotGiven values
        parse_params = {k: v for k, v in parse_params.items() if v is not NOT_GIVEN}
        
        # Filter out unsupported parameters
        parse_params = self._filter_unsupported_parameters(parse_params, model)
        
        log.debug("Sending structured completion request to OpenAI API")
        
        try:
            # Call the parse endpoint
            return self.client.beta.chat.completions.parse(**parse_params)
        except Exception as e:
            # Log the error
            log.error(f"Error in beta parse endpoint: {e}")
            
            # Check if the error is related to max_tokens vs max_completion_tokens
            error_str = str(e)
            if "max_tokens" in error_str and "max_completion_tokens" in error_str:
                log.warning("Detected error related to token parameter in beta parse. Attempting to fix...")
                
                # Swap the token parameter
                other_param = "max_completion_tokens" if token_param_name == "max_tokens" else "max_tokens"
                if token_param_name in parse_params:
                    tokens_value = parse_params.pop(token_param_name)
                    parse_params[other_param] = tokens_value
                    log.debug(f"Retrying beta parse with {other_param}={tokens_value}")
                    return self.client.beta.chat.completions.parse(**parse_params)
            
            # Re-raise the error
            raise

    def _create_messages(
        self, 
        prompt: str, 
        system_message: Optional[str] = None,
        images: Optional[List[str]] = None
    ) -> List[ChatCompletionMessageParam]:
        """
        Helper method to create message objects for the OpenAI API.
        
        Parameters
        ----------
        prompt : str
            The user prompt text
        system_message : Optional[str]
            Optional system message
        images : Optional[List[str]]
            Optional list of image paths or URLs
            
        Returns
        -------
        List[ChatCompletionMessageParam]
            List of message objects ready for the API
        """
        messages: List[ChatCompletionMessageParam] = []
        
        # Add system message if provided
        if system_message:
            system_message_param = ChatCompletionSystemMessageParam(
                role="system", content=system_message
            )
            messages.append(system_message_param)

        # Create user message content
        user_message_content: List[ChatCompletionContentPartParam] = []

        # Add text content
        text_param: ChatCompletionContentPartTextParam = {
            "type": "text",
            "text": prompt,
        }
        user_message_content.append(text_param)

        # Add images if provided
        if images:
            for image in images:
                # Check if the image is a URL or local file path
                if image.startswith("http"):
                    image_param: ChatCompletionContentPartImageParam = {
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                        },
                    }
                    user_message_content.append(image_param)
                else:
                    if not os.path.exists(image):
                        log.error(f"Image file not found: {image}")
                        continue
                    image_base64 = self.encode_image(image)
                    image_param: ChatCompletionContentPartImageParam = {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    }
                    user_message_content.append(image_param)
        
        # Create the user message
        user_message_param: ChatCompletionUserMessageParam = {
            "role": "user",
            "content": user_message_content,
        }
        
        messages.append(user_message_param)
        return messages

    @staticmethod
    def encode_image(image_path: str) -> str:
        """
        Encode an image file to base64 for API requests.
        
        Parameters
        ----------
        image_path : str
            Path to the image file
            
        Returns
        -------
        str
            Base64-encoded image data
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
