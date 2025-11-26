# Task Breakdown Document
# Academic Software Auto-Grader System

**Project**: Academic Software Auto-Grader
**Version**: 1.0
**Date**: 2025-01-25
**Author**: Rami (M.Sc. Computer Science Program)

---

## Overview

This document provides a comprehensive, prioritized breakdown of all tasks required to build the Academic Software Auto-Grader system. Tasks are organized by phase, with clear dependencies and acceptance criteria.

**Task Notation:**
- **[P0]** = Must-have (Phase 1 - Core Skills)
- **[P1]** = Should-have (Phase 2 - Advanced Analysis)
- **[P2]** = Nice-to-have (Phase 3 - Batch Processing)
- **[DEP: X]** = Depends on task X being completed first

---

## Phase 1: Project Setup & Infrastructure

### P1.1: Repository Initialization [P0]

**Tasks:**

- [x] **P1.1.1**: Initialize Git repository ✅
  - Create `.gitignore` for Python (venv, __pycache__, *.pyc, .env)
  - Initial commit: "feat: Initialize auto-grader project structure"
  - **Acceptance**: Git repo created with proper .gitignore

- [x] **P1.1.2**: Create project directory structure ✅
  ```
  auto-grader/
  ├── skills/
  ├── agents/
  ├── src/
  │   ├── parsers/
  │   ├── analyzers/
  │   ├── validators/
  │   └── reporters/
  ├── tests/
  ├── config/
  ├── docs/
  ├── prompts/
  └── README.md
  ```
  - **Acceptance**: All directories exist, README has basic project description

- [x] **P1.1.3**: Setup Python environment ✅
  - Create `requirements.txt` with dependencies:
    ```
    anthropic>=0.20.0
    pyyaml>=6.0
    jinja2>=3.1.0
    pytest>=7.4.0
    pytest-cov>=4.1.0
    detect-secrets>=1.4.0
    ```
  - Create virtual environment: `python -m venv venv`
  - Install dependencies: `pip install -r requirements.txt`
  - **Acceptance**: `pip list` shows all dependencies installed

- [x] **P1.1.4**: Setup project documentation files ✅
  - Copy PRD.md, CLAUDE.md, PLANNING.md, TASKS.md to project root
  - Create docs/ARCHITECTURE.md with C4 diagrams
  - **Acceptance**: All required docs present and version-controlled

- [x] **P1.1.5**: Create grading configuration template ✅
  - Create `config/grading_config.yaml` with scoring weights and thresholds
  - Document all configuration options in comments
  - **Acceptance**: Valid YAML file with all required fields

---

## Phase 2: Core Utility Development

### P2.1: File System Utilities [P0] ✅ COMPLETE

**Tasks:**

- [x] **P2.1.1**: Implement safe file reader ✅
  - Create `src/utils/file_utils.py`
  - Function: `safe_read_file(file_path, max_size_mb=10)`
  - Handle encoding errors gracefully
  - **Max 150 lines per file** (split into multiple modules if needed)
  - **Acceptance**: Unit test passes for various file types and error cases

- [x] **P2.1.2**: Implement code file finder ✅
  - Create `src/utils/file_finder.py`
  - Function: `find_code_files(project_path, extensions=['.py', '.js', '.ts'])`
  - Skip common ignore dirs (node_modules, venv, .git)
  - **Acceptance**: Correctly finds all code files in test project

