"""
Unit tests for security_scanner module.

Tests hardcoded secret detection functionality.
"""

import pytest
from src.analyzers.security_scanner import scan_for_secrets


def test_scan_for_secrets_clean_file(sample_python_file):
    """Test that clean files return no secrets."""
    from pathlib import Path
    secrets = scan_for_secrets(Path(sample_python_file).parent)
    assert len(secrets) == 0


def test_scan_for_secrets_detects_api_keys(file_with_secrets):
    """Test detection of API keys."""
    from pathlib import Path
    secrets = scan_for_secrets(Path(file_with_secrets).parent)

    assert len(secrets) > 0
    assert any('API_KEY' in s['context'] or 'sk-' in s['context'] for s in secrets)


def test_scan_for_secrets_detects_passwords(file_with_secrets):
    """Test detection of passwords."""
    from pathlib import Path
    secrets = scan_for_secrets(Path(file_with_secrets).parent)

    assert any('PASSWORD' in s['context'] or 'supersecret' in s['context'] for s in secrets)


def test_scan_for_secrets_detects_aws_keys(file_with_secrets):
    """Test detection of AWS access keys."""
    from pathlib import Path
    secrets = scan_for_secrets(Path(file_with_secrets).parent)

    assert any('AKIA' in s['context'] or 'aws_access_key_id' in s['context'] for s in secrets)


def test_secret_result_structure(file_with_secrets):
    """Test that secret results have correct structure."""
    from pathlib import Path
    secrets = scan_for_secrets(Path(file_with_secrets).parent)

    assert len(secrets) > 0
    secret = secrets[0]

    assert 'file' in secret
    assert 'line' in secret
    assert 'type' in secret
    assert 'context' in secret


def test_scan_empty_directory(temp_dir):
    """Test scanning empty directory."""
    secrets = scan_for_secrets(temp_dir)
    assert len(secrets) == 0


def test_scan_nonexistent_path():
    """Test handling of nonexistent paths."""
    secrets = scan_for_secrets("/nonexistent/path")
    assert len(secrets) == 0  # Should handle gracefully
