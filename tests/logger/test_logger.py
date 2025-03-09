import logging
import pytest
import io
from cws_helpers.logger import (
    configure_logging,
    FINE_LEVEL,
    STEP_LEVEL,
    SUCCESS_LEVEL
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