"""
Security Pattern Definitions

Regular expression patterns for detecting hardcoded secrets and credentials.
Used by security scanner to identify critical security vulnerabilities.

Design Decision: Centralize patterns for easy maintenance and updates.
Adding new secret types only requires modifying this file.
"""

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
