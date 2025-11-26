"""
File Finder Utility Module

Recursively finds code files in a project directory while respecting ignore patterns.
Used to collect all relevant files for analysis.

Key Features:
- Recursive directory traversal
- Configurable file extensions
- Automatic exclusion of common ignore directories
"""

import os
from typing import List, Set

from .file_finder_config import DEFAULT_IGNORE_DIRS


def find_code_files(
    project_path: str,
    extensions: List[str] = None,
    ignore_dirs: Set[str] = None
) -> List[str]:
    """
    Find all code files in a project directory.

    Recursively searches for files matching specified extensions,
    while skipping common ignore directories.

    Args:
        project_path: Root directory to search
        extensions: List of file extensions to find (e.g., ['.py', '.js'])
                   Default: ['.py', '.js', '.ts']
        ignore_dirs: Set of directory names to skip (default: DEFAULT_IGNORE_DIRS)

    Returns:
        List[str]: Absolute paths to all matching files, sorted by path

    Raises:
        NotADirectoryError: If project_path is not a directory

    Example:
        >>> files = find_code_files('/path/to/project', extensions=['.py'])
        >>> print(f"Found {len(files)} Python files")
        Found 42 Python files
    """
    if not os.path.isdir(project_path):
        raise NotADirectoryError(f"Not a directory: {project_path}")

    # Set defaults
    if extensions is None:
        extensions = ['.py', '.js', '.ts']

    if ignore_dirs is None:
        ignore_dirs = DEFAULT_IGNORE_DIRS.copy()

    code_files: List[str] = []

    for root, dirs, files in os.walk(project_path):
        # Remove ignore directories from search
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Find matching files
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                full_path = os.path.join(root, file)
                code_files.append(full_path)

    return sorted(code_files)


def find_markdown_files(
    project_path: str,
    ignore_dirs: Set[str] = None
) -> List[str]:
    """
    Find all Markdown documentation files in a project.

    Args:
        project_path: Root directory to search
        ignore_dirs: Set of directory names to skip

    Returns:
        List[str]: Absolute paths to all .md files

    Example:
        >>> docs = find_markdown_files('/path/to/project')
        >>> print(f"Found {len(docs)} documentation files")
        Found 8 documentation files
    """
    return find_code_files(
        project_path,
        extensions=['.md'],
        ignore_dirs=ignore_dirs
    )


def find_test_files(
    project_path: str,
    language: str = 'python'
) -> List[str]:
    """
    Find test files based on common naming conventions.

    Args:
        project_path: Root directory to search
        language: Programming language ('python' or 'javascript')

    Returns:
        List[str]: Paths to test files

    Example:
        >>> tests = find_test_files('/path/to/project', 'python')
        >>> print(f"Found {len(tests)} test files")
        Found 15 test files
    """
    if language == 'python':
        extensions = ['.py']
    elif language in ['javascript', 'typescript']:
        extensions = ['.js', '.ts']
    else:
        extensions = ['.py']

    all_files = find_code_files(project_path, extensions)

    # Filter for test file naming patterns
    test_files = [
        f for f in all_files
        if any([
            'test_' in os.path.basename(f),
            '_test' in os.path.basename(f),
            '.test.' in os.path.basename(f),
            '.spec.' in os.path.basename(f),
        ])
    ]

    return test_files
