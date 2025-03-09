"""
Pytest configuration file.

This file contains fixtures and configuration for pytest.
It helps ensure that the src directory is in the Python path
and that imports work correctly during testing.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path if it's not already there
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path)) 