# OpenAI Helper

A modular Python package for interacting with OpenAI's API, providing a simplified interface with support for:

- Text completions
- Image inputs (multimodal)
- JSON mode
- Structured outputs
- Streaming responses
- Automatic parsing of responses into Pydantic models

## Module Structure

The module is organized into the following directories:

```
openai_helper/
├── __init__.py              # Main entry point
├── core/                    # Core functionality
│   ├── __init__.py          # Exports core components
│   ├── base.py              # Base OpenAIHelper class
│   ├── chat/                # Chat completion functionality
│   │   ├── generic/         # Generic chat completion handlers
│   │   │   ├── __init__.py
│   │   │   ├── error_handlers.py # Error handling for chat completions
│   │   │   ├── generic_completion.py # Core chat completion implementation
│   │   │   └── mixin.py     # Generic chat completion mixin
│   │   └── structured/      # Structured output chat completion
│   │       ├── __init__.py
│   │       ├── mixin.py     # Structured completion functionality
│   │       ├── streaming.py # Streaming structured outputs
│   │       └── structured_completion.py # Core structured completion
│   ├── messages/            # Message handling
│   │   ├── __init__.py
│   │   ├── mixin.py         # Message creation mixin
│   │   └── utils.py         # Message utility functions
│   └── responses/           # Response processing
├── enums/                   # Enumerations
│   ├── __init__.py          # Exports all enums
│   ├── ai_models.py         # AIModel enum with model capabilities
│   ├── ai_providers.py      # AIProvider enum for provider identification
│   └── model_features.py    # Collections of model-specific features
├── types/                   # Type definitions
│   ├── __init__.py
│   └── response_types.py    # Response type definitions
└── utils/                   # Utility functions
    ├── __init__.py
    ├── image.py             # Image handling utilities
    └── model_utils.py       # Model-specific utilities
```

## Usage Examples

### Basic Usage

```python
from cws_helpers.openai_helper import OpenAIHelper

# Initialize the helper
helper = OpenAIHelper(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages
prompt = "Tell me a joke about programming."
messages = helper.create_messages(prompt=prompt)

# Simple text completion
response = helper.create_chat_completion(
    messages=messages,
    model="gpt-4o"
)

print(response)
```

### Working with Images (Multimodal)

```python
from cws_helpers.openai_helper import OpenAIHelper

# Initialize the helper
helper = OpenAIHelper(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages with image - path will be automatically encoded
prompt = "What's in this image?"
image_path = "path/to/your/image.jpg"
messages = helper.create_messages(prompt=prompt, images=[image_path])

# URL images can also be used directly
url_image = "https://example.com/image.jpg"
messages_with_url = helper.create_messages(prompt=prompt, images=[url_image])

# Multimodal input with image
response = helper.create_chat_completion(
    messages=messages,
    model="gpt-4o"
)

print(response)
```

### Using JSON Mode

```python
from cws_helpers.openai_helper import OpenAIHelper

# Initialize the helper
helper = OpenAIHelper(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages
prompt = """Generate a list of 3 programming languages with their creator and year. 
Return the response as a JSON object with the following structure:
{
    "languages": [
        {
            "name": "Programming Language Name",
            "creator": "Creator Name",
            "year": 1970
        },
        ...
    ]
}"""
messages = helper.create_messages(prompt=prompt)

# Get response in JSON format
response = helper.create_chat_completion(
    messages=messages,
    model="gpt-4o",
    json_mode=True
)

# response is a Python dictionary
for language in response["languages"]:
    print(f"{language['name']} - {language['creator']} ({language['year']})")
```

### Structured Outputs with Pydantic

```python
from pydantic import BaseModel
from typing import List
from cws_helpers.openai_helper import OpenAIHelper

# Define your response structure
class ProgrammingLanguage(BaseModel):
    name: str
    creator: str
    year: int

class LanguagesResponse(BaseModel):
    languages: List[ProgrammingLanguage]

# Initialize the helper
helper = OpenAIHelper(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages for the conversation
system_message = "You are a programming historian."
prompt = "List 3 programming languages with their creator and year."
messages = helper.create_messages(prompt=prompt, system_message=system_message)

# Get a structured response
response = helper.create_structured_chat_completion(
    messages=messages,
    model="gpt-4o",
    response_format=LanguagesResponse
)

# Work with the typed response
for language in response.parsed_model.languages:
    print(f"{language.name} - {language.creator} ({language.year})")
```

