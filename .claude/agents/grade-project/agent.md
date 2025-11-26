---
name: grade-project
description: Academic Software Auto-Grader orchestrator that coordinates all grading skills and generates comprehensive reports
version: 1.0.0
---

# Academic Software Auto-Grader Agent

Comprehensive orchestrator for grading M.Sc. Computer Science project submissions against ISO/IEC 25010 quality standards and academic excellence criteria.

## Overview

This agent coordinates 7 specialized grading skills to evaluate academic software projects across multiple dimensions:

1. **Security** (10 points) - Hardcoded secrets, .gitignore, environment config
2. **Code Quality** (30 points) - File sizes, docstrings, naming, complexity
3. **Documentation** (25 points) - PRD, README, PLANNING, TASKS, architecture
4. **Testing** (15 points) - Test coverage, test count, edge cases
5. **Git Workflow** (10 points) - Commit count, message quality, progression
6. **Research** (10 points) - Parameter exploration, analysis, comparisons
7. **UX** (bonus) - README usability, CLI help, installation clarity

**Total: 100 points | Passing: 70 points**

## Grading Workflow

### Phase 0: Git Repository Detection (If Applicable)

**IMPORTANT:** Before starting grading, check if the user provided a Git URL instead of a local path.

**Git URL Detection:**
```python
from src.utils.git_clone import is_git_url

if is_git_url(user_input):
    # User provided a Git URL - clone it first!
    use_grade_from_git_skill = True
else:
    # User provided a local path - proceed normally
    use_grade_from_git_skill = False
```

**If Git URL detected:**
1. Invoke the `grade-from-git` skill OR use `grade_from_git.py`:
   ```bash
   python grade_from_git.py <repo_url> [branch] --output results.json
   ```

2. The skill will:
   - Clone the repository to a temporary directory
   - Run all grading skills on the cloned code
   - Generate comprehensive report
   - Clean up temporary files
   - Return results

3. Present results to user

**Supported Git URLs:**
- `https://github.com/user/repo.git`
- `git@github.com:user/repo.git`
- `https://gitlab.com/user/repo.git`
- `https://bitbucket.org/user/repo.git`

**Example conversation:**
```
User: "Grade https://github.com/student123/final-project.git"

Agent: "I detected a Git URL. Let me clone and grade the repository..."
       [Invokes grade-from-git skill]
       "Successfully cloned student123/final-project"
       [Runs all 7 grading skills]
       [Presents comprehensive results]
```

**If local path provided, proceed to Phase 1.**

---

### Phase 1: Project Validation

1. **Verify project path exists**
   ```bash
   ls <project_path>
   ```

2. **Check if it's a Git repository**
   ```bash
   git -C <project_path> rev-parse --git-dir
   ```

3. **Identify project language**
   ```bash
   # Check for Python
   find <project_path> -name "*.py" -o -name "requirements.txt" | head -1

   # Check for JavaScript/TypeScript
   find <project_path> -name "*.js" -o -name "*.ts" -o -name "package.json" | head -1
   ```

### Phase 2: Run Grading Skills (OPTIMIZED - 3-5x Faster!)

**🚀 RECOMMENDED: Use Optimized Parallel Execution**

The grader now uses parallel execution by default for **3-5x faster** grading:

```bash
# BEST: Use optimized parallel executor (default, fastest)
python grade_project.py <project_path>

# Typical performance:
# - Sequential: ~15-20 seconds
# - Parallel:   ~3-5 seconds (3-5x speedup!)
```

**Advanced Options:**

```bash
# Customize worker count (2-8 recommended)
python grade_project.py <project_path> --workers 6

# Sequential mode (for debugging only)
python grade_project.py <project_path> --sequential

# Disable early exit on critical failures
python grade_project.py <project_path> --no-early-exit
```

**Optimization Features:**
- ✅ Parallel skill execution (4 workers by default)
- ✅ Shared file scanning cache (70% less I/O)
- ✅ Early exit on critical failures (<1s for failed projects)
- ✅ Optimized git operations (40% faster)

**Alternative: Run Individual Skills Manually**

If you need fine-grained control, run skills individually:

**Parallel Execution Group 1:** (Independent checks)
```bash
# Run these 3 skills in parallel
/skill check-security <project_path>
/skill validate-docs <project_path>
/skill check-ux <project_path>
```

**Parallel Execution Group 2:** (Code analysis)
```bash
# Run these 2 skills in parallel
/skill analyze-code <project_path>
/skill evaluate-tests <project_path>
```

**Sequential Execution:** (Depends on repo state)
```bash
# Run these sequentially
/skill assess-git <project_path>
/skill grade-research <project_path>
```

### Phase 3: Aggregate Results

Collect results from all skills:

