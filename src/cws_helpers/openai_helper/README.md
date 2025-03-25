# OpenAI Helper

The OpenAI Helper provides a simplified interface for interacting with OpenAI's API, making it easy to create chat completions with various features.

## Installation

This helper is included in the cws-helpers package:

```bash
# Install the package
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

### Using AIModel Enum

The OpenAI Helper provides an AIModel enum for model-specific behavior and improved maintainability:

```python
from cws_helpers.openai_helper import OpenAIHelper, AIModel

# Check if a model supports structured outputs
supports_structured = AIModel.supports_structured_outputs(AIModel.GPT_4O)  # True
supports_structured = AIModel.supports_structured_outputs("gpt-4")         # False

# Get the appropriate token parameter name for a model
token_param = AIModel.get_token_param_name(AIModel.O3_MINI)  # Returns "max_completion_tokens"
token_param = AIModel.get_token_param_name("gpt-4")         # Returns "max_tokens"

# Get the provider for a model
provider = AIModel.get_provider(AIModel.GPT_4_TURBO)  # Returns AIProvider.OPENAI

# Use the enum directly in API calls
response = helper.create_chat_completion(
    prompt="What is the capital of France?",
    model=AIModel.GPT_4.value  # Use .value to get the string representation
)
```

The helper automatically handles token parameter selection based on the model used:
- For "o" series models (o1, o3-mini, gpt-4o), it uses `max_completion_tokens`
- For other models, it uses `max_tokens`

If an error occurs due to using the wrong token parameter, the helper will automatically retry with the correct parameter.

### Model-Specific Parameter Compatibility

OpenAI's models have different parameter support. The helper automatically filters unsupported parameters based on the model:

```python
# For o3-mini and o1 models, parameters like temperature and top_p are not supported
# The helper will automatically remove them and log a warning
response = helper.create_chat_completion(
    prompt="What is the capital of France?",
    model="o3-mini",
    temperature=0.7,  # This will be automatically filtered out for o3-mini
    max_completion_tokens=100
)

# You can check which parameters are unsupported for a specific model
unsupported_params = AIModel.get_unsupported_parameters("o3-mini")
print(unsupported_params)  # {'temperature', 'top_p', 'parallel_tool_calls'}

# For other models like gpt-4, all standard parameters are supported
response = helper.create_chat_completion(
    prompt="What is the capital of France?",
    model="gpt-4",
    temperature=0.7,  # This will be included
    max_tokens=100
)
```

Current unsupported parameters for reasoning models (o3-mini, o1, o1-mini):
- `temperature`
- `top_p`
- `parallel_tool_calls`

### Using System Messages

System messages help set the behavior of the assistant. They're useful for providing context or instructions to the model.

```python
response = helper.create_chat_completion(
    prompt="Write a short poem about AI",
    system_message="You are a helpful assistant that speaks in rhyming verse.",
    model="gpt-4"
)
```

### Including Images

The OpenAI Helper supports multimodal models that can process both text and images. You can include images in your requests by providing a list of image paths or URLs.

```python
# Using a local image
response = helper.create_chat_completion(
    prompt="What's in this image?",
    images=["path/to/image.jpg"],
    model="gpt-4-vision-preview"
)

# Using an image URL
response = helper.create_chat_completion(
    prompt="What's in this image?",
    images=["https://example.com/image.jpg"],
    model="gpt-4-vision-preview"
)
```

### JSON Mode

JSON mode guarantees that the model's response will be valid JSON. This is useful when you need structured data from the model.

```python
response = helper.create_chat_completion(
    prompt="List the top 3 largest countries by area as JSON",
    json_mode=True,
    system_message="Return your response as a JSON array with country name and area in km²"
)

# The response will be a string containing valid JSON
import json
countries = json.loads(response)
```

### Structured Output with Pydantic

For more complex structured outputs, you can use Pydantic models to define the schema of the response.

```python
from pydantic import BaseModel
from typing import List

class Country(BaseModel):
    name: str
    capital: str
    population: int

# The response will be automatically parsed into a dictionary matching the model schema
response = helper.create_chat_completion(
    prompt="Give me information about France, Germany, and Italy",
    response_format=List[Country]
)

# Access the structured data
for country in response:
    print(f"{country['name']} has a population of {country['population']}")
