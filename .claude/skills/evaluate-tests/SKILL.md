---
name: evaluate-tests
description: Evaluates test suite quality including coverage, test count, and edge case handling
version: 1.0.0
---

# Test Evaluation Skill

Evaluates testing practices in academic software projects by checking:
- Test file presence and count
- Test coverage (minimum 70%, target 90% for critical paths)
- Edge case documentation
- Test structure and quality

**Scoring:** 15 points maximum (important for software quality)

## Instructions

### 1. Find Test Files

Use Glob to locate test files following common naming conventions:

**Python Patterns:**
- `test_*.py` (pytest convention)
- `*_test.py`
- Files in `tests/` directory

**JavaScript/TypeScript Patterns:**
- `*.test.js` or `*.test.ts` (Jest convention)
- `*.spec.js` or `*.spec.ts` (Jasmine/Mocha)
- Files in `__tests__/` directory

```bash
# Find Python test files
find . -name "test_*.py" -o -name "*_test.py"
find . -path "*/tests/*.py"

# Find JavaScript test files
find . -name "*.test.js" -o -name "*.spec.js"
find . -path "*/__tests__/*"
```

**Scoring:**
- No test files found: 0 points (auto-fail)
- Fewer than 5 test files: -5 points

### 2. Count Test Cases

Count individual test functions/methods:

**Python (pytest/unittest):**
```bash
# Count test functions
grep -r "def test_" tests/ | wc -l

# Or use Python helper
python src/analyzers/test_counter.py <project_path>
```

**JavaScript (Jest):**
```bash
# Count test cases
grep -r "test\|it(" __tests__/ | wc -l
```

**Requirements:**
- Minimum 10 test cases for small projects
- Minimum 30 test cases for medium projects
- Minimum 50 test cases for large projects

**Scoring:**
- < 10 tests: -3 points
- 10-29 tests: -1 point
- ≥ 30 tests: full points

### 3. Analyze Test Coverage

**For Python projects using pytest:**

Check if coverage.py is configured:
```bash
# Look for .coveragerc or pytest.ini
ls .coveragerc pytest.ini pyproject.toml

# Check if coverage is in requirements
grep "coverage\|pytest-cov" requirements.txt
```

If coverage configured, check for coverage report:
```bash
# Look for coverage reports
ls .coverage coverage.json htmlcov/ .coverage.*

# If coverage.json exists, parse it
python -c "import json; data=json.load(open('coverage.json')); print(f\"Coverage: {data['totals']['percent_covered']}%\")"
```

**For JavaScript projects using Jest:**

Check jest.config.js for coverage settings:
```bash
grep "collectCoverage\|coverageThreshold" jest.config.js
```

**Use Python helper for comprehensive analysis:**
```bash
python src/analyzers/test_analyzer.py <project_path>
```

**Coverage Requirements:**
- **Minimum:** 70% overall coverage
- **Target:** 90% for critical business logic
- **Threshold:** Projects with <70% coverage fail this category

**Scoring:**
- Coverage ≥ 90%: 10/10 points
- Coverage 80-89%: 8/10 points
- Coverage 70-79%: 6/10 points
- Coverage < 70%: 0/10 points (fail)

### 4. Check for Edge Case Testing

Look for evidence of edge case testing in test files:

**Keywords to search for:**
```bash
# Search for edge case mentions
grep -ri "edge case\|boundary\|corner case\|error handling\|exception" tests/

# Look for parameterized tests (good practice)
grep -r "@pytest.mark.parametrize\|test.each" tests/

# Check for error/exception testing
grep -r "pytest.raises\|expect.*toThrow\|assertRaises" tests/
```

**Good indicators:**
- Tests for empty inputs
- Tests for None/null values
- Tests for boundary values (0, -1, max values)
- Tests for malformed inputs
- Tests for exception handling

**Scoring:**
- No edge case testing evident: -2 points
- Some edge case tests: -0 points
- Comprehensive edge case coverage: +0 bonus (already in base score)

### 5. Evaluate Test Structure

Check for good testing practices:

**Test Organization:**
- Tests organized by module/feature
- Clear test file naming
- Use of test fixtures/setup

```bash
# Check for conftest.py (pytest fixtures)
ls tests/conftest.py

# Check for test organization
ls tests/unit/ tests/integration/ tests/fixtures/
```

