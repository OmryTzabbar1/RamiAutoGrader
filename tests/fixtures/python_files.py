"""
Python file fixtures for testing.

Provides sample Python files with various characteristics.
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_python_file(temp_dir):
    """Create a sample Python file for testing."""
    file_path = Path(temp_dir) / "sample.py"
    file_path.write_text('''"""
Sample Python module for testing.

This module demonstrates proper docstrings.
"""


def calculate_sum(a, b):
    """
    Calculate sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        int: Sum of a and b
    """
    return a + b


class Calculator:
    """Simple calculator class."""

    def add(self, x, y):
        """Add two numbers."""
        return x + y

    def subtract(self, x, y):
        """Subtract y from x."""
        return x - y


# Constant
MAX_VALUE = 100
''')
    return str(file_path)


@pytest.fixture
def sample_python_file_no_docstrings(temp_dir):
    """Create a Python file without docstrings."""
    file_path = Path(temp_dir) / "no_docs.py"
    file_path.write_text('''
def function_without_docstring(x):
    return x * 2


class ClassWithoutDocstring:
    def method(self):
        return "test"
''')
    return str(file_path)


@pytest.fixture
def large_python_file(temp_dir):
    """Create a Python file exceeding 150 lines."""
    file_path = Path(temp_dir) / "large.py"
    lines = ['"""Large file for testing."""\n']
    lines.extend([f'def function_{i}():\n    pass\n\n' for i in range(60)])
    file_path.write_text(''.join(lines))
    return str(file_path)


@pytest.fixture
def file_with_secrets(temp_dir):
    """Create a file containing hardcoded secrets."""
    secrets_file = Path(temp_dir) / "config.py"
    secrets_file.write_text('''
API_KEY = "sk-1234567890abcdef"
PASSWORD = "supersecret123"
aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"
''')
    return str(secrets_file)
