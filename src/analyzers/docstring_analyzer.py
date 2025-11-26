"""
Docstring Analyzer Module

Analyzes docstring coverage in Python code.
Academic requirement: 90% of functions/classes must have docstrings.

Uses AST parsing for accurate detection.
"""

from typing import List, Dict

from ..models.code_models import DocstringViolation
from ..parsers.python_parser import (
    parse_python_file,
    extract_functions,
    extract_classes,
    get_module_docstring
)
from ..utils.file_finder import find_code_files


def _should_check_function(func_name: str) -> bool:
    """Determine if function should be checked for docstring."""
    return not (func_name.startswith('_') and not func_name.startswith('__'))


def _should_check_method(method_name: str) -> bool:
    """Determine if method should be checked for docstring."""
    return not (method_name.startswith('_') and method_name != '__init__')


def check_docstrings(file_path: str) -> Dict:
    """
    Check docstring coverage in a Python file.

    Args:
        file_path: Path to Python file

    Returns:
        Dict containing total_items, missing, coverage, violations

    Example:
        >>> result = check_docstrings('script.py')
        >>> print(f"Coverage: {result['coverage']:.1%}")
    """
    tree = parse_python_file(file_path)
    if not tree:
        return {'total_items': 0, 'missing': 0, 'coverage': 0.0,
                'violations': [], 'error': 'Failed to parse file'}

    violations = []
    total_items = 1  # Module counts as 1

    # Check module docstring
    if not get_module_docstring(tree):
        violations.append(DocstringViolation(
            file_path, 'module', '<module>', 1))

    # Check functions
    for func in extract_functions(tree):
        if not _should_check_function(func.name):
            continue
        total_items += 1
        if not func.has_docstring:
            violations.append(DocstringViolation(
                file_path, 'function', func.name, func.line_number))

    # Check classes and methods
    for cls in extract_classes(tree):
        total_items += 1
        if not cls.has_docstring:
            violations.append(DocstringViolation(
                file_path, 'class', cls.name, cls.line_number))

        for method in cls.methods:
            if not _should_check_method(method.name):
                continue
            total_items += 1
            if not method.has_docstring:
                violations.append(DocstringViolation(
                    file_path, 'method',
                    f"{cls.name}.{method.name}", method.line_number))

    coverage = 1.0 - (len(violations) / total_items) if total_items > 0 else 0.0

    return {
        'total_items': total_items,
        'missing': len(violations),
        'coverage': coverage,
        'violations': violations
    }


def analyze_project_docstrings(
    project_path: str,
    min_coverage: float = 0.9
) -> Dict:
    """
    Analyze docstring coverage across entire project.

    Args:
        project_path: Root directory
        min_coverage: Minimum acceptable coverage (default: 0.9 = 90%)

    Returns:
        Dict with project-wide docstring analysis

    Example:
        >>> result = analyze_project_docstrings('/path/to/project')
        >>> if result['passed']:
        ...     print(f"Coverage: {result['coverage']:.1%}")
    """
    python_files = find_code_files(project_path, extensions=['.py'])

    total_items = 0
    total_missing = 0
    all_violations = []

    for file_path in python_files:
        result = check_docstrings(file_path)

        total_items += result['total_items']
        total_missing += result['missing']
        all_violations.extend(result['violations'])

    overall_coverage = 1.0 - (total_missing / total_items) if total_items > 0 else 0.0

    return {
        'total_files': len(python_files),
        'total_items': total_items,
        'missing': total_missing,
        'coverage': overall_coverage,
        'passed': overall_coverage >= min_coverage,
        'violations': all_violations
    }
