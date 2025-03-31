"""
Streaming functionality for structured completions.

This module provides functions for streaming structured chat completions
using the OpenAI API, with Pydantic model parsing support.
"""

from typing import List, Optional, Dict, Union, Iterable, Type, Generator, Tuple
from openai.types.chat import (
    ParsedChatCompletion,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from openai._types import NotGiven, NOT_GIVEN
from openai._streaming import Stream

from cws_helpers.logger import configure_logging

log = configure_logging(__name__)

# Import from our own modules
from ....utils.model_utils import get_token_param_name, filter_unsupported_parameters
from ....types.response_types import ResponseFormatT


def stream_structured_completion(
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
) -> Generator[Tuple[ParsedChatCompletion[ResponseFormatT], bool], None, None]:
    """
    Stream a structured chat completion using the OpenAI API.
    This method provides enhanced support for Pydantic models with automatic parsing.

    Parameters
    ----------
    messages : List[ChatCompletionMessageParam]
        List of message objects to send to the API
    model : str
        ID of the model to use
    response_format : Type[ResponseFormatT]
        A Pydantic model class that defines the structure of the response
    frequency_penalty : Optional[float]
        Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency
    logit_bias : Optional[Dict[str, int]]
        Modify the likelihood of specified tokens appearing in the completion
    logprobs : Optional[bool]
        Whether to return log probabilities of the output tokens
    max_tokens : Optional[int]
        Maximum number of tokens that can be generated (not supported by o-series models)
    max_completion_tokens : Optional[int]
        Maximum number of tokens to generate (required for o-series models)
    n : Optional[int]
        Number of chat completion choices to generate
    presence_penalty : Optional[float]
        Number between -2.0 and 2.0. Positive values penalize new tokens based on presence
    seed : Optional[int]
        If specified, system will make best effort to sample deterministically
    stop : Union[Optional[str], List[str]]
        Up to 4 sequences where the API will stop generating further tokens
    temperature : Optional[float]
        What sampling temperature to use, between 0 and 2
    tool_choice : ChatCompletionToolChoiceOptionParam
        Controls which (if any) function is called by the model
    tools : Iterable[ChatCompletionToolParam]
        List of tools the model may call
    top_logprobs : Optional[int]
        Number of most likely tokens to return at each position (0-20)
    top_p : Optional[float]
        Alternative to sampling with temperature, called nucleus sampling
    user : str
        Unique identifier representing your end-user

    Returns
    -------
    Generator[Tuple[ParsedChatCompletion[ResponseFormatT], bool], None, None]
        A generator that yields tuples of (parsed_completion, is_final).
        is_final is True for the final complete response, False for incremental updates.
    """
    log.debug("stream_structured_completion")

    # Determine which token parameter to use based on the model
    token_param_name = get_token_param_name(model)
    tokens_value = (
        max_completion_tokens
        if token_param_name == "max_completion_tokens"
        and max_completion_tokens is not None
        else max_tokens
    )
    log.debug(f"Using {token_param_name}={tokens_value} for model: {model}")

    # Prepare parameters for the stream endpoint
    stream_params = {
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
    stream_params = {k: v for k, v in stream_params.items() if v is not None}

    # Filter out NotGiven values
    stream_params = {k: v for k, v in stream_params.items() if v is not NOT_GIVEN}

    # Filter out unsupported parameters
    stream_params = filter_unsupported_parameters(stream_params, model)

    log.debug("Starting structured completion stream")

    try:
        # Call the beta stream endpoint
        with self.client.beta.chat.completions.stream(**stream_params) as stream:
            # Process the stream and yield parsed completions
            for event in stream:
                if event.type == "content.delta" and event.parsed is not None:
                    yield event.parsed, False
                elif event.type == "content.done":
                    # Get the final complete response
                    final_completion = stream.get_final_completion()
                    yield final_completion, True
                elif event.type == "error":
                    log.error("Stream error: %s", event.error)
                    raise Exception(f"Stream error: {event.error}")
                
    except Exception as e:
        # Log the error
        log.error(f"Error in stream: {e}")

        # Check if the error is related to max_tokens vs max_completion_tokens
        error_str = str(e)
        if "max_tokens" in error_str and "max_completion_tokens" in error_str:
            log.warning(
                "Detected error related to token parameter. Attempting to fix..."
            )

            # Swap the token parameter
            other_param = (
                "max_completion_tokens"
                if token_param_name == "max_tokens"
                else "max_tokens"
            )
            if token_param_name in stream_params:
                tokens_value = stream_params.pop(token_param_name)
                stream_params[other_param] = tokens_value
                log.debug(f"Retrying stream with {other_param}={tokens_value}")
                
                # Retry with the fixed parameters
                with self.client.beta.chat.completions.stream(**stream_params) as stream:
                    for event in stream:
                        if event.type == "content.delta" and event.parsed is not None:
                            yield event.parsed, False
                        elif event.type == "content.done":
                            # Get the final complete response
                            final_completion = stream.get_final_completion()
                            yield final_completion, True
                        elif event.type == "error":
                            log.error("Stream error: %s", event.error)
                            raise Exception(f"Stream error: {event.error}")

        # Re-raise the error
        raise