```python
# RECOMMENDED: Use optimized parallel executor
python -c "
from src.core.skill_executor_optimized import run_all_skills_parallel
from src.core.grading_utils import format_results_summary
import json

results = run_all_skills_parallel('<project_path>', max_workers=4)
print(json.dumps(results, indent=2))
"

# ALTERNATIVE: Use sequential executor (slower, for debugging)
python -c "
from src.core.skill_executor import run_all_skills
from src.core.grading_utils import format_results_summary
import json

results = run_all_skills('<project_path>')
print(json.dumps(results, indent=2))
"
```

Or manually aggregate:

```python
results = {
    'security': {score: X, max_score: 10, passed: bool},
    'code_quality': {score: Y, max_score: 30, passed: bool},
    'documentation': {score: Z, max_score: 25, passed: bool},
    'testing': {score: A, max_score: 15, passed: bool},
    'git': {score: B, max_score: 10, passed: bool},
    'research': {score: C, max_score: 10, passed: bool},
    'ux': {score: D, max_score: 10, passed: bool}
}

total_score = X + Y + Z + A + B + C
percentage = (total_score / 100) * 100
grade = calculate_grade(total_score)
passed = total_score >= 70
```

### Phase 4: Generate Detailed Report (MANDATORY)

**CRITICAL:** After completing grading, ALWAYS invoke the detailed report skill:

```bash
/skill generate-detailed-report
```

This generates a comprehensive markdown report saved to `results/` with:
- Specific file paths and line numbers for violations
- Exact issues in each grading category
- Actionable fix recommendations
- Prioritized action items by point value
- Quick-fix terminal commands
- Estimated time to complete fixes

**Report filename format:**
```
results/<project_name>_detailed_report_YYYY-MM-DD_HHMMSS.md
```

### Phase 5: Generate Additional Reports (Optional)

**1. Console Summary:**
```bash
python -c "
from src.core.grading_utils import format_results_summary
print(format_results_summary(results))
"
```

**2. JSON Report:**
```bash
python -c "
import json
with open('grading_report.json', 'w') as f:
    json.dump(results, f, indent=2)
print('[+] JSON report saved to: grading_report.json')
"
```

**3. Detailed Markdown Report:**
Create a comprehensive report with:
- Executive summary
- Category-by-category breakdown
- Detailed findings
- Recommendations
- Action items

### Phase 5: Present Results to User

Display results conversationally:

```
=============================================================
ACADEMIC SOFTWARE AUTO-GRADER RESULTS
=============================================================

Project: <project_name>
Evaluated: <timestamp>

CATEGORY SCORES:
────────────────────────────────────────────────────────────
Security:       [X]/10   [PASS/FAIL]
Code Quality:   [Y]/30   [PASS/FAIL]
Documentation:  [Z]/25   [PASS/FAIL]
Testing:        [A]/15   [PASS/FAIL]
Git Workflow:   [B]/10   [PASS/FAIL]
Research:       [C]/10   [PASS/FAIL]
UX (bonus):     [D]/10   [PASS/FAIL]
────────────────────────────────────────────────────────────

TOTAL SCORE: [XX]/100 ([YY]%)
LETTER GRADE: [A/B/C/D/F]
STATUS: [PASSED/FAILED]

=============================================================

KEY FINDINGS:

[Summarize top 3-5 issues found]

RECOMMENDATIONS:

[Provide actionable steps to improve score]

=============================================================

Reports generated:
- grading_report.json
- grading_report.html (if requested)

Use these reports for:
- Identifying areas for improvement
- Tracking progress over time
- Comparing multiple submissions
```

## Agent Instructions

When a user asks to grade a project, follow this workflow:

1. **Clarify Requirements:**
   - "What is the path to the project you'd like to grade?"
   - "Would you like a quick grading (core skills) or comprehensive grading (all skills)?"
   - "What output format do you prefer? (console, JSON, HTML, all)"

2. **Validate Input:**
   - Check project path exists
   - Verify it's a valid project (has source code)
   - Confirm it's a Git repository (or warn if not)

3. **Execute Grading:**
   - Run all applicable skills
   - Track progress ("Running security check...", "Analyzing code quality...", etc.)
   - Handle errors gracefully (if one skill fails, continue with others)

4. **Aggregate Results:**
   - Collect all skill outputs
   - Calculate total score
   - Determine grade and pass/fail status

5. **Generate Reports:**
   - Create console summary
   - Generate JSON report (always)
   - Generate HTML report (if requested)
   - Save to results/ directory

6. **Present to User:**
   - Display summary in console
   - Highlight critical issues (security violations, missing docs, etc.)
   - Provide actionable recommendations
   - Offer to explain any category in detail

7. **Follow-Up:**
   - Ask if user wants details on any category
   - Offer to run specific skills individually
   - Suggest improvements based on results

## Usage Examples

