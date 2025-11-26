"""
File Finder Configuration

Default ignore patterns for file discovery operations.
Centralized to allow easy customization and reuse.
"""

from typing import Set

# Default directories to ignore during file search
DEFAULT_IGNORE_DIRS: Set[str] = {
    'node_modules',
    'venv',
    'env',
    '.git',
    '__pycache__',
    'dist',
    'build',
    '.pytest_cache',
    '.mypy_cache',
    '.tox',
    'htmlcov',
    '.eggs',
    '*.egg-info',
    'temp',
    'tmp',
}
