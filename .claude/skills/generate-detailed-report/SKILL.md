---
name: generate-detailed-report
description: Generate comprehensive grading report with specific issues, file paths, and actionable recommendations
version: 1.0.0
---

# Generate Detailed Grading Report Skill

Creates a comprehensive, actionable grading report that goes beyond scores to provide:
- Specific file paths and line numbers for violations
- Exact issues found in each category
- Actionable fix recommendations
- Prioritized action items by point value

## When to Use This Skill

After running all grading skills, use this to generate a detailed report that helps students understand:
- **Exactly** what files have problems
- **Exactly** what needs to be fixed
- **Exactly** how to improve their score

## Input Required

- **Project path**: Path to the graded project
- **Grading results**: Complete results from all grading skills

## Instructions

### Step 1: Gather Complete Grading Results

Run all grading skills **in parallel** to get detailed results:

```bash
# Run all 7 grading skills in parallel groups
# Group 1 (parallel)
/skill check-security <project_path>
/skill validate-docs <project_path>
/skill check-ux <project_path>

# Group 2 (parallel)
/skill analyze-code <project_path>
/skill evaluate-tests <project_path>

# Group 3 (parallel)
/skill assess-git <project_path>
/skill grade-research <project_path>
```

Or let the grade-project agent orchestrate everything automatically.

### Step 2: Analyze Each Category in Detail

For each grading category, extract and present:

#### 🔒 SECURITY (10 points)

**Show specifically:**
- File paths where secrets were found (if any)
- Which .gitignore patterns are missing
- Whether .env.example exists

**Format:**
```
SECURITY: X/10 points

[If secrets found:]
✗ CRITICAL: Hardcoded secrets detected
  Location: src/config.py:23 (API key)
  Location: utils/db.py:45 (password)
  Fix: Move to .env file, add to .gitignore

[If .gitignore issues:]
✗ .gitignore missing required patterns
  Missing: .env, *.key, *.pem, __pycache__
  Fix: Add these patterns to .gitignore

[If .env.example missing:]
✗ No .env.example template found
  Fix: Create .env.example with:
    API_KEY=your_api_key_here
    DB_PASSWORD=your_password_here
```

#### 💻 CODE QUALITY (30 points)

**Show specifically:**
- Every file exceeding 150 lines (with exact line count)
- Files/functions missing docstrings
- Specific naming violations

**Format:**
```
CODE QUALITY: X/30 points

[File size violations:]
✗ 4 files exceed 150-line limit (-20 points)

  src/main.py: 215 lines (exceeds by 65)
    → Split into: src/main.py, src/handlers.py, src/utils.py

  src/processor.py: 180 lines (exceeds by 30)
    → Extract helper functions to separate module

  tests/test_all.py: 165 lines (exceeds by 15)
    → Split into: test_unit.py, test_integration.py

[Docstring issues:]
✗ Docstring coverage: 67% (target: 90%) (-6 points)

  Missing docstrings in:
    • src/utils.py:42 - function process_data()
    • src/handlers.py:15 - class DataHandler
    • src/models.py:89 - function validate_input()

  Fix: Add docstrings following format:
    def function_name():
        \"\"\"
        Brief description.

        Args:
            param: description

        Returns:
            description
        \"\"\"

[Naming violations:]
✗ 3 naming convention violations (-1.5 points)

  • src/utils.py:12 - variable 'MyVariable' should be 'my_variable'
  • src/main.py:34 - function 'ProcessData' should be 'process_data'
  • src/config.py:8 - constant 'api_key' should be 'API_KEY'
```

#### 📚 DOCUMENTATION (25 points)

**Show specifically:**
- Which documents are missing vs incomplete
- Word counts for each document
- Which required sections are missing

**Format:**
```
DOCUMENTATION: X/25 points

[Missing documents:]
✗ PLANNING.md not found (-5 points)
  Create with sections:
    - Architecture Overview
    - Design Decisions
    - Technology Choices
    - Implementation Plan

[Incomplete documents:]
⚠ TASKS.md: 89 words (too short, -3 points)
  Current sections: 2
  Missing sections:
    - Task breakdown with IDs
    - Status tracking (🔴 🟡 🟢)
    - Time estimates
    - Dependencies

  Add approximately 200+ more words with:
    - All development tasks
    - Task status updates
    - Completion tracking

⚠ README.md: 245 words (needs improvement, -2 points)
  Missing sections:
    - Installation instructions
    - Usage examples with code
    - Troubleshooting guide

  Add:
    - Step-by-step setup guide
    - 3+ code examples
    - Common issues & solutions

[Complete documents:]
✓ PRD.md: 487 words ✓
✓ CLAUDE.md: 312 words ✓
```

#### 🧪 TESTING (15 points)

**Show specifically:**
- Test file count
- Total test count
- Coverage percentage
- Which modules lack tests