**Test Naming:**
- Descriptive test names: `test_function_name_scenario_expected_result`
- Not just: `test1`, `test2`, etc.

```bash
# Look for descriptive test names
grep "def test_.*_when_.*_then_\|def test_.*_should_\|def test_.*_with_" tests/
```

### 6. Use Python Helper for Complete Analysis

Run the comprehensive test evaluator:

```bash
python src/analyzers/test_analyzer.py <project_path>
```

This will:
1. Find all test files
2. Count test cases
3. Check for coverage configuration
4. Parse coverage reports (if available)
5. Analyze test quality
6. Calculate test score

### 7. Calculate Test Score

**Scoring Formula:**
```
Base Score: 15 points

Components:
- Test presence: 3 points (has tests)
- Test count: 2 points (adequate number)
- Coverage: 10 points (based on percentage)
  - ≥90%: 10 points
  - 80-89%: 8 points
  - 70-79%: 6 points
  - <70%: 0 points
- Edge cases: up to -2 penalty if missing

Final Score: max(0, min(Total, 15))
```

**Passing Threshold:** 10.5/15 (70%)

### 8. Generate Report

Output a detailed test evaluation:

```json
{
  "score": 13.0,
  "max_score": 15,
  "passed": true,
  "test_files_found": 12,
  "total_tests": 47,
  "coverage": 0.82,
  "has_edge_case_tests": true,
  "details": {
    "test_files": [
      "tests/test_analyzer.py (8 tests)",
      "tests/test_validator.py (12 tests)",
      "tests/test_parser.py (15 tests)",
      "tests/integration/test_workflow.py (12 tests)"
    ],
    "coverage_by_module": {
      "src/analyzers/": 0.89,
      "src/validators/": 0.91,
      "src/parsers/": 0.75,
      "src/utils/": 0.82
    },
    "missing_coverage": [
      "src/parsers/javascript_parser.py: 65% coverage"
    ],
    "edge_case_examples": [
      "test_analyzer_with_empty_file",
      "test_validator_with_none_input",
      "test_parser_with_malformed_syntax"
    ]
  }
}
```

## Example Usage

```bash
# Run the test evaluation skill
/skill evaluate-tests

# When prompted, provide project path
/path/to/student/project
```

## Python Helpers Available

1. **test_analyzer.py** - Complete test evaluation
   ```bash
   python src/analyzers/test_analyzer.py <path>
   ```

2. **test_counter.py** - Count test cases
   ```bash
   python src/analyzers/test_counter.py <path>
   ```

## Success Criteria

- ✅ Test files present (minimum 5 files)
- ✅ Adequate test count (minimum 30 tests)
- ✅ Coverage ≥ 70% (target: 90%)
- ✅ Edge case testing documented
- ✅ Score ≥ 10.5/15 to pass

## Common Issues

1. **No tests at all** - Auto-fail, most serious issue
2. **Coverage not measured** - Students don't configure pytest-cov
3. **Only happy path tests** - Missing edge cases and error handling
4. **Poor test names** - `test1`, `test2` instead of descriptive names
5. **No integration tests** - Only unit tests, missing end-to-end testing

## Recommendations Format

Provide actionable feedback:
```
[+] Test Evaluation Results:

    Test Files: 12 found ✓
    Total Tests: 47 ✓
    Coverage: 82% ✓ (Target: 90%)

    Coverage by Module:
    ✓ src/validators/: 91%
    ✓ src/analyzers/: 89%
    ✓ src/utils/: 82%
    ⚠ src/parsers/: 75%

    Recommendations:
    1. Increase coverage in src/parsers/:
       - Add tests for javascript_parser.py (currently 65%)
       - Focus on error handling paths

    2. Add more edge case tests:
       - Test with empty/None inputs
       - Test with malformed data
       - Test boundary conditions

    3. Consider adding integration tests:
       - End-to-end workflow tests
       - Multi-module interaction tests

    Example test to add:
    ```python
    def test_parse_file_with_empty_input():
        '''Test parser handles empty files gracefully.'''
        with pytest.raises(ValueError, match="empty"):
            parse_file("")
    ```

    Final Score: 13/15 (87%) - PASSED
```
