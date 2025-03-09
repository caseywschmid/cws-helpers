# Changelog

All notable changes to the `cws-helpers` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-03-15

### Added
- OpenAI Helper module with the following features:
  - Simple interface for OpenAI's API
  - Support for text completions
  - Support for image inputs (local files and URLs)
  - JSON mode for structured outputs
  - Pydantic model integration for schema validation
  - Streaming responses
  - Function/tool calling
  - Comprehensive error handling
- Documentation for OpenAI Helper:
  - Detailed README.md in the helper's directory with usage instructions and examples
  - Updated main README.md with OpenAI Helper information
- Development environment improvements:
  - VS Code configuration for better Python and pytest integration
  - Added .env.example template for environment variables
  - Added conftest.py for pytest configuration

### Changed
- Updated project dependencies to include OpenAI and Pydantic
- Moved documentation from docs/ directory to README.md files in each helper's directory
- Updated How_to_add_a_new_helper.md with improved instructions for documentation

## [0.1.0] - 2025-03-09

### Added
- Initial project structure with Poetry dependency management
- Logger module with the following features:
  - Custom log levels (FINE, STEP, SUCCESS)
  - Colored console output
  - File logging with rotation
  - Environment variable configuration
- Comprehensive documentation:
  - README.md with installation and quick start guide
  - Logger_Docs.md with detailed usage instructions
  - How_to_add_a_new_helper.md guide for contributors
  - Testing_Guide.md for test development

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)

[0.2.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/caseywschmid/cws-helpers/releases/tag/v0.1.0 