**Format:**
```
TESTING: X/15 points

✓ Test files found: 5
✓ Total tests: 42
⚠ Coverage: 68% (target: 70%, -2 points)

[Modules below 70% coverage:]
  • src/processor.py: 45% coverage
    Missing tests for:
      - process_data() function
      - error handling in validate()
      - edge cases in transform()

  • src/utils.py: 52% coverage
    Missing tests for:
      - file operations
      - exception handling
      - boundary conditions

[To improve coverage:]
  1. Add tests for src/processor.py:
     test_process_data_valid_input()
     test_process_data_invalid_input()
     test_process_data_edge_cases()

  2. Run coverage report:
     pytest --cov=src --cov-report=html
     open htmlcov/index.html
```

#### 🔀 GIT WORKFLOW (10 points)

**Show specifically:**
- Exact commit count
- Examples of good/bad commit messages
- Missing commit message conventions

**Format:**
```
GIT WORKFLOW: X/10 points

Commits: 6 (minimum: 15, recommended: 15-25) (-5 points)

[Commit history analysis:]
✓ Good commits:
  • feat(core): Add data processing module [T-123]
  • docs(readme): Add installation instructions

✗ Problematic commits:
  • "update" (too vague)
  • "fix" (no context)
  • "wip" (work-in-progress, should be completed)

[To improve:]
1. Make 9-19 more atomic commits showing:
   - Feature development progression
   - Testing additions
   - Documentation updates
   - Bug fixes

2. Follow conventional format:
   <type>(<scope>): <description> [TASK-ID]

   Types: feat, fix, docs, test, refactor, chore

   Examples:
   feat(auth): Implement user login system [T-101]
   test(auth): Add login validation tests [T-102]
   docs(api): Document authentication endpoints [T-103]

3. Show development progression:
   - Initial structure → Implementation → Testing → Documentation
```

#### 🔬 RESEARCH (10 points)

**Show specifically:**
- What research documentation is missing
- Which prompts should be documented
- What analysis is lacking

**Format:**
```
RESEARCH: X/10 points

⚠ Limited research documentation (-4 points)

[Missing:]
✗ No prompts/ directory found
  Create: prompts/
    ├── README.md (lessons learned)
    ├── architecture/
    │   └── 001-design-decisions.md
    ├── code-generation/
    │   └── 001-implementation-prompts.md
    └── testing/
        └── 001-test-generation.md

✗ No parameter exploration documented
  Add to PLANNING.md:
    - Parameters tested (3+ required)
    - Results comparison
    - Performance metrics

✗ No comparative analysis
  Add section comparing:
    - Approach A vs Approach B
    - Trade-offs analysis
    - Final decision rationale

[To score full points:]
  1. Create prompts/ directory with 5+ documented prompts
  2. Document parameter exploration in PLANNING.md
  3. Add comparative analysis of design choices
```

### Step 3: Generate Prioritized Action Plan

Sort fixes by point value (highest impact first):

```
═══════════════════════════════════════════════════════════════
PRIORITIZED ACTION PLAN
═══════════════════════════════════════════════════════════════

To reach 70 (passing): Need +X points
To reach 85 (good):    Need +X points
To reach 90 (excellent): Need +X points

Priority 1: CODE QUALITY (+20 points potential)
  □ Refactor src/main.py (215 → <150 lines)
  □ Refactor src/processor.py (180 → <150 lines)
  □ Refactor tests/test_all.py (165 → <150 lines)
  □ Add docstrings to 8 functions/classes
  □ Fix 3 naming convention violations

Priority 2: DOCUMENTATION (+10 points potential)
  □ Create PLANNING.md with architecture decisions
  □ Expand TASKS.md to 300+ words with task tracking
  □ Add installation section to README.md
  □ Add usage examples to README.md

Priority 3: GIT WORKFLOW (+5 points potential)
  □ Make 9-19 more atomic commits
  □ Use conventional commit format
  □ Show development progression

Priority 4: RESEARCH (+4 points potential)
  □ Create prompts/ directory
  □ Document 5+ prompt examples
  □ Add parameter exploration analysis

═══════════════════════════════════════════════════════════════
ESTIMATED TIME TO FIX: 4-6 hours
WITH FIXES: Current score + 39 points = XX/100 (Grade: X)
═══════════════════════════════════════════════════════════════
```

### Step 4: Add Quick Reference Commands

Provide copy-paste commands for common fixes:

```
QUICK FIX COMMANDS
─────────────────────────────────────────────────────────────

Check file sizes:
  python -c "from src.analyzers.file_size_analyzer import check_file_sizes; \
  violations = check_file_sizes('.', 150); \
  print('\\n'.join(f'{v.file_path}: {v.line_count} lines' for v in violations))"

Check docstring coverage:
  python -c "from src.analyzers.docstring_analyzer import analyze_project_docstrings; \
  result = analyze_project_docstrings('.'); \
  print(f\"Coverage: {result['coverage']:.1%}\"); \
  print('Missing:', result['missing'])"

Run test coverage:
  pytest --cov=src --cov-report=term-missing
  pytest --cov=src --cov-report=html
  open htmlcov/index.html

Check git commits:
  git log --oneline
  git log --format="%s" | head -20

Initialize missing files:
  touch PLANNING.md TASKS.md .env.example
  mkdir -p prompts/architecture prompts/code-generation prompts/testing
```

