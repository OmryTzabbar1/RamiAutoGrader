"""
File Utilities Module

Provides safe file reading operations with proper error handling and size limits.
Used by various grading skills to access project files securely.

Key Features:
- Size-limited file reading to prevent memory issues
- Encoding error handling
- Detailed error messages for debugging
"""

import os
from typing import Optional


class FileSizeError(Exception):
    """Raised when file exceeds maximum allowed size."""
    pass


class FileEncodingError(Exception):
    """Raised when file cannot be decoded with common encodings."""
    pass


def safe_read_file(
    file_path: str,
    max_size_mb: int = 10,
    encoding: str = 'utf-8'
) -> str:
    """
    Safely read a file with size limits and encoding fallback.

    Prevents reading excessively large files that could cause memory issues.
    Attempts multiple encodings if the default fails.

    Args:
        file_path: Absolute path to the file to read
        max_size_mb: Maximum file size in megabytes (default: 10)
        encoding: Primary encoding to try (default: 'utf-8')

    Returns:
        str: File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
        FileSizeError: If file exceeds max_size_mb
        FileEncodingError: If file can't be decoded with any encoding
        PermissionError: If file can't be read due to permissions

    Example:
        >>> content = safe_read_file('/path/to/file.py')
        >>> print(f"Read {len(content)} characters")
        Read 1234 characters
    """
    # Check file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check file size
    size_bytes = os.path.getsize(file_path)
    max_bytes = max_size_mb * 1024 * 1024

    if size_bytes > max_bytes:
        raise FileSizeError(
            f"File {file_path} is {size_bytes / 1024 / 1024:.2f}MB, "
            f"exceeds {max_size_mb}MB limit"
        )

    # Try reading with primary encoding
    encodings_to_try = [encoding, 'utf-8', 'latin-1', 'cp1252']

    for enc in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except PermissionError as e:
            raise PermissionError(
                f"Permission denied reading {file_path}: {e}"
            )

    # All encodings failed
    raise FileEncodingError(
        f"Could not decode {file_path} with encodings: {encodings_to_try}"
    )


def file_exists(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: Path to check

    Returns:
        bool: True if file exists, False otherwise

    Example:
        >>> if file_exists('README.md'):
        ...     print("README found")
        README found
    """
    return os.path.isfile(file_path)


def get_file_size_bytes(file_path: str) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to file

    Returns:
        int: File size in bytes

    Raises:
        FileNotFoundError: If file doesn't exist

    Example:
        >>> size = get_file_size_bytes('script.py')
        >>> print(f"File is {size} bytes")
        File is 2048 bytes
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return os.path.getsize(file_path)
