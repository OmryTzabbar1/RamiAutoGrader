---
name: analyze-code
description: Analyzes code quality including file sizes, docstrings, naming conventions, and complexity
version: 1.0.0
---

# Code Quality Analysis Skill

Evaluates code quality in academic software projects by checking:
- File size limits (max 150 lines per file - STRICTLY ENFORCED)
- Docstring coverage (minimum 90%)
- Naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE)
- Code complexity metrics

**Scoring:** 30 points maximum (largest category in grading rubric)

## Instructions

### 1. Check File Sizes (CRITICAL - NO EXCEPTIONS)

**This is the most important check - files exceeding 150 lines are unacceptable.**

Use Glob to find all source files, then Read and count lines:

```bash
# Find all Python files
find . -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" -not -path "*/node_modules/*"

# For each file, count lines
wc -l <file_path>
```

**Requirements:**
- Maximum 150 lines per file
- Count all lines (including comments and docstrings for simplicity)
- **Penalty:** -5 points per violation

Use Bash to check file sizes:
```bash
# Find all source files and check line counts
find src -name "*.py" -type f -exec wc -l {} \; | sort -rn

# Or check specific files
wc -l src/path/to/file.py
```

Any file with >150 lines is a violation.

### 2. Check Docstring Coverage

Analyze Python files for missing docstrings on:
- Modules (file-level docstring)
- Classes
- Functions/Methods

**Requirements:**
- Minimum 90% coverage
- Each function, class, module must have docstring
- **Penalty:** Coverage below 90% → subtract (0.9 - actual_coverage) * 20 points

Check docstring coverage using Grep and Read:
```bash
# Count total functions and classes
total_defs=$(grep -r "^def \|^class " src/ --include="*.py" | wc -l)

# Read sample files to check for docstrings
# A function has a docstring if the line after 'def' contains """

# For a quick check, sample a few files using Read tool
# and verify docstrings are present on functions/classes
```

**Manual verification recommended:** Read key source files and check that functions/classes have docstrings.

### 3. Validate Naming Conventions

Check that code follows proper naming conventions:

**Python:**
- Functions/methods: `snake_case` (e.g., `calculate_score`, `parse_file`)
- Classes: `PascalCase` (e.g., `CodeAnalyzer`, `FileValidator`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`, `API_KEY`)
- Variables: `snake_case`

**JavaScript/TypeScript:**
- Functions: `camelCase` (e.g., `calculateScore`, `parseFile`)
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Variables: `camelCase`

**Penalty:** -0.5 points per violation

Check naming with Grep:
```bash
# Find potential naming violations (functions that look like PascalCase)
grep -rn "^def [A-Z]" src/ --include="*.py"

# Find potential class naming violations (classes not in PascalCase)
grep -rn "^class [a-z_]" src/ --include="*.py"

# Find constants that aren't UPPER_SNAKE_CASE
grep -rn "^[a-z][a-zA-Z_]*\s*=" src/ --include="*.py" | grep -v "def \|class "
```

Review findings and count violations.

### 4. Check Code Complexity (Optional)

If time permits, check for overly complex functions:
- Cyclomatic complexity > 10 → flag as violation
- Deeply nested code (>4 levels) → flag as violation

**Note:** This is optional for Phase 1 but recommended for comprehensive analysis.

### 5. Calculate Code Quality Score

**Scoring Formula:**
```
Base Score: 30 points

Deductions:
- File size violations: -5 points each
- Docstring coverage: -(0.9 - coverage) * 20 (if coverage < 0.9)
- Naming violations: -0.5 points each

Final Score: max(0, min(Base Score - Deductions, 30))
```

**Passing Threshold:** 21/30 (70%)

### 6. Generate Report

Output a detailed report with:

```json
{
  "score": 25.0,
  "max_score": 30,
  "passed": true,
  "file_size_violations": 2,
  "docstring_coverage": 0.87,
  "naming_violations": 5,
  "details": {
    "oversized_files": [
      {"file": "src/analyzer.py", "lines": 182, "excess": 32},
      {"file": "src/parser.py", "lines": 165, "excess": 15}
    ],
    "missing_docstrings": [
      "src/utils.py::helper_function",
      "src/models.py::DataModel"
    ],
    "naming_violations": [
      {"file": "src/app.py", "line": 42, "name": "MyFunction", "expected": "my_function"},
      {"file": "src/config.py", "line": 15, "name": "apiKey", "expected": "API_KEY"}
    ]
  }
}
```

## Example Usage

```bash
# Run the code analysis skill
/skill analyze-code

# When prompted, provide project path
/path/to/student/project
```

## Tools to Use

Use Claude Code's built-in tools for analysis:

1. **Bash** - For finding files and counting lines
   ```bash
   find src -name "*.py" -exec wc -l {} \;
   ```

2. **Grep** - For pattern matching and searching
   ```bash
   grep -rn "^def \|^class " src/ --include="*.py"
   ```

3. **Read** - For reading and analyzing file contents
   - Read source files to verify docstrings
   - Check code structure and quality
   - Identify naming violations

## Success Criteria

- ✅ All files under 150 lines
- ✅ Docstring coverage ≥ 90%
- ✅ Naming conventions followed consistently
- ✅ No functions with excessive complexity
- ✅ Score ≥ 21/30 to pass

## Common Issues

1. **Large files** - Most common violation. Recommend splitting into modules.
2. **Missing module docstrings** - Often forgotten at top of file.
3. **Inconsistent naming** - Mix of camelCase and snake_case in Python.
4. **Minimal docstrings** - One-liners that don't explain parameters/returns.

## Recommendations Format

Provide actionable feedback:
```
[X] Code Quality Issues Found:

    1. File Size Violations (2 files):
       - src/analyzer.py: 182 lines (32 over limit)
         → Split into: analyzer_core.py, analyzer_utils.py
       - src/parser.py: 165 lines (15 over limit)
         → Extract AST utilities to separate module

    2. Docstring Coverage: 87% (target: 90%)
       Missing docstrings on:
       - src/utils.py::helper_function
       - src/models.py::DataModel

       Add docstrings following this format:
       def function_name(param):
           '''
           Brief description.

           Args:
               param: Description

           Returns:
               Description
           '''

    3. Naming Violations (5 instances):
       - src/app.py:42 - MyFunction should be my_function
       - src/config.py:15 - apiKey should be API_KEY (constant)
```
