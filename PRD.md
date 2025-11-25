# Product Requirements Document (PRD)
# Academic Software Auto-Grader System

## 1. Project Overview & Background

### 1.1 Project Information
- **Project Name**: Academic Software Auto-Grader
- **Version**: 1.0
- **Date**: 2025-01-25
- **Author**: Rami (Computer Science M.Sc. Program)

### 1.2 Problem Statement

M.Sc. Computer Science students must submit software projects that meet rigorous academic excellence standards as defined in Dr. Segal Yoram's comprehensive guidelines. Manual evaluation of these submissions is:
- **Time-intensive**: Reviewing 12+ quality dimensions across multiple documents
- **Inconsistent**: Human reviewers may miss criteria or apply standards differently
- **Non-scalable**: Cannot efficiently handle multiple submissions
- **Delayed feedback**: Students wait days/weeks for evaluation results

### 1.3 Project Purpose

The Auto-Grader system provides **automated, comprehensive evaluation** of M.Sc. software projects against ISO/IEC 25010 quality standards and academic excellence criteria. It:
- Validates presence and quality of required documentation (PRD, Architecture, README, etc.)
- Analyzes code structure, quality, and adherence to best practices
- Evaluates testing coverage and quality
- Assesses research methodology and analysis depth
- Generates detailed feedback reports with specific improvement recommendations

### 1.4 Market Analysis

**Existing Solutions:**
- Generic code linters (pylint, eslint) - Only check syntax/style, miss documentation
- GitHub Actions CI/CD - Requires manual configuration, no academic standards
- Turnitin - Plagiarism only, no quality assessment

**Our Differentiation:**
- **Academic-specific**: Built for ISO/IEC 25010 and M.Sc. excellence standards
- **Holistic evaluation**: Documentation + Code + Research + UX
- **Claude Code integration**: Leverages LLM capabilities for intelligent analysis
- **Actionable feedback**: Not just pass/fail, but specific improvement guidance

### 1.5 Target Audience & Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| M.Sc. Students | Primary Users | Submit projects, receive fast feedback, improve work quality |
| Course Instructors | Evaluators | Reduce grading time, ensure consistent standards |
| Academic Institutions | Administrators | Maintain program quality, accreditation compliance |
| Teaching Assistants | Support Staff | Pre-screen submissions before instructor review |

---

## 2. Objectives & Success Metrics

### 2.1 Project Goals
- [ ] **G1**: Automate 80%+ of the manual grading checklist from the guidelines
- [ ] **G2**: Reduce evaluation time from 2-3 hours to <15 minutes per submission
- [ ] **G3**: Achieve 90%+ accuracy compared to expert human evaluation
- [ ] **G4**: Provide actionable feedback with specific file/line references
- [ ] **G5**: Support iterative improvement workflow (students can re-run grader)

### 2.2 Key Performance Indicators (KPIs)

| KPI | Target | Measurement Method |
|-----|--------|-------------------|
| Grading Accuracy | 90% agreement with human expert | Compare auto-grader scores with instructor scores on 50 sample projects |
| Processing Time | <15 min per project | Measure end-to-end execution time |
| Coverage | 80% of checklist items | Map each skill to guideline requirements |
| User Satisfaction | 4.5/5 rating | Post-use survey from students and instructors |
| False Positive Rate | <10% | Track incorrect warnings/errors flagged |

### 2.3 Acceptance Criteria
- [ ] **AC1**: System validates all mandatory document types (PRD, CLAUDE.md, PLANNING.md, TASKS.md, README)
- [ ] **AC2**: Code analysis enforces 150-line file limit
- [ ] **AC3**: Detects hardcoded API keys and secrets
- [ ] **AC4**: Validates test coverage ≥70%
- [ ] **AC5**: Checks Git commit history quality (10+ meaningful commits)
- [ ] **AC6**: Generates structured JSON/HTML report with scores and recommendations
- [ ] **AC7**: Can be invoked via CLI: `claude-code /grade-project`

---

## 3. Functional Requirements

### 3.1 Feature List (Prioritized)

