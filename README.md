# Academic Software Auto-Grader System

An intelligent auto-grading system for M.Sc. Computer Science project submissions, built as a collection of **Claude Code skills** and orchestrated by a conversational AI agent.

## Overview

This system evaluates academic software projects against **ISO/IEC 25010 quality standards** and academic excellence criteria, providing comprehensive, automated grading with actionable feedback.

**Key Innovation:** Hybrid approach combining static analysis (file sizes, naming, coverage) with LLM-powered subjective assessment (documentation quality, research depth, UX evaluation).

## Architecture

- **Claude Code Skills** (7 modular grading components)
- **Orchestrator Agent** (intelligent coordinator with natural language interface)
- **Python Analyzers** (helper scripts for static analysis)
- **Multi-format Reports** (JSON, HTML, console output)

## Grading Rubric (100 Points Total)

| Category | Points | Checks |
|----------|--------|--------|
| **Security** | 10 | Hardcoded secrets, .gitignore, .env config |
| **Code Quality** | 30 | File sizes (≤150 lines), docstrings (≥90%), naming conventions |
| **Documentation** | 25 | PRD, README, PLANNING, TASKS, architecture docs |
| **Testing** | 15 | Test coverage (≥70%), test count, edge cases |
| **Git Workflow** | 10 | Commit count (15-25), conventional format, distribution |
| **Research** | 10 | Parameter exploration, statistical analysis, comparisons |
| **UX (bonus)** | 10 | README usability, CLI help, installation clarity |

**Passing Grade:** 70/100 (70%)

## Installation

### Prerequisites

- **Python 3.8+** (for helper scripts)
- **Claude Code CLI** (for skills and agent)
- **Git** (for repository analysis)

### Setup

```bash
# Clone repository
git clone https://github.com/OmryTzabbar1/RamiAutoGrader.git
cd RamiAutoGrader

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
cp config/.env.example .env
# Edit .env with your settings
```

## Usage

### Option 1: Use the Orchestrator Agent (Recommended)

The agent provides a conversational interface and automatically coordinates all skills:

```bash
# Invoke the agent
claude agent grade-project

# Then interact conversationally:
# Agent: "What project would you like to grade?"
# You: "Grade ./my-project"
# Agent: [Runs all 7 skills and generates comprehensive report]
```

The agent can:
- Grade projects with a single command
- Run quick grading (core skills only) or comprehensive grading (all skills)
- Explain results in detail
- Provide actionable recommendations
- Generate multiple report formats

### Option 2: Run Individual Skills

Each skill can be run independently using the `/skill` command:

#### Security Check (10 points)
```bash
/skill check-security

# Checks:
# - Hardcoded secrets (API keys, passwords, tokens)
# - .gitignore patterns (.env, *.key, *.pem)
# - Environment configuration (.env.example)
```

#### Code Quality Analysis (30 points)
```bash
/skill analyze-code

# Checks:
# - File size limit: 150 lines maximum (STRICTLY ENFORCED)
# - Docstring coverage: 90% minimum
# - Naming conventions: snake_case, PascalCase, UPPER_SNAKE_CASE
# - Code complexity (optional)
```

#### Documentation Validation (25 points)
```bash
/skill validate-docs

# Checks:
# - Required documents: PRD.md, README.md, PLANNING.md, TASKS.md
# - README quality: sections, code examples, troubleshooting
# - Architecture documentation
```

#### Test Evaluation (15 points)
```bash
/skill evaluate-tests

# Checks:
# - Test file presence (minimum 5 files)
# - Test count (minimum 30 tests)
# - Coverage (70% minimum, 90% target)
# - Edge case testing
```

#### Git Workflow Assessment (10 points)
```bash
/skill assess-git

# Checks:
# - Commit count (15-25 commits showing progression)
# - Conventional commit format: <type>(<scope>): <description> [TASK-ID]
# - Commit distribution over time
```

#### Research Quality Evaluation (10 points)
```bash
/skill grade-research

# Checks:
# - Parameter exploration (3+ parameters tested)
# - Statistical analysis (metrics, baselines)
# - Comparative analysis (pros/cons of approaches)
# - Data visualizations
```

#### UX Quality Evaluation (10 points - bonus)
```bash
/skill check-ux

# Checks:
# - README usability (clear sections, examples)
# - CLI help availability (--help flag)
# - Installation clarity
# - Usage examples
```

### Option 3: Use Python Helpers Directly

For integration into other tools or scripts:

