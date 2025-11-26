"""
Unit tests for file_size_analyzer module.

Tests the 150-line file size limit enforcement.
"""

import pytest
from pathlib import Path
from src.analyzers.file_size_analyzer import check_file_sizes, generate_size_report


def test_check_file_sizes_no_violations(sample_python_file):
    """Test that small files pass the size check."""
    violations = check_file_sizes(Path(sample_python_file).parent, limit=150)
    assert len(violations) == 0


def test_check_file_sizes_with_violations(large_python_file):
    """Test that large files are detected as violations."""
    violations = check_file_sizes(Path(large_python_file).parent, limit=150)
    assert len(violations) > 0
    assert any('large.py' in v['file'] for v in violations)


def test_check_file_sizes_custom_limit(sample_python_file):
    """Test custom line limit."""
    violations = check_file_sizes(Path(sample_python_file).parent, limit=10)
    assert len(violations) > 0  # Sample file should exceed 10 lines


def test_check_file_sizes_violation_details(large_python_file):
    """Test that violation details are correct."""
    violations = check_file_sizes(Path(large_python_file).parent, limit=150)
    violation = violations[0]

    assert 'file' in violation
    assert 'lines' in violation
    assert 'limit' in violation
    assert 'excess' in violation
    assert violation['lines'] > violation['limit']
    assert violation['excess'] == violation['lines'] - violation['limit']


def test_generate_size_report_no_violations(sample_python_file):
    """Test report generation with no violations."""
    violations = check_file_sizes(Path(sample_python_file).parent, limit=150)
    report = generate_size_report(violations)

    assert "0 files exceed" in report or "No violations" in report.lower()


def test_generate_size_report_with_violations(large_python_file):
    """Test report generation with violations."""
    violations = check_file_sizes(Path(large_python_file).parent, limit=150)
    report = generate_size_report(violations)

    assert "large.py" in report
    assert "lines" in report.lower()


def test_check_file_sizes_empty_directory(temp_dir):
    """Test that empty directories return no violations."""
    violations = check_file_sizes(temp_dir, limit=150)
    assert len(violations) == 0


def test_check_file_sizes_nonexistent_path():
    """Test handling of nonexistent paths."""
    violations = check_file_sizes("/nonexistent/path", limit=150)
    assert len(violations) == 0  # Should handle gracefully
