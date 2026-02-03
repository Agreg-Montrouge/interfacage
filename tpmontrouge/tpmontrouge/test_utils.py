"""
Test utilities for skipping tests based on environment
"""
import os
import unittest

# Check if we're running in a CI environment
CI_ENV = os.getenv('CI', 'false').lower() == 'true' or os.getenv('SKIP_GUI_TESTS', 'false').lower() == 'true'

def skip_if_ci(reason="GUI tests are skipped on CI"):
    """
    Decorator to skip tests when running in CI environment
    
    Usage:
        @skip_if_ci()
        def test_something_with_gui(self):
            ...
    """
    return unittest.skipIf(CI_ENV, reason)