```

### Enhanced Structured Output with Beta Parse Endpoint

The OpenAI Helper now supports the beta parse endpoint for even better structured output handling. This provides improved validation and automatic parsing of responses into Pydantic models.

```python
from pydantic import BaseModel
from typing import List

class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str

# The response will be a ParsedChatCompletion object with the parsed data
completion = helper.create_chat_completion(
    prompt="Solve the equation 2x + 5 = 15",
    system_message="You are a helpful math tutor. Provide step-by-step solutions.",
    response_format=MathResponse,
    model="gpt-4o"
)

# Access the parsed data
message = completion.choices[0].message
if message.parsed:
    for step in message.parsed.steps:
        print(f"Step: {step.explanation}")
        print(f"Result: {step.output}")
    print(f"Final answer: {message.parsed.final_answer}")
```

You can disable this feature if needed:

```python
# Use the legacy approach instead of the beta parse endpoint
response = helper.create_chat_completion(
    prompt="Give me information about France",
    response_format=Country,
    use_beta_parse=False  # Disable the beta parse endpoint
)
```

### Streaming Responses

For long responses or real-time applications, you can use streaming to get tokens as they're generated.

```python
stream = helper.create_chat_completion(
    prompt="Write a long story about a space adventure",
    stream=True
)

# Process the stream
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Function/Tool Calling

You can define tools that the model can use to perform actions or retrieve information.

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = helper.create_chat_completion(
    prompt="What's the weather like in New York?",
    tools=tools,
    tool_choice="auto"
)
```

## Environment Variables

- `OPENAI_HELPER_PACKAGE_TEST`: Set to "True" to run in test mode
- `MUTE_OPENAI_HELPER_WARNING`: Set to "True" to mute version compatibility warnings

## API Reference

### `OpenAIHelper`

#### `__init__(api_key: str, organization: str)`

Initializes the OpenAI helper with your API key and organization.

**Parameters:**
- `api_key`: Your OpenAI API key
- `organization`: Your OpenAI organization ID

#### `create_chat_completion(prompt: str, **kwargs)`

Creates a chat completion using the specified parameters.

**Required Parameters:**
- `prompt`: The text prompt to send to the chat completion API.

**Optional Parameters:**
- `images`: A list of local image paths or URLs to include in the request.
- `system_message`: An optional system message to include in the chat completion request.
- `model`: ID of the model to use. Defaults to "gpt-4-turbo-preview".
- `stream`: If True, returns a stream of response chunks instead of a complete response.
- `json_mode`: If True, ensures the response is valid JSON.
- `max_tokens`: The maximum number of tokens to generate. Defaults to 4096.
- `max_completion_tokens`: The maximum number of tokens to generate for "o" series models. If not provided, `max_tokens` is used.
- `temperature`: Controls randomness. Higher values (e.g., 0.8) make output more random, lower values (e.g., 0.2) make it more focused. Defaults to 0.7.
- `response_format`: An object specifying the format that the model must output, or a Pydantic model for structured output.
- `seed`: For deterministic results, provide a seed value.
- `tool_choice`: Controls which (if any) function is called by the model.
- `tools`: A list of tools the model may call.
- `use_beta_parse`: If True and a Pydantic model is provided as response_format, use the beta parse endpoint for better structured output handling. Defaults to True.

**Returns:**
- For regular requests: A string containing the model's response.
- For JSON mode or structured output with legacy approach: A dictionary or structured data.
- For structured output with beta parse endpoint: A ParsedChatCompletion object.
- For streaming: A stream object that yields response chunks.

#### `create_structured_chat_completion(messages: List[ChatCompletionMessageParam], model: str, response_format: Type[ResponseFormatT], **kwargs)`

Creates a structured chat completion using the beta parse endpoint.

**Required Parameters:**
- `messages`: List of message objects to send to the API.
- `model`: ID of the model to use.
- `response_format`: A Pydantic model class that defines the structure of the response.

**Optional Parameters:**
- Same as `create_chat_completion`, with the exception of `prompt`, `system_message`, `images`, and `json_mode`.

**Returns:**
- A ParsedChatCompletion object containing the structured response.

#### `encode_image(image_path: str) -> str`

Static method to encode an image file to base64 for API requests.

**Parameters:**
- `image_path`: Path to the image file

**Returns:**
- Base64-encoded image data as a string

### `AIModel`

Enum representing different AI models supported by the OpenAIHelper.

#### Models

- `GPT_4_5_PREVIEW` - "gpt-4.5-preview"
- `O3_MINI` - "o3-mini"
- `O1` - "o1"
- `O1_MINI` - "o1-mini"
- `GPT_4O` - "gpt-4o"
- `GPT_4O_MINI` - "gpt-4o-mini"
- `GPT_4_TURBO` - "gpt-4-turbo"
- `GPT_4` - "gpt-4"
- `GPT_3_5_TURBO` - "gpt-3.5-turbo"

#### `supports_structured_outputs(model_name: Union[str, AIModel]) -> bool`

Checks if a model supports structured outputs.

**Parameters:**
- `model_name`: Name of the model to check (string or AIModel enum)

**Returns:**
- Boolean indicating if the model supports structured outputs

#### `get_token_param_name(model_name: Union[str, AIModel]) -> str`

Determines which token parameter name to use based on the model.

**Parameters:**
- `model_name`: Name of the model (string or AIModel enum)

**Returns:**
- Either 'max_tokens' or 'max_completion_tokens' depending on the model

#### `get_provider(model_name: Union[str, AIModel]) -> AIProvider`

Gets the provider for a specific model.

**Parameters:**
- `model_name`: The AIModel or model name string to get the provider for

**Returns:**
- The AIProvider for the model

#### `from_string(model_name: str) -> AIModel`

Converts a string representation to an AIModel enum value.

**Parameters:**
- `model_name`: String name of the model

**Returns:**
- AIModel enum value

**Raises:**
- ValueError: If the model name is not recognized

### `AIProvider`

Enum representing different AI providers supported by the system.

#### Providers

- `OPENAI` - OpenAI
- `ANTHROPIC` - Anthropic

#### `from_string(provider_name: str) -> AIProvider`

Converts a string representation to an AIProvider enum value.

**Parameters:**
- `provider_name`: String name of the provider (case-insensitive)

**Returns:**
- AIProvider enum value

**Raises:**
- ValueError: If the provider name is not recognized

## Version Compatibility

This helper is designed to work with OpenAI API version 1.65.5. If you're using a different version, you may see a warning message. You can mute this warning by setting the `MUTE_OPENAI_HELPER_WARNING` environment variable to "True".

The beta parse endpoint requires a newer version of the OpenAI SDK. If your version doesn't support it, the helper will automatically fall back to the legacy approach.

## Error Handling

The helper includes error handling for common issues:
- Missing image files
- JSON parsing errors
- API authentication errors
- Beta parse endpoint availability

## Examples

### Complete Example with Error Handling

```python
import os
from cws_helpers import OpenAIHelper

