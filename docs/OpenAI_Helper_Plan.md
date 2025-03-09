# Open AI Helper Plan

## Code
```python
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ------------------ Configure Logging (USE THE LOGGER IN THIS PROJECT) ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# ------------------ Imports ------------------ #
from importlib.metadata import version

if os.getenv("OPENAI_HELPER_PACKAGE_TEST", "False").lower() in ("true", "1", "t"):
    log.info("Running in test mode.")

import json
from openai import OpenAI
from typing import List, Optional, Annotated, Dict, Any, Union, Iterable, Type
import base64
from openai.types.chat_model import ChatModel
from openai.types.chat.completion_create_params import ResponseFormat
from openai.types.chat.chat_completion_tool_choice_option_param import (
    ChatCompletionToolChoiceOptionParam,
)
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_content_part_param import (
    ChatCompletionContentPartParam,
)
from openai.types.chat.chat_completion_content_part_text_param import (
    ChatCompletionContentPartTextParam,
)
from openai.types.chat.chat_completion_content_part_image_param import (
    ChatCompletionContentPartImageParam,
    ImageURL,
)
from openai._types import NotGiven, NOT_GIVEN
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion_modality import ChatCompletionModality
from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from pydantic import BaseModel
from openai._streaming import Stream

OPENAI_VERSION = "1.65.4"


class OpenAIHelper:
    """
    A helper class for interacting with the OpenAI API.
    Provides methods for creating chat completions with support for:
    - Basic text responses
    - Image inputs
    - JSON mode
    - Structured outputs using JSON schema
    - Pydantic model parsing
    """

    def __init__(
        self,
        api_key: Annotated[str, "The OpenAI API Key you wish to use"],
        organization: str,
    ):
        self.client = OpenAI(api_key=api_key, organization=organization)
        self.check_dependency_versions()

    def check_dependency_versions(self):
        current_openai_version = version("openai")
        # Check if the warning should be muted
        mute_warning = os.getenv("MUTE_OPENAI_HELPER_WARNING", "False").lower() in (
            "true",
            "1",
            "t",
        )

        if not mute_warning and current_openai_version != OPENAI_VERSION:
            log.warning(
                f"The 'OpenAIHelper' tool was created using openai version {OPENAI_VERSION}. The version you have installed in this project ({current_openai_version}) may not be compatible with this tool. If you encounter any issues, either downgrade your OpenAI version to{OPENAI_VERSION} or email the creator at caseywschmid@gmail.com to have the package updated."
            )
            log.info(
                "This warning can be muted by setting the MUTE_OPENAI_HELPER_WARNING environment variable to 'True'."
            )

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
        model: Union[str, ChatModel] = "gpt-4-turbo-preview",
        stream: bool = False,
        json_mode: bool = False,
        max_tokens: Optional[int] | None = 4096,
        temperature: Optional[float] | None = 0.7,
        n: Optional[int] | None = 1,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: Union[ResponseFormat, Dict[str, Any], Type[BaseModel], NotGiven] = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        stream_options: Optional[ChatCompletionStreamOptionsParam] = None,
        modality: Optional[ChatCompletionModality] = None,
    ) -> Union[Dict[str, Any], str, ChatCompletion, Stream[ChatCompletionChunk]]:
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
          [Example Python
          code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
          for counting tokens.

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

        timeout: Override the client-level default timeout for this request,
          in seconds

        stream_options: Optional configuration for streaming responses
        modality: Optional modality configuration for multi-modal models

        Returns
        -------
        dict or str
            The response from the OpenAI API. Returns a dictionary if json_mode
            is True, otherwise returns a string.
        """
        log.fine("[OpenAIHelper] create_chat_completion")

        # Handle response format
        if isinstance(response_format, type) and issubclass(response_format, BaseModel):
            # Convert Pydantic model to JSON schema
            schema = response_format.model_json_schema()
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": schema.get("title", "response"),
                    "schema": schema,
                    "strict": True
                }
            }
        elif json_mode:
            response_format = {"type": "json_object"}

        # Create the messages
        messages: List[ChatCompletionMessageParam] = []
        if system_message:
            system_message_param = ChatCompletionSystemMessageParam(
                role="system", content=system_message
            )
            messages.append(system_message_param)

        user_message_content: List[ChatCompletionContentPartParam] = []

        text_param: ChatCompletionContentPartTextParam = {
            "type": "text",
            "text": prompt,
        }

        user_message_content.append(text_param)

        if images:
            for image in images:
                # perform a check to see if the image is a local file path or a url
                # urls lool like this: "https://edugatherer-images.s3.amazonaws.com/MATH/agile_mind/item_01597/test_1597_1.gif"
                if image.startswith("http"):
                    image_url: ImageURL = {
                        "url": image,
                        # Optionally specify "detail" if needed, e.g., "detail": "high"
                    }
                    image_param: ChatCompletionContentPartImageParam = {
                        "type": "image_url",
                        "image_url": image_url,
                    }
                    user_message_content.append(image_param)
                else:
                    if not os.path.exists(image):
                        log.error(f"Image file not found: {image}")
                        continue
                    image_base64 = self.encode_image(image)
                    image_url: ImageURL = {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                        # Optionally specify "detail" if needed, e.g., "detail": "high"
                    }
                    image_param: ChatCompletionContentPartImageParam = {
                        "type": "image_url",
                        "image_url": image_url,
                    }
                    user_message_content.append(image_param)
        else:
            log.info("[OpenAIHelper] No images")

        # Create the user message
        user_message_param: ChatCompletionUserMessageParam = {
            "role": "user",
            "content": user_message_content,
        }

        messages.append(user_message_param)

        completion_params = {
            "messages": messages,
            "model": model,
            "stream": stream,
            "frequency_penalty": frequency_penalty,
            "logit_bias": logit_bias,
            "logprobs": logprobs,
            "max_tokens": max_tokens,
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
        }

        # Filter out None values
        completion_params = {
            k: v for k, v in completion_params.items() if v is not None
        }

        # Filter out NotGiven values and potentially problematic parameters for debugging
        completion_params = {
            k: v for k, v in completion_params.items() if v is not NOT_GIVEN
        }

        log.info("[OpenAIHelper] Sending completion request to OpenAI API")

        response: Any = self.client.chat.completions.create(**completion_params)

        # Handle streaming responses
        if stream:
            return response
        
        content = response.choices[0].message.content
        if isinstance(response_format, dict) and response_format.get("type") == "json_schema":
            # Parse response according to schema if using structured output
            try:
                content = json.loads(content)
            except json.JSONDecodeError as e:
                log.error(f"Failed to decode JSON response: {e}")
                log.error(f"Response: {content}")
                raise e

        return content

    @staticmethod
    def encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

```

