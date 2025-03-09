# CWS Helpers

A collection of helper utilities for personal Python projects, providing enhanced functionality and convenience features.

## Available Packages

- **Logger**: Enhanced logging system with custom levels, colored output, and file logging capabilities
- *(More packages to be added)*

For detailed documentation on each package, please refer to the `/docs` directory.

## Installation

This package uses Poetry for dependency management. To install:

```bash
# Clone the repository
git clone https://github.com/caseywschmid/cws-helpers.git

# Navigate to the project directory
cd cws-helpers

# Install dependencies using Poetry
poetry install
```

### Package Structure

This project uses a `src` layout, which means the actual package code is in the `src/cws_helpers` directory. When you install the package (either via Poetry or pip), the package will be available as `cws_helpers` in your Python environment.

```
cws-helpers/
├── src/
│   └── cws_helpers/  # This becomes the importable package
│       ├── __init__.py
│       ├── logger/
│       └── ...
└── ...
```

## Quick Start

```python
# Example using the logger package
from cws_helpers.logger import configure_logging

logger = configure_logging(
    logger_name="my_app",
    keep_logs=True
)

logger.info("Application started")
logger.success("Operation completed successfully!")
```

For detailed usage instructions and API documentation for each package, see the corresponding documentation in the `/docs` directory.

## Dependencies

- Python ^3.9
- python-dotenv ^1.0.1
- pytest ^8.3.5 (dev dependency)

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Install development dependencies: `poetry install`
4. Run tests: `poetry run pytest`
5. Submit a pull request

## License

MIT License

## Author

Casey Schmid (caseywschmid@gmail.com)

