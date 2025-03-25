# How to Update an Existing Helper in cws-helpers

This guide provides detailed instructions for updating an existing helper module in the cws-helpers package. It covers the entire process from making code changes to releasing a new version.

## Table of Contents

1. [Understanding the Update Process](#understanding-the-update-process)
2. [Preparing Your Development Environment](#preparing-your-development-environment)
3. [Making Code Changes](#making-code-changes)
4. [Writing and Updating Tests](#writing-and-updating-tests)
5. [Updating Documentation](#updating-documentation)
6. [Version Management](#version-management)
7. [Creating a Release](#creating-a-release)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Understanding the Update Process

Updating a helper in the cws-helpers package involves several key steps:

1. **Code Changes**: Modifying the helper's implementation to add features, fix bugs, or improve performance
2. **Testing**: Ensuring that your changes work correctly and don't break existing functionality
3. **Documentation**: Updating the helper's documentation to reflect the changes
4. **Version Management**: Incrementing the package version according to semantic versioning principles
5. **Release**: Creating a new release of the package

Each of these steps is crucial for maintaining a high-quality, reliable package.

## Preparing Your Development Environment

Before making any changes, ensure your development environment is properly set up:

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/caseywschmid/cws-helpers.git
   cd cws-helpers
   ```

2. **Create a new branch** for your changes:
   ```bash
   git checkout -b update-helper-name
   ```

3. **Install dependencies** using Poetry:
   ```bash
   poetry install
   ```

4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

5. **Run the tests** to ensure everything is working before you start:
   ```bash
   poetry run pytest
   ```

## Making Code Changes

When updating an existing helper, follow these guidelines:

### 1. Locate the Helper Files

The helper's code is typically organized as follows:
- Main implementation: `src/cws_helpers/helper_name/helper_name.py`
- Public API: `src/cws_helpers/helper_name/__init__.py`
- Models (if applicable): `src/cws_helpers/helper_name/models/`
- Enums (if applicable): `src/cws_helpers/helper_name/enums/`

### 2. Understand the Existing Code

Before making changes:
- Read through the existing implementation to understand how it works
- Review the tests to understand the expected behavior
- Check the documentation to understand the intended usage

### 3. Make Your Changes

When modifying the code:
- Follow the existing code style and patterns
- Add comprehensive docstrings to new functions, classes, and methods
- Ensure backward compatibility when possible
- Add appropriate error handling
- Keep functions focused and modular

### 4. Example: Adding a New Method

```python
def new_method(self, param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """
    Description of what the new method does.
    
    Parameters
    ----------
    param1 : str
        Description of param1
    param2 : Optional[int], optional
        Description of param2, by default None
        
    Returns
    -------
    Dict[str, Any]
        Description of the return value
        
    Raises
    ------
    SomeError
        When the method encounters a specific error condition
    """
    # Implementation
    result = {}
    
    # Add appropriate logging
    log.info(f"Processing {param1}")
    
    # Add error handling
    if not self._validate_input(param1):
        log.warning(f"Invalid input: {param1}")
        raise ValueError(f"Invalid input: {param1}")
    
    # Method logic
    # ...
    
    return result
```

### 5. Update the Public API

If you've added new functionality, update the `__init__.py` file to expose it:

```python
# src/cws_helpers/helper_name/__init__.py
from .helper_name import HelperClass, new_function, SomeError

__all__ = ['HelperClass', 'new_function', 'SomeError']
```

## Writing and Updating Tests

Tests are crucial for ensuring your changes work correctly and don't break existing functionality.

### 1. Locate the Test Files

Tests are typically located in:
- `tests/helper_name/test_helper_name.py`

### 2. Add Tests for New Functionality

For each new feature or method, add corresponding tests:

```python
def test_new_method():
    """Test the new_method function with valid inputs."""
    helper = HelperClass()
    result = helper.new_method("valid_input", 42)
    assert "expected_key" in result
    assert result["expected_key"] == "expected_value"

def test_new_method_invalid_input():
    """Test the new_method function with invalid inputs."""
    helper = HelperClass()
    with pytest.raises(ValueError):
        helper.new_method("invalid_input")
```

### 3. Update Existing Tests if Behavior Changes

If you've modified existing behavior, update the corresponding tests:

```python
# Before
def test_existing_method():
    helper = HelperClass()
    result = helper.existing_method("input")
    assert result == "old_expected_output"

# After
def test_existing_method():
    helper = HelperClass()
    result = helper.existing_method("input")
    assert result == "new_expected_output"
```

### 4. Run the Tests

Run the tests to ensure everything is working:

```bash
# Run all tests
poetry run pytest

# Run tests for a specific helper
poetry run pytest tests/helper_name/

# Run a specific test
poetry run pytest tests/helper_name/test_helper_name.py::test_new_method

# Run tests with verbose output
poetry run pytest -v
```

## Updating Documentation

Documentation is essential for users to understand how to use your helper.

### 1. Update the Helper's README.md

The helper's README.md file should be updated to reflect any changes:

```markdown
# Helper Name

Brief description of what the helper does.

## Usage

```python
from cws_helpers import HelperClass

# Example usage of existing functionality
helper = HelperClass()
result = helper.existing_method("input")

# Example usage of new functionality
new_result = helper.new_method("input", 42)
```

## API Reference

### `HelperClass`

#### `existing_method(param)`

Description of the existing method.

#### `new_method(param1, param2=None)`

Description of the new method.
- `param1`: Description of param1
- `param2`: Description of param2 (optional)

Returns: Description of the return value
```

### 2. Update Docstrings

Ensure all new functions, classes, and methods have comprehensive docstrings:

```python
def new_method(self, param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """
    Description of what the new method does.
    
    Parameters
    ----------
    param1 : str
        Description of param1
    param2 : Optional[int], optional
        Description of param2, by default None
        
    Returns
    -------
    Dict[str, Any]
        Description of the return value
        
    Raises
    ------
    SomeError
        When the method encounters a specific error condition
    """
```

### 3. Update the Main README.md if Necessary

If you've added significant new functionality, update the main README.md file to highlight it.

## Version Management

When updating a helper, you need to increment the package version according to semantic versioning principles.

### 1. Determine the Version Increment

- **PATCH** (0.1.0 → 0.1.1): For backward-compatible bug fixes
- **MINOR** (0.1.0 → 0.2.0): For backward-compatible new features
- **MAJOR** (0.1.0 → 1.0.0): For breaking changes

### 2. Update the CHANGELOG.md

Add an entry for the new version in the CHANGELOG.md file:

```markdown
## [0.4.0] - YYYY-MM-DD

### Added
- New feature X to helper_name
- New method Y to HelperClass

### Changed
- Improved performance of method Z
- Updated dependency requirements

### Fixed
- Bug in method W

[0.4.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.3.0...v0.4.0
```

Make sure to:
- Use today's date in the YYYY-MM-DD format
- Include appropriate sections (Added, Changed, Fixed, etc.)
- Add a comparison link at the bottom
- Be specific about which helper was changed and what changes were made

## Creating a Release

Once your changes are complete, tested, and documented, it's time to create a release.

### 1. Ensure Tests Pass

Run the tests to make sure everything is working correctly:

```bash
poetry run pytest
# Or to run tests for a specific helper:
poetry run pytest tests/helper_name/
```

### 2. Use the Release Script

The project includes a release script that automates updating version numbers, creating a git tag, and pushing changes:

```bash
# Run from the project root directory
./scripts/release.sh <version> "<commit_message>"

# Example:
./scripts/release.sh 0.4.0 "Update helper_name with new features"
```

This script will:
- Update the version in `src/cws_helpers/__init__.py`
- Update the version in `pyproject.toml`
- Commit these changes with the provided message
- Create a git tag for the new version
- Push the changes and tag to GitHub

> **IMPORTANT**: Always update the CHANGELOG.md file manually BEFORE running the release script.

### 3. Create a GitHub Release

1. Go to the GitHub repository
2. Navigate to "Releases"
3. Click "Create a new release"
4. Select the tag you created
5. Add a title and description (you can copy from the CHANGELOG.md)
6. Publish the release

## Best Practices

Follow these best practices when updating helpers:

### Code Quality

- **Maintain backward compatibility** when possible
- **Follow the existing code style** and patterns
- **Keep functions focused and modular**
- **Add comprehensive error handling**
- **Use type hints** for better IDE support and documentation

### Testing

- **Write tests for all new functionality**
- **Update tests for modified functionality**
- **Ensure all tests pass** before committing
- **Consider edge cases** in your tests

### Documentation

- **Update all relevant documentation**
- **Add examples** for new functionality
- **Keep docstrings up-to-date**
- **Document breaking changes** clearly

### Version Management

- **Follow semantic versioning** principles
- **Update the version in all required files**
- **Maintain a detailed CHANGELOG.md**

## Troubleshooting

### Common Issues and Solutions

#### Tests Failing After Updates

1. **Check for breaking changes**: Ensure your changes don't break existing functionality
2. **Update test expectations**: If behavior has intentionally changed, update the tests
3. **Check for environment issues**: Ensure dependencies are installed correctly

#### Import Errors

1. **Check the `__init__.py` files**: Ensure new functionality is properly exported
2. **Verify the package structure**: Ensure files are in the correct locations

#### Version Conflicts

1. **Check all version references**: Ensure the version is updated consistently across all files
2. **Verify semantic versioning**: Ensure the version increment follows semantic versioning principles

#### Documentation Discrepancies

1. **Review all documentation**: Ensure documentation accurately reflects the code
2. **Check examples**: Ensure examples work with the updated code

## Conclusion

Updating a helper in the cws-helpers package involves careful planning, implementation, testing, and documentation. By following this guide, you can ensure that your updates are high-quality, reliable, and easy for users to adopt.

Remember that the goal is to provide a seamless experience for users of the package, with clear documentation and reliable functionality. 