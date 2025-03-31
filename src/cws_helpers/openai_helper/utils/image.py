"""
Image utility functions for OpenAI API interactions.

This module provides utility functions for working with images
in OpenAI API requests.
"""

import base64
import os
from typing import Optional

# ------------------ Configure Logging ------------------ #
from cws_helpers.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

def encode_image(image_path: str) -> str:
    """
    Encode an image to base64 for including in OpenAI API requests.
    
    This function reads an image file from the specified path and
    encodes it as a base64 string with the appropriate data URI prefix
    required by OpenAI's API.
    
    Parameters
    ----------
    image_path : str
        Path to the image file to encode
        
    Returns
    -------
    str
        Base64-encoded image with data URI prefix
        
    Raises
    ------
    FileNotFoundError
        If the image file does not exist
    """
    # Check if file exists
    if not os.path.exists(image_path):
        log.error(f"Image file not found at path: {image_path}")
        raise FileNotFoundError(f"Image file not found at path: {image_path}")
        
    try:
        with open(image_path, "rb") as image_file:
            # Read the image file and encode it
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            # Return in the format expected by OpenAI
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        log.error(f"Error encoding image at {image_path}: {str(e)}")
        raise 