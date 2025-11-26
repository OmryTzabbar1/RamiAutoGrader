"""
Unit tests for grading_utils module.

Tests grade calculation and result formatting.
"""

import pytest
from src.core.grading_utils import calculate_grade, format_results_summary


class TestCalculateGrade:
    """Tests for calculate_grade function."""

    def test_grade_a(self):
        """Test A grade (90-100)."""
        assert calculate_grade(90) == 'A'
        assert calculate_grade(95) == 'A'
        assert calculate_grade(100) == 'A'

    def test_grade_b(self):
        """Test B grade (80-89)."""
        assert calculate_grade(80) == 'B'
        assert calculate_grade(85) == 'B'
        assert calculate_grade(89) == 'B'

    def test_grade_c(self):
        """Test C grade (70-79)."""
        assert calculate_grade(70) == 'C'
        assert calculate_grade(75) == 'C'
        assert calculate_grade(79) == 'C'

    def test_grade_d(self):
        """Test D grade (60-69)."""
        assert calculate_grade(60) == 'D'
        assert calculate_grade(65) == 'D'
        assert calculate_grade(69) == 'D'

    def test_grade_f(self):
        """Test F grade (0-59)."""
        assert calculate_grade(0) == 'F'
        assert calculate_grade(30) == 'F'
        assert calculate_grade(59) == 'F'

    def test_grade_boundary_values(self):
        """Test boundary values."""
        assert calculate_grade(89.9) == 'B'
        assert calculate_grade(90.0) == 'A'
        assert calculate_grade(79.9) == 'C'
        assert calculate_grade(80.0) == 'B'


class TestFormatResultsSummary:
    """Tests for format_results_summary function."""

    @pytest.fixture
    def sample_results(self):
        """Create sample grading results."""
        return {
            'total_score': 75.0,
            'max_score': 100,
            'percentage': 75.0,
            'grade': 'C',
            'passed': True,
            'results': {
                'security': {'score': 10, 'max_score': 10},
                'code_quality': {'score': 25, 'max_score': 30},
                'documentation': {'score': 20, 'max_score': 25},
                'testing': {'score': 10, 'max_score': 15},
                'git': {'score': 8, 'max_score': 10},
                'research': {'score': 7, 'max_score': 10}
            }
        }

    def test_format_contains_category_scores(self, sample_results):
        """Test that formatted summary contains all category scores."""
        summary = format_results_summary(sample_results)

        assert 'Security:' in summary
        assert 'Code Quality:' in summary
        assert 'Documentation:' in summary
        assert 'Testing:' in summary
        assert 'Git Workflow:' in summary
        assert 'Research:' in summary

    def test_format_contains_total_score(self, sample_results):
        """Test that total score is included."""
        summary = format_results_summary(sample_results)

        assert 'TOTAL:' in summary
        assert '75.0' in summary
        assert '/ 100' in summary

    def test_format_contains_grade(self, sample_results):
        """Test that grade is included."""
        summary = format_results_summary(sample_results)

        assert 'GRADE:' in summary
        assert 'C' in summary

    def test_format_contains_status(self, sample_results):
        """Test that pass/fail status is included."""
        summary = format_results_summary(sample_results)

        assert 'STATUS:' in summary
        assert 'PASSED' in summary

    def test_format_failed_status(self, sample_results):
        """Test formatting for failed results."""
        sample_results['total_score'] = 50.0
        sample_results['passed'] = False
        sample_results['grade'] = 'F'

        summary = format_results_summary(sample_results)

        assert 'FAILED' in summary

    def test_format_has_separators(self, sample_results):
        """Test that summary has visual separators."""
        summary = format_results_summary(sample_results)

        assert '=' in summary  # Header/footer separator
        assert '-' in summary  # Score separator
