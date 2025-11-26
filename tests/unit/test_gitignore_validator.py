"""
Unit tests for gitignore_validator module.

Tests .gitignore validation functionality.
"""

import pytest
from pathlib import Path
from src.validators.gitignore_validator import validate_gitignore


def test_validate_gitignore_valid(sample_gitignore):
    """Test validation of properly configured .gitignore."""
    result = validate_gitignore(Path(sample_gitignore).parent)

    assert result['passed'] is True
    assert result['has_gitignore'] is True
    assert len(result['missing_patterns']) == 0


def test_validate_gitignore_missing_file(temp_dir):
    """Test validation when .gitignore doesn't exist."""
    result = validate_gitignore(temp_dir)

    assert result['passed'] is False
    assert result['has_gitignore'] is False


def test_validate_gitignore_incomplete(temp_dir):
    """Test validation of incomplete .gitignore."""
    gitignore_path = Path(temp_dir) / ".gitignore"
    gitignore_path.write_text('''# Python
__pycache__/
*.pyc
''')

    result = validate_gitignore(temp_dir)

    assert result['has_gitignore'] is True
    # Should be missing some security patterns
    assert len(result['missing_patterns']) > 0


def test_validate_gitignore_required_patterns(sample_gitignore):
    """Test that all required patterns are checked."""
    result = validate_gitignore(Path(sample_gitignore).parent)

    required = ['.env', '*.key', '*.pem', 'credentials.json', 'secrets.yaml']
    # All should be present in a valid gitignore
    for pattern in required:
        assert pattern not in result['missing_patterns']


def test_validate_gitignore_message_format(sample_gitignore):
    """Test that result message is formatted correctly."""
    result = validate_gitignore(Path(sample_gitignore).parent)

    assert 'message' in result
    assert isinstance(result['message'], str)
    assert len(result['message']) > 0
