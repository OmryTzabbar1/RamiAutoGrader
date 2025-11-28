"""
Unit tests for generate-summary skill.

Tests cover:
- Valid summary generation
- Perfect score handling
- Failing score handling
- Error handling (file not found, invalid JSON, API errors)
- Summary validation (length, format)
"""

import os
import pytest
import json
from unittest.mock import Mock, patch, mock_open
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../skills/generate-summary/scripts'))

from summarize_report import (
    generate_summary,
    validate_summary,
    load_grading_report,
    format_prompt
)


class TestValidateSummary:
    """Test summary validation logic."""

    def test_valid_summary(self):
        """Test validation of correct summary."""
        summary = "Score: 77/100. Strong documentation and security. Fix: 2 files exceed 150 lines; increase test coverage to 70%+."
        result = validate_summary(summary)

        assert result["valid"] is True
        assert result["word_count"] == 23
        assert len(result["issues"]) == 0

    def test_summary_too_short(self):
        """Test validation fails for too short summary."""
        summary = "Score: 77/100. Good work but needs improvement."
        result = validate_summary(summary)

        assert result["valid"] is False
        assert "Too short" in result["issues"][0]
        assert result["word_count"] < 30

    def test_summary_too_long(self):
        """Test validation fails for too long summary."""
        summary = "Score: 77/100. " + " ".join(["word"] * 50)
        result = validate_summary(summary)

        assert result["valid"] is False
        assert "Too long" in result["issues"][0]
        assert result["word_count"] > 50

    def test_summary_missing_score_prefix(self):
        """Test validation fails when summary doesn't start with 'Score:'."""
        summary = "Strong documentation and security. Fix 2 files that exceed 150 lines and increase test coverage to 70 percent or higher."
        result = validate_summary(summary)

        assert result["valid"] is False
        assert "Does not start with 'Score:'" in result["issues"]

    def test_summary_has_markdown(self):
        """Test validation fails when summary contains markdown."""
        summary = "Score: 77/100. **Strong** documentation. Fix: increase coverage."
        result = validate_summary(summary)

        assert result["valid"] is False
        assert "Contains markdown formatting" in result["issues"]