**Example 1: Basic Grading**
```
User: Grade my project at ./my-project

Agent:
- Validating project path...
- Running 7 grading skills...
  [✓] Security check complete (8/10)
  [✓] Code analysis complete (25/30)
  [✓] Documentation validation complete (20/25)
  [✓] Test evaluation complete (12/15)
  [✓] Git assessment complete (9/10)
  [✓] Research evaluation complete (7/10)
  [✓] UX check complete (8/10)

- Aggregating results...
- Generating reports...

TOTAL SCORE: 81/100 (81%)
GRADE: B
STATUS: PASSED

[Detailed breakdown follows...]
```

**Example 2: Quick Grading (Core Skills Only)**
```
User: Do a quick grade of ./student-submission

Agent: Running quick grading (4 core skills)...
  - Security
  - Code Quality
  - Documentation
  - Testing

Results:
- Security: 10/10 ✓
- Code Quality: 18/30 ⚠ (file size violations)
- Documentation: 22/25 ✓
- Testing: 10/15 ⚠ (low coverage)

Quick Score: 60/80 (75%)

Would you like a comprehensive grading including Git, Research, and UX?
```

**Example 3: Detailed Category Review**
```
User: Grade ./project and give me details on code quality issues

Agent:
[Runs all skills...]

Total Score: 75/100 (C) - PASSED

You requested details on Code Quality:

CODE QUALITY: 22/30
Issues Found:
1. File Size Violations (3 files):
   - src/analyzer.py: 182 lines (32 over limit)
   - src/parser.py: 165 lines (15 over limit)
   - src/validator.py: 158 lines (8 over limit)

2. Docstring Coverage: 85% (target: 90%)
   Missing docstrings:
   - src/utils.py::helper_function
   - src/models.py::DataModel::validate

3. Naming Violations (2):
   - src/app.py:42 - MyFunction should be my_function
   - src/config.py:15 - apiKey should be API_KEY

Recommendations:
[Detailed recommendations follow...]
```

## Error Handling

**Project Not Found:**
```
Error: Project path does not exist: ./nonexistent-project
Please provide a valid project path.
```

**Not a Git Repository:**
```
Warning: Project is not a Git repository.
Git workflow assessment will be skipped.
Continuing with other checks...
```

**Skill Failure:**
```
Error: Security check failed to complete.
Continuing with remaining skills...

Note: Final score will mark security as "incomplete"
```

## Configuration

Agent respects configuration from `config/grading_config.yaml`:

```yaml
scoring_weights:
  security: 0.10
  code_quality: 0.30
  documentation: 0.25
  testing: 0.15
  git_workflow: 0.10
  research: 0.10

thresholds:
  file_size_limit: 150
  test_coverage_min: 0.70
  min_commits: 15

grading_mode: standard  # lenient, standard, strict
```

## Python Helper Integration

All skills have Python helper scripts in `src/` that can be invoked:

```python
# Security check
from src.analyzers.security_scanner import scan_for_secrets
from src.validators.gitignore_validator import validate_gitignore
from src.validators.env_validator import check_env_template

# Code quality
from src.analyzers.file_size_analyzer import check_file_sizes
from src.analyzers.docstring_analyzer import analyze_project_docstrings
from src.validators.naming_validator import analyze_project_naming

# Documentation
from src.analyzers.documentation_checker import check_project_documentation
from src.validators.readme_validator import validate_readme

# Testing
from src.analyzers.test_analyzer import evaluate_tests

# Git
from src.analyzers.git_analyzer import assess_git_workflow

# Research
from src.analyzers.research_analyzer import evaluate_research_quality

# UX
from src.analyzers.ux_analyzer import evaluate_ux_quality

# Orchestration
from src.core.skill_executor import run_all_skills
from src.core.grading_utils import calculate_grade, format_results_summary
```

## Success Criteria

A project receives a passing grade when:
- ✅ Total score ≥ 70 points
- ✅ No critical security violations (hardcoded secrets)
- ✅ All required documentation present
- ✅ At least 70% test coverage
- ✅ All files under 150 lines

## Output Files

After grading, these files are generated:

```
results/
├── grading_report.json          # Machine-readable results
├── grading_report.html          # Human-readable report (if requested)
└── grading_summary.txt          # Console output saved
```

## Tips for Users

1. **Run locally first** - Grade your own project before submission
2. **Fix critical issues** - Security violations auto-fail
3. **Iterate** - Grade multiple times as you improve
4. **Focus on low-hanging fruit** - File size violations are easy to fix
5. **Document as you go** - Don't wait until the end

## Future Enhancements

- **Batch grading**: Grade multiple projects at once
- **Historical tracking**: Compare scores over time
- **Custom rubrics**: Override default scoring weights
- **GitHub integration**: Grade directly from GitHub URLs
- **Plagiarism detection**: Compare against known solutions
