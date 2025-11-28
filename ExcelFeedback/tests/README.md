# ExcelFeedback Tests

This directory contains unit tests and integration tests for the ExcelFeedback project.

---

## Test Structure

```
tests/
├── unit/                           # Unit tests for individual skills
│   ├── test_extract_metadata.py    # PDF metadata extraction tests
│   ├── test_generate_summary.py    # Summary generation tests
│   └── test_populate_excel.py      # Excel creation tests
│
├── integration/                    # Integration tests for full workflow
│   └── test_full_workflow.py       # End-to-end workflow tests
│
├── fixtures/                       # Test data
│   └── sample_students/            # Sample student data
│       ├── john_doe/
│       ├── alice_johnson/
│       └── charlie_brown/
│
└── README.md                       # This file
```

---

## Running Tests

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (for Claude API mocking)
export ANTHROPIC_API_KEY=test-key
```

---

### Run All Tests

```bash
# Run all tests (unit + integration)
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=skills --cov-report=html

# Run in parallel (faster)
pytest tests/ -n auto
```

---

### Run Unit Tests Only

```bash
# All unit tests
pytest tests/unit/ -v

# Specific skill
pytest tests/unit/test_extract_metadata.py -v
pytest tests/unit/test_generate_summary.py -v
pytest tests/unit/test_populate_excel.py -v
```

---

### Run Integration Tests Only

```bash
# All integration tests
pytest tests/integration/ -v

# Specific test
pytest tests/integration/test_full_workflow.py::TestFullWorkflow::test_full_workflow_three_students -v
```

---

## Test Coverage

### Current Coverage

| Component | Coverage | Tests |
|-----------|----------|-------|
| extract-pdf-metadata | 90%+ | 12 tests |
| generate-summary | 85%+ | 11 tests |
| populate-excel | 90%+ | 14 tests |
| **Total** | **88%+** | **37 tests** |

### Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=skills --cov-report=html

# Open report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## Unit Tests

### test_extract_metadata.py

**Tests for PDF metadata extraction skill**

- `test_all_fields_valid`: Confidence score with all valid fields
- `test_missing_partner_name`: Confidence score when partner missing
- `test_invalid_student_id`: Confidence score with invalid ID format
- `test_all_fields_missing`: Confidence score when all fields missing
- `test_extract_text_success`: PDF text extraction
- `test_extract_text_multiple_pages`: Multi-page PDF handling
- `test_file_not_found`: Missing PDF file handling
- `test_corrupted_pdf`: Corrupted PDF handling
- `test_successful_extraction`: Full metadata extraction workflow
- `test_api_error_with_retries`: Claude API retry logic
- `test_parse_error`: Invalid JSON response handling
- `test_low_confidence_extraction`: Low confidence flagging

**Run**:
```bash
pytest tests/unit/test_extract_metadata.py -v
```

---

### test_generate_summary.py

**Tests for summary generation skill**

- `test_valid_summary`: Validation of correct summary
- `test_summary_too_short`: Validation fails for short summary
- `test_summary_too_long`: Validation fails for long summary
- `test_summary_missing_score_prefix`: Validation fails without "Score:"
- `test_summary_has_markdown`: Validation fails with markdown
- `test_load_valid_report`: JSON loading
- `test_load_invalid_json`: Invalid JSON handling
- `test_format_prompt_complete_report`: Prompt formatting
- `test_file_not_found`: Missing grading report handling
- `test_successful_summary_generation`: Full summary workflow
- `test_api_error_with_retries`: Claude API retry logic
- `test_invalid_summary_fallback`: Fallback on validation failure
- `test_perfect_score_summary`: Perfect score (100/100) handling

**Run**:
```bash
pytest tests/unit/test_generate_summary.py -v
```

---

### test_populate_excel.py

**Tests for Excel creation skill**

- `test_create_excel_valid_data`: Excel creation with valid data
- `test_create_excel_single_student`: Single student handling
- `test_create_excel_many_students`: 30 students handling
- `test_header_formatting`: Header row formatting (bold, color, alignment)
- `test_column_widths`: Column width verification
- `test_hyperlink_creation`: GitHub URL hyperlink creation
- `test_text_wrapping`: Summary column text wrapping
- `test_borders`: Border application on all cells
- `test_empty_student_data`: Empty data error handling
- `test_none_student_data`: None data error handling
- `test_output_directory_creation`: Output directory auto-creation
- `test_filename_sanitization`: Special character removal from filename
- `test_missing_github_url`: Missing GitHub URL handling
- `test_notes_column_populated`: Manual review flags

**Run**:
```bash
pytest tests/unit/test_populate_excel.py -v
```

---

## Integration Tests

### test_full_workflow.py

**Tests for complete ExcelFeedback workflow**

- `test_full_workflow_three_students`: Complete workflow with 3 students
- `test_workflow_with_missing_pdf`: Missing PDF handling
- `test_workflow_with_low_confidence_extraction`: Low confidence flagging
- `test_workflow_performance_many_students`: Performance test (30 students)
- `test_workflow_excel_formatting`: Excel formatting verification

**Run**:
```bash
pytest tests/integration/test_full_workflow.py -v
```

---

## Test Fixtures

### Sample Students

**Location**: `tests/fixtures/sample_students/`

**Students**:
1. **john_doe** - Average score (77/100)
2. **alice_johnson** - High score (92/100)
3. **charlie_brown** - Low score (65/100, low confidence extraction)

**Each Student Folder Contains**:
- `grading_results.json`: Grading scores and violations
- `metadata.json`: GitHub URL and student folder info
- `student_submission.txt`: Sample PDF text (simulated)

---

## Mocking Claude API

Unit tests mock Claude API responses to avoid real API calls during testing.

**Example**:
```python
@patch('anthropic.Anthropic')
def test_successful_extraction(mock_anthropic):
    mock_content = Mock()
    mock_content.text = '{"student_id": "12345678", ...}'

    mock_message = Mock()
    mock_message.content = [mock_content]

    mock_client = Mock()
    mock_client.messages.create.return_value = mock_message
    mock_anthropic.return_value = mock_client

    # Test code here