# Set up API credentials
api_key = os.environ.get("OPENAI_API_KEY")
organization = os.environ.get("OPENAI_ORGANIZATION")

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

try:
    # Initialize the helper
    helper = OpenAIHelper(api_key=api_key, organization=organization)
    
    # Create a chat completion
    response = helper.create_chat_completion(
        prompt="Explain quantum computing in simple terms",
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500
    )
    
    print(response)
    
except Exception as e:
    print(f"Error: {e}")
```

### Advanced Example with Structured Output

```python
from pydantic import BaseModel
from typing import List
from cws_helpers import OpenAIHelper
import os

# Define a Pydantic model for the response
class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    instructions: List[str]
    prep_time_minutes: int
    cook_time_minutes: int

# Initialize the helper
helper = OpenAIHelper(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORGANIZATION")
)

# Get a structured recipe using the beta parse endpoint
completion = helper.create_chat_completion(
    prompt="Give me a recipe for chocolate chip cookies",
    system_message="You are a professional chef. Provide detailed recipes in the requested format.",
    response_format=Recipe,
    temperature=0.3,
    model="gpt-4o"
)

# Access the structured data
message = completion.choices[0].message
if message.parsed:
    recipe = message.parsed
    print(f"Recipe: {recipe.name}")
    print("\nIngredients:")
    for ingredient in recipe.ingredients:
        print(f"- {ingredient}")
    print("\nInstructions:")
    for i, step in enumerate(recipe.instructions, 1):
        print(f"{i}. {step}")
    print(f"\nPrep time: {recipe.prep_time_minutes} minutes")
    print(f"Cook time: {recipe.cook_time_minutes} minutes")
``` 