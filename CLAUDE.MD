# CLAUDE.md - Auto-Grader Development Guidelines

## Project Overview

This project builds an **Academic Software Auto-Grader System** as a collection of Claude Code CLI skills. The system evaluates M.Sc. Computer Science project submissions against ISO/IEC 25010 quality standards and academic excellence criteria defined by Dr. Segal Yoram.

**Key Architecture Decision**: Implemented as **modular Claude Code skills** (not agents) for composability, reusability, and maintainability.

---

## CRITICAL REQUIREMENTS - Read This First

### Git Workflow (MANDATORY)

**⚠️ NEVER make just one commit** - This is unacceptable for academic excellence evaluation.

- **Commit frequently**: After each skill implementation, after each test suite, after each documentation update
- **Minimum commits**: 15-25 commits showing clear development progression
- **Commit message format**: `<type>(<scope>): <description> [TASK-ID]`
  - Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
  - Example: `feat(skills): Add document validator skill [P2.2.1]`
- **Reference TASKS.md**: Each commit should map to a task ID for traceability

**Good Commit Progression Example:**
```
feat: Initialize project structure and skill stubs
docs: Add PRD with complete requirements analysis
feat(skills): Implement document validator skill [P2.2.1]
test(skills): Add unit tests for document validator
feat(skills): Implement code structure analyzer [P2.2.2]
test(skills): Add tests for file size limit enforcement
feat(skills): Implement security scanner for hardcoded secrets [P2.2.3]
docs(prompts): Document prompts used for skill architecture
refactor: Split large analyzer module into focused utilities
feat(skills): Implement test coverage evaluator [P2.2.4]
test: Add integration tests for full grading workflow
docs: Update README with installation and usage examples
fix: Handle edge case where .git directory is missing
feat(reporting): Add HTML report generation with CSS styling
chore: Optimize LLM prompts to reduce token usage
```

### Prompt Documentation (MANDATORY)

**📝 SAVE EVERY SIGNIFICANT PROMPT** to the `prompts/` directory **as you work**, not at the end!

**Required Structure:**
```
prompts/
├── README.md                    # Lessons learned, best practices
├── architecture/
│   ├── 001-skill-vs-agent-decision.md
│   ├── 002-skill-orchestration-pattern.md
│   └── 003-grading-rubric-design.md
├── code-generation/
│   ├── 001-document-validator-skill.md
│   ├── 002-ast-parser-for-python.md
│   └── 003-security-scanner-regex-patterns.md
├── testing/
│   ├── 001-unit-test-generation.md
│   └── 002-integration-test-scenarios.md
└── documentation/
    ├── 001-readme-structure.md
    └── 002-architecture-diagrams.md
```

**Each prompt file should include:**
```markdown
# [Prompt Title]

## Context
Why you needed this prompt, what problem you were solving.

## Prompt Text
```
[Exact prompt you used]
```

## Output Received
[Summary or excerpt of what Claude generated]

## Iteration Notes
- What worked well
- What needed refinement
- How you improved the prompt

## Lessons Learned
Best practices to apply to future prompts
```

---

## Code Quality Standards

### File Size Limits (STRICTLY ENFORCED)

**Maximum file length: 150 lines** - **NO EXCEPTIONS**

When a file approaches 150 lines:
1. Identify logical boundaries (classes, functions, concerns)
2. Extract into separate modules
3. Use clear imports to maintain readability
4. Update docstrings to reference related modules

**Example Refactoring:**
```python
# BEFORE: analyze_code.py (215 lines) ❌

# AFTER: Refactor into multiple files ✅
src/analyzers/
├── file_size_checker.py      # 85 lines
├── naming_validator.py        # 72 lines
├── docstring_analyzer.py      # 95 lines
└── complexity_metrics.py      # 68 lines
```

### Code Organization

**Mandatory Directory Structure:**
```
auto-grader/
├── skills/                    # Claude Code skill entry points
│   ├── validate-docs.skill/
│   │   ├── skill.json         # Skill manifest
│   │   └── handler.py         # Skill logic (<150 lines)
│   ├── analyze-code.skill/
│   ├── check-security.skill/
│   ├── evaluate-tests.skill/
│   ├── assess-git.skill/
│   ├── grade-research.skill/
│   ├── check-ux.skill/
│   ├── generate-report.skill/
│   └── grade-github-project.skill/  # Fetch & grade from GitHub
├── agents/                    # Claude Code agents
│   └── grader-orchestrator/   # Main orchestrator agent
│       ├── agent.yaml         # Agent configuration
│       └── main.py            # Agent entry point
├── src/                       # Shared utilities (imported by skills)
│   ├── core/
│   │   ├── project_scanner.py
│   │   └── config_loader.py
│   ├── utils/
│   │   ├── file_utils.py
│   │   ├── git_utils.py
│   │   └── github_utils.py    # GitHub repo cloning/fetching
│   ├── parsers/
│   │   ├── python_parser.py
│   │   ├── js_parser.py
│   │   └── markdown_parser.py
│   ├── analyzers/
│   │   ├── code_quality.py
│   │   ├── test_coverage.py
│   │   └── git_history.py
│   ├── validators/
│   │   ├── document_validator.py
│   │   └── security_validator.py
│   └── reporters/
│       ├── json_reporter.py
│       ├── html_reporter.py
│       └── cli_reporter.py
├── tests/
│   ├── unit/
│   │   ├── test_validators.py
│   │   └── test_analyzers.py
│   ├── integration/
│   │   └── test_full_grading.py
│   └── fixtures/
│       └── sample_projects/
├── data/
│   └── grading_rubric.yaml    # Configurable scoring weights
├── results/                   # Auto-generated reports
├── docs/
│   ├── architecture/
│   │   ├── c4-context.md
│   │   ├── c4-container.md
│   │   └── c4-component.md
│   └── ADRs/
│       ├── 001-skill-architecture.md
│       └── 002-grading-algorithm.md
├── config/
│   ├── .env.example
│   └── grading_config.yaml
├── prompts/                   # Prompt engineering log
│   ├── README.md
│   ├── architecture/
│   ├── code-generation/
│   ├── testing/
│   └── documentation/
├── README.md
├── requirements.txt
├── .env
└── .gitignore
```

