"""
Security Report Generator Module

Generates comprehensive security validation reports.
"""

from typing import List, Dict


def generate_security_report(
    secrets_found: List,
    gitignore_result: Dict,
    env_result: Dict
) -> Dict:
    """
    Generate comprehensive security validation report.

    Aggregates results from:
    - Secret scanning
    - .gitignore validation
    - Environment configuration check

    Args:
        secrets_found: List of SecretFinding objects
        gitignore_result: Result from validate_gitignore()
        env_result: Result from check_env_template()

    Returns:
        Dict containing:
            - passed: bool (overall pass/fail)
            - score: int (0-10)
            - max_score: int (always 10)
            - secrets_found: int (count)
            - gitignore_valid: bool
            - env_config_valid: bool
            - critical_issues: List (secrets)
            - warnings: List[str]

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
        'warnings': gitignore_result.get('missing_patterns', []) +
                   env_result.get('issues', [])
    }
