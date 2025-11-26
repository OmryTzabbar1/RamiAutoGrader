"""
Security Scanner Module

Detects hardcoded secrets and security vulnerabilities in source code.
This is a CRITICAL security check - hardcoded secrets result in auto-fail.

Key Features:
- Regex-based secret detection
- Multiple secret types (API keys, passwords, tokens, AWS keys, etc.)
- Line-level reporting for easy fixing
"""

import re
from typing import List

from ..utils.file_finder import find_code_files
from ..models.code_models import SecretFinding
from .security_patterns import SECRET_PATTERNS, EXCEPTION_PATTERNS


def scan_for_secrets(
    project_path: str,
    extensions: List[str] = None
) -> List[SecretFinding]:
    """
    Scan project for hardcoded secrets.

    Args:
        project_path: Root directory to scan
        extensions: File extensions to scan (default: ['.py', '.js', '.ts'])

    Returns:
        List[SecretFinding]: All detected secrets

    Example:
        >>> findings = scan_for_secrets('/path/to/project')
        >>> if findings:
        ...     print(f"CRITICAL: Found {len(findings)} hardcoded secrets!")
        CRITICAL: Found 2 hardcoded secrets!
    """
    if extensions is None:
        extensions = ['.py', '.js', '.ts', '.env', '.yaml', '.yml', '.json']

    code_files = find_code_files(project_path, extensions=extensions)
    findings = []

    for file_path in code_files:
        # Skip .env.example files (they're supposed to have placeholders)
        if file_path.endswith('.env.example'):
            continue

        # Skip test fixtures (they contain intentional test data)
        if '/fixtures/' in file_path.replace('\\', '/') or '\\fixtures\\' in file_path:
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            findings.extend(_scan_file(file_path, lines))

        except Exception as e:
            print(f"Warning: Could not scan {file_path}: {e}")
            continue

    return findings


def _scan_file(file_path: str, lines: List[str]) -> List[SecretFinding]:
    """Scan a single file for secrets."""
    findings = []

    for line_num, line in enumerate(lines, start=1):
        for secret_type, patterns in SECRET_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)

                for match in matches:
                    # Check if it's an exception (placeholder)
                    if _is_exception(match.group(0)):
                        continue

                    finding = SecretFinding(
                        secret_type=secret_type,
                        file_path=file_path,
                        line_number=line_num,
                        snippet=line.strip()
                    )
                    findings.append(finding)

    return findings


def _is_exception(text: str) -> bool:
    """Check if matched text is a known exception/placeholder."""
    for exception_pattern in EXCEPTION_PATTERNS:
        if re.search(exception_pattern, text, re.IGNORECASE):
            return True
    return False
