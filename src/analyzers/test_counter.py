"""
Test Counter Module

Counts and analyzes test functions in test files.
Provides metrics for test quality evaluation.
"""

import re
from typing import Dict


def count_python_tests(file_path: str) -> int:
    """
    Count test functions in a Python test file.

    Args:
        file_path: Path to test file

    Returns:
        int: Number of test functions found

    Example:
        >>> count = count_python_tests('test_example.py')
        >>> print(f"Found {count} tests")
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Match test function definitions
        test_pattern = r'^\s*def\s+(test_\w+)\s*\('
        tests = re.findall(test_pattern, content, re.MULTILINE)

        return len(tests)
    except Exception:
        return 0


def analyze_test_file(file_path: str) -> Dict:
    """
    Analyze a single test file for quality metrics.

    Args:
        file_path: Path to test file

    Returns:
        Dict with test metrics (num_tests, num_assertions, has_docstrings, lines)

    Example:
        >>> metrics = analyze_test_file('test_example.py')
        >>> print(f"Tests: {metrics['num_tests']}, Assertions: {metrics['num_assertions']}")
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        num_tests = count_python_tests(file_path)

        # Count assertions (simple heuristic)
        assertions = len(re.findall(r'\bassert\b', content))

        # Check for docstrings in tests
        has_docstrings = bool(re.search(r'def test_\w+\([^)]*\):\s*"""', content))

        return {
            'file_path': file_path,
            'num_tests': num_tests,
            'num_assertions': assertions,
            'has_docstrings': has_docstrings,
            'lines': len(content.split('\n'))
        }
    except Exception as e:
        return {
            'file_path': file_path,
            'error': str(e)
        }