```python
# Import orchestrator
from src.core.skill_executor import run_all_skills
from src.core.grading_utils import format_results_summary

# Grade a project
results = run_all_skills('./student-project')

# Display summary
print(format_results_summary(results))

# Access individual scores
print(f"Security: {results['results']['security']['score']}/10")
print(f"Code Quality: {results['results']['code_quality']['score']}/30")
print(f"Total: {results['total_score']}/100")
print(f"Grade: {results['grade']}")
```

## Output Formats

### Console Summary

```
============================================================
ACADEMIC SOFTWARE AUTO-GRADER RESULTS
============================================================

CATEGORY SCORES:
────────────────────────────────────────────────────────────
Security:        8.0 / 10   [PASS]
Code Quality:   22.0 / 30   [PASS]
Documentation:  20.0 / 25   [PASS]
Testing:        12.0 / 15   [PASS]
Git Workflow:    9.0 / 10   [PASS]
Research:        7.0 / 10   [PASS]
UX (bonus):      8.0 / 10   [PASS]
────────────────────────────────────────────────────────────

TOTAL SCORE: 78.0/100 (78.0%)
GRADE: C
STATUS: PASSED

============================================================
```

### JSON Report

```json
{
  "total_score": 78.0,
  "max_score": 100,
  "percentage": 78.0,
  "grade": "C",
  "passed": true,
  "categories": {
    "security": {
      "score": 8.0,
      "max_score": 10,
      "passed": true,
      "secrets_found": 0,
      "gitignore_valid": true,
      "env_valid": true
    },
    "code_quality": {
      "score": 22.0,
      "max_score": 30,
      "passed": true,
      "file_size_violations": 2,
      "docstring_coverage": 0.87,
      "naming_violations": 5
    }
    // ... other categories
  }
}
```

### HTML Report (optional)

Color-coded, interactive HTML report with:
- Executive summary
- Category breakdown with charts
- Detailed findings
- Actionable recommendations
- Progress tracking over time

## Configuration

Customize grading behavior via `config/grading_config.yaml`:

```yaml
scoring_weights:
  security: 0.10
  code_quality: 0.30
  documentation: 0.25
  testing: 0.15
  git_workflow: 0.10
  research: 0.10

thresholds:
  file_size_limit: 150           # lines
  test_coverage_min: 0.70        # 70%
  test_coverage_critical: 0.90   # 90% for core logic
  min_commits: 15
  max_complexity: 10

penalties:
  hardcoded_secret: -50          # Major security violation
  missing_docstring: -2          # Per function
  exceeds_file_limit: -10        # Per file

grading_mode: standard  # Options: lenient, standard, strict
```

## Project Structure

```
RamiAutoGrader/
├── .claude/                    # Claude Code skills and agents
│   ├── skills/                 # 7 grading skills (Markdown format)
│   │   ├── check-security/SKILL.md
│   │   ├── analyze-code/SKILL.md
│   │   ├── validate-docs/SKILL.md
│   │   ├── evaluate-tests/SKILL.md
│   │   ├── assess-git/SKILL.md
│   │   ├── grade-research/SKILL.md
│   │   └── check-ux/SKILL.md
│   └── agents/                 # Orchestrator agent
│       └── grade-project/agent.md
├── src/                        # Python helper scripts
│   ├── core/                   # Orchestration and utilities
│   ├── analyzers/              # Static analysis tools
│   ├── validators/             # Validation logic
│   ├── parsers/                # AST parsing
│   └── utils/                  # File operations, Git commands
├── config/                     # Configuration files
│   ├── grading_config.yaml     # Grading rubric
│   └── .env.example            # Environment template
├── docs/                       # Project documentation
├── tests/                      # Test suite
└── results/                    # Generated grading reports
```

## Development Workflow

### For Students (Using the Grader)

1. **Before submission:**
   ```bash
   # Grade your own project
   claude agent grade-project
   # You: "Grade ./my-project"
   ```

2. **Review results:**
   - Check total score (need ≥70 to pass)
   - Read detailed findings
   - Follow recommendations

3. **Fix issues:**
   - Address critical violations (security, file sizes)
   - Improve low-scoring categories
   - Add missing documentation/tests

4. **Re-grade:**
   ```bash
   # Grade again after improvements
   claude agent grade-project
   ```

5. **Submit when passing:**
   - Ensure score ≥ 70/100
   - All critical checks pass
   - Documentation complete

### For Instructors (Grading Submissions)

