# How to add a new Helper to cws-helpers

This guide explains how to add a new helper module to the cws-helpers package. This is for developers who want to contribute to or extend the package.

## General Information

- This project uses Poetry for development and dependency management
- The project follows a `src` layout, where the actual package code is in the `src/cws_helpers` directory
- When installed, the package is available as `cws_helpers` (without the `src/` prefix)
- End users of your helper will not need Poetry - they can install the package with pip

## Package Structure

```
cws-helpers/
├── src/
│   └── cws_helpers/  # This becomes the importable package
│       ├── __init__.py
│       ├── logger/
│       │   ├── __init__.py
│       │   └── logger.py
│       └── your_new_helper/  # Your new helper goes here
│           ├── __init__.py
│           └── your_new_helper.py
├── tests/
│   └── your_new_helper/
│       ├── __init__.py
│       └── test_your_new_helper.py
└── docs/
    └── Your_New_Helper_Docs.md
```

## Step-by-Step Guide

1. **Create the directory structure**:
   ```bash
   mkdir -p src/cws_helpers/your_new_helper
   mkdir -p tests/your_new_helper
   touch src/cws_helpers/your_new_helper/__init__.py
   touch src/cws_helpers/your_new_helper/your_new_helper.py
   touch tests/your_new_helper/__init__.py
   touch tests/your_new_helper/test_your_new_helper.py
   ```

2. **Implement your helper module**:
   - Write your code in `src/cws_helpers/your_new_helper/your_new_helper.py`
   - Add appropriate docstrings and comments to explain functionality
   - Include comprehensive error handling

3. **Update the `__init__.py` file**:
   In `src/cws_helpers/your_new_helper/__init__.py`, import and expose the functionality from your helper module:
   ```python
   # src/cws_helpers/your_new_helper/__init__.py
   """
   Your helper module description.
   
   This module provides [brief description of functionality].
   """
   
   from .your_new_helper import YourHelperClass, your_helper_function
   
   __all__ = ['YourHelperClass', 'your_helper_function']
   ```

4. **Update the main package `__init__.py`**:
   In `src/cws_helpers/__init__.py`, import your helper to make it available at the top level (optional):
   ```python
   # src/cws_helpers/__init__.py
   """CWS Helpers - Collection of utility helpers for personal projects."""
   
   __version__ = "0.1.0"
   
   # For convenient imports
   from .logger import configure_logging
   from .your_new_helper import YourHelperClass, your_helper_function
   ```

5. **Add dependencies if needed**:
   If your helper requires additional dependencies, add them using Poetry:
   ```bash
   poetry add dependency-name
   ```
   This will automatically update the `pyproject.toml` file and the `poetry.lock` file. These dependencies will be installed automatically when users install your package with pip.

6. **Write tests**:
   Create tests for your helper in `tests/your_new_helper/test_your_new_helper.py`:
   ```python
   # tests/your_new_helper/test_your_new_helper.py
   import pytest
   from cws_helpers.your_new_helper import YourHelperClass, your_helper_function
   
   def test_your_helper_function():
       # Test your helper function
       result = your_helper_function(...)
       assert result == expected_result
   
   def test_your_helper_class():
       # Test your helper class
       helper = YourHelperClass(...)
       assert helper.some_method() == expected_result
   ```

7. **Create documentation**:
   Create a documentation file in the `docs` directory:
   ```bash
   touch docs/Your_New_Helper_Docs.md
   ```
   Include detailed usage instructions, examples, and API documentation. Make sure to include clear installation instructions for users (who will use pip, not Poetry).

8. **Update the README.md**:
   Add your new helper to the "Available Packages" section in the main README.md file.

9. **Install and test**:
   ```bash
   # Install your package in development mode
   poetry install
   
   # Run tests
   poetry run pytest tests/your_new_helper
   ```

10. **Commit your changes**:
    ```bash
    git add .
    git commit -m "Add new helper: your_new_helper"
    git push
    ```

## Best Practices

1. **Follow PEP 8** for code style and formatting
2. **Write comprehensive docstrings** for all public functions, classes, and methods
3. **Include type hints** to improve code readability and IDE support
4. **Add detailed comments** explaining complex logic
5. **Write thorough tests** covering normal usage and edge cases
6. **Keep dependencies minimal** to avoid bloating the package
7. **Document for end users** who will install with pip, not Poetry