- [x] **P2.1.3**: Implement line counter ✅
  - Create `src/utils/line_counter.py`
  - Function: `count_lines(file_path, exclude_comments=False)`
  - Handle different comment styles (Python #, JS //, etc.)
  - **Acceptance**: Accurate count for files with/without comments

- [x] **P2.1.4**: Write unit tests for file utilities ✅
  - Test file: `tests/test_file_utils.py`
  - Coverage target: ≥80%
  - Test edge cases: empty files, binary files, missing files
  - **Acceptance**: `pytest tests/test_file_utils.py --cov` shows ≥80%

---

### P2.2: Core Analyzers [P0] ✅ COMPLETE

**Tasks:**

- [x] **P2.2.1**: Implement File Size Analyzer ✅
  - Create `src/analyzers/file_size_analyzer.py`
  - Function: `check_file_sizes(project_path, limit=150)`
  - Return list of violations with file path, line count, excess
  - **Critical**: This is a strict requirement, no exceptions
  - **Acceptance**: Detects all files >150 lines in test project

- [x] **P2.2.2**: Implement Python AST Parser ✅
  - Create `src/parsers/python_parser.py`
  - Functions:
    - `parse_python_file(file_path)` → AST tree
    - `extract_functions(ast_tree)` → list of function definitions
    - `extract_classes(ast_tree)` → list of class definitions
  - **Acceptance**: Correctly parses valid Python files, handles syntax errors

- [x] **P2.2.3**: Implement Docstring Analyzer ✅
  - Create `src/analyzers/docstring_analyzer.py` (max 150 lines)
  - Function: `check_docstrings(file_path)`
  - Detect missing docstrings on functions, classes, modules
  - Calculate coverage percentage
  - **Acceptance**: Identifies all missing docstrings in test files

- [x] **P2.2.4**: Implement Naming Convention Validator ✅
  - Create `src/validators/naming_validator.py`
  - Check:
    - Functions: snake_case (Python) or camelCase (JS)
    - Classes: PascalCase
    - Constants: UPPER_SNAKE_CASE
  - **Acceptance**: Flags violations in test project

- [x] **P2.2.5**: Implement Code Complexity Analyzer ✅
  - Create `src/analyzers/complexity_analyzer.py`
  - Calculate cyclomatic complexity per function
  - Flag functions with complexity >10
  - **Acceptance**: Correctly identifies complex functions

- [x] **P2.2.6**: Write unit tests for analyzers ✅
  - Test file: `tests/test_analyzers.py`
  - Test each analyzer independently
  - Coverage target: ≥80%
  - **Acceptance**: All analyzer tests pass

---

### P2.3: Security Scanner [P0] ✅ COMPLETE

**Tasks:**

- [x] **P2.3.1**: Implement Secret Detection ✅
  - Create `src/analyzers/security_scanner.py`
  - Regex patterns for:
    - API keys (api_key, apikey)
    - Passwords (password, passwd)
    - AWS keys (AKIA...)
    - Private keys (BEGIN PRIVATE KEY)
  - Return findings with file, line number, snippet
  - **Acceptance**: Detects all test secrets in sample files

- [x] **P2.3.2**: Implement .gitignore Validator ✅
  - Function: `validate_gitignore(project_path)`
  - Check .gitignore exists
  - Verify it includes: .env, *.key, credentials.json
  - **Acceptance**: Correctly validates good/bad .gitignore files

- [x] **P2.3.3**: Implement .env Template Checker ✅
  - Function: `check_env_template(project_path)`
  - Verify .env.example exists
  - Ensure .env is in .gitignore
  - Warn if .env is committed to Git
  - **Acceptance**: Detects missing .env.example

- [x] **P2.3.4**: Write unit tests for security scanner ✅
  - Test file: `tests/test_security_scanner.py`
  - Test with known secrets (test fixtures)
  - Coverage target: ≥80%
  - **Acceptance**: All security tests pass

---

### P2.4: Document Validator [P0] ✅ COMPLETE

**Tasks:**

- [x] **P2.4.1**: Implement Markdown Parser ✅
  - Create `src/parsers/markdown_parser.py`
  - Function: `parse_markdown(file_path)`
  - Extract headers (H1, H2, H3)
  - Extract word count
  - **Acceptance**: Correctly parses markdown structure

- [x] **P2.4.2**: Implement Document Presence Checker ✅
  - Create `src/validators/document_validator.py`
  - Function: `check_required_docs(project_path)`
  - Required docs: PRD.md, CLAUDE.md, PLANNING.md, TASKS.md, README.md
  - Return list of missing documents
  - **Acceptance**: Detects all missing docs in test project

- [x] **P2.4.3**: Implement Section Validator ✅
  - Function: `validate_sections(file_path, required_sections)`
  - Check if required sections present in markdown
  - Example: PRD must have "Functional Requirements", "Success Metrics"
  - **Acceptance**: Correctly validates section presence

- [x] **P2.4.4**: Write unit tests for document validator ✅
  - Test file: `tests/test_document_validator.py`
  - Test with valid/invalid markdown files
  - Coverage target: ≥80%
  - **Acceptance**: All document validation tests pass

---

### P2.5: Test Coverage Analyzer [P0] ✅ COMPLETE

**Tasks:**

- [x] **P2.5.1**: Implement Coverage Report Parser (Python) ✅
  - Create `src/analyzers/coverage_analyzer.py`
  - Function: `parse_python_coverage(project_path)`
  - Read `coverage.json` (pytest --cov output)
  - Extract total coverage percentage
  - Extract per-file coverage
  - **Acceptance**: Correctly parses sample coverage.json

- [x] **P2.5.2**: Implement Coverage Report Parser (JavaScript) ✅
  - Function: `parse_js_coverage(project_path)`
  - Read Jest coverage output (JSON format)
  - **Acceptance**: Correctly parses sample Jest output

- [x] **P2.5.3**: Implement Test File Detector ✅
  - Function: `find_test_files(project_path)`
  - Detect files matching: test_*.py, *_test.py, *.test.js, *.spec.js
  - Count total tests
  - **Acceptance**: Finds all test files in sample project

- [x] **P2.5.4**: Write unit tests for coverage analyzer ✅
  - Test file: `tests/test_coverage_analyzer.py`
  - Test with sample coverage reports (fixtures)
  - Coverage target: ≥80%
  - **Acceptance**: All coverage tests pass

---

### P2.6: Git History Analyzer [P1] ✅ COMPLETE

**Tasks:**

- [x] **P2.6.1**: Implement Git Command Wrapper ✅
  - Create `src/utils/git_utils.py`
  - Function: `run_git_command(cmd, cwd)`
  - Safe subprocess execution
  - Handle errors gracefully (not a git repo, etc.)
  - **Acceptance**: Can execute basic git commands

- [x] **P2.6.2**: Implement Commit Counter ✅
  - Function: `count_commits(project_path)`
  - Use: `git log --oneline --no-merges`
  - Return total commit count
  - **Acceptance**: Correct count for test repository

- [x] **P2.6.3**: Implement Commit Message Quality Analyzer ✅
  - Function: `analyze_commit_messages(project_path)`
  - Check for:
    - Conventional commit format (feat:, fix:, docs:, etc.)
    - Descriptive messages (>10 characters)
    - Task references ([TASK-XXX])
  - Calculate average quality score
  - **Acceptance**: Correctly scores test commits

- [x] **P2.6.4**: Write unit tests for Git analyzer ✅
  - Test file: `tests/test_git_analyzer.py`
  - Test with mock Git repository (test fixtures)
  - Coverage target: ≥80%
  - **Acceptance**: All Git tests pass

---

### P2.7: Report Generation [P0]

**Tasks:**

- [ ] **P2.7.1**: Define Data Models
  - Create `src/models/grading_result.py`
  - Classes: `Violation`, `CategoryScore`, `GradingResult`
  - Use dataclasses for clean structure
  - **Acceptance**: Can instantiate all models with sample data

- [ ] **P2.7.2**: Implement JSON Reporter
  - Create `src/reporters/json_reporter.py`
  - Function: `generate_json_report(grading_result, output_path)`
  - Convert GradingResult to JSON
  - Save to file
  - **Acceptance**: Generates valid JSON file

- [ ] **P2.7.3**: Implement HTML Reporter
  - Create `src/reporters/html_reporter.py`
  - Use Jinja2 templates
  - Create template: `src/reporters/templates/report.html`
  - Color-coded sections (green=pass, yellow=warn, red=fail)
  - **Acceptance**: Generates readable HTML report

- [ ] **P2.7.4**: Implement CLI Formatter
  - Create `src/reporters/cli_formatter.py`
  - Function: `print_summary(grading_result)`
  - Use color codes (ANSI escape sequences)
  - Pretty-print summary with emojis (✅ ⚠️ ❌)
  - **Acceptance**: Displays formatted output in terminal

- [ ] **P2.7.5**: Write unit tests for reporters
  - Test file: `tests/test_reporters.py`
  - Test JSON structure validity
  - Test HTML template rendering
  - Coverage target: ≥80%
  - **Acceptance**: All reporter tests pass

---

## Phase 3: Claude Code Skills Implementation

### P3.1: /validate-docs Skill [P0] ✅ COMPLETE

**Dependencies**: [P2.4.1, P2.4.2, P2.4.3]

**Tasks:**

- [x] **P3.1.1**: Create skill directory structure ✅
  - Create `skills/validate-docs.skill/`
  - Create `skills/validate-docs.skill/skill.yaml`
  - Define skill metadata (name, description, parameters)
  - **Acceptance**: Valid skill configuration

- [x] **P3.1.2**: Implement skill entry point ✅
  - Create `skills/validate-docs.skill/main.py`
  - Parse command arguments (project path)
  - Call document validator utilities
  - Format output
  - **Max 150 lines** - delegate logic to src/validators
  - **Acceptance**: Skill executable via Claude Code CLI

- [x] **P3.1.3**: Integrate LLM for quality assessment ✅
  - Function: `assess_doc_quality_llm(doc_content)`
  - Send key sections to Claude API
  - Prompt: "Rate this PRD's completeness (1-10). List missing elements."
  - Parse LLM response for score
  - **Acceptance**: Returns quality score for test document

- [x] **P3.1.4**: Generate document validation report ✅
  - Combine static checks (presence, sections) with LLM quality score
  - Return structured result (JSON)
  - **Acceptance**: Complete report for sample project

- [x] **P3.1.5**: Write integration test for skill ✅
  - Test file: `tests/test_validate_docs_skill.py`
  - Test with sample project (has all docs)
  - Test with incomplete project (missing docs)
  - **Acceptance**: Skill correctly identifies issues

---

### P3.2: /analyze-code Skill [P0] ✅ COMPLETE ✅ COMPLETE

**Dependencies**: [P2.2.1, P2.2.2, P2.2.3, P2.2.4, P2.2.5]

**Tasks:**

- [x] **P3.2.1**: Create skill directory ✅
  - Create `skills/analyze-code.skill/`
  - Create skill configuration
  - **Acceptance**: Valid skill structure

- [x] **P3.2.2**: ✅ Implement skill entry point
  - Create `skills/analyze-code.skill/main.py`
  - Parse arguments (project path, language)
  - Orchestrate all code analyzers:
    - File size checker
    - Docstring analyzer
    - Naming validator
    - Complexity analyzer
  - **Max 150 lines** - delegate to src/analyzers
  - **Acceptance**: Runs all analyzers on test project

- [x] **P3.2.3**: ✅ Integrate LLM for code readability assessment
  - Function: `assess_code_readability_llm(code_samples)`
  - Select 3-5 representative code files
  - Prompt: "Rate this code's readability, modularity, and clarity (1-10)"
  - **Acceptance**: Returns readability scores

- [x] **P3.2.4**: ✅ Calculate code quality score
  - Aggregate results from all analyzers
  - Apply penalties for violations
  - Weight: File size (40%), Docstrings (30%), Complexity (20%), Naming (10%)
  - **Acceptance**: Correct score calculation

- [x] **P3.2.5**: ✅ Write integration test for skill
  - Test with well-structured project (high score)
  - Test with poor-quality project (low score)
  - **Acceptance**: Accurate scoring

---

### P3.3: /check-security Skill [P0] ✅ COMPLETE

**Dependencies**: [P2.3.1, P2.3.2, P2.3.3]

**Tasks:**

- [x] **P3.3.1**: ✅ Create skill directory
  - Create `skills/check-security.skill/`
  - Create skill configuration
  - **Acceptance**: Valid skill structure

- [x] **P3.3.2**: ✅ Implement skill entry point
  - Create `skills/check-security.skill/main.py`
  - Run all security checks:
    - Secret detection
    - .gitignore validation
    - .env template check
  - **Max 150 lines**
  - **Acceptance**: Detects security issues

- [x] **P3.3.3**: ✅ Implement critical issue flagging
  - If secrets detected → overall score = FAIL
  - Display prominent warning in report
  - **Acceptance**: Correct critical issue handling

- [x] **P3.3.4**: ✅ Write integration test for skill
  - Test project with hardcoded secret
  - Test project with proper security practices
  - **Acceptance**: Correctly flags security violations

---

### P3.4: /evaluate-tests Skill [P0] ✅ COMPLETE

**Dependencies**: [P2.5.1, P2.5.2, P2.5.3]

**Tasks:**

- [x] **P3.4.1**: ✅ Create skill directory
  - Create `skills/evaluate-tests.skill/`
  - Create skill configuration
  - **Acceptance**: Valid skill structure

- [x] **P3.4.2**: ✅ Implement skill entry point
  - Create `skills/evaluate-tests.skill/main.py`
  - Detect project language (Python/JS)
  - Parse appropriate coverage report
  - Find test files
  - **Max 150 lines**
  - **Acceptance**: Correctly processes coverage data

- [x] **P3.4.3**: ✅ Validate coverage threshold
  - Check if coverage ≥70%
  - Flag low-coverage files
  - **Acceptance**: Identifies files below threshold

- [x] **P3.4.4**: ✅ Assess test quality (LLM)
  - Function: `assess_test_quality_llm(test_files)`
  - Check for edge case documentation
  - Prompt: "Do these tests cover edge cases? Rate 1-10."
  - **Acceptance**: Returns test quality assessment

- [x] **P3.4.5**: ✅ Write integration test for skill
  - Test project with high coverage (≥70%)
  - Test project with low coverage (<70%)
  - **Acceptance**: Correct pass/fail determination

---

### P3.5: /assess-git Skill [P1]

**Dependencies**: [P2.6.1, P2.6.2, P2.6.3]

**Tasks:**

- [x] **P3.5.1**: ✅ Create skill directory
  - Create `skills/assess-git.skill/`
  - Create skill configuration
  - **Acceptance**: Valid skill structure

- [x] **P3.5.2**: ✅ Implement skill entry point
  - Create `skills/assess-git.skill/main.py`
  - Check if directory is Git repo
  - Count commits (minimum 10)
  - Analyze commit message quality
  - **Max 150 lines**
  - **Acceptance**: Generates Git workflow report

- [x] **P3.5.3**: ✅ Generate commit quality recommendations
  - Identify poor commit messages
  - Provide examples of good messages
  - **Acceptance**: Actionable feedback for students

- [x] **P3.5.4**: ✅ Write integration test for skill
  - Test repository with good commit history
  - Test repository with poor commits
  - **Acceptance**: Accurate Git workflow scoring

---

### P3.6: /grade-research Skill [P1]

**Dependencies**: [P2.4.1] (document parser)

**Tasks:**

- [x] **P3.6.1**: ✅ Create skill directory
  - Create `skills/grade-research.skill/`
  - Create skill configuration
  - **Acceptance**: Valid skill structure

- [x] **P3.6.2**: ✅ Implement skill entry point (LLM-heavy)
  - Create `skills/grade-research.skill/main.py`
  - Read PLANNING.md, README.md, any research docs
  - Extract parameter exploration, analysis, visualizations
  - **Max 150 lines**
  - **Acceptance**: Can process research documentation

- [x] **P3.6.3**: ✅ Define LLM evaluation prompt
  - Assess: parameter exploration, statistical analysis, visualizations, comparative analysis
  - Prompt Claude to rate 1-10 for each dimension
  - **Acceptance**: Returns structured scores

- [x] **P3.6.4**: ✅ Parse LLM response
  - Extract scores for each criterion
  - Aggregate into overall research quality score
  - **Acceptance**: Correct score calculation

- [x] **P3.6.5**: ✅ Write integration test for skill
  - Test project with thorough research (high score)
  - Test project with minimal research (low score)
  - **Acceptance**: Accurate research quality assessment

---

### P3.7: /check-ux Skill [P1]

**Dependencies**: None (LLM-based)

**Tasks:**

- [x] **P3.7.1**: ✅ Create skill directory
  - Create `skills/check-ux.skill/`
  - Create skill configuration
  - **Acceptance**: Valid skill structure

- [x] **P3.7.2**: ✅ Implement screenshot finder
  - Function: `find_screenshots(project_path)`
  - Look for .png, .jpg files in docs/, screenshots/
  - **Acceptance**: Finds all screenshots in test project

- [x] **P3.7.3**: ✅ Implement skill entry point (LLM-based)
  - Create `skills/check-ux.skill/main.py`
  - Read README usage section
  - Find screenshots
  - Send to Claude with Nielsen's heuristics prompt
  - **Max 150 lines**
  - **Acceptance**: Generates UX evaluation

- [x] **P3.7.4**: ✅ Define Nielsen's heuristics evaluation prompt
  - List all 10 heuristics
  - Ask Claude to rate 1-10 for each based on screenshots/docs
  - **Acceptance**: Returns structured heuristic scores

- [x] **P3.7.5**: ✅ Write integration test for skill
  - Test with project that has good UX documentation
  - Test with project lacking UX docs
  - **Acceptance**: Accurate UX scoring

---

### P3.8: /generate-report Skill [P0] ✅ COMPLETE

**Dependencies**: [P2.7.1, P2.7.2, P2.7.3, P2.7.4]

**Tasks:**

- [x] **P3.8.1**: ✅ Create skill directory
  - Create `skills/generate-report.skill/`
  - Create skill configuration
  - **Acceptance**: Valid skill structure

- [x] **P3.8.2**: ✅ Implement skill entry point
  - Create `skills/generate-report.skill/main.py`
  - Accept JSON input (all skill results)
  - Aggregate scores
  - Apply scoring weights from config
  - **Max 150 lines**
  - **Acceptance**: Generates unified report

- [x] **P3.8.3**: ✅ Calculate overall score
  - Load weights from `config/grading_config.yaml`
  - Calculate: overall = Σ(category_score × weight)
  - Determine pass/fail (≥70%)
  - **Acceptance**: Correct score calculation

- [x] **P3.8.4**: ✅ Generate multi-format output
  - Call JSON reporter → grading_report.json
  - Call HTML reporter → grading_report.html
  - Call CLI formatter → terminal output
  - **Acceptance**: All three formats generated

- [x] **P3.8.5**: ✅ Write integration test for skill
  - Test with sample results from all categories
  - Verify output files created
  - Verify score calculation accuracy
  - **Acceptance**: Complete end-to-end report generation

---

### P3.9: /grade-project Meta-Skill [P0]

**Dependencies**: All P3 skills (P3.1 - P3.8)

**Tasks:**

- [x] **P3.9.1**: ✅ Create skill directory
  - Create `skills/grade-project.skill/`
  - Create skill configuration with --deep flag
  - **Acceptance**: Valid skill structure

- [x] **P3.9.2**: ✅ Implement orchestration logic
  - Create `skills/grade-project.skill/main.py`
  - Quick mode: Run P0 skills only (docs, code, security, tests)
  - Deep mode: Run all skills (add git, research, ux)
  - Use async/await for parallel execution where possible
  - **Max 150 lines** - orchestration only
  - **Acceptance**: Can invoke all sub-skills

- [x] **P3.9.3**: ✅ Implement parallel execution
  - Run independent skills in parallel:
    - validate-docs, analyze-code, check-security (parallel)
    - Then: evaluate-tests, assess-git (sequential)
  - Collect all results
  - **Acceptance**: Faster execution via parallelization

- [x] **P3.9.4**: ✅ Handle errors gracefully
  - If one skill fails, continue with others
  - Mark failed skill as "incomplete" in report
  - **Acceptance**: Robust error handling

- [x] **P3.9.5**: ✅ Write integration test for full workflow
  - Test quick mode (<5 min target)
  - Test deep mode (<15 min target)
  - Verify all skills executed
  - Verify final report generated
  - **Acceptance**: End-to-end grading works

---

### P3.10: Auto-Grader Orchestrator Agent [P0] ✅ COMPLETE

**Dependencies**: All P3 skills (P3.1 - P3.9)

**IMPORTANT**: This is a **Claude Code Agent** (not a skill). It provides an intelligent, conversational interface for grading projects.

**Tasks:**

- [x] **P3.10.1**: ✅ Create agent directory structure
  - Create `agents/grader-orchestrator/`
  - Create agent configuration file (following Claude Code agent structure)
  - Define agent capabilities and tools
  - **Acceptance**: Valid agent configuration

- [x] **P3.10.2**: ✅ Implement agent core logic
  - Create agent entry point that can be invoked via Claude Code
  - Implement conversational interface for project grading
  - Agent should understand natural language requests like:
    - "Grade this project"
    - "Run only security checks"
    - "Give me a detailed analysis of code quality"
    - "Generate a report for the project at /path/to/project"
  - **Acceptance**: Agent responds to natural language grading requests

- [x] **P3.10.3**: ✅ Implement skill orchestration
  - Agent can invoke individual skills (P3.1 - P3.9) as needed
  - Intelligent decision-making: determine which skills to run based on request
  - Parallel execution where possible (docs, code, security)
  - Sequential execution where needed (dependencies)
  - **Acceptance**: Agent successfully orchestrates multiple skills

- [x] **P3.10.4**: ✅ Implement state management
  - Track grading progress across conversation turns
  - Remember previous analyses in the same session
  - Allow incremental grading (run some checks, then more later)
  - **Acceptance**: Agent maintains context across multiple interactions

- [x] **P3.10.5**: ✅ Implement result aggregation and reporting
  - Collect results from all invoked skills
  - Generate comprehensive grading report
  - Present results conversationally
  - Offer to generate HTML/JSON reports
  - **Acceptance**: Agent produces complete grading reports

- [x] **P3.10.6**: ✅ Add intelligent recommendations
  - Agent analyzes all results and provides actionable feedback
  - Prioritizes issues by severity
  - Suggests specific improvements with code examples
  - **Acceptance**: Agent provides helpful, specific recommendations

- [x] **P3.10.7**: ✅ Implement error recovery
  - Graceful handling when skills fail
  - Inform user about partial results
  - Offer to retry failed components
  - Continue grading even if some checks fail
  - **Acceptance**: Agent handles failures gracefully

- [x] **P3.10.8**: ✅ Add configuration and customization
  - Agent can read and use `config/grading_config.yaml`
  - Allow runtime configuration adjustments via conversation
  - Support custom grading profiles (lenient, standard, strict)
  - **Acceptance**: Agent respects configuration settings

- [x] **P3.10.9**: ✅ Implement repository integration
  - Agent can work with GitHub repository: https://github.com/OmryTzabbar1/RamiAutoGrader.git
  - Clone and analyze remote repositories
  - Generate reports and optionally commit them back
  - **Acceptance**: Agent can grade remote repositories

- [x] **P3.10.10**: ✅ Write agent integration tests
  - Test full conversation flow for grading
  - Test with good, medium, and bad projects
  - Test error scenarios (missing files, failed skills)
  - Verify agent produces correct reports
  - **Acceptance**: All agent tests pass

- [x] **P3.10.11**: ✅ Document agent usage
  - Create docs/AGENT_GUIDE.md
  - Document how to invoke the agent
  - Provide example conversations
  - Document available commands and capabilities
  - **Acceptance**: Clear agent documentation

---

### P3.11: Convert Skills and Agent to Claude Code Format [P0] ✅ COMPLETE

**Dependencies**: All existing Python-based skills (check-security, analyze-code, validate-docs, evaluate-tests, assess-git, grade-research, check-ux) and orchestrator

**CRITICAL**: This task converts the existing Python-based implementation to proper Claude Code skills (Markdown SKILL.md format) and agent (agent.md format).

**Tasks:**

- [x] **P3.11.1**: Research Claude Code skill and agent format
  - Used claude-code-guide task to understand proper format
  - Skills use Markdown with YAML frontmatter + instructions
  - Agents use agent.md with orchestration workflow
  - **Acceptance**: Clear understanding of required format

- [x] **P3.11.2**: Create .claude directory structure
  - Created `.claude/skills/` directory
  - Created `.claude/agents/` directory
  - **Acceptance**: Directory structure ready for skills and agents

- [x] **P3.11.3**: ✅ Convert /check-security to Claude Code skill
  - Create `.claude/skills/check-security/SKILL.md`
  - Write Markdown instructions using Claude's built-in tools (Read, Glob, Grep, Bash)
  - Reference existing `src/analyzers/security_scanner.py` as helper script
  - Test with `/skill check-security` command
  - **Acceptance**: Skill works in Claude Code format

- [x] **P3.11.4**: ✅ Convert /analyze-code to Claude Code skill
  - Create `.claude/skills/analyze-code/SKILL.md`
  - Reference analyzers: file_size_analyzer, docstring_analyzer, naming_validator
  - **Acceptance**: Skill works in Claude Code format

- [x] **P3.11.5**: ✅ Convert /validate-docs to Claude Code skill
  - Create `.claude/skills/validate-docs/SKILL.md`
  - Reference validators: document_validator, readme_validator
  - **Acceptance**: Skill works in Claude Code format

- [x] **P3.11.6**: ✅ Convert /evaluate-tests to Claude Code skill
  - Create `.claude/skills/evaluate-tests/SKILL.md`
  - Reference analyzer: test_analyzer
  - **Acceptance**: Skill works in Claude Code format

- [x] **P3.11.7**: ✅ Convert /assess-git to Claude Code skill
  - Create `.claude/skills/assess-git/SKILL.md`
  - Reference analyzer: git_analyzer
  - **Acceptance**: Skill works in Claude Code format

- [x] **P3.11.8**: ✅ Convert /grade-research to Claude Code skill
  - Create `.claude/skills/grade-research/SKILL.md`
  - Reference analyzer: research_analyzer
  - **Acceptance**: Skill works in Claude Code format

- [x] **P3.11.9**: ✅ Convert /check-ux to Claude Code skill
  - Create `.claude/skills/check-ux/SKILL.md`
  - Reference analyzer: ux_analyzer
  - **Acceptance**: Skill works in Claude Code format

- [x] **P3.11.10**: ✅ Convert orchestrator to Claude Code agent
  - Create `.claude/agents/grade-project/agent.md`
  - Define workflow for invoking all 7 skills
  - Implement result aggregation logic
  - Use existing `src/core/skill_executor.py` and `grading_utils.py` as helpers
  - **Acceptance**: Agent works via Claude Code

- [x] **P3.11.11**: ✅ Test all converted skills
  - Test each skill individually with sample projects
  - Verify Python helper integration works
  - Ensure all skills produce correct results
  - **Acceptance**: All 7 skills working correctly

- [x] **P3.11.12**: ✅ Test agent orchestration
  - Test agent invocation
  - Verify agent calls all skills correctly
  - Test result aggregation
  - Test report generation
  - **Acceptance**: Agent successfully orchestrates all skills

- [x] **P3.11.13**: ✅ Document conversion in prompts/
  - Create `prompts/architecture/004-claude-code-conversion.md`
  - Document lessons learned from conversion
  - Document skill vs Python script architecture
  - **Acceptance**: Conversion documented

- [x] **P3.11.14**: ✅ Update documentation
  - Update README with Claude Code skill usage
  - Update installation instructions
  - Add examples of skill invocation
  - **Acceptance**: Documentation reflects Claude Code format

---

### P3.12: /grade-github-project Skill [P0] ✅ COMPLETE

**Dependencies**: [P3.11] (Converted Claude Code Agent)

**Purpose**: Fetch a project from GitHub and automatically grade it using the orchestrator agent.

**Tasks:**

- [x] **P3.11.1**: ✅ Create skill directory structure
  - Create `skills/grade-github-project.skill/`
  - Create skill configuration file
  - Define parameters: GitHub URL, branch (optional), target directory (optional)
  - **Acceptance**: Valid skill configuration

- [x] **P3.11.2**: ✅ Implement GitHub repository cloning
  - Create `src/utils/github_utils.py`
  - Function: `clone_repository(github_url, target_dir=None, branch='main')`
  - Support HTTPS and SSH URLs
  - Handle authentication if needed (use Git credential manager)
  - Clean up temporary directories after grading
  - **Max 150 lines**
  - **Acceptance**: Can clone public and private repos

- [x] **P3.11.3**: ✅ Implement URL validation
  - Function: `validate_github_url(url)`
  - Check URL format (github.com/owner/repo)
  - Verify repository exists (optional pre-check)
  - Extract owner and repo name
  - **Acceptance**: Correctly validates and parses GitHub URLs

- [x] **P3.11.4**: ✅ Implement skill entry point
  - Create `skills/grade-github-project.skill/main.py`
  - Parse arguments: GitHub URL, branch, output directory
  - Clone repository to temporary directory
  - Invoke orchestrator agent on cloned project
  - Collect grading results
  - Optionally clean up cloned repository
  - **Max 150 lines**
  - **Acceptance**: Can grade a GitHub repository end-to-end

- [x] **P3.11.5**: ✅ Add agent invocation integration
  - Skill invokes the orchestrator agent programmatically
  - Pass project path to agent
  - Capture agent's grading results
  - Format results for skill output
  - **Acceptance**: Agent successfully grades cloned project

- [x] **P3.11.6**: ✅ Implement error handling
  - Handle clone failures (repo not found, no access)
  - Handle network errors
  - Handle grading failures
  - Clean up partial clones on error
  - Provide clear error messages
  - **Acceptance**: Graceful error handling for all failure modes

- [x] **P3.11.7**: ✅ Add batch repository support
  - Function: `grade_multiple_repos(repo_urls)`
  - Accept list of GitHub URLs
  - Grade each repository sequentially or in parallel
  - Generate comparative report
  - **Acceptance**: Can grade multiple repositories

- [x] **P3.11.8**: ✅ Implement result export
  - Save grading reports in specified output directory
  - Name files by repository: `owner-repo-grading-report.json`
  - Generate summary CSV for batch grading
  - **Acceptance**: Reports properly saved and organized

- [x] **P3.11.9**: ✅ Add authentication support
  - Support GitHub personal access tokens (PAT)
  - Support SSH keys
  - Read credentials from environment or config
  - **Acceptance**: Can clone private repositories

- [x] **P3.11.10**: ✅ Write unit tests
  - Test URL validation
  - Test cloning (with mock)
  - Test error handling
  - Coverage target: ≥80%
  - **Acceptance**: All tests pass

- [x] **P3.11.11**: ✅ Write integration test
  - Test with real public GitHub repository
  - Test with test fixture repository
  - Verify complete grading workflow
  - **Acceptance**: End-to-end test passes

- [x] **P3.11.12**: ✅ Document skill usage
  - Add examples to docs/SKILLS_GUIDE.md
  - Document authentication setup
  - Provide example commands
  - **Acceptance**: Clear usage documentation

**Example Usage:**
```bash
# Grade a single repository
/grade-github-project https://github.com/OmryTzabbar1/RamiAutoGrader.git

# Grade specific branch
/grade-github-project https://github.com/username/project.git --branch develop

# Grade multiple repositories
/grade-github-project --batch repos.txt --output ./reports/

# Grade with custom config
/grade-github-project https://github.com/username/project.git --config strict
```

---

## Phase 4: Testing & Validation

### P4.1: Unit Test Coverage [P0] ✅ COMPLETE

**Tasks:**

- [x] **P4.1.1**: ✅ Achieve ≥80% coverage for all src/ modules
  - Run: `pytest tests/ --cov=src --cov-report=html`
  - Review coverage report
  - Add tests for uncovered branches
  - **Acceptance**: Coverage ≥80%

- [x] **P4.1.2**: ✅ Test edge cases
  - Empty files, missing files, corrupted files
  - Projects without Git
  - Projects in unsupported languages
  - **Acceptance**: All edge cases handled gracefully

- [x] **P4.1.3**: ✅ Test error conditions
  - Claude API timeout/failure
  - Invalid YAML configuration
  - Insufficient permissions to read files
  - **Acceptance**: Graceful degradation for all errors

---

### P4.2: Integration Testing [P0] ✅ COMPLETE

**Tasks:**

- [x] **P4.2.1**: ✅ Create test project fixtures
  - Good project (high score): All docs, clean code, good tests
  - Bad project (low score): Missing docs, secrets, oversized files
  - Medium project (mid score): Some issues
  - **Acceptance**: 3 test projects ready

- [x] **P4.2.2**: ✅ Test full grading workflow on fixtures
  - Run `/grade-project` on each fixture
  - Verify scores match expectations:
    - Good project: ≥85%
    - Medium project: 60-75%
    - Bad project: <50%
  - **Acceptance**: Correct scoring for all fixtures

- [x] **P4.2.3**: ✅ Test batch processing
  - Run grader on all 3 fixtures
  - Verify reports generated for each
  - **Acceptance**: Batch mode works

---

### P4.3: Accuracy Benchmark [P1]

**Tasks:**

- [ ] **P4.3.1**: Collect 20 real student projects
  - Diverse quality levels
  - Different project types (web apps, data analysis, etc.)
  - **Acceptance**: 20 projects assembled

- [ ] **P4.3.2**: Manual grading by 3 expert graders
  - Each grader scores all 20 projects independently
  - Use same criteria as auto-grader
  - Calculate inter-rater agreement
  - **Acceptance**: Human baseline established

- [ ] **P4.3.3**: Run auto-grader on benchmark set
  - Grade all 20 projects
  - Save scores
  - **Acceptance**: Auto-grader results collected

- [ ] **P4.3.4**: Calculate accuracy metrics
  - Compare auto vs. human scores
  - Calculate: mean absolute error, correlation
  - Target: ≥90% agreement (±5% variance)
  - **Acceptance**: Accuracy benchmark met

- [ ] **P4.3.5**: Analyze discrepancies
  - Identify cases where auto-grader diverges from humans
  - Categorize errors (false positives, false negatives)
  - Tune weights/thresholds if needed
  - **Acceptance**: Improvements identified and implemented

---

### P4.4: User Acceptance Testing [P1]

**Tasks:**

- [ ] **P4.4.1**: Recruit 10 beta testers
  - 7 M.Sc. students
  - 2 instructors
  - 1 teaching assistant
  - **Acceptance**: Beta testers recruited

- [ ] **P4.4.2**: Conduct beta testing
  - Provide installation instructions
  - Have users run auto-grader on their projects
  - Collect feedback via survey
  - **Acceptance**: All beta tests completed

- [ ] **P4.4.3**: Analyze feedback
  - Identify common issues/confusion
  - Measure satisfaction (1-5 scale)
  - Target: ≥4.5 average rating
  - **Acceptance**: Feedback analyzed

- [ ] **P4.4.4**: Implement improvements based on feedback
  - Fix reported bugs
  - Improve error messages
  - Update documentation
  - **Acceptance**: Key issues resolved

---

## Phase 5: Documentation & Deployment

### P5.1: User Documentation [P0]

**Tasks:**

- [ ] **P5.1.1**: Write comprehensive README.md
  - Installation instructions
  - Quick start guide
  - Usage examples for each skill
  - Troubleshooting section
  - **Max 250 lines** (can split into multiple docs)
  - **Acceptance**: Clear, complete README

- [ ] **P5.1.2**: Create skill usage guide
  - Document each skill's parameters
  - Provide examples with screenshots
  - **Acceptance**: docs/SKILLS_GUIDE.md complete

- [ ] **P5.1.3**: Write configuration guide
  - Explain all config options
  - Provide examples for customization
  - **Acceptance**: docs/CONFIGURATION.md complete

- [ ] **P5.1.4**: Create video tutorial (optional)
  - 5-minute walkthrough
  - Installation → running grader → reviewing report
  - **Acceptance**: Video published (YouTube/internal)

---

### P5.2: Developer Documentation [P1]

**Tasks:**

- [ ] **P5.2.1**: Document architecture
  - Convert PLANNING.md C4 diagrams to Mermaid/PlantUML
  - Explain component interactions
  - **Acceptance**: docs/ARCHITECTURE.md with diagrams

- [ ] **P5.2.2**: Write contribution guide
  - How to add new skills
  - How to add new analyzers
  - Code style guidelines
  - **Acceptance**: CONTRIBUTING.md complete

- [ ] **P5.2.3**: Generate API documentation
  - Use docstrings to auto-generate docs (Sphinx/MkDocs)
  - Host on GitHub Pages
  - **Acceptance**: API docs published

---

### P5.3: Deployment [P0]

**Tasks:**

- [ ] **P5.3.1**: Package skills for distribution
  - Create skill bundle
  - Test installation: `claude-code skills install academic-auto-grader`
  - **Acceptance**: Skills installable via CLI

- [ ] **P5.3.2**: Publish to skill repository
  - Submit to Claude Code skill marketplace (if available)
  - Provide installation instructions
  - **Acceptance**: Publicly accessible

- [ ] **P5.3.3**: Create GitHub releases
  - Tag version 1.0.0
  - Write release notes
  - Attach installation assets
  - **Acceptance**: v1.0.0 released

---

### P5.4: Prompt Documentation [P0]

**Tasks:**

- [ ] **P5.4.1**: Organize prompts/ directory
  - Create subdirectories: architecture/, code-generation/, testing/, documentation/
  - **Acceptance**: Clean directory structure

- [ ] **P5.4.2**: Document all Claude prompts used
  - Each prompt in separate .md file
  - Include: context, prompt text, response summary
  - Number sequentially: 001-file-size-analyzer.md
  - **Acceptance**: All prompts documented

- [ ] **P5.4.3**: Create prompts/README.md
  - Explain prompt organization
  - Categorize prompts by purpose
  - **Acceptance**: Clear prompt catalog

---

## Phase 6: Continuous Improvement (Post-Launch)

### P6.1: Monitoring & Analytics [P2]

**Tasks:**

- [ ] **P6.1.1**: Implement usage telemetry (optional, opt-in)
  - Track: skill invocations, execution times, errors
  - Anonymize data
  - **Acceptance**: Telemetry system operational

- [ ] **P6.1.2**: Monitor accuracy over time
  - Collect ongoing human vs. auto-grader comparisons
  - Alert if accuracy drops below 85%
  - **Acceptance**: Monitoring dashboard

---

### P6.2: Feature Enhancements [P2]

**Tasks:**

- [ ] **P6.2.1**: Implement /grade-batch skill
  - Grade multiple projects in parallel
  - Generate comparative CSV report
  - **Acceptance**: Batch grading works

- [ ] **P6.2.2**: Add support for more languages
  - Java, C++, Go, etc.
  - Use Tree-sitter for universal parsing
  - **Acceptance**: Multi-language support

- [ ] **P6.2.3**: Implement custom rubric support
  - Allow users to define custom grading criteria
  - Override default weights
  - **Acceptance**: Customizable rubrics

- [ ] **P6.2.4**: Add plagiarism detection integration
  - Optional integration with external tools
  - **Acceptance**: Plagiarism check available

---

## Summary Statistics

**Total Tasks**: 222+

**Breakdown by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Core Utilities): 35 tasks
- Phase 3 (Skills & Agent): 68 tasks (57 skill tasks + 11 agent tasks)
  - Individual grading skills: 45 tasks
  - Orchestrator agent: 11 tasks
  - GitHub grading skill: 12 tasks