class TestLoadGradingReport:
    """Test grading report loading."""

    def test_load_valid_report(self):
        """Test loading valid JSON grading report."""
        mock_data = {
            "total_score": 77,
            "max_score": 100,
            "category_scores": {"documentation": 25, "code_quality": 20}
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            report = load_grading_report("test_report.json")

            assert report["total_score"] == 77
            assert report["max_score"] == 100
            assert report["category_scores"]["documentation"] == 25

    def test_load_invalid_json(self):
        """Test loading invalid JSON raises error."""
        with patch("builtins.open", mock_open(read_data="not valid json")):
            with pytest.raises(json.JSONDecodeError):
                load_grading_report("invalid.json")


class TestFormatPrompt:
    """Test prompt formatting."""

    def test_format_prompt_complete_report(self):
        """Test prompt formatting with complete grading report."""
        report = {
            "total_score": 77,
            "max_score": 100,
            "category_scores": {
                "documentation": 25,
                "code_quality": 20,
                "testing": 10
            },
            "violations": [
                "src/analyzer.py: 182 lines",
                "Test coverage: 67%"
            ],
            "strengths": [
                "Excellent documentation",
                "No hardcoded secrets"
            ]
        }

        prompt = format_prompt(report)

        assert "Total Score: 77/100" in prompt
        assert "documentation: 25" in prompt
        assert "src/analyzer.py: 182 lines" in prompt
        assert "Excellent documentation" in prompt
        assert "30-50 words STRICT" in prompt

    def test_format_prompt_minimal_report(self):
        """Test prompt formatting with minimal report (no violations/strengths)."""
        report = {
            "total_score": 50,
            "max_score": 100,
            "category_scores": {"documentation": 10}
        }

        prompt = format_prompt(report)

        assert "Total Score: 50/100" in prompt
        assert "Violations:\nNone" in prompt
        assert "Strengths:\nNone" in prompt


class TestGenerateSummary:
    """Test full summary generation workflow."""

    def test_file_not_found(self):
        """Test handling of missing grading report file."""
        result = generate_summary("/nonexistent/path/to/report.json")

        assert result == "Error: Grading report not found. Cannot generate feedback summary."

    def test_corrupted_json(self):
        """Test handling of corrupted JSON file."""
        with patch("builtins.open", mock_open(read_data="not valid json")):
            with patch("os.path.exists", return_value=True):
                result = generate_summary("corrupted.json")

                assert result == "Error: Grading report is corrupted. Cannot parse JSON."

    @patch('anthropic.Anthropic')
    def test_successful_summary_generation(self, mock_anthropic):
        """Test successful summary generation."""
        mock_data = {
            "total_score": 77,
            "max_score": 100,
            "category_scores": {
                "documentation": 25,
                "code_quality": 20,
                "testing": 10,
                "security": 10,
                "git": 7,
                "research": 5
            },
            "violations": [
                "src/analyzer.py: 182 lines (exceeds 150 limit)",
                "Test coverage: 67% (below 70% minimum)"
            ],
            "strengths": [
                "Excellent documentation coverage",
                "No hardcoded secrets found"
            ]
        }

        mock_content = Mock()
        mock_content.text = "Score: 77/100. Strong documentation (25/25) and excellent security practices (10/10). Code quality needs improvement: 2 files exceed 150-line limit. Increase test coverage from 67% to 70%."

        mock_message = Mock()
        mock_message.content = [mock_content]

        mock_client = Mock()
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client

        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("os.path.exists", return_value=True):
                with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                    result = generate_summary("test_report.json")

                    assert result.startswith("Score: 77/100")
                    assert "documentation" in result.lower()
                    assert "test coverage" in result.lower()
                    word_count = len(result.split())
                    assert 30 <= word_count <= 50

    @patch('anthropic.Anthropic')
    def test_api_error_with_retries(self, mock_anthropic):
        """Test API error handling with retries."""
        mock_data = {
            "total_score": 77,
            "max_score": 100,
            "category_scores": {"documentation": 25}
        }

        from anthropic import APIError
        mock_client = Mock()
        mock_client.messages.create.side_effect = APIError("API Error")
        mock_anthropic.return_value = mock_client

        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("os.path.exists", return_value=True):
                with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                    with patch('time.sleep'):  # Skip sleep in tests
                        result = generate_summary("test_report.json")

                        assert "Error: Failed to generate summary" in result
                        assert mock_client.messages.create.call_count == 3  # 3 retries

    @patch('anthropic.Anthropic')
    def test_invalid_summary_fallback(self, mock_anthropic):
        """Test fallback when summary validation fails."""
        mock_data = {
            "total_score": 77,
            "max_score": 100,
            "category_scores": {"documentation": 25}
        }

        # Return too short summary
        mock_content = Mock()
        mock_content.text = "Score: 77/100. Good."  # Only 4 words

        mock_message = Mock()
        mock_message.content = [mock_content]

        mock_client = Mock()
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client

        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("os.path.exists", return_value=True):
                with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                    result = generate_summary("test_report.json")

                    # Should use fallback after max retries
                    assert "Score: 77/100" in result
                    assert "See detailed report" in result

    @patch('anthropic.Anthropic')
    def test_perfect_score_summary(self, mock_anthropic):
        """Test summary generation for perfect score."""
        mock_data = {
            "total_score": 100,
            "max_score": 100,
            "category_scores": {
                "documentation": 25,
                "code_quality": 30,
                "testing": 15,
                "security": 10,
                "git": 10,
                "research": 10
            },
            "violations": [],
            "strengths": [
                "Exceptional code quality",
                "100% test coverage",
                "Perfect documentation"
            ]
        }

        mock_content = Mock()
        mock_content.text = "Score: 100/100 - Exceptional work! Outstanding code quality (30/30), perfect test coverage (15/15), and comprehensive documentation (25/25). Exemplary academic project demonstrating mastery of principles."

        mock_message = Mock()
        mock_message.content = [mock_content]

        mock_client = Mock()
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client

        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("os.path.exists", return_value=True):
                with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                    result = generate_summary("test_report.json")

                    assert "Score: 100/100" in result
                    assert "exceptional" in result.lower() or "outstanding" in result.lower()