```

---

## Continuous Integration

### GitHub Actions (Future)

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=skills --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## Writing New Tests

### Unit Test Template

```python
import pytest
from unittest.mock import Mock, patch

def test_my_new_feature():
    """Test description following convention: test_<function>_<scenario>_<expected>."""
    # Arrange
    input_data = ...
    expected = ...

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected
```

### Integration Test Template

```python
def test_new_integration_scenario(fixtures_dir, temp_output_dir):
    """Test description."""
    # Arrange: Set up test data
    student_data = [...]

    # Act: Run workflow
    result = populate_excel(student_data, "Test", temp_output_dir)

    # Assert: Verify results
    assert os.path.exists(result)
```

---

## Troubleshooting

### Issue: Tests fail with "ANTHROPIC_API_KEY not found"

**Solution**: Set mock API key for tests
```bash
export ANTHROPIC_API_KEY=test-key
```

---

### Issue: Excel tests fail with "openpyxl not installed"

**Solution**: Install all dependencies
```bash
pip install -r requirements.txt
```

---

### Issue: Integration tests fail with "fixtures not found"

**Solution**: Run tests from project root
```bash
cd ExcelFeedback/
pytest tests/integration/
```

---

## Test Quality Standards

- **Coverage**: 70%+ minimum, 90%+ for critical paths
- **Edge Cases**: Test boundary conditions, empty inputs, errors
- **Mocking**: Mock external dependencies (Claude API, file I/O)
- **Assertions**: Use specific assertions with clear messages
- **Documentation**: Docstrings on all test functions

---

## Performance Benchmarks

**Target Performance** (on standard development machine):

| Test Suite | Target Time |
|------------|-------------|
| Unit tests | < 5 seconds |
| Integration tests | < 10 seconds |
| All tests | < 15 seconds |

**Current Performance**:
- Unit tests: ~3 seconds
- Integration tests: ~6 seconds
- All tests: ~9 seconds ✅

---

**Last Updated**: 2025-11-28