### Naming Conventions

**Python (primary language):**
- Files: `snake_case.py` (e.g., `document_validator.py`)
- Classes: `PascalCase` (e.g., `CodeQualityAnalyzer`)
- Functions/Methods: `snake_case` (e.g., `check_file_size()`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_LINES = 150`)
- Variables: `snake_case` (e.g., `total_score`)

**JavaScript/TypeScript (if used):**
- Files: `kebab-case.ts` (e.g., `skill-orchestrator.ts`)
- Classes: `PascalCase`
- Functions: `camelCase`
- Constants: `UPPER_SNAKE_CASE`

### Documentation Requirements

#### Every Function Must Have:
```python
def validate_test_coverage(project_path: str, min_coverage: float = 0.7) -> dict:
    """
    Validate that unit tests meet minimum coverage requirements.

    This function runs coverage.py on the project's test suite and compares
    the measured coverage against the threshold defined in ISO/IEC 25010
    quality standards (70% minimum, 90% for critical paths).

    Args:
        project_path: Absolute path to the project root directory
        min_coverage: Minimum acceptable coverage ratio (default: 0.7 = 70%)

    Returns:
        dict: {
            'coverage': float (0.0-1.0),
            'passed': bool,
            'details': {
                'statement_coverage': float,
                'branch_coverage': float,
                'missing_lines': list[str]  # "file.py:42-45"
            }
        }

    Raises:
        FileNotFoundError: If project_path does not exist
        RuntimeError: If coverage tool execution fails

    Example:
        >>> result = validate_test_coverage('/path/to/student/project')
        >>> print(f"Coverage: {result['coverage']:.1%}")
        Coverage: 73.5%
    """
```

#### Every Class Must Have:
```python
class CodeQualityAnalyzer:
    """
    Analyzes source code quality metrics against academic standards.

    This analyzer enforces file size limits, naming conventions, docstring
    coverage, and code complexity thresholds. It uses AST parsing for
    language-agnostic analysis where possible.

    Design Decision: Chose AST-based analysis over regex to accurately
    handle edge cases like multi-line strings and nested functions.

    Attributes:
        max_file_lines (int): Maximum lines per file (default: 150)
        min_docstring_coverage (float): Required docstring ratio (default: 0.9)
        max_complexity (int): Maximum cyclomatic complexity (default: 10)

    Example:
        >>> analyzer = CodeQualityAnalyzer()
        >>> results = analyzer.analyze_directory('/path/to/src')
        >>> print(results['violations'])
        ['file.py exceeds 150 lines (actual: 182)', ...]
    """
```

#### Every Module Must Have:
```python
"""
Code Quality Analyzer Module

Provides comprehensive static analysis of source code quality for academic
software projects. Enforces ISO/IEC 25010 maintainability characteristics:
modularity, reusability, analyzability, modifiability, and testability.

This module is used by the `analyze-code` skill to evaluate student
submissions. It supports Python, JavaScript, and TypeScript codebases.

Design Rationale:
- AST parsing chosen over regex for accuracy
- Pluggable analyzer architecture for language extensibility
- Caching of parse trees to avoid redundant work

Example:
    from src.analyzers.code_quality import CodeQualityAnalyzer

    analyzer = CodeQualityAnalyzer()
    report = analyzer.analyze_directory('./student_project/src')
"""
```

---

## Configuration Management

### Environment Variables

**NEVER hardcode**:
- Claude API keys
- File paths (use relative paths or config)
- Scoring thresholds (use `grading_config.yaml`)

**Required `.env` variables:**
```bash
# Claude API (inherited from Claude Code, but document if skill needs it)
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Customize grading strictness
GRADING_MODE=standard  # Options: lenient, standard, strict
MAX_FILE_LINES=150
MIN_TEST_COVERAGE=0.70

# Optional: LLM model selection
CLAUDE_MODEL=claude-sonnet-4-5-20250929
```

**Create `.env.example`:**
```bash
# Claude API Key (required)
ANTHROPIC_API_KEY=your_key_here

# Grading Configuration
GRADING_MODE=standard
MAX_FILE_LINES=150
MIN_TEST_COVERAGE=0.70

# Model Selection
CLAUDE_MODEL=claude-sonnet-4-5-20250929
```

**Load environment variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

MAX_FILE_LINES = int(os.environ.get("MAX_FILE_LINES", "150"))
MIN_TEST_COVERAGE = float(os.environ.get("MIN_TEST_COVERAGE", "0.7"))
```

### Configuration Files

**`config/grading_config.yaml`** - Centralized grading rubric:
```yaml
# Grading Rubric Configuration
version: "1.0"

scoring_weights:
  documentation: 0.25      # PRD, README, Architecture docs
  code_quality: 0.30       # Structure, naming, comments
  testing: 0.15            # Coverage, edge cases
  security: 0.10           # Secrets, vulnerabilities
  git_workflow: 0.10       # Commit history, branching
  research_quality: 0.10   # Parameter exploration, analysis

thresholds:
  file_size_limit: 150           # lines
  test_coverage_min: 0.70        # 70%
  test_coverage_critical: 0.90   # 90% for core logic
  min_commits: 10
  max_complexity: 10             # cyclomatic complexity

penalties:
  hardcoded_secret: -50          # Major security violation
  missing_docstring: -2          # Per function
  exceeds_file_limit: -10        # Per file
  insufficient_commits: -15      # If < min_commits

point_distribution:
  total_points: 100
  passing_score: 70
  excellence_threshold: 90
```

---

## Testing Requirements

### Coverage Targets
- **Minimum**: 70% overall code coverage
- **Critical Paths**: 90%+ coverage for grading logic (validators, analyzers)
- **Business Logic**: 85%+ for scoring algorithms

### Test Types Required

1. **Unit Tests** - Test each validator/analyzer in isolation
2. **Edge Case Tests** - Boundary conditions and unusual scenarios
3. **Error Handling Tests** - Failure scenarios
4. **Integration Tests** - Full grading workflow

### Test Structure
```python
def test_function_name_scenario_expected_result():
    """
    Test that [function] does [behavior] when [condition].
    """
    # Arrange
    input_data = ...
    expected = ...

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected
```

---

## Error Handling

### Required Practices

1. **Defensive Programming**: Validate all inputs
2. **Clear Error Messages**: User-friendly and actionable
3. **Detailed Logging**: For debugging purposes
4. **Graceful Degradation**: System continues functioning when possible

---

## Git Practices

### IMPORTANT: Frequent Commits Required

**⚠️ NEVER make just one large commit** - this is unacceptable for academic evaluation!

- **Make multiple commits throughout development** as you complete each logical unit of work
- Commit after completing each task, feature, or significant change
- Each commit should represent a single logical change
- Aim for **15-25+ commits minimum** for a complete project
- Build up a clear history that shows the evolution of the project

### Commit Messages

**Format:**
```
<type>(<scope>): <short description> [TASK-ID]

<optional longer description>

<optional references to issues/tasks>
```

**Types:**
- `feat`: New feature (skill implementation, analyzer addition)
- `fix`: Bug fix
- `docs`: Documentation changes (README, prompts/, ADRs)
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Build config, dependencies, tooling

---

## Task Tracking & Progress Updates

### Automatic TASKS.md Updates

**CRITICAL**: Update `TASKS.md` as you work!

1. **Before starting a task**: Change status from 🔴 to 🟡, add timestamp
2. **While working**: Add progress notes
3. **After completing**: Change to 🟢, add completion timestamp
4. **Update phase progress** after each task completion
5. **Daily Progress Log**: Add entries at end of each work session

### CRITICAL: Document Prompts as You Work

**Do NOT wait until the end!** Save prompts immediately after using them.

---

## Quality Checklist Before Completion

### Code Quality
- [ ] All files under 150 lines
- [ ] Docstrings on all functions/classes/modules
- [ ] No hardcoded secrets
- [ ] 70%+ test coverage
- [ ] Edge cases documented with test examples
- [ ] Error handling comprehensive

### Git & Version Control
- [ ] Git history shows 15-25+ commits
- [ ] Each commit represents a logical unit of work
- [ ] Commit messages follow `<type>(<scope>): <description> [TASK-ID]` format
- [ ] Commits reference task IDs from TASKS.md
- [ ] Clean, meaningful progression of development

### Documentation
- [ ] README complete as full user manual
- [ ] Architecture diagrams created (C4 Model: Context, Container, Component)
- [ ] ADRs document major decisions
- [ ] `prompts/` directory fully populated
- [ ] `prompts/README.md` documents best practices learned

### Testing
- [ ] Unit tests for all validators and analyzers
- [ ] Integration test for full grading workflow
- [ ] Edge case tests
- [ ] Test coverage report generated
- [ ] All tests pass

### Configuration
- [ ] `.env.example` created with all required variables
- [ ] `grading_config.yaml` documented with comments
- [ ] No hardcoded paths or thresholds
- [ ] `.gitignore` updated

---

**Remember**: This is an academic excellence project. Every decision should demonstrate depth of understanding, professional practices, research rigor, and prompt engineering mastery.
