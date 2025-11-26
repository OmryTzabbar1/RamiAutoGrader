"""
Shared pytest fixtures for Academic Auto-Grader tests.

Provides common test data, mock objects, and helper functions.
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


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
def sample_readme(temp_dir):
    """Create a sample README.md file."""
    readme_path = Path(temp_dir) / "README.md"
    readme_path.write_text('''# Test Project

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from myproject import main
main.run()
```

## Configuration

Edit config.yaml to customize settings.

## Troubleshooting

### Issue: Module not found
**Solution:** Install dependencies first.
''')
    return str(readme_path)


@pytest.fixture
def sample_gitignore(temp_dir):
    """Create a sample .gitignore file."""
    gitignore_path = Path(temp_dir) / ".gitignore"
    gitignore_path.write_text('''# Python
__pycache__/
*.pyc
*.pyo
venv/
.env

# IDE
.vscode/
.idea/

# Security
*.key
*.pem
credentials.json
secrets.yaml
''')
    return str(gitignore_path)


@pytest.fixture
def sample_env_example(temp_dir):
    """Create a sample .env.example file."""
    env_example_path = Path(temp_dir) / ".env.example"
    env_example_path.write_text('''# API Configuration
API_KEY=your_key_here
API_URL=https://api.example.com

# Database
DB_HOST=localhost
DB_PORT=5432
''')
    return str(env_example_path)


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