| Priority | Feature | Description | User Story |
|----------|---------|-------------|------------|
| P0 (Must) | Document Validator | Checks presence and completeness of PRD, Architecture docs, README, TASKS.md | As a student, I want to know if I'm missing required documents before submission |
| P0 (Must) | Code Structure Analyzer | Validates file size limits, naming conventions, modular structure | As a student, I want to ensure my code meets organizational standards |
| P0 (Must) | Code Quality Checker | Analyzes docstrings, comments, naming, code smells | As an instructor, I want to verify code adheres to quality standards |
| P0 (Must) | Security Scanner | Detects hardcoded secrets, API keys, missing .gitignore | As an instructor, I need to ensure students don't expose sensitive data |
| P0 (Must) | Test Coverage Analyzer | Measures unit test coverage, validates edge case documentation | As a student, I want to know if my testing is sufficient |
| P1 (Should) | Git History Evaluator | Analyzes commit frequency, message quality, branching strategy | As an instructor, I want to see evidence of proper development workflow |
| P1 (Should) | Research Quality Assessor | Evaluates parameter exploration, statistical analysis, visualizations | As an instructor, I need to verify research methodology rigor |
| P1 (Should) | UX/UI Evaluator | Checks Nielsen's heuristics compliance, screenshots, user documentation | As a student, I want feedback on my interface design |
| P2 (Nice) | Prompt Engineering Log Validator | Ensures prompts/ directory is populated with categorized prompts | As an instructor, I want to see how students used AI tools |
| P2 (Nice) | Cost Analysis Checker | Validates API token usage tables are present and documented | As an instructor, I need to verify students tracked their API costs |

### 3.2 Use Cases

#### Use Case 1: Initial Project Submission Validation
- **Actor**: M.Sc. Student
- **Preconditions**: Student has cloned project repository, has Claude Code installed
- **Main Flow**:
  1. Student navigates to project root directory
  2. Student runs `/grade-project` in Claude Code CLI
  3. System scans directory structure
  4. System validates presence of required documents
  5. System generates preliminary report highlighting missing items
  6. Student reviews report and adds missing components
- **Postconditions**: Student knows all required files are present
- **Alternative Flows**:
  - If `.git` not found, warn that Git history cannot be evaluated
  - If Python/JS project not detected, ask user to specify language

#### Use Case 2: Deep Code Quality Analysis
- **Actor**: Student preparing final submission
- **Preconditions**: All documents present, code written
- **Main Flow**:
  1. Student runs `/grade-project --deep` for comprehensive analysis
  2. System checks file sizes (150-line limit)
  3. System analyzes docstring coverage
  4. System runs code complexity metrics
  5. System scans for hardcoded secrets
  6. System validates `.env.example` exists
  7. System generates detailed report with file:line references
- **Postconditions**: Student receives actionable feedback to improve code quality
- **Alternative Flows**: If secrets detected, immediately flag as critical issue

#### Use Case 3: Instructor Batch Grading
- **Actor**: Course Instructor
- **Preconditions**: Multiple student submissions in separate directories
- **Main Flow**:
  1. Instructor runs `/grade-batch ./submissions/*`
  2. System processes each project directory
  3. System generates comparative summary (CSV/Excel)
  4. System flags outliers (exceptionally high/low scores)
  5. Instructor reviews summary and deep-dives into flagged submissions
- **Postconditions**: Instructor has preliminary scores for all submissions
- **Alternative Flows**: If project fails to grade, log error and continue

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **Response Time**:
  - Quick scan (<30 seconds) for document presence check
  - Deep analysis (<15 minutes) for full grading including LLM calls
- **Throughput**: Support batch processing of 10 projects in parallel
- **Resource Utilization**:
  - Memory: <2GB per project analysis
  - Disk: <100MB for grader installation
  - API Tokens: <100k tokens per project (estimated $0.15 with Claude Sonnet)

### 4.2 Security Requirements
- **Authentication**: Uses user's existing Claude Code credentials
- **Authorization**: Read-only access to project files
- **Data Protection**:
  - No submission data sent to external servers (except Claude API per user consent)
  - Grading reports stored locally only
  - Option to anonymize reports (remove student names)

### 4.3 Scalability Requirements
- **Expected Load**:
  - Single user: 1-5 projects per session
  - Batch mode: Up to 50 projects
- **Scaling Strategy**:
  - Horizontal: Parallel processing via async/multiprocessing
  - Vertical: Optimize LLM prompts to reduce token usage

### 4.4 Availability & Reliability
- **Uptime Target**: 99% (dependent on Claude API availability)
- **Recovery Time Objective**: <5 minutes (restart grading from last checkpoint)
- **Fault Tolerance**: Graceful degradation if Claude API fails (static analysis continues)

### 4.5 Usability Requirements
- **Learnability**: First-time users can run basic grading within 5 minutes
- **Efficiency**: Power users can customize grading criteria via config file
- **Error Prevention**: Clear error messages if project structure is non-standard
- **Documentation**: Comprehensive README with examples