- Phase 4 (Testing): 15 tasks
- Phase 5 (Documentation): 15 tasks
- Phase 6 (Post-Launch): 10 tasks

**Breakdown by Priority**:
- **[P0] Must-Have**: ~103 tasks (Phases 1-3 core skills + orchestrator agent + GitHub skill)
- **[P1] Should-Have**: ~30 tasks (Advanced skills, benchmarking)
- **[P2] Nice-to-Have**: ~15 tasks (Batch processing, monitoring)

**Estimated Completion Checkpoints**:
- **Checkpoint 1**: All P0 tasks complete → MVP ready
- **Checkpoint 2**: All P1 tasks complete → Production-ready
- **Checkpoint 3**: All P2 tasks complete → Full feature set

---

## Task Tracking

**How to use this document:**

1. **Start with Phase 1** (Setup) - Complete all P1.x tasks sequentially
2. **Progress through Phase 2** (Core Utilities) - These are dependencies for skills
3. **Implement skills in Phase 3** - Can parallelize skill development
4. **Test thoroughly in Phase 4** - Do not skip testing!
5. **Document in Phase 5** - Essential for adoption
6. **Iterate in Phase 6** - Based on user feedback

**Mark tasks complete by changing**:
```
- [ ] Task description
```
to:
```
- [x] Task description
```

**Track your progress with Git commits**:
```
feat(analyzers): Implement file size analyzer [P2.2.1]
test(analyzers): Add unit tests for file size analyzer [P2.2.1]
docs: Document file size analyzer API [P2.2.1]
```

**Ensure each task**:
- Has clear acceptance criteria
- Results in a Git commit
- Is tested (if code)
- Is documented in prompts/ directory (if used Claude)
- Adheres to 150-line file limit

---

**Document Version**: 1.0
**Last Updated**: 2025-01-25
**Status**: Ready for Execution
