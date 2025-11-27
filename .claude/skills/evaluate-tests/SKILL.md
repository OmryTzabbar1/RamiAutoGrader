---
name: evaluate-tests
description: Evaluates test suite quality including coverage, test count, and edge case handling
version: 1.1.0
---

# Test Evaluation Skill

Evaluates testing practices in academic software projects by checking:
- Test file presence and count
- Test coverage (minimum 70%, adjusted by strictness)
- Edge case documentation
- Test structure and quality

**Scoring:** 15 points maximum (important for software quality)

---

## Strictness Parameter (Optional)

This skill supports **adaptive grading strictness** based on student self-assessment.

**Default**: `strictness = 1.0` (standard grading)
**Range**: `1.0 to 1.3` (higher = more critical evaluation)

**How strictness affects grading:**
- **Penalties are multiplied** by strictness value
- **Coverage thresholds are raised** for higher strictness
- **Minimum test count is increased** for higher strictness

**Examples:**
- Student self-grade = 70  → strictness = 1.21
- Student self-grade = 85  → strictness = 1.255
- Student self-grade = 95  → strictness = 1.285

**Usage**: If strictness is specified in the grading request, apply it to all penalty calculations and thresholds.

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
- No test files found: 0 points (auto-fail, not affected by strictness)
- Fewer than 5 test files: `-5 × strictness` points
  - strictness=1.0: -5 points
  - strictness=1.3: -6.5 points

### 2. Count Test Cases

Count individual test functions/methods:

**Python (pytest/unittest):**
```bash
# Count test functions
grep -r "def test_" tests/ | wc -l
```

**JavaScript (Jest):**
```bash
# Count test cases
grep -r "test\|it(" __tests__/ | wc -l
```

**Requirements (adjusted by strictness):**
- **Minimum test count** (scales with strictness):
  - strictness=1.0: 10 tests minimum
  - strictness=1.2: 14 tests minimum (10 + 0.2 × 20)
  - strictness=1.3: 16 tests minimum (10 + 0.3 × 20)
  - Formula: `min_tests = 10 + (strictness - 1.0) × 20`

**Scoring:**
- < min_tests: `-3 × strictness` points
  - Example: strictness=1.3, min=16 tests, actual=12 tests → -3.9 points
- min_tests to (min_tests × 3 - 1): `-1 × strictness` point
  - Example: strictness=1.3, min=16, actual=25 tests → -1.3 points
- ≥ (min_tests × 3): full points

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
```

**For JavaScript projects using Jest:**

Check jest.config.js for coverage settings:
```bash
grep "collectCoverage\|coverageThreshold" jest.config.js
```

**Coverage Requirements (adjusted by strictness):**
- **Minimum threshold** (scales with strictness):
  - strictness=1.0: 70% coverage required
  - strictness=1.2: 78% coverage required (70% + 0.2 × 40%)
  - strictness=1.3: 82% coverage required (70% + 0.3 × 40%)
  - Formula: `required_coverage = 0.70 + (strictness - 1.0) × 0.40`

**Scoring (adjusted thresholds):**
- Coverage ≥ (required + 20%): 10/10 points (excellent)
- Coverage (required + 10%) to (required + 19%): 8/10 points (good)
- Coverage required to (required + 9%): 6/10 points (acceptable)
- Coverage < required: 0/10 points (fail)

**Examples:**
- strictness=1.0: 70% required, 90%+ excellent, 80-89% good, 70-79% acceptable
- strictness=1.3: 82% required, 102%+ excellent (unlikely), 92-101% good, 82-91% acceptable

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

### 6. Calculate Test Score

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
