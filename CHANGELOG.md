# Changelog

All notable changes to the `cws-helpers` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-04-05

### Added
- Google Helper module with the following features:
  - GoogleHelper class for interacting with Google APIs
  - Authentication handling with token refresh
  - SheetsHandler for Google Sheets operations
  - DriveHandler for Google Drive operations
  - DocsHandler for Google Docs operations
  - Comprehensive error handling
- Documentation for Google Helper:
  - Detailed README.md in the helper's directory with usage instructions and examples
  - Updated main README.md with Google Helper information
- Tests for Google Helper:
  - Unit tests for all GoogleHelper methods and handlers

### Changed
- Updated project dependencies to include Google API libraries

## [0.4.0] - 2025-03-29

### Added
- YouTube Helper module with the following features:
  - YoutubeHelper class for interacting with YouTube videos
  - Video information extraction using yt-dlp
  - URL validation and video ID extraction
  - Caption/subtitle handling with multiple format support
  - Comprehensive error handling with custom exceptions
  - Pydantic models for type-safe data handling
- Documentation for YouTube Helper:
  - Detailed README.md in the helper's directory with usage instructions and examples
  - Updated main README.md with YouTube Helper information
- Tests for YouTube Helper:
  - Unit tests for all YoutubeHelper methods

### Changed
- Updated project dependencies to include yt-dlp

## [0.3.0] - 2025-03-22

### Added
- AWS Helper module with the following features:
  - S3Helper class for S3 operations
  - Type-safe interface with Pydantic models
  - Support for raw data and JSON operations
  - Automatic pagination for listing objects
  - Environment variable fallbacks for credentials
  - Comprehensive error handling with custom exceptions
- Documentation for AWS Helper:
  - Detailed README.md in the helper's directory with usage instructions and examples
  - Updated main README.md with AWS Helper information
- Tests for AWS Helper:
  - Unit tests for all S3Helper methods
  - Mocked AWS services using moto

### Changed
- Updated project dependencies to include boto3

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

[0.5.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/caseywschmid/cws-helpers/releases/tag/v0.1.0 