### Using Stream Mode

```python
from cws_helpers.openai_helper import OpenAIHelper

# Initialize the helper
helper = OpenAIHelper(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages
prompt = "Write a short story about AI."
messages = helper.create_messages(prompt=prompt)

# Stream the response
stream = helper.create_chat_completion(
    messages=messages,
    model="gpt-4o",
    stream=True
)

# Process the streaming response
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Structured Outputs with Pydantic Models

```python
from typing import List
from pydantic import BaseModel
from cws_helpers.openai_helper import OpenAIHelper

# Define your response structure with steps
class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str

class MathResponseWithExplanation(MathResponse):
    explanation: str

# Initialize the helper
helper = OpenAIHelper(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages
system_message = "You are a helpful math tutor."
prompt = "solve 8x + 31 = 2"
messages = helper.create_messages(prompt=prompt, system_message=system_message)

# Get structured response
response = helper.create_structured_chat_completion(
    messages=messages,
    model="gpt-4o",
    response_format=MathResponseWithExplanation
)

# Access the structured data
steps = response.parsed_model.steps
for i, step in enumerate(steps, 1):
    print(f"Step {i}: {step.explanation}")
    print(f"Result: {step.output}")
    
print(f"Final answer: {response.parsed_model.final_answer}")
print(f"Explanation: {response.parsed_model.explanation}")
```

### Streaming Structured Outputs

```python
from pydantic import BaseModel
from typing import List
from cws_helpers.openai_helper import OpenAIHelper

# Define the response format using Pydantic
class EntityExtraction(BaseModel):
    attributes: List[str]
    colors: List[str]
    animals: List[str]

# Initialize the helper
helper = OpenAIHelper(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages
system_message = "Extract entities from the input text"
prompt = "The quick brown fox jumps over the lazy dog with piercing blue eyes"
messages = helper.create_messages(prompt=prompt, system_message=system_message)

# Stream the structured completion
print("\nStreaming response:")
for parsed_data, is_final in helper.stream_structured_completion(
    messages=messages,
    model="gpt-4o-mini",
    response_format=EntityExtraction,
    temperature=0.7,
):
    if is_final:
        print("\nFinal completion:")
        print(parsed_data)
    else:
        print(parsed_data)
```

## Using AIModel for Model-Specific Logic

```python
from cws_helpers.openai_helper import AIModel, AIProvider

# Check if a model supports structured outputs
supports_structured = AIModel.supports_structured_outputs("gpt-4o")
print(f"Does gpt-4o support structured outputs? {supports_structured}")

# Get the appropriate token parameter name for a model
token_param = AIModel.get_token_param_name("o3-mini")
print(f"Token parameter for o3-mini: {token_param}")  # Returns "max_completion_tokens"

# Get the provider for a model
provider = AIModel.get_provider("gpt-4")
print(f"Provider for gpt-4: {provider}")  # Returns AIProvider.OPENAI

# Get unsupported parameters for a model
unsupported = AIModel.get_unsupported_parameters("o1-mini")
print(f"Unsupported parameters for o1-mini: {unsupported}")
```

## Compatibility

This module was developed and tested with OpenAI Python SDK version 1.68.2. If you encounter issues with other versions, you can silence the compatibility warning by setting the environment variable:

```
MUTE_OPENAI_HELPER_WARNING=True
```

## Development

To contribute to this module, please follow the modular structure. Each file should have:

1. Comprehensive docstrings
2. Type annotations
3. Proper error handling
4. Logging for important operations

When adding new functionality, consider which module it belongs in:
- `core`: For main functionality that users will interact with directly
- `utils`: For helper functions and utilities
- `types`: For type definitions and parsing logic
- `enums`: For enumeration types and constants