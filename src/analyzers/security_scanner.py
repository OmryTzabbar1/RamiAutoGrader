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
import os
from typing import List, Dict
from dataclasses import dataclass

from ..utils.file_finder import find_code_files


# Secret detection patterns (regex)
SECRET_PATTERNS = {
    'api_key': [
        r'(api[_-]?key|apikey)\s*[=:]\s*["\']([^"\']{20,})["\']',
        r'key\s*[=:]\s*["\']([A-Za-z0-9]{32,})["\']',
    ],
    'password': [
        r'(password|passwd|pwd)\s*[=:]\s*["\']([^"\']{8,})["\']',
    ],
    'secret': [
        r'(secret|token)\s*[=:]\s*["\']([^"\']{20,})["\']',
    ],
    'aws_key': [
        r'(AKIA[0-9A-Z]{16})',  # AWS Access Key pattern
    ],
    'private_key': [
        r'-----BEGIN (RSA|EC|OPENSSH|DSA|PGP) PRIVATE KEY-----',
    ],
    'github_token': [
        r'(ghp_[a-zA-Z0-9]{36})',  # GitHub Personal Access Token
    ],
    'slack_token': [
        r'(xox[pboa]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24,32})',
    ],
}

# Exceptions - patterns that look like secrets but aren't
EXCEPTION_PATTERNS = [
    r'your_key_here',
    r'your_.*_here',
    r'example',
    r'dummy',
    r'fake',
    r'test',
    r'placeholder',
    r'<.*>',
    r'\{.*\}',
]


@dataclass
class SecretFinding:
    """
    Represents a detected secret in code.

    Attributes:
        secret_type: Type of secret (e.g., 'api_key', 'password')
        file_path: File containing the secret
        line_number: Line number where secret was found
        snippet: Code snippet showing the secret (truncated)
        severity: Always 'critical' for secrets
    """
    secret_type: str
    file_path: str
    line_number: int
    snippet: str
    severity: str = 'critical'

    def __str__(self) -> str:
        return (
            f"{self.file_path}:{self.line_number} - "
            f"{self.secret_type}: {self.snippet[:60]}..."
        )


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
