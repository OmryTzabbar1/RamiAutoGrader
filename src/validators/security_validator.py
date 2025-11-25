"""
Security Validator Module

Validates security best practices:
- .gitignore exists and contains required patterns
- .env.example template exists
- .env file is properly ignored (not committed)
"""

import os
from typing import List, Dict, Set


REQUIRED_GITIGNORE_PATTERNS = {
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


def check_env_template(project_path: str) -> Dict:
    """
    Check if .env.example template exists.

    Args:
        project_path: Root directory of project

    Returns:
        Dict containing:
            - env_example_exists: bool
            - env_exists: bool
            - env_in_gitignore: bool
            - passed: bool

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


def generate_security_report(
    secrets_found: List,
    gitignore_result: Dict,
    env_result: Dict
) -> Dict:
    """
    Generate comprehensive security validation report.

    Args:
        secrets_found: List of SecretFinding objects
        gitignore_result: Result from validate_gitignore()
        env_result: Result from check_env_template()

    Returns:
        Dict containing complete security assessment

    Example:
        >>> report = generate_security_report(secrets, gi, env)
        >>> if not report['passed']:
        ...     print(f"Security Score: {report['score']}/10 - FAILED")
    """
    # Critical: Any secrets = auto-fail
    has_secrets = len(secrets_found) > 0

    score = 10  # Start with perfect score

    if has_secrets:
        score = 0  # Auto-fail for secrets
    else:
        if not gitignore_result['passed']:
            score -= 3
        if not env_result['passed']:
            score -= 2

    return {
        'passed': not has_secrets and gitignore_result['passed'] and env_result['passed'],
        'score': max(0, score),
        'max_score': 10,
        'secrets_found': len(secrets_found),
        'gitignore_valid': gitignore_result['passed'],
        'env_config_valid': env_result['passed'],
        'critical_issues': secrets_found,
        'warnings': gitignore_result.get('missing_patterns', []) + env_result.get('issues', [])
    }
