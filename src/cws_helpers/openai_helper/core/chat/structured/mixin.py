"""
Mixin for structured completion functionality in OpenAIHelper.
"""

from typing import List, TypeVar, Type, Any, ContextManager, Optional, Dict, Union, Iterable, Generator, Tuple
from openai.types.chat import ChatCompletionMessageParam, ParsedChatCompletion, ChatCompletionToolChoiceOptionParam, ChatCompletionToolParam
from openai._streaming import Stream
from pydantic import BaseModel
from openai._types import NotGiven, NOT_GIVEN

# Define a type variable for response format types
ResponseFormatT = TypeVar('ResponseFormatT', bound=BaseModel)


class StructuredCompletionMixin:
    """
    Mixin providing structured completion functionality for OpenAIHelper.
    """

    def create_structured_chat_completion(
        self,
        messages: List[ChatCompletionMessageParam],
        model: str,
        response_format: Type[ResponseFormatT],
        **kwargs: Any
    ) -> ParsedChatCompletion[ResponseFormatT]:
        """
        Creates a structured chat completion using the beta.chat.completions.parse endpoint.
        This method provides enhanced support for Pydantic models with automatic parsing.

        Parameters
        ----------
        messages : List[ChatCompletionMessageParam]
            List of message objects to send to the API
        model : str
            ID of the model to use
        response_format : Type[ResponseFormatT]
            A Pydantic model class that defines the structure of the response
        **kwargs : Any
            Additional parameters to pass to the API

        Returns
        -------
        ParsedChatCompletion[ResponseFormatT]
            A ParsedChatCompletion object containing the structured response.
            The parsed data can be accessed via completion.choices[0].message.parsed
        """
        from .structured_completion import create_structured_chat_completion as create_structured_chat_completion_impl
        return create_structured_chat_completion_impl(self, messages, model, response_format, **kwargs)

    def stream_structured_completion(
        self,
        messages: List[ChatCompletionMessageParam],
        model: str,
        response_format: Type[ResponseFormatT],
        **kwargs: Any
    ) -> ContextManager[Stream[ParsedChatCompletion[ResponseFormatT]]]:
        """
        Stream a structured chat completion using the beta.chat.completions.parse endpoint.
        This method provides enhanced support for Pydantic models with automatic parsing.

        Parameters
        ----------
        messages : List[ChatCompletionMessageParam]
            List of message objects to send to the API
        model : str
            ID of the model to use
        response_format : Type[ResponseFormatT]
            A Pydantic model class that defines the structure of the response
        **kwargs : Any
            Additional parameters to pass to the API

        Returns
        -------
        ContextManager[Stream[ParsedChatCompletion[ResponseFormatT]]]
            A context manager that yields a stream of parsed completions

        Example
        -------
        >>> with helper.stream_structured_completion(
        ...     messages=messages,
        ...     model="gpt-4o",
        ...     response_format=MyModel
        ... ) as stream:
        ...     for event in stream:
        ...         if event.type == "content.delta":
        ...             if event.parsed is not None:
        ...                 print("content.delta parsed:", event.parsed)
        ...         elif event.type == "content.done":
        ...             print("content.done")
        ...         elif event.type == "error":
        ...             print("Error in stream:", event.error)
        ...
        >>> final_completion = stream.get_final_completion()
        """
        from .streaming import stream_structured_completion as stream_structured_completion_impl
        return stream_structured_completion_impl(self, messages, model, response_format, **kwargs)
