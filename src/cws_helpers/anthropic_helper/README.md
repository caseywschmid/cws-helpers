# Anthropic Helper

A helper module for interacting with Anthropic's Claude API. This module provides a simplified interface for making requests to Claude models, with support for text completions, system prompts, streaming responses, and cost calculation.

## Installation

This helper is included in the cws-helpers package:

```bash
pip install git+https://github.com/caseywschmid/cws-helpers.git
```

## API Key Setup

To use the Anthropic Helper, you need an API key from Anthropic. You can get one by signing up at [https://console.anthropic.com/](https://console.anthropic.com/).

There are three ways to provide your API key:

1. **Environment Variable**: Set the `CLAUDE_API_KEY` environment variable in your shell:
   ```bash
   export CLAUDE_API_KEY=your_api_key
   ```

2. **.env File**: Create a `.env` file in your project root with the following content:
   ```
   CLAUDE_API_KEY=your_api_key
   ```
   The helper will automatically load this file when initialized.

3. **Direct Initialization**: Pass the API key directly to the AnthropicHelper constructor:
   ```python
   from cws_helpers.anthropic_helper import AnthropicHelper
   
   helper = AnthropicHelper(api_key="your_api_key")
   ```

## Features

- Simple interface for sending messages to Claude models
- Support for system prompts to guide Claude's behavior
- Conversation history management
- Streaming responses for real-time output
- Automatic token counting
- Cost calculation based on token usage (including prompt caching)
- Automatic retries with exponential backoff for rate limiting
- Comprehensive logging
- Support for all Claude models (3.7, 3.5, 3, and 2 series)
- Automatic loading of API key from .env file

## Usage

### Basic Usage

```python
from cws_helpers.anthropic_helper import AnthropicHelper

# Initialize the helper (API key will be loaded from .env file or environment variable)
helper = AnthropicHelper()

# Send a simple message to Claude
response = helper.create_message("Tell me about artificial intelligence")
print(response)
```

### Using System Prompts

```python
from cws_helpers.anthropic_helper import AnthropicHelper

# Initialize the helper (API key will be loaded from .env file or environment variable)
helper = AnthropicHelper()

# Use a system prompt to guide Claude's behavior
system_prompt = "You are a helpful AI assistant that specializes in explaining complex topics in simple terms."
response = helper.create_message(
    prompt="Explain quantum computing to me",
    system=system_prompt
)
print(response)
```

### Multi-turn Conversations

```python
from cws_helpers.anthropic_helper import AnthropicHelper

# Initialize the helper (API key will be loaded from .env file or environment variable)
helper = AnthropicHelper()

# Create a conversation with multiple turns
messages = [
    {"role": "user", "content": "Hello, can you help me with Python programming?"},
    {"role": "assistant", "content": "Of course! I'd be happy to help with Python programming. What specific question or topic would you like assistance with?"},
    {"role": "user", "content": "How do I use list comprehensions?"}
]

response = helper.create_conversation(messages)
print(response)
```

### Streaming Responses

```python
from cws_helpers.anthropic_helper import AnthropicHelper

# Initialize the helper (API key will be loaded from .env file or environment variable)
helper = AnthropicHelper()

# Get a streaming response for real-time output
for chunk in helper.create_message(
    prompt="Write a short story about a robot learning to paint",
    stream=True
):
    print(chunk, end="", flush=True)
```

### Using Different Models

```python
from cws_helpers.anthropic_helper import AnthropicHelper, ClaudeModel

# Initialize the helper (API key will be loaded from .env file or environment variable)
helper = AnthropicHelper()

# Use Claude 3.7 Sonnet for most intelligent model
response = helper.create_message(
    prompt="Analyze the philosophical implications of artificial consciousness",
    model=ClaudeModel.CLAUDE_3_7_SONNET_LATEST.value
)
print(response)

# Use Claude 3.5 Haiku for faster, cost-effective responses
response = helper.create_message(
    prompt="What's the capital of France?",
    model=ClaudeModel.CLAUDE_3_5_HAIKU_LATEST.value
)
print(response)
```

### Counting Tokens

```python
from cws_helpers.anthropic_helper import AnthropicHelper

# Initialize the helper (API key will be loaded from .env file or environment variable)
helper = AnthropicHelper()

# Count tokens in a text string
text = "This is a sample text to count tokens for."
token_count = helper.count_tokens(text)
print(f"Token count: {token_count}")
```

### Cost Calculation

```python
from cws_helpers.anthropic_helper import ClaudeCostCalculator, ClaudeModel

# Calculate the cost of an API call
input_tokens = 500
output_tokens = 1000
model = ClaudeModel.CLAUDE_3_5_SONNET_LATEST.value

# Calculate standard input/output cost
cost = ClaudeCostCalculator.calculate_cost(model, input_tokens, output_tokens)
print(f"Estimated cost: ${cost:.6f}")

# Calculate prompt caching costs
prompt_tokens = 2000
write_cost = ClaudeCostCalculator.calculate_prompt_cache_cost(model, prompt_tokens, "write")
read_cost = ClaudeCostCalculator.calculate_prompt_cache_cost(model, prompt_tokens, "read")
print(f"Prompt cache write cost: ${write_cost:.6f}")
print(f"Prompt cache read cost: ${read_cost:.6f}")
```

## API Reference

### `AnthropicHelper`

#### `__init__(api_key=None, model=ClaudeModel.default(), max_retries=3, initial_retry_delay=1.0, timeout=120.0)`

Initialize the AnthropicHelper.

- `api_key` (str, optional): The Anthropic API key. If not provided, it will be read from the CLAUDE_API_KEY environment variable.
- `model` (str, optional): The default Claude model to use. Defaults to Claude 3.5 Sonnet Latest.
- `max_retries` (int, optional): Maximum number of retries for rate limiting. Defaults to 3.
- `initial_retry_delay` (float, optional): Initial delay between retries in seconds. Defaults to 1.0.
- `timeout` (float, optional): Timeout for API requests in seconds. Defaults to 120.0.

#### `create_message(prompt, system=None, max_tokens=4096, temperature=0.7, model=None, stream=False)`

Create a message with Claude.

- `prompt` (str): The user's prompt/question
- `system` (str, optional): System prompt to guide Claude's behavior
- `max_tokens` (int, optional): Maximum tokens in the response. Defaults to 4096.
- `temperature` (float, optional): Temperature for response generation. Defaults to 0.7.
- `model` (str, optional): Claude model to use. If not provided, uses the default model.
- `stream` (bool, optional): Whether to stream the response. Defaults to False.

Returns:
- If `stream=False`: A string containing the response text
- If `stream=True`: An iterable of response chunks

#### `create_conversation(messages, system=None, max_tokens=4096, temperature=0.7, model=None, stream=False)`

Create a conversation with Claude using multiple messages.

- `messages` (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content' keys
- `system` (str, optional): System prompt to guide Claude's behavior
- `max_tokens` (int, optional): Maximum tokens in the response. Defaults to 4096.
- `temperature` (float, optional): Temperature for response generation. Defaults to 0.7.
- `model` (str, optional): Claude model to use. If not provided, uses the default model.
- `stream` (bool, optional): Whether to stream the response. Defaults to False.

Returns:
- If `stream=False`: A string containing the response text
- If `stream=True`: An iterable of response chunks

#### `count_tokens(text, model=None)`

Count the number of tokens in a text string.

- `text` (str): The text to count tokens for
- `model` (str, optional): The model to use for counting. If not provided, uses the default model.

Returns:
- An integer representing the number of tokens in the text

### `ClaudeModel`

An enum of available Claude models:

#### Claude 3.7 Models
- `CLAUDE_3_7_SONNET_LATEST`: "claude-3-7-sonnet-latest"
- `CLAUDE_3_7_SONNET_20250219`: "claude-3-7-sonnet-20250219"

#### Claude 3.5 Models
- `CLAUDE_3_5_HAIKU_LATEST`: "claude-3-5-haiku-latest"
- `CLAUDE_3_5_HAIKU_20241022`: "claude-3-5-haiku-20241022"
- `CLAUDE_3_5_SONNET_LATEST`: "claude-3-5-sonnet-latest"
- `CLAUDE_3_5_SONNET_20241022`: "claude-3-5-sonnet-20241022"
- `CLAUDE_3_5_SONNET_20240620`: "claude-3-5-sonnet-20240620"

#### Claude 3 Models
- `CLAUDE_3_OPUS_LATEST`: "claude-3-opus-latest"
- `CLAUDE_3_OPUS_20240229`: "claude-3-opus-20240229"
- `CLAUDE_3_SONNET_20240229`: "claude-3-sonnet-20240229"
- `CLAUDE_3_HAIKU_20240307`: "claude-3-haiku-20240307"

#### Claude 2 Models
- `CLAUDE_2_1`: "claude-2.1"
- `CLAUDE_2_0`: "claude-2.0"

### `ClaudeCostCalculator`

A utility class for calculating the cost of Claude API calls based on token usage.

#### `calculate_cost(model, input_tokens, output_tokens)`

Calculate the cost of a Claude API call based on token usage and model.

- `model` (str): The Claude model used
- `input_tokens` (int): Number of input tokens used
- `output_tokens` (int): Number of output tokens used

Returns:
- A float representing the total cost in USD

#### `calculate_prompt_cache_cost(model, tokens, operation="write")`

Calculate the cost of prompt caching operations.

- `model` (str): The Claude model used
- `tokens` (int): Number of tokens in the prompt
- `operation` (str): Either "write" or "read"

Returns:
- A float representing the total cost in USD

## Error Handling

The AnthropicHelper includes automatic retries for rate limiting errors and provides helpful error messages for common issues. Other errors are logged and re-raised for the caller to handle.

### API Key Errors

If the API key is not provided and cannot be found in the environment variables or .env file, the helper will raise a ValueError with detailed instructions on how to set up the API key:

```python
from cws_helpers.anthropic_helper import AnthropicHelper

try:
    # This will fail if CLAUDE_API_KEY is not set
    helper = AnthropicHelper()
except ValueError as e:
    print(f"API key error: {e}")
    # Output will include instructions on how to set up the API key
```

### Other API Errors

```python
from cws_helpers.anthropic_helper import AnthropicHelper
import anthropic

helper = AnthropicHelper()

try:
    response = helper.create_message("Tell me about AI")
    print(response)
except anthropic.RateLimitError:
    print("Rate limit exceeded even after retries")
except anthropic.AuthenticationError:
    print("Authentication error - check your API key")
except anthropic.APIError as e:
    print(f"API error: {e}")
```

## Logging

The AnthropicHelper uses the cws_helpers.logger module for logging. You can configure the logging level to see more or less information:

```python
import logging
from cws_helpers.logger import configure_logging

# Configure logging for your module
log = configure_logging(__name__)
log.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logs
```

## Notes

- The AnthropicHelper was developed with anthropic==0.49.0. Using a different version may cause compatibility issues.
- Cost calculations are based on the official Anthropic pricing as of June 2024. These rates may change over time.
- The default model is Claude 3.5 Sonnet Latest, which provides a good balance of quality and cost.
- Prompt caching is a feature that allows you to cache prompts for repeated use, which can reduce costs for frequently used prompts.