1. **Single project:**
   ```bash
   claude agent grade-project
   # Agent: "What project would you like to grade?"
   # You: "Grade ./student-submissions/student-123"
   ```

2. **Batch grading (future feature):**
   ```bash
   # Grade multiple projects
   /grade-batch ./student-submissions/
   ```

3. **Review reports:**
   - JSON reports in `results/`
   - Compare across submissions
   - Track improvement over time

## Common Issues & Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'anthropic'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Not a Git repository"

**Solution:** Initialize Git or skip Git assessment
```bash
git init
git add .
git commit -m "Initial commit"
```

### Issue: "File size violations (all files fail)"

**Solution:** Files exceed 150-line limit - split into smaller modules
```bash
# Use the analyzer to identify oversized files
python src/analyzers/file_size_analyzer.py ./my-project

# Refactor files using Single Responsibility Principle
```

### Issue: "Test coverage below 70%"

**Solution:** Add more tests
```bash
# Run coverage report
pytest --cov=src tests/

# Identify uncovered lines
pytest --cov=src --cov-report=html tests/
# Open htmlcov/index.html
```

## Example: Complete Grading Session

```bash
# Start the agent
$ claude agent grade-project

Agent: "Hello! I'm the Academic Software Auto-Grader. What project would you like to grade?"

You: "Grade ./my-final-project"

Agent: "Grading ./my-final-project..."
[*] Running comprehensive grading (7 skills)...
  [✓] Security check complete (10/10)
  [✓] Code analysis complete (26/30)
  [✓] Documentation validation complete (23/25)
  [✓] Test evaluation complete (13/15)
  [✓] Git assessment complete (8/10)
  [✓] Research evaluation complete (9/10)
  [✓] UX check complete (7/10)

[Aggregating results...]

============================================================
TOTAL SCORE: 89/100 (89%)
GRADE: B
STATUS: PASSED
============================================================

Great work! Your project demonstrates solid academic rigor.

Key Strengths:
- Excellent security practices (no secrets found)
- Comprehensive documentation with all required sections
- Good test coverage (85%)

Areas for Improvement:
- 2 files exceed 150-line limit (need refactoring)
- Docstring coverage at 87% (target: 90%)
- Could add more parameter exploration in research

Would you like details on any specific category?

You: "Tell me about the file size violations"

Agent: "I found 2 files exceeding the 150-line limit:

1. src/analyzer.py: 182 lines (32 over limit)
   Recommendation: Split into analyzer_core.py and analyzer_utils.py

2. src/parser.py: 165 lines (15 over limit)
   Recommendation: Extract AST utilities to separate module

This is the most straightforward improvement - refactoring these would boost your Code Quality score from 26/30 to 29/30, bringing your total to 92/100 (A-)!"
```

## Academic Standards Enforced

This auto-grader enforces rigorous academic standards:

✅ **150-line file limit** - Encourages modularity (STRICTLY ENFORCED)
✅ **90% docstring coverage** - Ensures comprehensive documentation
✅ **70% test coverage** - Validates testing rigor
✅ **15-25 commits** - Demonstrates iterative development
✅ **Conventional commits** - Professional version control practices
✅ **Comprehensive documentation** - PRD, README, PLANNING, TASKS required
✅ **Research methodology** - Parameter exploration and analysis
✅ **Security best practices** - No secrets, proper .gitignore

## Documentation

- [PRD.md](PRD.md) - Product Requirements Document
- [PLANNING.MD](PLANNING.MD) - Technical Architecture & ADRs
- [CLAUDE.MD](CLAUDE.MD) - Development Guidelines
- [TASKS.MD](TASKS.MD) - Task Breakdown & Progress

## Project Status

✅ **Phase 1 Complete:** Infrastructure & Core Utilities
✅ **Phase 2 Complete:** All 7 Grading Skills
✅ **Phase 3 Complete:** Orchestrator Agent
🚧 **Current:** Testing & Documentation

See [TASKS.MD](TASKS.MD) for detailed progress tracking.

## Contributing

This is an academic project for the M.Sc. Computer Science program. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Follow development guidelines (CLAUDE.MD)
4. Submit pull request with tests

## License

Academic project for M.Sc. Computer Science program.

## Contact

**Repository:** https://github.com/OmryTzabbar1/RamiAutoGrader.git
**Issues:** https://github.com/OmryTzabbar1/RamiAutoGrader/issues

---

**Built with:** Claude Code, Python, AST parsing, Git analysis
**Grading Standard:** ISO/IEC 25010 Software Quality Model