---

## 5. Assumptions, Dependencies & Constraints

### 5.1 Assumptions
- Students submit projects as Git repositories
- Projects are in Python, JavaScript/TypeScript, or other mainstream languages
- Students have Claude Code CLI installed and configured
- Submission directories follow a recognizable structure (src/, tests/, docs/, etc.)

### 5.2 External Dependencies

| Dependency | Type | Risk Level |
|------------|------|------------|
| Claude API | External | Medium - API downtime affects LLM-based grading |
| Git | External Tool | Low - Universally available |
| Python AST/Tree-sitter | Library | Low - Stable parsing libraries |
| pytest/coverage.py | Testing Tools | Low - Industry standard |

### 5.3 Technical Constraints
- Must run within Claude Code CLI environment
- Cannot execute student code (security risk) - static analysis only
- LLM context window limits (200k tokens for Sonnet 4.5)

### 5.4 Organizational Constraints
- Must complete project within academic semester timeline
- Grading criteria must align with provided PDF guidelines
- Budget: Minimize API costs (<$10 per 50 projects)

### 5.5 Out-of-Scope Items
- Plagiarism detection (use Turnitin separately)
- Automated code execution/testing (students must run tests themselves)
- Integration with university LMS (Moodle, Canvas) - manual export/import
- GUI interface (CLI only in v1.0)

---

## 6. Technical Architecture Preview

### 6.1 System Components
```
auto-grader/
├── skills/                  # Claude Code CLI skills
│   ├── validate-docs/       # Check PRD, README, etc.
│   ├── analyze-code/        # File size, structure, quality
│   ├── check-security/      # Secrets detection
│   ├── evaluate-tests/      # Coverage analysis
│   ├── assess-git/          # Commit history
│   ├── grade-research/      # Parameter exploration, viz
│   ├── check-ux/            # UI/UX heuristics
│   └── generate-report/     # Final scoring and feedback
├── src/                     # Shared utilities
│   ├── parsers/             # Language-specific AST parsers
│   ├── analyzers/           # Metric calculation engines
│   └── reporters/           # JSON/HTML report generators
├── config/                  # Grading rubrics (YAML)
├── tests/                   # Unit tests for skills
├── docs/                    # Architecture diagrams
└── README.md
```

### 6.2 Skill Invocation Flow
1. User runs `/grade-project` in Claude Code
2. Main orchestrator skill loads grading config
3. Parallel execution of independent skills (docs, code, security)
4. Sequential execution of dependent skills (git requires code scan first)
5. Aggregation of results into unified report
6. Display summary in CLI + save detailed HTML report

---

## 7. Success Criteria & Validation

### 7.1 Validation Methodology
- **Unit Testing**: Each skill has ≥80% test coverage
- **Integration Testing**: Full grading workflow tested on 20 diverse projects
- **Accuracy Benchmark**: Compare auto-grader scores vs. 3 expert human graders on 10 projects
  - Target: ≥90% agreement (±5% score variance)
- **User Acceptance Testing**: 10 students + 2 instructors test beta version, provide feedback
  - Target: ≥4.5/5 satisfaction rating

### 7.2 Go-Live Criteria
- [ ] All P0 features implemented and tested
- [ ] Accuracy benchmark met (90%+ agreement)
- [ ] Performance target met (<15 min per project)
- [ ] Security review passed (no exposure of student data)
- [ ] Documentation complete (README, skills API docs)
- [ ] Deployed as Claude Code skill package

---

## 8. Appendices

### 8.1 Glossary

| Term | Definition |
|------|------------|
| Claude Code CLI | Anthropic's command-line interface for interacting with Claude AI |
| Skill | Modular, reusable command in Claude Code (e.g., `/format-code`) |
| ISO/IEC 25010 | International standard for software product quality |
| PRD | Product Requirements Document |
| ADR | Architecture Decision Record |
| Edge Case | Boundary condition or unusual scenario in code testing |

### 8.2 References
1. Dr. Segal Yoram - "Guidelines for Submitting Excellent Software for M.Sc. in Computer Science" (2025)
2. ISO/IEC 25010:2011 - Systems and software Quality Requirements and Evaluation
3. Nielsen's 10 Usability Heuristics
4. MIT Software Quality Assurance Plan
5. Google Engineering Practices Documentation
6. Claude Code Skills Documentation

---

**Document Version**: 1.0
**Last Updated**: 2025-01-25
**Status**: Final for Implementation
