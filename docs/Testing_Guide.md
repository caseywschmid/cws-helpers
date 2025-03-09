# Testing Guide for cws-helpers

This document provides guidelines for writing and running tests for the `cws-helpers` package.

## Testing Philosophy

Testing is a critical part of maintaining high-quality, reliable code. For the `cws-helpers` package, we focus on:

- **Unit tests** for individual components and functions
- **Integration tests** to ensure different parts of a helper work together
- **Edge case testing** to handle unexpected inputs gracefully

## Package Structure

This project uses a `src` layout, which means the actual package code is in the `src/cws_helpers` directory. When you install the package (either via Poetry or pip), the package will be available as `cws_helpers` in your Python environment.

```
cws-helpers/
├── src/
│   └── cws_helpers/  # This becomes the importable package
│       ├── __init__.py
│       ├── logger/
│       └── ...
└── tests/
    ├── logger/
    └── ...
```

## Setting Up the Testing Environment

### Prerequisites

The project uses `pytest` for testing, which is specified as a development dependency in our Poetry configuration:

```bash
# If not already added, add pytest to dev dependencies
poetry add --group dev pytest

# For coverage reporting (recommended)
poetry add --group dev pytest-cov
```

### Test Directory Structure

Tests are organized in a structure that mirrors the package itself:

```
cws-helpers/
├── src/
│   └── cws_helpers/
│       ├── logger/
│       ├── youtube/
│       └── ...
└── tests/
    ├── logger/
    │   ├── __init__.py
    │   └── test_logger.py
    ├── youtube/
    │   ├── __init__.py
    │   └── test_youtube.py
    └── ...
```

For each helper module in `src/cws_helpers/`, create a corresponding directory in `tests/`.

## Writing Tests

### Basic Test Structure

Tests should be clear, focused, and descriptive. Each test function should test a specific aspect of functionality:

```python
def test_feature_with_normal_input():
    """Test that feature X works with normal, expected input Y."""
    # Arrange - set up test data
    input_data = "example"
    
    # Act - call the function being tested
    result = function_under_test(input_data)
    
    # Assert - verify the expected outcome
    assert result == "expected output"
```

### Using Fixtures

Fixtures are a powerful way to set up shared test environments:

```python
@pytest.fixture
def sample_logger():
    """Fixture to provide a pre-configured logger for tests."""
    logger = configure_logging("test_logger", log_level=logging.INFO)
    # Return the resource
    yield logger
    # Cleanup code (if needed) goes here

def test_logger_output(sample_logger):
    """Test logger produces expected output."""
    # Test using the fixture
    sample_logger.info("Test message")
    # Assert expected behavior
```

### Mocking

For tests that involve external resources or side effects, use mocking:

```python
from unittest.mock import patch, MagicMock

@patch('cws_helpers.youtube.core.requests.get')
def test_youtube_api_call(mock_get):
    """Test YouTube API call handles response correctly."""
    # Configure mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"id": "123", "title": "Test Video"}]}
    mock_get.return_value = mock_response
    
    # Test function that uses requests.get
    helper = YouTubeHelper()
    result = helper.get_video_info("test_id")
    
    # Assertions
    assert result.title == "Test Video"
    mock_get.assert_called_once()
```

### Testing Custom Log Outputs

For testing logging output, capture and inspect the output stream:

```python
import io
import sys

@pytest.fixture
def capture_stderr():
    """Capture stderr for testing logged output."""
    captured_output = io.StringIO()
    sys.stderr = captured_output
    yield captured_output
    sys.stderr = sys.__stderr__

def test_console_output(capture_stderr):
    """Test that logs appear in console with correct formatting."""
    logger = configure_logging("test_console", log_level=logging.INFO)
    logger.info("Test info message")
    
    output = capture_stderr.getvalue()
    assert "INFO" in output
    assert "Test info message" in output
```

### Testing File Operations

For file operations, use temporary directories:

```python
def test_file_logging(tmp_path):
    """Test that logs are written to file when keep_logs=True."""
    log_dir = tmp_path / "logs"
    logger = configure_logging("test_file", log_level=logging.INFO, 
                              keep_logs=True, log_dir=str(log_dir))
    
    logger.info("Test file message")
    
    log_file = log_dir / "logs.log"
    assert log_file.exists()
    content = log_file.read_text()
    assert "INFO" in content
    assert "Test file message" in content
```

## Running Tests

### Running All Tests

To run all tests in the project:

```bash
# From the project root directory
poetry run pytest

# With coverage report
poetry run pytest --cov=src/cws_helpers
```

### Running Specific Tests

To run specific test modules or functions:

```bash
# Run tests for a specific module
poetry run pytest tests/logger/

# Run a specific test file
poetry run pytest tests/logger/test_logger.py

# Run a specific test function
poetry run pytest tests/logger/test_logger.py::test_file_logging
```

### Test Options

Useful pytest options include:

- `-v` or `--verbose`: Show more detailed output
- `-xvs`: Exit on first failure, verbose mode, and don't capture output
- `--pdb`: Enter debugger on failures
- `--cov`: Generate coverage report
- `--cov-report html`: Generate HTML coverage report

## Continuous Integration

For continuous integration, consider:

1. Adding a GitHub Actions workflow to automatically run tests on push
2. Configuring coverage thresholds to maintain test quality
3. Adding pre-commit hooks to run tests before committing

Example GitHub Actions workflow file (`.github/workflows/test.yml`):

```yaml
name: Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.13]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
    - name: Install dependencies
      run: |
        poetry install
    - name: Run tests
      run: |
        poetry run pytest --cov=src/cws_helpers --cov-report xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Test Documentation

Good test documentation should:

1. Explain **what** is being tested
2. Clarify **why** certain test approaches were chosen
3. Provide examples of how to test new components

Include docstrings in all test functions to explain their purpose:

```python
def test_custom_log_levels():
    """
    Test that custom log levels are properly registered.
    
    This test verifies:
    1. Custom level names are registered with the logging system
    2. Custom logging methods are added to Logger instances
    """
    # Test code...
```

## Adding Tests for New Helpers

When adding a new helper module to the package:

1. Create a corresponding test directory in `tests/`
2. Write tests for all public functions and classes
3. Include tests for edge cases and error conditions
4. Use appropriate fixtures and mocks to isolate the component being tested

For example, when adding a new `aws_helper`:

```
tests/aws_helper/
├── __init__.py
├── test_s3.py
├── test_dynamodb.py
└── conftest.py  # Shared fixtures for AWS tests
```

## Common Testing Patterns

### Testing Error Handling

```python
def test_aws_connection_error():
    """Test that AWS connection errors are handled gracefully."""
    with patch('boto3.client') as mock_client:
        mock_client.side_effect = ConnectionError("Failed to connect")
        
        # Verify the helper handles the connection error properly
        with pytest.raises(AWSConnectionError):
            aws_helper = AWSHelper()
            aws_helper.get_s3_objects("my-bucket")
```

### Testing Different Input Types

```python
@pytest.mark.parametrize("input_value, expected", [
    ("string input", "processed string"),
    (123, "processed 123"),
    (None, "default value"),
])
def test_process_input_types(input_value, expected):
    """Test that the function handles different input types correctly."""
    result = process_input(input_value)
    assert result == expected
```

## Conclusion

A comprehensive test suite is essential for maintaining the reliability and quality of the `cws-helpers` package. By following these guidelines, you'll ensure that the helpers work as expected and continue to function correctly as the codebase evolves.

Remember that tests are an investment in the long-term health of your codebase, making it easier to refactor, add features, and fix bugs with confidence.