## Implementation Plan for Adding OpenAI Helper to cws-helpers

### 1. Project Structure Changes

Create the necessary directory structure for the OpenAI helper:

```bash
mkdir -p src/cws_helpers/openai_helper
mkdir -p tests/openai_helper
touch src/cws_helpers/openai_helper/__init__.py
touch src/cws_helpers/openai_helper/openai_helper.py
touch tests/openai_helper/__init__.py
touch tests/openai_helper/test_openai_helper.py
```

### 2. Dependencies

The OpenAI helper requires the following dependencies:
- `openai==1.65.4` (specific version required)
- `pydantic` (for model schema support)

Add these dependencies to the project using Poetry:

```bash
poetry add openai==1.65.4 pydantic
```

This will update the `pyproject.toml` file with the new dependencies.

### 3. Implementation

#### 3.1 Main Helper Implementation

Move the OpenAI helper code from the plan to `src/cws_helpers/openai_helper/openai_helper.py` with the following modifications:

1. Remove the path manipulation code at the top:
```python
# Remove these lines
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
```

2. Update the import for the logger:
```python
# Change from
from cws_helpers.logger import configure_logging
# To
from ...logger import configure_logging
```

3. Add comprehensive docstrings and comments as per the project requirements.

#### 3.2 Module `__init__.py`

In `src/cws_helpers/openai_helper/__init__.py`, add:

```python
"""
OpenAI Helper module for interacting with OpenAI's API.

This module provides a simplified interface for making requests to OpenAI's API,
with support for text completions, image inputs, JSON mode, structured outputs,
and streaming responses.
"""

from .openai_helper import OpenAIHelper

__all__ = ["OpenAIHelper"]
```

#### 3.3 Update Main Package `__init__.py`

Update `src/cws_helpers/__init__.py` to include the OpenAI helper:

```python
"""CWS Helpers - Collection of utility helpers for personal projects."""

__version__ = "0.1.1"  # Increment version for new feature

# For convenient imports
from .logger import configure_logging
from .openai_helper import OpenAIHelper
```

### 4. Testing

Create tests in `tests/openai_helper/test_openai_helper.py`:

