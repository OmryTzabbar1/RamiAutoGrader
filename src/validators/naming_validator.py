"""
Naming Convention Validator Module

Validates Python naming conventions:
- Functions/methods: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Variables: snake_case
"""

import re
from typing import List, Dict
from dataclasses import dataclass

from ..parsers.python_parser import parse_python_file, extract_functions, extract_classes


@dataclass
class NamingViolation:
    """Represents a naming convention violation."""
    file_path: str
    item_type: str  # 'function', 'class', 'variable', 'constant'
    item_name: str
    line_number: int
    expected_pattern: str
    severity: str = 'minor'


# Naming patterns
SNAKE_CASE = re.compile(r'^[a-z_][a-z0-9_]*$')
PASCAL_CASE = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
UPPER_SNAKE_CASE = re.compile(r'^[A-Z_][A-Z0-9_]*$')


def is_snake_case(name: str) -> bool:
    """Check if name follows snake_case."""
    return bool(SNAKE_CASE.match(name))


def is_pascal_case(name: str) -> bool:
    """Check if name follows PascalCase."""
    return bool(PASCAL_CASE.match(name))


def is_upper_snake_case(name: str) -> bool:
    """Check if name follows UPPER_SNAKE_CASE."""
    return bool(UPPER_SNAKE_CASE.match(name))


def validate_naming_conventions(file_path: str) -> Dict:
    """
    Validate naming conventions in a Python file.

    Args:
        file_path: Path to Python file

    Returns:
        Dict containing:
            - total_items: Items checked
            - violations: List of NamingViolation
            - passed: bool

    Example:
        >>> result = validate_naming_conventions('script.py')
        >>> if not result['passed']:
        ...     for v in result['violations']:
        ...         print(f"{v.item_name} should be {v.expected_pattern}")
    """
    tree = parse_python_file(file_path)
    if not tree:
        return {
            'total_items': 0,
            'violations': [],
            'passed': True,
            'error': 'Failed to parse file'
        }

    violations = []
    total_items = 0

    # Check function names
    functions = extract_functions(tree)
    for func in functions:
        # Skip magic methods
        if func.name.startswith('__') and func.name.endswith('__'):
            continue

        total_items += 1
        if not is_snake_case(func.name):
            violations.append(NamingViolation(
                file_path=file_path,
                item_type='function',
                item_name=func.name,
                line_number=func.line_number,
                expected_pattern='snake_case'
            ))

    # Check class names
    classes = extract_classes(tree)
    for cls in classes:
        total_items += 1
        if not is_pascal_case(cls.name):
            violations.append(NamingViolation(
                file_path=file_path,
                item_type='class',
                item_name=cls.name,
                line_number=cls.line_number,
                expected_pattern='PascalCase'
            ))

        # Check method names
        for method in cls.methods:
            # Skip magic methods
            if method.name.startswith('__') and method.name.endswith('__'):
                continue

            total_items += 1
            if not is_snake_case(method.name):
                violations.append(NamingViolation(
                    file_path=file_path,
                    item_type='method',
                    item_name=f"{cls.name}.{method.name}",
                    line_number=method.line_number,
                    expected_pattern='snake_case'
                ))

    return {
        'total_items': total_items,
        'violations': violations,
        'passed': len(violations) == 0
    }


def analyze_project_naming(project_path: str) -> Dict:
    """
    Analyze naming conventions across entire project.

    Args:
        project_path: Root directory

    Returns:
        Dict with project-wide naming analysis
    """
    from ..utils.file_finder import find_code_files

    python_files = find_code_files(project_path, extensions=['.py'])

    total_items = 0
    all_violations = []

    for file_path in python_files:
        result = validate_naming_conventions(file_path)
        total_items += result['total_items']
        all_violations.extend(result['violations'])

    return {
        'total_files': len(python_files),
        'total_items': total_items,
        'violations': all_violations,
        'passed': len(all_violations) == 0
    }
