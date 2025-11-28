"""
Unit tests for extract-pdf-metadata skill.

Tests cover:
- Valid PDF extraction
- Missing fields
- Invalid formats
- Error handling (file not found, corrupted PDF, API errors)
- Confidence scoring
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../skills/extract-pdf-metadata/scripts'))

from extract_metadata import extract_metadata, calculate_confidence, extract_pdf_text


class TestCalculateConfidence:
    """Test confidence scoring logic."""

    def test_all_fields_valid(self):
        """Test confidence score when all fields are valid."""
        metadata = {
            "student_id": "12345678",
            "student_name": "John Doe",
            "partner_name": "Jane Smith",
            "assignment_name": "Design Patterns"
        }
        confidence = calculate_confidence(metadata)
        assert confidence == 1.0

    def test_missing_partner_name(self):
        """Test confidence score when partner name is missing."""
        metadata = {
            "student_id": "12345678",
            "student_name": "John Doe",
            "partner_name": "NOT_FOUND",
            "assignment_name": "Design Patterns"
        }
        confidence = calculate_confidence(metadata)
        assert confidence == 0.6

    def test_invalid_student_id(self):
        """Test confidence score with invalid student ID format."""
        metadata = {
            "student_id": "ABC123",
            "student_name": "John Doe",
            "partner_name": "Jane Smith",
            "assignment_name": "Design Patterns"
        }
        confidence = calculate_confidence(metadata)
        assert confidence == 0.6

    def test_all_fields_missing(self):
        """Test confidence score when all fields are missing."""
        metadata = {
            "student_id": "NOT_FOUND",
            "student_name": "NOT_FOUND",
            "partner_name": "NOT_FOUND",
            "assignment_name": "NOT_FOUND"
        }
        confidence = calculate_confidence(metadata)
        assert confidence == 0.0

    def test_single_word_name(self):
        """Test confidence score with single-word student name."""
        metadata = {
            "student_id": "12345678",
            "student_name": "John",
            "partner_name": "Jane Smith",
            "assignment_name": "Design Patterns"
        }
        confidence = calculate_confidence(metadata)
        assert confidence == 0.7


class TestExtractPDFText:
    """Test PDF text extraction."""

    @patch('pdfplumber.open')
    def test_extract_text_success(self, mock_open):
        """Test successful PDF text extraction."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Student ID: 12345678\nName: John Doe"

        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf

        mock_open.return_value = mock_pdf

        text = extract_pdf_text("test.pdf")
        assert "Student ID: 12345678" in text
        assert "Name: John Doe" in text

    @patch('pdfplumber.open')
    def test_extract_text_multiple_pages(self, mock_open):
        """Test extraction from multi-page PDF."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1 content"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2 content"

        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page1, mock_page2]
        mock_pdf.__enter__.return_value = mock_pdf

        mock_open.return_value = mock_pdf

        text = extract_pdf_text("test.pdf")
        assert "Page 1 content" in text
        assert "Page 2 content" in text


class TestExtractMetadata:
    """Test full metadata extraction workflow."""

    def test_file_not_found(self):
        """Test handling of missing PDF file."""
        result = extract_metadata("/nonexistent/path/to/file.pdf")
        assert result["extraction_status"] == "FILE_NOT_FOUND"
        assert result["confidence"] == 0.0
        assert result["student_id"] == "NOT_FOUND"

    @patch('pdfplumber.open')
    def test_corrupted_pdf(self, mock_open):
        """Test handling of corrupted PDF."""
        mock_open.side_effect = Exception("PDF corrupted")

        with patch('os.path.exists', return_value=True):
            result = extract_metadata("corrupted.pdf")
            assert result["extraction_status"] == "PDF_CORRUPTED"
            assert result["confidence"] == 0.0

    @patch('pdfplumber.open')
    @patch('anthropic.Anthropic')
    def test_successful_extraction(self, mock_anthropic, mock_open):
        """Test successful metadata extraction."""
        mock_page = Mock()
        mock_page.extract_text.return_value = """
        Student ID: 12345678
        Name: John Doe
        Partner: Jane Smith
        Assignment: Design Patterns
        """

        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_open.return_value = mock_pdf

        mock_content = Mock()
        mock_content.text = '{"student_id": "12345678", "student_name": "John Doe", "partner_name": "Jane Smith", "assignment_name": "Design Patterns"}'

        mock_message = Mock()
        mock_message.content = [mock_content]

        mock_client = Mock()
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client

        with patch('os.path.exists', return_value=True):
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                result = extract_metadata("test.pdf")

                assert result["student_id"] == "12345678"
                assert result["student_name"] == "John Doe"
                assert result["partner_name"] == "Jane Smith"
                assert result["assignment_name"] == "Design Patterns"
                assert result["confidence"] == 1.0
                assert result["extraction_status"] == "SUCCESS"

    @patch('pdfplumber.open')
    @patch('anthropic.Anthropic')
    def test_api_error_with_retries(self, mock_anthropic, mock_open):
        """Test Claude API error handling with retries."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Some text"

        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_open.return_value = mock_pdf

        from anthropic import APIError
        mock_client = Mock()
        mock_client.messages.create.side_effect = APIError("API Error")
        mock_anthropic.return_value = mock_client

        with patch('os.path.exists', return_value=True):
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                with patch('time.sleep'):  # Skip sleep in tests
                    result = extract_metadata("test.pdf")

                    assert result["extraction_status"] == "API_ERROR"
                    assert result["confidence"] == 0.0
                    assert mock_client.messages.create.call_count == 3  # 3 retries

    @patch('pdfplumber.open')
    @patch('anthropic.Anthropic')
    def test_parse_error(self, mock_anthropic, mock_open):
        """Test handling of invalid JSON response."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Some text"

        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_open.return_value = mock_pdf

        mock_content = Mock()
        mock_content.text = "This is not valid JSON"

        mock_message = Mock()
        mock_message.content = [mock_content]

        mock_client = Mock()
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client

        with patch('os.path.exists', return_value=True):
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                result = extract_metadata("test.pdf")

                assert result["extraction_status"] == "PARSE_ERROR"
                assert result["confidence"] == 0.0

    @patch('pdfplumber.open')
    @patch('anthropic.Anthropic')
    def test_low_confidence_extraction(self, mock_anthropic, mock_open):
        """Test extraction with low confidence triggers manual review."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Some text"

        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_open.return_value = mock_pdf

        mock_content = Mock()
        mock_content.text = '{"student_id": "ABC", "student_name": "John", "partner_name": "NOT_FOUND", "assignment_name": "DP"}'

        mock_message = Mock()
        mock_message.content = [mock_content]

        mock_client = Mock()
        mock_client.messages.create.return_value = mock_message
        mock_anthropic.return_value = mock_client

        with patch('os.path.exists', return_value=True):
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
                result = extract_metadata("test.pdf")

                assert result["confidence"] < 0.7
                assert result["extraction_status"] == "NEEDS_MANUAL_REVIEW"