```python
import os
import pytest
from unittest.mock import patch, MagicMock
from cws_helpers.openai_helper import OpenAIHelper

# Mock OpenAI API responses
@pytest.fixture
def mock_openai_response():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    return mock_response

# Test initialization
def test_init():
    with patch('openai.OpenAI') as mock_openai:
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        mock_openai.assert_called_once_with(api_key="test_key", organization="test_org")

# Test basic chat completion
def test_create_chat_completion(mock_openai_response):
    with patch('openai.OpenAI') as mock_openai:
        mock_instance = mock_openai.return_value
        mock_instance.chat.completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(prompt="Hello")
        
        assert response == "Test response"
        mock_instance.chat.completions.create.assert_called_once()

# Test JSON mode
def test_json_mode(mock_openai_response):
    with patch('openai.OpenAI') as mock_openai:
        mock_instance = mock_openai.return_value
        mock_openai_response.choices[0].message.content = '{"result": "success"}'
        mock_instance.chat.completions.create.return_value = mock_openai_response
        
        helper = OpenAIHelper(api_key="test_key", organization="test_org")
        response = helper.create_chat_completion(prompt="Hello", json_mode=True)
        
        assert response == '{"result": "success"}'
        # Verify response_format was set correctly
        call_args = mock_instance.chat.completions.create.call_args[1]
        assert call_args["response_format"] == {"type": "json_object"}

# Test image encoding
def test_encode_image(tmp_path):
    # Create a test image file
    test_image = tmp_path / "test.jpg"
    test_image.write_bytes(b"test image content")
    
    encoded = OpenAIHelper.encode_image(str(test_image))
    assert isinstance(encoded, str)
    assert len(encoded) > 0
```

### 5. Documentation

Create a documentation file in `docs/OpenAI_Helper_Docs.md`:

```markdown
# OpenAI Helper

The OpenAI Helper provides a simplified interface for interacting with OpenAI's API, making it easy to create chat completions with various features.

## Installation

```bash
# Install the package
pip install cws-helpers

# Or directly from GitHub
pip install git+https://github.com/caseywschmid/cws-helpers.git
```

## Usage

### Basic Usage

```python
from cws_helpers import OpenAIHelper
import os

# Initialize the helper
helper = OpenAIHelper(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORGANIZATION")
)

# Create a simple chat completion
response = helper.create_chat_completion(
    prompt="What is the capital of France?",
    model="gpt-3.5-turbo"
)

print(response)
```

### Using System Messages

```python
response = helper.create_chat_completion(
    prompt="Write a short poem about AI",
    system_message="You are a helpful assistant that speaks in rhyming verse.",
    model="gpt-4"
)
```

### Including Images

```python
response = helper.create_chat_completion(
    prompt="What's in this image?",
    images=["path/to/image.jpg"],
    model="gpt-4-vision-preview"
)
```

### JSON Mode

```python
response = helper.create_chat_completion(
    prompt="List the top 3 largest countries by area as JSON",
    json_mode=True,
    system_message="Return your response as a JSON array with country name and area in km²"
)
```

### Structured Output with Pydantic

```python
from pydantic import BaseModel
from typing import List

class Country(BaseModel):
    name: str
    capital: str
    population: int

response = helper.create_chat_completion(
    prompt="Give me information about France, Germany, and Italy",
    response_format=List[Country]
)
```

## Environment Variables

- `OPENAI_HELPER_PACKAGE_TEST`: Set to "True" to run in test mode
- `MUTE_OPENAI_HELPER_WARNING`: Set to "True" to mute version compatibility warnings

## API Reference

### `OpenAIHelper`

#### `__init__(api_key: str, organization: str)`

Initializes the OpenAI helper with your API key and organization.

#### `create_chat_completion(...)`

Creates a chat completion using the specified parameters. See method documentation for all available parameters.

#### `encode_image(image_path: str) -> str`

Static method to encode an image file to base64 for API requests.
```

### 6. Update README.md

Add the OpenAI helper to the "Available Packages" section in the main README.md file.

### 7. Update CHANGELOG.md

```markdown
## [0.1.1] - YYYY-MM-DD

### Added
- New helper: openai_helper for interacting with OpenAI's API
- Support for text completions, image inputs, JSON mode, and structured outputs

[0.1.1]: https://github.com/caseywschmid/cws-helpers/compare/v0.1.0...v0.1.1
```

### 8. Potential Issues and Considerations

1. **Version Dependency**: The helper is tied to a specific version of the OpenAI package (1.65.4). This might cause issues if users have different versions installed. The current version check and warning system helps mitigate this.

2. **API Key Management**: Consider adding support for loading API keys from environment variables or a .env file to make it easier for users to manage credentials securely.

3. **Error Handling**: Enhance error handling for API rate limits, network issues, and other common OpenAI API errors.

4. **Streaming Support**: The current implementation returns the stream object directly. Consider adding helper methods to process streaming responses more easily.

5. **Testing Strategy**: Since testing requires actual API calls, consider implementing a comprehensive mocking strategy or integration tests with API keys for CI/CD.

6. **Documentation**: Ensure the documentation includes examples for all major use cases, especially for more complex features like function calling and streaming.

### 9. Implementation Steps

1. Add the dependencies to the project
2. Create the directory structure
3. Implement the OpenAI helper module
4. Write tests
5. Create documentation
6. Update the main package files
7. Update version and changelog
8. Test the implementation
9. Commit and tag the new version