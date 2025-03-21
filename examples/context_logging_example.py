#!/usr/bin/env python3
"""
Example demonstrating contextual logging with cws_helpers.logger.

Run this script with different CONTEXT_DISPLAY settings to see how 
context information appears in logs.

Examples:
    # No context (default)
    python context_logging_example.py
    
    # Function-only context
    CONTEXT_DISPLAY=function python context_logging_example.py
    
    # Class and function context
    CONTEXT_DISPLAY=class_function python context_logging_example.py
    
    # Full context with file and line information
    CONTEXT_DISPLAY=full python context_logging_example.py
"""

import os
import time
from cws_helpers.logger import configure_logging

# Configure logging
log = configure_logging("context_example")


def simple_function():
    """Example of logging from a simple function."""
    log.info("This is a log from a simple function")
    log.warning("This is a warning from a simple function")
    nested_function()


def nested_function():
    """Example of logging from a nested function call."""
    log.fine("This is a FINE log from a nested function")


class ExampleService:
    """Example service class to demonstrate class method logging."""
    
    def __init__(self):
        """Initialize the service."""
        log.debug("Initializing ExampleService")
        
    def process_data(self, data):
        """Process some data and log the steps."""
        log.step("Starting data processing")
        
        # Do some processing
        time.sleep(0.5)
        log.info(f"Processing data: {data}")
        
        # Simulate more processing
        time.sleep(0.5)
        
        # Call another method
        self.validate_result("processed_" + data)
        
        log.success(f"Successfully processed data: {data}")
        
    def validate_result(self, result):
        """Validate a processing result."""
        log.info(f"Validating result: {result}")
        
        try:
            # Simulate validation logic
            if "error" in result:
                raise ValueError("Validation failed")
            log.fine("Validation passed")
        except Exception as e:
            log.error(f"Error during validation: {str(e)}")


def main():
    """Main function to demonstrate all logging features."""
    context_display = os.environ.get("CONTEXT_DISPLAY", "none")
    log.info(f"Starting example with CONTEXT_DISPLAY={context_display}")
    
    # Call a simple function
    simple_function()
    
    # Use a class with methods
    service = ExampleService()
    service.process_data("sample_data")
    
    # Try with error
    try:
        service.process_data("error_data")
    except Exception as e:
        log.error(f"Error in main: {str(e)}")
    
    log.success("Example completed successfully")


if __name__ == "__main__":
    main() 