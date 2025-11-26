"""
Docstring Analyzer Module

Analyzes docstring coverage in Python code.
Academic requirement: 90% of functions/classes must have docstrings.

Uses AST parsing for accurate detection.
"""

from typing import List, Dict
from dataclasses import dataclass

from ..parsers.python_parser import (
    parse_python_file,
    extract_functions,
    extract_classes,
    get_module_docstring
)
from ..utils.file_finder import find_code_files


@dataclass
class DocstringViolation:
    """Represents a missing docstring."""
    file_path: str
    item_type: str  # 'module', 'function', 'class', 'method'
    item_name: str
    line_number: int


def check_docstrings(file_path: str) -> Dict:
    """
    Check docstring coverage in a Python file.

    Args:
        file_path: Path to Python file

    Returns:
        Dict containing:
            - total_items: Number of items checked
            - missing: Number without docstrings
            - coverage: Percentage (0.0-1.0)
            - violations: List of DocstringViolation

    Example:
        >>> result = check_docstrings('script.py')
        >>> print(f"Coverage: {result['coverage']:.1%}")
        Coverage: 85.5%
    """
    tree = parse_python_file(file_path)
    if not tree:
        return {
            'total_items': 0,
            'missing': 0,
            'coverage': 0.0,
            'violations': [],
            'error': 'Failed to parse file'
        }

    violations = []
    total_items = 0

    # Check module docstring
    total_items += 1
    if not get_module_docstring(tree):
        violations.append(DocstringViolation(
            file_path=file_path,
            item_type='module',
            item_name='<module>',
            line_number=1
        ))

    # Check functions
    functions = extract_functions(tree)
    for func in functions:
        # Skip private/dunder functions
        if func.name.startswith('_') and not func.name.startswith('__'):
            continue

        total_items += 1
        if not func.has_docstring:
            violations.append(DocstringViolation(
                file_path=file_path,
                item_type='function',
                item_name=func.name,
                line_number=func.line_number
            ))

    # Check classes and their methods
    classes = extract_classes(tree)
    for cls in classes:
        total_items += 1
        if not cls.has_docstring:
            violations.append(DocstringViolation(
                file_path=file_path,
                item_type='class',
                item_name=cls.name,
                line_number=cls.line_number
            ))

        # Check methods
        for method in cls.methods:
            # Skip private methods except __init__
            if method.name.startswith('_') and method.name != '__init__':
                continue

            total_items += 1
            if not method.has_docstring:
                violations.append(DocstringViolation(
                    file_path=file_path,
                    item_type='method',
                    item_name=f"{cls.name}.{method.name}",
                    line_number=method.line_number
                ))

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
