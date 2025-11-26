"""
Shared pytest fixtures for Academic Auto-Grader tests.

Provides common test data, mock objects, and helper functions.
"""

import pytest
import tempfile
import shutil

# Import all fixtures from submodules
pytest_plugins = [
    'tests.fixtures.python_files',
    'tests.fixtures.config_files',
    'tests.fixtures.sample_project',
]


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)
