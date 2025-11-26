"""
Environment Configuration Validator Module

Validates environment variable configuration:
- .env.example template exists
- .env file is properly ignored (not committed)
"""

import os
from typing import Dict


def check_env_template(project_path: str) -> Dict:
    """
    Check if .env.example template exists and .env is properly ignored.

    Args:
        project_path: Root directory of project

    Returns:
        Dict containing:
            - env_example_exists: bool
            - env_exists: bool
            - env_in_gitignore: bool
            - passed: bool
            - issues: List[str]
            - message: str

    Example:
        >>> result = check_env_template('/path/to/project')
        >>> if result['env_exists'] and not result['env_in_gitignore']:
        ...     print("WARNING: .env file may be committed!")
    """
    env_example = os.path.join(project_path, '.env.example')
    env_file = os.path.join(project_path, '.env')
    gitignore = os.path.join(project_path, '.gitignore')

    env_example_exists = os.path.exists(env_example)
    env_exists = os.path.exists(env_file)

    # Check if .env is in .gitignore
    env_in_gitignore = False
    if os.path.exists(gitignore):
        with open(gitignore, 'r', encoding='utf-8') as f:
            content = f.read()
            env_in_gitignore = '.env' in content

    # Determine if passed
    passed = True
    issues = []

    if not env_example_exists:
        passed = False
        issues.append('Missing .env.example template')

    if env_exists and not env_in_gitignore:
        passed = False
        issues.append('WARNING: .env exists but not in .gitignore!')

    return {
        'env_example_exists': env_example_exists,
        'env_exists': env_exists,
        'env_in_gitignore': env_in_gitignore,
        'passed': passed,
        'issues': issues,
        'message': 'Environment configuration OK' if passed else
                   '; '.join(issues)
    }