## Output Format

Generate a comprehensive markdown report and save it to the `results/` folder.

**Filename:** `results/<project_name>_detailed_report_YYYY-MM-DD_HHMMSS.md`

**Report structure:**

1. **Executive Summary**: Score, grade, pass/fail
2. **Category Details**: Each category with specific issues
3. **Action Plan**: Prioritized fixes by point value
4. **Quick Commands**: Copy-paste terminal commands
5. **Timeline**: Estimated effort to fix issues

### How to Generate the Report

Use the Python detailed reporter module:

```python
from datetime import datetime
from pathlib import Path
from src.reporters.detailed_reporter import generate_detailed_report
import json

# Load grading results
with open('grading_results.json', 'r') as f:
    results = json.load(f)

# Generate detailed report
project_name = Path(project_path).name
report_content = generate_detailed_report(results, project_path)

# Create results directory if it doesn't exist
Path('results').mkdir(exist_ok=True)

# Save to markdown file with timestamp
timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
report_filename = f"results/{project_name}_detailed_report_{timestamp}.md"

with open(report_filename, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"\n✓ Detailed report saved to: {report_filename}")
```

Or use the command-line helper:

```bash
# After grading, generate detailed report
python -c "
from datetime import datetime
from pathlib import Path
from src.reporters.detailed_reporter import generate_detailed_report
import json
import sys

project_path = sys.argv[1]
results_file = sys.argv[2] if len(sys.argv) > 2 else 'grading_results.json'

# Load results
with open(results_file, 'r') as f:
    results = json.load(f)

# Generate report
report = generate_detailed_report(results, project_path)

# Save to file
Path('results').mkdir(exist_ok=True)
project_name = Path(project_path).name
timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
filename = f'results/{project_name}_detailed_report_{timestamp}.md'

with open(filename, 'w', encoding='utf-8') as f:
    f.write(report)

print(f'✓ Report saved: {filename}')
" <project_path> [results.json]
```

## Success Criteria

The detailed report should:
- ✅ Identify every specific file with issues
- ✅ Provide exact line numbers or locations
- ✅ Explain WHY each item lost points
- ✅ Show HOW to fix each issue
- ✅ Prioritize fixes by point value
- ✅ Include copy-paste commands
- ✅ Estimate time to complete fixes

## Example Usage

### Using the Skill Directly

```bash
/skill generate-detailed-report
```

Then provide:
- **Project path**: `./student-submission`
- **Results file**: `grading_results.json` (or paste results)

### Integrated with Grading

```bash
# Run all grading skills in parallel, then generate report

# Step 1: Run grading skills in parallel groups
# (See instructions above for parallel skill invocation)

# Step 2: After all skills complete, generate detailed report
/skill generate-detailed-report ./student-project

with open('grading_results.json') as f:
    results = json.load(f)

report = generate_detailed_report(results, './student-project')

Path('results').mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
filename = f'results/student-project_detailed_report_{timestamp}.md'

with open(filename, 'w') as f:
    f.write(report)

print(f'✓ Report saved: {filename}')
"
```

The skill generates:
- ✅ Markdown file in `results/` folder
- ✅ 200+ line detailed report
- ✅ Specific issues with file paths and line numbers
- ✅ Actionable recommendations
- ✅ Quick fix commands
- ✅ Timestamped filename for version control

## Integration with Grader

The orchestrator agent is configured to ALWAYS invoke this skill after grading:

```
User: "Grade ./my-project"

Agent: [Phase 1] Validates project
Agent: [Phase 2] Runs all 7 grading skills in parallel
Agent: [Phase 3] Aggregates results
       Score: 66/100 (D) - FAILED

Agent: [Phase 4] AUTOMATICALLY invokes /skill generate-detailed-report
       ✓ Generating detailed report...
       ✓ Report saved: results/my-project_detailed_report_2024-11-26_120530.md

Agent: [Presents summary and links to detailed report]

User can then:
- Review the markdown report for specific issues
- Follow actionable recommendations
- Use quick-fix commands
- Track progress as they fix issues
```

**Automatic Report Generation:**
The agent will ALWAYS create a detailed markdown report after grading, regardless of score. This ensures students have comprehensive feedback with specific file paths and actionable fixes.

## Notes

- Be specific: Always include file paths and line numbers
- Be actionable: Every issue should have a fix
- Be prioritized: Sort by point value (highest first)
- Be helpful: Include copy-paste commands
- Be encouraging: Frame as improvement opportunities
