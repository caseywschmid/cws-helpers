# Testing Guide for cws-helpers

This document provides guidelines for writing and running tests for the `cws-helpers` package. This guide is for developers contributing to the package.

## Testing Philosophy

Testing is a critical part of maintaining high-quality, reliable code. For the `cws-helpers` package, we focus on:

- **Unit tests** for individual components and functions
- **Integration tests** to ensure different parts of a helper work together
- **Edge case testing** to handle unexpected inputs gracefully

## Package Structure

This project uses a `src` layout, which means the actual package code is in the `src/cws_helpers` directory. When you install the package, the package will be available as `cws_helpers` in your Python environment.

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

The project uses `pytest` for testing, which is specified as a development dependency in our Poetry configuration. Note that Poetry is only needed for development, not for using the package.

```bash
# Install the project with development dependencies
poetry install

# For coverage reporting (if not already included)
poetry add --group dev pytest-cov
```

### Test Directory Structure

Tests are organized in a structure that mirrors the package itself:

```
cws-helpers/
├── src/
│   └── cws_helpers/
│       ├── logger/
│       └── ...
└── tests/
    ├── logger/
    │   ├── __init__.py
    │   └── test_logger.py
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
import pytest
from cws_helpers.logger import configure_logging
import logging

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

@patch('cws_helpers.some_helper.requests.get')
def test_api_call(mock_get):
    """Test API call handles response correctly."""
    # Configure mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test_data"}
    mock_get.return_value = mock_response
    
    # Test function that uses requests.get
    from cws_helpers.some_helper import ApiHelper
    helper = ApiHelper()
    result = helper.get_data("test_id")
    
    # Assertions
    assert result == "test_data"
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
    from cws_helpers.logger import configure_logging
    import logging
    
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
    from cws_helpers.logger import configure_logging
    import logging
    
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
        poetry run pytest --cov=src/cws_helpers
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
```

## Best Practices

1. **Write tests before or alongside code**: Consider test-driven development (TDD)
2. **Test both normal and edge cases**: Ensure your code handles unexpected inputs gracefully
3. **Keep tests focused**: Each test should verify one specific behavior
4. **Use descriptive test names**: Names should describe what is being tested
5. **Isolate tests**: Tests should not depend on each other
6. **Mock external dependencies**: Don't rely on external services for unit tests
7. **Aim for high coverage**: Strive for at least 80% code coverage
8. **Run tests frequently**: Integrate testing into your development workflow