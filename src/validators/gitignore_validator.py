"""
GitIgnore Validator Module

Validates .gitignore file exists and contains required security patterns.
"""

import os
from typing import Dict, Set


REQUIRED_GITIGNORE_PATTERNS: Set[str] = {
    '.env',
    '*.key',
    'credentials.json',
    'secrets.yaml',
    '*.pem',
}


def validate_gitignore(project_path: str) -> Dict:
    """
    Validate .gitignore file exists and contains security patterns.

    Args:
        project_path: Root directory of project

    Returns:
        Dict containing:
            - exists: bool
            - missing_patterns: List of required patterns not found
            - passed: bool
            - message: str

    Example:
        >>> result = validate_gitignore('/path/to/project')
        >>> if not result['passed']:
        ...     print(f"Missing: {result['missing_patterns']}")
    """
    gitignore_path = os.path.join(project_path, '.gitignore')

    if not os.path.exists(gitignore_path):
        return {
            'exists': False,
            'missing_patterns': list(REQUIRED_GITIGNORE_PATTERNS),
            'passed': False,
            'message': '.gitignore file not found'
        }

    # Read .gitignore
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required patterns
    missing = []
    for pattern in REQUIRED_GITIGNORE_PATTERNS:
        if pattern not in content:
            missing.append(pattern)

    return {
        'exists': True,
        'missing_patterns': missing,
        'passed': len(missing) == 0,
        'message': 'Valid .gitignore' if len(missing) == 0 else
                   f'Missing {len(missing)} required patterns'
    }
