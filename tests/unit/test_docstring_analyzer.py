"""
Unit tests for docstring_analyzer module.

Tests docstring coverage analysis functionality.
"""

import pytest
from src.analyzers.docstring_analyzer import (
    analyze_project_docstrings,
    check_docstrings
)


def test_analyze_project_with_good_docstrings(sample_python_file):
    """Test analysis of file with complete docstrings."""
    from pathlib import Path
    result = analyze_project_docstrings(Path(sample_python_file).parent, min_coverage=0.9)

    assert result['passed'] is True
    assert result['coverage'] >= 0.9
    assert result['total_items'] > 0
    assert result['documented_items'] > 0


def test_analyze_project_with_missing_docstrings(sample_python_file_no_docstrings):
    """Test analysis of file with missing docstrings."""
    from pathlib import Path
    result = analyze_project_docstrings(
        Path(sample_python_file_no_docstrings).parent,
        min_coverage=0.9
    )

    assert result['passed'] is False
    assert result['coverage'] < 0.9
    assert len(result['missing']) > 0


def test_check_docstrings_complete(sample_python_file):
    """Test checking a file with all docstrings."""
    result = check_docstrings(sample_python_file)

    assert result['total'] > 0
    assert result['documented'] == result['total']
    assert result['coverage'] == 1.0
    assert len(result['missing']) == 0


def test_check_docstrings_incomplete(sample_python_file_no_docstrings):
    """Test checking a file with missing docstrings."""
    result = check_docstrings(sample_python_file_no_docstrings)

    assert result['total'] > 0
    assert result['documented'] < result['total']
    assert result['coverage'] < 1.0
    assert len(result['missing']) > 0


def test_docstring_coverage_calculation(sample_python_file_no_docstrings):
    """Test that coverage is calculated correctly."""
    result = check_docstrings(sample_python_file_no_docstrings)

    expected_coverage = result['documented'] / result['total']
    assert result['coverage'] == pytest.approx(expected_coverage)


def test_missing_items_format(sample_python_file_no_docstrings):
    """Test that missing items are properly formatted."""
    result = check_docstrings(sample_python_file_no_docstrings)

    for missing in result['missing']:
        assert 'file' in missing
        assert 'type' in missing
        assert 'name' in missing


def test_analyze_empty_directory(temp_dir):
    """Test analysis of directory with no Python files."""
    result = analyze_project_docstrings(temp_dir, min_coverage=0.9)

    assert result['total_items'] == 0
    assert result['coverage'] == 1.0  # No items = perfect coverage
    assert result['passed'] is True
