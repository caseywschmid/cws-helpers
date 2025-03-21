import logging
import pytest
import io
import os
import re
from unittest.mock import patch
from cws_helpers.logger import (
    configure_logging,
    FINE_LEVEL,
    STEP_LEVEL,
    SUCCESS_LEVEL,
    CONTEXT_DISPLAY,
    ConsoleFormatter
)

@pytest.fixture
def test_handler():
    """Create a StringIO handler for capturing log output."""
    string_io = io.StringIO()
    handler = logging.StreamHandler(string_io)
    handler.setLevel(logging.INFO)
    yield handler, string_io
    handler.close()

def test_custom_log_levels():
    """Test that custom log levels are properly registered."""
    assert logging.getLevelName(FINE_LEVEL) == "FINE"
    assert logging.getLevelName(STEP_LEVEL) == "STEP"
    assert logging.getLevelName(SUCCESS_LEVEL) == "SUCCESS"
    
    # Test that logger methods exist
    logger = logging.getLogger("test")
    assert hasattr(logger, "fine")
    assert hasattr(logger, "step")
    assert hasattr(logger, "success")

def test_console_output(test_handler):
    """Test that logs appear in console with correct formatting."""
    handler, string_io = test_handler
    
    # Configure logger with our test handler
    logger = logging.getLogger("test_console")
    for h in logger.handlers[:]:
        logger.removeHandler(h)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Log a test message
    logger.info("Test info message")
    
    # Get output and verify
    output = string_io.getvalue()
    assert "Test info message" in output

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
    assert "test_file" in content
    assert "Test file message" in content

def test_log_levels_filtering():
    """Test that log level filtering works correctly."""
    logger = configure_logging("test_levels", log_level=logging.INFO)
    
    # Create a handler that captures logs for testing
    test_handler = logging.StreamHandler(io.StringIO())
    logger.addHandler(test_handler)
    
    # DEBUG should be filtered out with INFO level
    logger.debug("Debug message")
    # INFO should pass through
    logger.info("Info message")
    
    output = test_handler.stream.getvalue()
    assert "Debug message" not in output
    assert "Info message" in output

class TestClass:
    """Test class for testing class method context information."""
    
    def test_method(self, logger):
        """Log from a class method to test class context detection."""
        logger.info("Message from class method")
        return "test_complete"

@pytest.fixture
def logger():
    """Create a logger for testing context display."""
    # Configure a test logger
    log = logging.getLogger("test_context")
    for h in log.handlers[:]:
        log.removeHandler(h)
    
    string_io = io.StringIO()
    handler = logging.StreamHandler(string_io)
    # Use our ConsoleFormatter for proper context display
    handler.setFormatter(ConsoleFormatter())
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    
    return log

@patch.dict(os.environ, {"CONTEXT_DISPLAY": "function"})
def test_context_display_function(logger):
    """Test that function name appears in logs with CONTEXT_DISPLAY=function."""
    # Reset the CONTEXT_DISPLAY value for the test
    # We need to patch the imported value directly
    import cws_helpers.logger.logger as logger_module
    with patch.object(logger_module, 'CONTEXT_DISPLAY', 'function'):
        
        def test_function():
            logger.info("Test message from function")
            
        test_function()
        
        # Get the output and check for function name
        output = logger.handlers[-1].stream.getvalue()
        assert "Test message from function" in output
        # The function name should appear in the output
        assert "test_function" in output

@patch.dict(os.environ, {"CONTEXT_DISPLAY": "class_function"})
def test_context_display_class_function(logger):
    """Test that class.function appears in logs with CONTEXT_DISPLAY=class_function."""
    # Reset the CONTEXT_DISPLAY value for the test
    import cws_helpers.logger.logger as logger_module
    with patch.object(logger_module, 'CONTEXT_DISPLAY', 'class_function'):
        
        test_obj = TestClass()
        test_obj.test_method(logger)
        
        # Get the output and check for class.function format
        output = logger.handlers[-1].stream.getvalue()
        assert "Message from class method" in output
        # The class and method names should appear in the output
        assert "TestClass.test_method" in output

@patch.dict(os.environ, {"CONTEXT_DISPLAY": "full"})
def test_context_display_full(logger):
    """Test that full context appears in logs with CONTEXT_DISPLAY=full."""
    # Reset the CONTEXT_DISPLAY value for the test
    import cws_helpers.logger.logger as logger_module
    with patch.object(logger_module, 'CONTEXT_DISPLAY', 'full'):
        
        logger.info("Test message with full context")
        
        # Get the output and check for file and line information
        output = logger.handlers[-1].stream.getvalue()
        assert "Test message with full context" in output
        
        # Check for file name and line number format with a regex
        # The pattern looks for [something with test_logger.py:NUMBER]
        context_pattern = r'\[.*test_logger\.py:\d+\]'
        assert re.search(context_pattern, output), f"Output didn't match pattern. Output: {output}"

@patch.dict(os.environ, {"CONTEXT_DISPLAY": "none"})
def test_context_display_none(logger):
    """Test that no context appears in logs with CONTEXT_DISPLAY=none."""
    # Reset the CONTEXT_DISPLAY value for the test
    import cws_helpers.logger.logger as logger_module
    with patch.object(logger_module, 'CONTEXT_DISPLAY', 'none'):
        
        logger.info("Test message with no context")
        
        # Get the output and check that there's no context bracket
        output = logger.handlers[-1].stream.getvalue()
        assert "Test message with no context" in output
        # No context brackets should appear - we check specifically for our grey context formatting
        assert "\x1b[90m[" not in output  # No grey context bracket