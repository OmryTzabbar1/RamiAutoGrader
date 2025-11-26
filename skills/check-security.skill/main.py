"""
Check Security Skill

Comprehensive security scanning for academic software projects.
Detects hardcoded secrets, validates .gitignore, checks environment configuration.

This skill delegates heavy lifting to:
- src/analyzers/security_scanner.py
- src/validators/security_validator.py
"""

import sys
import os
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.security_scanner import scan_for_secrets
from src.validators.gitignore_validator import validate_gitignore
from src.validators.env_validator import check_env_template
from src.reporters.security_reporter import generate_security_report


def check_security(project_path: str, fail_on_secrets: bool = True) -> dict:
    """
    Run comprehensive security checks on a project.

    Args:
        project_path: Path to project directory
        fail_on_secrets: If True, return fail status if secrets found

    Returns:
        dict: Security scan results

    Example:
        >>> result = check_security('/path/to/project')
        >>> print(f"Security Score: {result['score']}/10")
    """
    print(f"[*] Security Scan: {project_path}")
    print("=" * 60)

    # 1. Scan for hardcoded secrets (CRITICAL)
    print("\n[*] Scanning for hardcoded secrets...")
    secrets = scan_for_secrets(project_path)

    if secrets:
        print(f"\n[X] CRITICAL: Found {len(secrets)} hardcoded secret(s)!")
        for secret in secrets:
            print(f"   {secret}")
    else:
        print("[+] No hardcoded secrets detected")

    # 2. Validate .gitignore
    print("\n[*] Validating .gitignore...")
    gitignore_result = validate_gitignore(project_path)

    if gitignore_result['passed']:
        print("[+] .gitignore properly configured")
    else:
        print(f"[!] {gitignore_result['message']}")
        if gitignore_result['missing_patterns']:
            print("   Missing patterns:")
            for pattern in gitignore_result['missing_patterns']:
                print(f"   - {pattern}")

    # 3. Check environment configuration
    print("\n[*] Checking environment configuration...")
    env_result = check_env_template(project_path)

    if env_result['passed']:
        print("[+] Environment configuration OK")
    else:
        print(f"[!] {env_result['message']}")

    # 4. Generate comprehensive report
    report = generate_security_report(secrets, gitignore_result, env_result)

    # 5. Display summary
    print("\n" + "=" * 60)
    print(f"Security Score: {report['score']}/{report['max_score']}")

    if report['passed']:
        print("[+] PASSED - No critical security issues")
    else:
        print("[X] FAILED - Critical security issues found")

        if fail_on_secrets and secrets:
            print("\n[!] CRITICAL: Hardcoded secrets = AUTO-FAIL")
            print("   Remove all secrets and use environment variables!")

    return report


def main():
    """Skill entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Security scanner for academic projects'
    )
    parser.add_argument(
        'project_path',
        help='Path to project directory'
    )
    parser.add_argument(
        '--fail_on_secrets',
        type=bool,
        default=True,
        help='Fail immediately if secrets found'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    # Run security check
    result = check_security(args.project_path, args.fail_on_secrets)

    # Output JSON if requested
    if args.json:
        print("\n" + json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
