# Changelog

All notable changes to the `cws-helpers` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.1] - 2025-04-02

### Added
- Enhanced OpenAI Helper with model-specific parameter compatibility:
  - Added `get_unsupported_parameters` method to AIModel to identify parameters not supported by specific models
  - Added automatic parameter filtering in API calls based on model compatibility
  - Added comprehensive test suite for parameter compatibility
  - Updated documentation with examples of model-specific parameter handling

### Fixed
- Fixed error when using temperature parameter with o3-mini and o1 models by automatically filtering it out
- Fixed error when using top_p parameter with o3-mini and o1 models by automatically filtering it out
- Fixed error when using parallel_tool_calls parameter with o3-mini and o1 models by automatically filtering it out

## [0.10.0] - 2025-04-01

### Added
- Enhanced OpenAI Helper with model-specific logic:
  - Added AIModel and AIProvider enums for model management
  - Improved token parameter handling for different model types
  - Automatic detection and use of appropriate token parameter (max_tokens vs max_completion_tokens)
  - Added support for the latest "o" series models (o1, o3-mini, gpt-4o)
  - Added automatic error recovery for token parameter errors
  - Added model-specific structured output support detection
  - Added comprehensive tests for all new functionality

### Changed
- Updated OpenAI dependency to version 1.68.2
- Improved error handling in OpenAI API calls
- Enhanced documentation for model-specific features

## [0.9.2] - 2025-03-23

### Changed
- Updated OpenAI dependency to use version constraint `^1.65.5` instead of fixed version `1.65.5` to allow compatibility with newer versions
- Enhanced version compatibility checking in OpenAIHelper to support semantic versioning principles
- Improved logging around version compatibility warnings

## [0.9.1] - 2025-03-21

### Fixed
- Changed some log statements to "debug" level to prevent unnecessary output in production

## [0.9.0] - 2025-03-21

### Added
- Enhanced Logger with contextual information:
  - Added automatic detection of calling context (function name, class, file, line number)
  - New `CONTEXT_DISPLAY` environment variable with options: "none", "function", "class_function", "full"
  - Right-aligned context display to maintain clean log formatting
  - Added example script demonstrating contextual logging
  - Comprehensive tests for the new functionality
  - Updated documentation with examples of contextual logging options

### Changed
- Enhanced OpenAI Helper with structured outputs support:
  - Added support for the beta parse endpoint for improved Pydantic model handling
  - New `create_structured_chat_completion` method for direct access to the parse endpoint
  - Added `use_beta_parse` parameter to control when the beta endpoint is used
  - Automatic fallback to standard endpoint when beta is not available
  - Comprehensive tests for all new functionality
  - Updated documentation with examples of using structured outputs

### Removed
- Removed `DETAILED_CONSOLE_OUTPUT` environment variable from logger as the new contextual logging feature provides a more comprehensive and flexible alternative

### Fixed
- Refactored message creation in OpenAI Helper into a helper method for better code organization
- Improved error handling for JSON parsing and API compatibility

## [0.8.0] - 2025-03-21

### Added
- Enhanced OpenAI Helper with structured outputs support:
  - Added support for the beta parse endpoint for improved Pydantic model handling
  - New `create_structured_chat_completion` method for direct access to the parse endpoint
  - Added `use_beta_parse` parameter to control when the beta endpoint is used
  - Automatic fallback to standard endpoint when beta is not available
  - Comprehensive tests for all new functionality
  - Updated documentation with examples of using structured outputs

### Changed
- Refactored message creation in OpenAI Helper into a helper method for better code organization
- Improved error handling for JSON parsing and API compatibility

## [0.7.4] - 2025-03-20

### Changed
- Enhanced `list_available_captions` method in YoutubeHelper:
  - Now returns full `YTDLPCaption` objects instead of just `CaptionExtension` enums
  - This provides access to caption URLs and other metadata, enabling direct download
  - Updated documentation and examples to reflect this change
  - All tests updated to verify the new return type

## [0.7.3] - 2025-03-19

### Added
- Enhanced `list_available_captions` method in YoutubeHelper:
  - Added new `return_all_captions` parameter (default: False) to control caption filtering
  - Now uses caption preferences from `_extract_captions` by default
  - Returns all available captions only when explicitly requested

### Changed
- Improved efficiency of caption handling with early returns
- Updated tests to verify new caption filtering behavior

## [0.7.2] - 2025-03-18

### Added
- Enhanced caption handling in YoutubeHelper:
  - Added new `_process_captions_for_model` method for better caption data processing
  - Added support for custom download options in `get_video_info` method
  - Added comprehensive tests for caption functionality

### Fixed
- Fixed issue with captions not being properly processed in YoutubeHelper
- Fixed validation errors when processing caption data from yt-dlp
- Improved handling of automatic captions with 'auto-' prefix

### Changed
- Updated YouTube helper documentation:
  - Corrected method signatures and return types to match implementation
  - Added detailed documentation for models and caption handling
  - Updated examples to demonstrate proper caption usage
  - Fixed discrepancies between documentation and actual implementation

## [0.7.1] - 2025-03-15

### Changed
- Enhanced logging in YoutubeHelper:
  - Added method name context to log messages for better traceability
  - Changed log level from debug to fine for several methods to improve log readability
  - Added logging to previously unlogged methods

## [0.7.0] - 2025-03-10

### Added
- Anthropic Helper module for interacting with Claude API:
  - AnthropicHelper class for simplified Claude API interactions
  - Support for all Claude models (3.7, 3.5, 3, and 2 series)
  - Text message creation with system prompts
  - Conversation history support
  - Streaming responses
  - Token counting
  - Cost calculation with up-to-date pricing
  - Prompt caching cost calculation
  - Automatic retries with exponential backoff for rate limiting
  - Automatic loading of API key from .env file with helpful error messages
  - Comprehensive error handling and logging
- Documentation for Anthropic Helper:
  - Detailed README.md with usage examples and API reference

## [0.6.0] - 2025-04-12

### Added
- PowerPath API Helper module with the following features:
  - Complete interface for the PowerPath educational content management API
  - PowerPathClient for making API requests with automatic error handling
  - Pydantic models for all PowerPath resources (users, courses, modules, etc.)
  - 53 API functions covering all available PowerPath endpoints (100% coverage)
  - Comprehensive error handling with custom exceptions
  - Default base URL configuration for simplified usage
  - SQL query support for advanced data access
- Documentation for PowerPath Helper:
  - Detailed README.md with implementation status, usage examples, and API reference
  - Updated main README.md with PowerPath Helper information
- Tests for PowerPath Helper:
  - Unit tests for all API functions and models
  - 100% test coverage for all implemented endpoints

### Changed
- Updated project dependencies to include requests and pydantic

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

[0.10.1]: https://github.com/caseywschmid/cws-helpers/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.9.2...v0.10.0
[0.9.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.7.4...v0.8.0
[0.7.4]: https://github.com/caseywschmid/cws-helpers/compare/v0.7.3...v0.7.4
[0.7.3]: https://github.com/caseywschmid/cws-helpers/compare/v0.7.2...v0.7.3
[0.7.2]: https://github.com/caseywschmid/cws-helpers/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/caseywschmid/cws-helpers/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/caseywschmid/cws-helpers/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/caseywschmid/cws-helpers/releases/tag/v0.1.0 