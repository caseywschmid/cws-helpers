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
from openai.types.chat.completion_create_params import CompletionCreateParams
from openai.types import ResponseFormatJSONObject, ResponseFormatJSONSchema
from openai._types import NotGiven, NOT_GIVEN
from openai._streaming import Stream
from pydantic import BaseModel

# Import AIModel enum if available, with fallback if not
try:
    from .enums.ai_models import AIModel
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

    def create_chat_completion(
        self,
        prompt: str,
        images: Optional[
            Annotated[List[str], "The list of image paths you want to pass in"]
        ] = None,
        system_message: Optional[
            Annotated[
                str,
                "The system message you want to pass in.",
            ]
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
        modality: Optional[ChatCompletionModality] = None,
        use_beta_parse: bool = True,
    ) -> Union[Dict[str, Any], str, ChatCompletion, Stream[ChatCompletionChunk], ParsedChatCompletion]:
        """
        Creates a chat completion using the specified parameters and returns the
        response from the OpenAI API.

        This method supports:
        - Basic text responses
        - Image inputs 
        - JSON mode
        - Structured outputs using JSON schema or Pydantic models
        - Streaming responses
        - Function/tool calling
        - All latest OpenAI API features
        - Beta structured outputs with automatic parsing (when use_beta_parse=True)

        Parameters
        ----------
        prompt: The text prompt to send to the chat completion API.

        images : A list of local image paths. These images will be encoded to
          base64 and included in the chat completion request.

        system_message: An optional system message to include in the chat
          completion request. Defaults to None.

        json_mode : bool, optional If True, the response from the OpenAI API
          will be returned as a JSON object. Defaults to False. If you set this
           to True, you must also tell the LLM to output JSON as its response
           in the prompt or system message.

        model: ID of the model to use. Defaults to "gpt-4-turbo-preview".

        stream: If set, partial message deltas will be sent, like in ChatGPT.
          Tokens will be sent as data-only [server-sent
          events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
          as they become available, with the stream terminated by a `data:
          [DONE]` message. [Example Python
          code](https://cookbook.openai.com/examples/how_to_stream_completions).

        frequency_penalty: Number between -2.0 and 2.0. Positive values
          penalize new tokens based on their existing frequency in the text so
          far, decreasing the model's likelihood to repeat the same line
          verbatim. [See more information about frequency and presence
          penalties.](https://platform.openai.com/docs/guides/text-generation/parameter-details)

        logit_bias: Modify the likelihood of specified tokens appearing in
          the completion. Accepts a JSON object that maps tokens (specified by
          their token ID in the tokenizer) to an associated bias value from
          -100 to 100. Mathematically, the bias is added to the logits
          generated by the model prior to sampling. The exact effect will vary
          per model, but values between -1 and 1 should decrease or increase
          likelihood of selection; values like -100 or 100 should result in a
          ban or exclusive selection of the relevant token.

        logprobs: Whether to return log probabilities of the output tokens or
          not. If true, returns the log probabilities of each output token
          returned in the `content` of `message`.

        max_tokens: The maximum number of [tokens](/tokenizer) that can be
          generated in the chat completion. The total length of input tokens
          and generated tokens is limited by the model's context length.
          Note: This parameter is not supported by the o-series models (o1, o3-mini).
          Use `max_completion_tokens` for those models.
          [Example Python
          code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
          for counting tokens.
          
        max_completion_tokens: The maximum number of tokens to generate in the 
          chat completion. Required for o-series models (o1, o3-mini) that don't
          support max_tokens. For other models, max_tokens will be used if 
          max_completion_tokens is not provided.

        n: How many chat completion choices to generate for each input
          message. Note that you will be charged based on the number of
          generated tokens across all of the choices. Keep `n` as `1` to
          minimize costs.

        presence_penalty: Number between -2.0 and 2.0. Positive values
          penalize new tokens based on whether they appear in the text so far,
          increasing the model's likelihood to talk about new topics. [See more
          information about frequency and presence
          penalties.](https://platform.openai.com/docs/guides/text-generation/parameter-details)

        response_format: An object specifying the format that the model must
          output. Compatible with [GPT-4 Turbo]
          (https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) and
          all GPT-3.5 Turbo models newer than `gpt-3.5-turbo-1106`. Setting to
          `{ "type": "json_object" }` enables JSON mode, which guarantees the
          message the model generates is valid JSON. **Important:** when using
          JSON mode, you **must** also instruct the model to produce JSON
          yourself via a system or user message. Without this, the model may
          generate an unending stream of whitespace until the generation
          reaches the token limit, resulting in a long-running and seemingly
          "stuck" request. Also note that the message content may be partially
          cut off if `finish_reason="length"`, which indicates the generation
          exceeded `max_tokens` or the conversation exceeded the max context
          length.

        seed: This feature is in Beta. If specified, our system will make a
          best effort to sample deterministically, such that repeated requests
          with the same `seed` and parameters should return the same result.
          Determinism is not guaranteed, and you should refer to the
          `system_fingerprint` response parameter to monitor changes in the
          backend.

        stop: Up to 4 sequences where the API will stop generating further
          tokens.

        temperature: What sampling temperature to use, between 0 and 2.
          Higher values like 0.8 will make the output more random, while lower
          values like 0.2 will make it more focused and deterministic. We
          generally recommend altering this or `top_p` but not both.

        tool_choice: Controls which (if any) function is called by the model.
          `none` means the model will not call a function and instead generates
          a message. `auto` means the model can pick between generating a
          message or calling a function. Specifying a particular function via
          `{"type": "function", "function": {"name": "my_function"}}` forces
          the model to call that function. `none` is the default when no
          functions are present. `auto` is the default if functions are
          present.

        tools: A list of tools the model may call. Currently, only functions
          are supported as a tool. Use this to provide a list of functions the
          model may generate JSON inputs for. A max of 128 functions are
          supported.

        top_logprobs: An integer between 0 and 20 specifying the number of
          most likely tokens to return at each token position, each with an
          associated log probability. `logprobs` must be set to `true` if this
          parameter is used.

        top_p: An alternative to sampling with temperature, called nucleus
          sampling, where the model considers the results of the tokens with
          top_p probability mass. So 0.1 means only the tokens comprising the
          top 10% probability mass are considered. We generally recommend
          altering this or `temperature` but not both.

        user: A unique identifier representing your end-user, which can help
          OpenAI to monitor and detect abuse. [Learn
          more](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

        stream_options: Optional configuration for streaming responses
        
        modality: Optional modality configuration for multi-modal models
        
        use_beta_parse: If True and a Pydantic model is provided as response_format,
          use the beta.chat.completions.parse endpoint for better structured output
          handling. Defaults to True.

        Returns
        -------
        dict or str or ParsedChatCompletion
            The response from the OpenAI API. Returns:
            - A dictionary if json_mode is True or a Pydantic model is used with the legacy approach
            - A string for basic text responses
            - A ParsedChatCompletion object if a Pydantic model is used with the beta parse endpoint
            - A Stream object if streaming is enabled
        """
        log.debug("create_chat_completion")

        # Check if we should use the beta parse endpoint for structured outputs
        if (use_beta_parse and 
            isinstance(response_format, type) and 
            issubclass(response_format, BaseModel) and
            hasattr(self.client, 'beta') and
            hasattr(self.client.beta, 'chat') and
            hasattr(self.client.beta.chat, 'completions') and
            hasattr(self.client.beta.chat.completions, 'parse')):
            
            log.debug("Using beta.chat.completions.parse for structured output")
            
            # Create messages for the beta parse endpoint
            messages = self._create_messages(prompt, system_message, images)
            
            try:
                # Call the structured chat completion method
                return self.create_structured_chat_completion(
                    messages=messages,
                    model=model,
                    response_format=response_format,
                    frequency_penalty=frequency_penalty,
                    logit_bias=logit_bias,
                    logprobs=logprobs,
                    max_tokens=max_tokens,
                    max_completion_tokens=max_completion_tokens,
                    n=n,
                    presence_penalty=presence_penalty,
                    seed=seed,
                    stop=stop,
                    temperature=temperature,
                    tool_choice=tool_choice,
                    tools=tools,
                    top_logprobs=top_logprobs,
                    top_p=top_p,
                    user=user,
                )
            except Exception as e:
                log.warning(f"Beta parse endpoint failed: {e}. Falling back to standard endpoint.")
                # Fall back to the standard approach if the beta endpoint fails
                pass

        # Handle response format for standard endpoint
        if isinstance(response_format, type) and issubclass(response_format, BaseModel):
            # Convert Pydantic model to JSON schema
            schema = response_format.model_json_schema()
            response_format = ResponseFormatJSONSchema(
                type="json_schema",
                schema=schema,
            )
        elif json_mode:
            response_format = ResponseFormatJSONObject(type="json_object")

        # Create the messages
        messages = self._create_messages(prompt, system_message, images)

        # Determine which token parameter to use based on the model
        token_param_name = self._get_token_param_name(model)
        tokens_value = max_completion_tokens if token_param_name == "max_completion_tokens" and max_completion_tokens is not None else max_tokens
        log.debug(f"Using {token_param_name}={tokens_value} for model: {model}")

        completion_params = {
            "messages": messages,
            "model": model,
            "stream": stream,
            "frequency_penalty": frequency_penalty,
            "logit_bias": logit_bias,
            "logprobs": logprobs,
            "n": n,
            "presence_penalty": presence_penalty,
            "response_format": response_format,
            "seed": seed,
            "stop": stop,
            "temperature": temperature,
            "tool_choice": tool_choice,
            "tools": tools,
            "top_logprobs": top_logprobs,
            "top_p": top_p,
            "user": user,
            "stream_options": stream_options,
            "modality": modality,
            token_param_name: tokens_value,  # Use the appropriate token parameter
        }

        # Filter out None values
        completion_params = {
            k: v for k, v in completion_params.items() if v is not None
        }

        # Filter out NotGiven values and potentially problematic parameters for debugging
        completion_params = {
            k: v for k, v in completion_params.items() if v is not NOT_GIVEN
        }

        log.debug(f"Sending completion request to OpenAI API with params: {completion_params}")

        try:
            response: Any = self.client.chat.completions.create(**completion_params)
        except Exception as e:
            # Log the error
            log.error(f"Error in OpenAI API call: {e}")
            
            # Check if the error is related to max_tokens vs max_completion_tokens
            error_str = str(e)
            if "max_tokens" in error_str and "max_completion_tokens" in error_str:
                log.warning("Detected error related to token parameter. Attempting to fix...")
                
                # Swap the token parameter
                other_param = "max_completion_tokens" if token_param_name == "max_tokens" else "max_tokens"
                if token_param_name in completion_params:
                    tokens_value = completion_params.pop(token_param_name)
                    completion_params[other_param] = tokens_value
                    log.debug(f"Retrying with {other_param}={tokens_value}")
                    response = self.client.chat.completions.create(**completion_params)
                else:
                    # If neither parameter is in the dictionary, re-raise the error
                    raise
            else:
                # Re-raise the error if it's not related to token parameters
                raise

        # Handle streaming responses
        if stream:
            return response
        
        content = response.choices[0].message.content
        
        # Check if we need to parse JSON response
        # For real ResponseFormatJSONSchema or mocked version in tests
        is_json_schema = False
        if hasattr(response_format, "type") and getattr(response_format, "type", None) == "json_schema":
            is_json_schema = True
        elif hasattr(response_format, "__class__") and hasattr(response_format.__class__, "__name__") and response_format.__class__.__name__ == "ResponseFormatJSONSchema":
            is_json_schema = True
            
        if is_json_schema:
            # Parse response according to schema if using structured output
            try:
                content = json.loads(content)
            except json.JSONDecodeError as e:
                log.error(f"Failed to decode JSON response: {e}")
                log.error(f"Response: {content}")
                raise e

        return content

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
