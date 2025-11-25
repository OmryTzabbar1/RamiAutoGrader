# Technical Planning & Architecture Document
# Academic Software Auto-Grader System

**Project**: Academic Software Auto-Grader
**Version**: 1.0
**Date**: 2025-01-25
**Author**: Rami (M.Sc. Computer Science Program)

---

## Table of Contents
1. [System Architecture Overview](#1-system-architecture-overview)
2. [Architecture Decision Records (ADRs)](#2-architecture-decision-records-adrs)
3. [Component Design](#3-component-design)
4. [Data Models](#4-data-models)
5. [Skill Specifications](#5-skill-specifications)
6. [Integration Points](#6-integration-points)
7. [Error Handling Strategy](#7-error-handling-strategy)
8. [Testing Strategy](#8-testing-strategy)
9. [Deployment Plan](#9-deployment-plan)

---

## 1. System Architecture Overview

### 1.1 C4 Model - Context Diagram (Level 1)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                     Academic Environment                        │
│                                                                 │
│  ┌──────────────┐              ┌──────────────────────┐        │
│  │              │              │                      │        │
│  │  M.Sc.       │─────────────▶│   Auto-Grader        │        │
│  │  Student     │  Submits     │   System             │        │
│  │              │  Project     │  (Claude Code CLI)   │        │
│  └──────────────┘              └──────────┬───────────┘        │
│                                           │                     │
│  ┌──────────────┐                         │                     │
│  │              │◀────────────────────────┘                     │
│  │  Instructor  │   Receives Grading                            │
│  │              │   Reports                                     │
│  └──────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    │ API Calls
                                    ▼
                        ┌────────────────────┐
                        │                    │
                        │  Claude API        │
                        │  (Anthropic)       │
                        │                    │
                        └────────────────────┘
```

**External Systems:**
- **Claude API**: LLM service for intelligent code/document analysis
- **Git**: Version control system (student projects must be Git repos)
- **Student Project Repository**: Local directory being graded

---

### 1.2 C4 Model - Container Diagram (Level 2)

```
┌────────────────────────────────────────────────────────────────────┐
│                    Auto-Grader System                              │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                                                             │  │
│  │          Claude Code Orchestrator Agent                     │  │
│  │          (Intelligent Grading Coordinator)                  │  │
│  │                                                             │  │
│  │  - Natural language interface                               │  │
│  │  - Skill orchestration                                      │  │
│  │  - Result aggregation                                       │  │
│  │  - Conversational reporting                                 │  │
│  │                                                             │  │
│  └────────────────────────┬────────────────────────────────────┘  │
│                           │ invokes                               │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                                                             │  │
│  │              Claude Code CLI Skills Layer                   │  │
│  │                                                             │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │ /validate- │  │ /analyze-  │  │ /check-    │  ...       │  │
│  │  │ docs       │  │ code       │  │ security   │            │  │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘            │  │
│  │        │               │               │                    │  │
│  └────────┼───────────────┼───────────────┼────────────────────┘  │
│           │               │               │                       │
│           ▼               ▼               ▼                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                                                             │  │
│  │                  Core Analysis Engine                       │  │
│  │                                                             │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │ Parsers    │  │ Analyzers  │  │ Validators │            │  │
│  │  │ (AST, MD)  │  │ (Metrics)  │  │ (Rules)    │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  │                                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                                                             │  │
│  │              Report Generation Layer                        │  │
│  │                                                             │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │  │
│  │  │ JSON       │  │ HTML       │  │ CLI        │            │  │
│  │  │ Exporter   │  │ Renderer   │  │ Formatter  │            │  │
│  │  └────────────┘  └────────────┘  └────────────┘            │  │
│  │                                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

### 1.3 C4 Model - Component Diagram (Level 3)

**Focus: Core Analysis Engine**

```
┌──────────────────────────────────────────────────────────────────┐
│                    Core Analysis Engine                          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   Parsers Package                        │    │
│  │                                                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │    │
│  │  │ PythonParser │  │ JSParser     │  │ MarkdownParser│  │    │
│  │  │ (uses AST)   │  │ (Tree-sitter)│  │ (Mistune)    │   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Analyzers Package                       │    │
│  │                                                          │    │
│  │  ┌──────────────────┐  ┌──────────────────┐             │    │
│  │  │ FileSizeAnalyzer │  │ DocstringAnalyzer│             │    │
│  │  └──────────────────┘  └──────────────────┘             │    │
│  │  ┌──────────────────┐  ┌──────────────────┐             │    │
│  │  │ComplexityAnalyzer│  │ CoverageAnalyzer │             │    │
│  │  └──────────────────┘  └──────────────────┘             │    │
│  │  ┌──────────────────┐  ┌──────────────────┐             │    │
│  │  │ SecurityScanner  │  │ GitHistoryAnalyz.│             │    │
│  │  └──────────────────┘  └──────────────────┘             │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Validators Package                      │    │
│  │                                                          │    │
│  │  ┌──────────────────┐  ┌──────────────────┐             │    │
│  │  │ DocumentValidator│  │ StructureValidator│            │    │
│  │  └──────────────────┘  └──────────────────┘             │    │
│  │  ┌──────────────────┐  ┌──────────────────┐             │    │
│  │  │ NamingValidator  │  │ TestValidator    │             │    │
│  │  └──────────────────┘  └──────────────────┘             │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Architecture Decision Records (ADRs)

### ADR-001: Use Claude Code Skills Instead of Autonomous Agents

**Status**: Accepted
**Date**: 2025-01-25
**Decision Maker**: Rami

**Context:**
We need to decide between two implementation approaches:
1. **Claude Code Skills**: Modular commands (e.g., `/analyze-code`, `/check-security`)
2. **Autonomous Agents**: Long-running processes that handle entire grading workflow

**Decision:**
Implement as **Claude Code Skills** collection.

**Rationale:**
| Criteria | Skills | Agents |
|----------|--------|--------|
| **Modularity** | ✅ Each skill independent | ❌ Monolithic agent |
| **Reusability** | ✅ Use skills in other contexts | ❌ Grading-specific only |
| **Composability** | ✅ Run `/analyze-code` alone or as part of `/grade-project` | ❌ All-or-nothing execution |
| **Testing** | ✅ Unit test each skill | ❌ Complex integration tests |
| **User Control** | ✅ Students can run specific checks | ❌ Must grade everything |
| **Maintenance** | ✅ Fix one skill without affecting others | ❌ Changes ripple through agent |

**Consequences:**
- **Positive**: Easier to develop incrementally, better separation of concerns
- **Negative**: Need orchestration skill to coordinate multi-skill workflows
- **Mitigation**: Create `/grade-project` meta-skill that invokes others in sequence

---

### ADR-002: Add Orchestrator Agent for Intelligent Workflow Coordination

**Status**: Accepted
**Date**: 2025-01-26
**Decision Maker**: Rami

**Context:**
While ADR-001 established that individual grading components should be skills (for modularity), we also need a high-level coordinator that can:
1. Understand natural language grading requests
2. Intelligently decide which skills to invoke
3. Maintain conversational context across multiple interactions
4. Provide comprehensive, actionable feedback

**Decision:**
Implement a **Claude Code Agent** (orchestrator) that sits above the skills layer.

**Architecture:**
```
User Request → Orchestrator Agent → Individual Skills → Results → Agent → User
```

**Rationale:**

| Aspect | Skills Alone | Skills + Agent |
|--------|--------------|----------------|
| **Flexibility** | Manual skill invocation | Natural language requests ✅ |
| **Intelligence** | No context between runs | Maintains conversation ✅ |
| **User Experience** | Technical CLI commands | Conversational interface ✅ |
| **Orchestration** | Manual coordination | Automatic skill selection ✅ |
| **Reporting** | Static reports | Interactive feedback ✅ |

**Key Capabilities:**
- **Natural Language**: "Grade this project" → agent decides which skills to run
- **Contextual**: "Now check only the security" → agent remembers previous work
- **Adaptive**: Agent can run partial checks, retry failures, provide recommendations
- **Repository-aware**: Can work with GitHub repo: https://github.com/OmryTzabbar1/RamiAutoGrader.git

**Consequences:**
- **Positive**: Better UX, more intelligent grading, conversational feedback
- **Positive**: Skills remain modular (can still be used independently)
- **Negative**: Additional complexity (agent + skills architecture)
- **Mitigation**: Agent delegates all actual grading to skills, staying thin and focused on orchestration

**Implementation Note:**
- Skills: Individual grading components (validate-docs, analyze-code, etc.)
- Agent: Intelligent coordinator that invokes skills and manages workflow
- Both follow 150-line limit and full documentation requirements

---

### ADR-003: Use Python AST for Static Code Analysis

**Status**: Accepted
**Date**: 2025-01-25

**Context:**
Need to analyze Python code for:
- File size (line count)
- Docstring presence
- Function/class complexity
- Naming conventions

**Alternatives Considered:**
1. **Python AST** (Abstract Syntax Tree) - Built-in `ast` module
2. **Tree-sitter** - Universal parser
3. **Regex parsing** - Pattern matching

**Decision:**
Use **Python `ast` module** for Python code analysis.

**Rationale:**
```python
# Example: Detecting missing docstrings
import ast

def check_docstrings(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())

    issues = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                issues.append(f"Missing docstring: {node.name} at line {node.lineno}")

    return issues
```

**Advantages**:
- ✅ Built-in (no external dependencies)
- ✅ Accurate (understands Python syntax)
- ✅ Fast (no LLM calls needed)

**Disadvantages**:
- ❌ Python-only (need different parser for JS/TS)
- **Mitigation**: Use Tree-sitter for multi-language support in future

---

### ADR-004: Store Grading Configuration in YAML

**Status**: Accepted
**Date**: 2025-01-25

**Context:**
Grading criteria (scoring weights, thresholds) should be configurable.

**Decision:**
Use **YAML configuration file** at `config/grading_config.yaml`.

**Example Configuration:**
```yaml
# config/grading_config.yaml
scoring_weights:
  documentation: 0.25      # PRD, README, Architecture
  code_quality: 0.30       # Structure, naming, docstrings
  testing: 0.15            # Coverage, edge cases
  security: 0.10           # No secrets, .gitignore
  git_workflow: 0.10       # Commit history
  research_quality: 0.10   # Parameter exploration, viz

thresholds:
  file_size_limit: 150            # Lines per file (STRICT)
  test_coverage_min: 0.70         # 70% minimum
  min_commits: 10                 # Meaningful commits
  max_function_complexity: 10     # Cyclomatic complexity
  min_docstring_coverage: 0.90    # 90% of functions

penalties:
  hardcoded_secret: -50           # Critical security issue
  missing_required_doc: -10       # Per document
  oversized_file: -5              # Per 10 lines over limit
```

**Rationale:**
- Instructors can adjust weights without code changes
- Easy to version control
- Human-readable format

---

### ADR-005: No Code Execution (Static Analysis Only)

**Status**: Accepted
**Date**: 2025-01-25

**Context:**
Should the auto-grader execute student code to validate functionality?

**Decision:**
**NO** - Static analysis only. Do not execute submitted code.

**Security Risks of Code Execution:**
```python
# Malicious student code example
import os
os.system("rm -rf /")  # Deletes entire filesystem

# Or resource exhaustion
while True:
    fork()  # Fork bomb
```

**Trade-offs:**
| Approach | Pros | Cons |
|----------|------|------|
| **Static Analysis** | ✅ Safe, fast, no dependencies | ❌ Can't verify functionality |
| **Sandboxed Execution** | ✅ Can run tests | ❌ Complex, resource-intensive, security risk |

**Chosen Approach:**
- ✅ Analyze code structure, documentation, tests
- ✅ Check if test files exist and are well-structured
- ❌ Do NOT run student code or tests
- **Mitigation**: Require students to provide test results/screenshots

---

### ADR-006: Hybrid LLM + Static Analysis Approach

**Status**: Accepted
**Date**: 2025-01-25

**Context:**
Some checks are objective (file size, test coverage), others are subjective (code readability, documentation quality).

**Decision:**
Use **hybrid approach**:
- **Static Analysis**: Objective, deterministic checks
- **LLM (Claude API)**: Subjective quality assessment

**Task Distribution:**

| Task | Method | Rationale |
|------|--------|-----------|
| File size check | Static | Simple line count |
| Test coverage | Static | Parse coverage.py output |
| Hardcoded secrets | Static | Regex patterns |
| Docstring presence | Static | AST parsing |
| **Code readability** | **LLM** | Subjective judgment |
| **Documentation quality** | **LLM** | Completeness, clarity |
| **Research methodology** | **LLM** | Analysis depth |
| **UX heuristics** | **LLM** | Nielsen's principles |

**Cost Optimization:**
```
Scenario 1 (All LLM):
- PRD analysis: 5k tokens
- Code files (20 files × 3k): 60k tokens
- Tests: 10k tokens
- Git log: 2k tokens
= 77k tokens input + 5k output = ~$0.30 per project

Scenario 2 (All Static):
- 0 tokens
= $0 per project
- But misses subjective quality assessment

Scenario 3 (Hybrid - CHOSEN):
- Documentation quality: 10k tokens
- Code readability (sample files): 15k tokens
- Research assessment: 5k tokens
= 30k tokens input + 3k output = ~$0.10 per project
```

**Target**: <$10 for 50 projects = **$0.20 per project budget**

---

### ADR-007: Generate Reports in JSON + HTML Formats

**Status**: Accepted
**Date**: 2025-01-25

**Context:**
Grading reports need to be:
- Machine-readable (for batch processing)
- Human-readable (for students/instructors)

**Decision:**
Generate **both formats**:

**1. JSON (Machine-readable)**
```json
{
  "project_path": "/path/to/student/project",
  "timestamp": "2025-01-25T14:30:00Z",
  "overall_score": 87.5,
  "breakdown": {
    "documentation": {
      "score": 22.5,
      "max_score": 25,
      "details": {
        "prd_present": true,
        "readme_present": true,
        "architecture_docs": true,
        "prd_quality_score": 0.90
      }
    },
    "code_quality": {
      "score": 25.5,
      "max_score": 30,
      "violations": [
        {
          "type": "oversized_file",
          "file": "src/main.py",
          "line_count": 180,
          "limit": 150,
          "penalty": -2.5
        }
      ]
    }
  }
}
```

**2. HTML (Human-readable)**
- Styled with CSS for readability
- Color-coded sections (red=critical, yellow=warning, green=pass)
- Clickable links to file:line references

**Rationale:**
- JSON for `/grade-batch` processing (CSV export, aggregation)
- HTML for student feedback (open in browser)

---

## 3. Component Design

### 3.1 Document Validator Component

**Purpose**: Verify presence and quality of required documentation

**Input**: Project directory path
**Output**: DocumentValidationResult object

**Required Documents Checklist:**
```python
REQUIRED_DOCS = {
    "PRD.md": {
        "sections": ["Project Overview", "Objectives", "Functional Requirements"],
        "min_words": 1000
    },
    "CLAUDE.md": {
        "sections": ["AI Tool Usage", "Prompt Documentation"],
        "min_words": 500
    },
    "PLANNING.md": {
        "sections": ["Architecture", "Technical Decisions"],
        "min_words": 800
    },
    "TASKS.md": {
        "sections": ["Task Breakdown"],
        "min_words": 300
    },
    "README.md": {
        "sections": ["Installation", "Usage"],
        "min_words": 200
    }
}
```

**Implementation Strategy:**
1. **File Presence Check** (Static)
   ```python
   import os

   def check_files_exist(project_path):
       missing = []
       for doc in REQUIRED_DOCS.keys():
           if not os.path.exists(os.path.join(project_path, doc)):
               missing.append(doc)
       return missing
   ```

2. **Section Validation** (Static + LLM)
   - Static: Parse markdown headers with regex
   - LLM: Assess if sections are comprehensive

3. **Quality Assessment** (LLM)
   ```
   Prompt to Claude:
   "Evaluate this PRD.md against ISO/IEC 25010 standards.
   Does it clearly define:
   - Functional requirements with acceptance criteria?
   - Non-functional requirements (performance, security)?
   - Success metrics?

   Rate 1-10 and provide specific improvements."
   ```

---

### 3.2 Code Structure Analyzer Component

**Purpose**: Validate code organization and file size limits

**Checks:**
1. **File Size Enforcement** (CRITICAL)
   ```python
   def check_file_sizes(project_path):
       violations = []
       for root, dirs, files in os.walk(project_path):
           for file in files:
               if file.endswith(('.py', '.js', '.ts')):
                   path = os.path.join(root, file)
                   line_count = sum(1 for _ in open(path))
                   if line_count > 150:
                       violations.append({
                           "file": path,
                           "lines": line_count,
                           "excess": line_count - 150
                       })
       return violations
   ```

2. **Directory Structure Validation**
   ```
   Expected structure:
   project/
   ├── src/           (or lib/, app/) - Source code
   ├── tests/         - Test files
   ├── docs/          - Additional documentation
   ├── config/        - Configuration files
   ├── prompts/       - AI prompt logs
   ├── .gitignore
   ├── README.md
   └── requirements.txt (or package.json)
   ```

3. **Naming Conventions**
   - Files: snake_case for Python, camelCase for JS
   - Classes: PascalCase
   - Functions: snake_case (Python) or camelCase (JS)

---

### 3.3 Security Scanner Component

**Purpose**: Detect hardcoded secrets and security vulnerabilities

**Detection Patterns:**
```python
import re

SECRET_PATTERNS = {
    "api_key": r'(api[_-]?key|apikey)\s*=\s*["\'][^"\']+["\']',
    "password": r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
    "secret": r'(secret|token)\s*=\s*["\'][^"\']+["\']',
    "aws_key": r'(AKIA[0-9A-Z]{16})',
    "private_key": r'-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----',
}

def scan_for_secrets(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    findings = []
    for secret_type, pattern in SECRET_PATTERNS.items():
        for match in re.finditer(pattern, content, re.IGNORECASE):
            findings.append({
                "type": secret_type,
                "file": file_path,
                "line": content[:match.start()].count('\n') + 1,
                "snippet": match.group(0)[:50] + "..."
            })
    return findings
```

**Additional Checks:**
- ✅ `.gitignore` exists and includes `.env`, `*.key`, `credentials.json`
- ✅ `.env.example` exists (template for environment variables)
- ❌ `.env` file committed to Git (should be ignored)

---

### 3.4 Test Coverage Analyzer Component

**Purpose**: Measure test coverage and validate test quality

**For Python Projects:**
```python
# Assumes student ran: pytest --cov=src --cov-report=json

import json

def parse_coverage_report(project_path):
    coverage_file = os.path.join(project_path, "coverage.json")
    if not os.path.exists(coverage_file):
        return {
            "coverage_present": False,
            "error": "No coverage.json found. Did you run pytest --cov?"
        }

    with open(coverage_file, 'r') as f:
        data = json.load(f)

    total_coverage = data['totals']['percent_covered']

    return {
        "coverage_present": True,
        "total_coverage": total_coverage,
        "passes_threshold": total_coverage >= 70.0,
        "files": data['files']
    }
```

**For JavaScript Projects:**
```bash
# Assumes: npm run test -- --coverage --json
# Parse jest coverage output (JSON format)
```

**Test Quality Heuristics:**
1. Coverage ≥70% (minimum)
2. Edge cases documented in comments
3. Test file naming: `test_*.py` or `*.test.js`

---

### 3.5 Git History Evaluator Component

**Purpose**: Analyze commit history quality

**Metrics:**
```python
import subprocess
import re

def analyze_git_history(project_path):
    os.chdir(project_path)

    # Get commit log
    result = subprocess.run(
        ["git", "log", "--oneline", "--no-merges"],
        capture_output=True,
        text=True
    )
    commits = result.stdout.strip().split('\n')

    analysis = {
        "total_commits": len(commits),
        "passes_min_threshold": len(commits) >= 10,
        "commit_messages": []
    }

    # Analyze commit message quality
    for commit in commits:
        sha, message = commit.split(' ', 1)

        quality_score = 0
        if re.match(r'^(feat|fix|docs|test|refactor|chore):', message):
            quality_score += 1  # Conventional commit format
        if len(message) > 10:
            quality_score += 1  # Descriptive message
        if '[' in message and ']' in message:
            quality_score += 1  # Contains task reference

        analysis["commit_messages"].append({
            "sha": sha,
            "message": message,
            "quality_score": quality_score
        })

    avg_quality = sum(c["quality_score"] for c in analysis["commit_messages"]) / len(commits)
    analysis["avg_message_quality"] = avg_quality

    return analysis
```

**Good Commit Examples:**
```
feat(auth): Add user login functionality [TASK-001]
test(auth): Add unit tests for login edge cases [TASK-001]
docs: Update README with installation instructions
fix(api): Handle null response from external API [TASK-005]
```

**Bad Commit Examples:**
```
update
fixed stuff
changes
asdf
```

---

## 4. Data Models

### 4.1 GradingResult Schema

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Violation:
    type: str              # e.g., "oversized_file", "missing_docstring"
    severity: str          # "critical", "warning", "info"
    file: str              # File path
    line: Optional[int]    # Line number (if applicable)
    message: str           # Human-readable description
    penalty: float         # Score deduction

@dataclass
class CategoryScore:
    category: str          # e.g., "code_quality"
    score: float           # Achieved score
    max_score: float       # Maximum possible
    violations: List[Violation]
    details: Dict          # Category-specific data

@dataclass
class GradingResult:
    project_path: str
    timestamp: datetime
    overall_score: float
    max_score: float
    passed: bool           # True if score >= 70%
    categories: List[CategoryScore]
    summary: str           # LLM-generated summary
    recommendations: List[str]  # Specific improvement actions
```

---

### 4.2 Configuration Schema

```yaml
# config/grading_config.yaml

version: "1.0"

scoring_weights:
  documentation: 0.25
  code_quality: 0.30
  testing: 0.15
  security: 0.10
  git_workflow: 0.10
  research_quality: 0.10

thresholds:
  file_size_limit: 150
  test_coverage_min: 0.70
  min_commits: 10
  max_function_complexity: 10
  min_docstring_coverage: 0.90

penalties:
  hardcoded_secret: -50        # CRITICAL
  missing_required_doc: -10
  oversized_file: -5           # Per 10 lines
  low_test_coverage: -10       # If <70%
  poor_commit_history: -5      # If <10 commits

llm_config:
  model: "claude-sonnet-4"
  max_tokens: 4000
  temperature: 0.0             # Deterministic grading

output:
  formats: ["json", "html"]
  save_location: "./grading_reports/"
```

---

## 5. Skill Specifications

### 5.1 `/validate-docs` Skill

**Command**: `/validate-docs [project_path]`

**Purpose**: Check presence and quality of required documentation

**Execution Flow:**
```
1. Scan project directory for required files
2. Parse each markdown file
3. Validate section presence (static)
4. Send key sections to Claude for quality assessment (LLM)
5. Generate score and violation list
6. Return DocumentValidationResult
```

**Output Example:**
```
✅ PRD.md found
  ✅ Contains "Project Overview" section
  ✅ Contains "Functional Requirements" section
  ⚠️  Quality score: 7/10 - Missing acceptance criteria details

❌ CLAUDE.md NOT FOUND
  Penalty: -10 points

✅ README.md found
  ✅ Contains "Installation" section
  ✅ Contains "Usage" section
  ✅ Quality score: 9/10
```

---

### 5.2 `/analyze-code` Skill

**Command**: `/analyze-code [project_path] [--language python|javascript]`

**Purpose**: Validate code structure, quality, and adherence to standards

**Checks:**
1. File size limits (150 lines) - **CRITICAL**
2. Docstring coverage (90% target)
3. Naming conventions
4. Code complexity (cyclomatic complexity <10)
5. Import organization
6. Code readability (LLM assessment)

**Output Example:**
```
Code Structure Analysis
=======================

❌ CRITICAL: 3 files exceed 150-line limit
  - src/main.py: 215 lines (65 over limit)
  - src/utils.py: 180 lines (30 over limit)
  - src/api.py: 160 lines (10 over limit)

⚠️  Docstring Coverage: 75% (target: 90%)
  Missing docstrings:
  - src/helpers.py:42 - function calculate_score()
  - src/api.py:18 - class APIClient

✅ Naming Conventions: All files pass
✅ Code Complexity: Average 4.2 (max allowed: 10)

Overall Code Quality Score: 22/30
```

---

### 5.3 `/check-security` Skill

**Command**: `/check-security [project_path]`

**Purpose**: Detect security vulnerabilities and secrets

**Output Example:**
```
Security Scan Results
=====================

❌ CRITICAL: Hardcoded secrets detected
  - src/config.py:12 - API key exposed
    Line: api_key = "sk-1234567890abcdef"
    Penalty: -50 points

✅ .gitignore present and properly configured
✅ .env.example template found
⚠️  .env file found but NOT in .gitignore (verify it's not committed)

Security Score: 5/10 (FAIL)
```

---

### 5.4 `/evaluate-tests` Skill

**Command**: `/evaluate-tests [project_path]`

**Purpose**: Assess test coverage and quality

**Output Example:**
```
Test Coverage Analysis
======================

✅ Coverage report found: 78%
✅ Passes minimum threshold (70%)

File-level breakdown:
  src/main.py: 85%
  src/utils.py: 72%
  src/api.py: 65% ⚠️  (below 70%)

Test Quality Assessment:
  ✅ Edge cases documented in comments
  ✅ Test files follow naming convention
  ⚠️  No integration tests found

Testing Score: 13/15
```

---

### 5.5 `/assess-git` Skill

**Command**: `/assess-git [project_path]`

**Purpose**: Evaluate Git workflow and commit history

**Output Example:**
```
Git History Evaluation
======================

✅ Total commits: 18 (minimum: 10)
⚠️  Commit message quality: 6.2/10 average

Good commits (8):
  ✅ feat(auth): Add user login [TASK-001]
  ✅ test(auth): Add edge case tests [TASK-001]
  ✅ docs: Update README with API docs

Poor commits (10):
  ❌ "update" (too vague)
  ❌ "fixed stuff" (no context)
  ❌ "asdf" (meaningless)

Recommendations:
  - Use conventional commit format: type(scope): description
  - Reference task IDs in square brackets
  - Write descriptive messages (>10 characters)

Git Workflow Score: 7/10
```

---

### 5.6 `/grade-research` Skill

**Command**: `/grade-research [project_path]`

**Purpose**: Evaluate research methodology and analysis (LLM-heavy)

**What it looks for:**
1. Parameter exploration documentation
2. Statistical analysis (mean, std dev, confidence intervals)
3. Visualizations (charts, graphs)
4. Comparison of approaches
5. Ablation studies

**Example Prompt to Claude:**
```
You are evaluating a graduate-level software research project.

Analyze the following research documentation:
[Insert PLANNING.md and relevant sections]

Assess the following criteria (1-10 scale each):
1. Parameter Exploration: Did they test multiple configurations?
2. Statistical Rigor: Are results quantified with error bars/CI?
3. Visualization Quality: Are charts clear and informative?
4. Comparative Analysis: Did they compare multiple approaches?
5. Depth of Analysis: Is the methodology thorough?

Provide specific examples and improvement suggestions.
```

---

### 5.7 `/check-ux` Skill

**Command**: `/check-ux [project_path]`

**Purpose**: Evaluate UI/UX against Nielsen's heuristics

**Nielsen's 10 Heuristics:**
1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency
8. Aesthetic and minimalist design
9. Help users recognize and recover from errors
10. Help and documentation

**LLM Prompt Example:**
```
Evaluate this application's UX/UI:

Screenshots provided:
[List screenshot paths]

README describes:
[Insert usage section]

Rate 1-10 for each of Nielsen's heuristics:
1. Visibility of system status - Does the app show loading states, progress?
2. Match between system and real world - Are labels intuitive?
...
10. Help and documentation - Is there a user guide?

Provide specific examples from screenshots.
```

---

### 5.8 `/generate-report` Skill

**Command**: `/generate-report [grading_results_json]`

**Purpose**: Aggregate all skill results into final report

**Inputs**: JSON objects from all previous skills
**Outputs**:
- `grading_report.json` (machine-readable)
- `grading_report.html` (human-readable)
- CLI summary

**HTML Template Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Grading Report - [Project Name]</title>
    <style>
        .pass { color: green; }
        .warn { color: orange; }
        .fail { color: red; }
    </style>
</head>
<body>
    <h1>Auto-Grader Report</h1>
    <div class="summary">
        <h2>Overall Score: <span class="pass">87.5/100</span></h2>
        <p>Status: ✅ PASS (≥70% required)</p>
    </div>

    <div class="category">
        <h3>Documentation (22.5/25)</h3>
        <ul>
            <li class="pass">✅ PRD.md - Quality: 9/10</li>
            <li class="fail">❌ CLAUDE.md - MISSING (-10 pts)</li>
        </ul>
    </div>

    <!-- Repeat for each category -->
</body>
</html>
```

---

### 5.9 `/grade-project` Meta-Skill

**Command**: `/grade-project [project_path] [--deep]`

**Purpose**: Orchestrate full grading workflow

**Execution Flow:**
```python
async def grade_project(project_path, deep=False):
    results = {}

    # Phase 1: Quick checks (parallel)
    results['docs'] = await run_skill('validate-docs', project_path)
    results['structure'] = await run_skill('analyze-code', project_path, quick=not deep)
    results['security'] = await run_skill('check-security', project_path)

    # Phase 2: Deeper analysis (if --deep flag)
    if deep:
        results['tests'] = await run_skill('evaluate-tests', project_path)
        results['git'] = await run_skill('assess-git', project_path)
        results['research'] = await run_skill('grade-research', project_path)
        results['ux'] = await run_skill('check-ux', project_path)

    # Phase 3: Aggregation
    final_report = await run_skill('generate-report', results)

    # Display summary
    print_summary(final_report)

    # Save reports
    save_json(final_report, f"{project_path}/grading_report.json")
    save_html(final_report, f"{project_path}/grading_report.html")

    return final_report
```

**Quick Mode** (`/grade-project`):
- ~1 minute execution
- Document presence, file sizes, security scan
- 70% of grading criteria

**Deep Mode** (`/grade-project --deep`):
- ~10-15 minutes execution
- Full LLM analysis, test coverage, research quality
- 100% of grading criteria

---

## 6. Integration Points

### 6.1 Claude API Integration

**Authentication**: Uses Claude Code CLI's existing API credentials

**API Call Pattern:**
```python
import anthropic

def analyze_with_claude(prompt, content, max_tokens=4000):
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=max_tokens,
        temperature=0.0,  # Deterministic for grading
        messages=[{
            "role": "user",
            "content": f"{prompt}\n\n{content}"
        }]
    )

    return message.content[0].text
```

**Rate Limiting:**
- Batch LLM calls where possible
- Use caching for repeated prompts
- Implement exponential backoff if rate limited

---

### 6.2 Git Integration

**Required Git Commands:**
```bash
# Check if directory is a Git repo
git rev-parse --is-inside-work-tree

# Get commit history
git log --oneline --no-merges

# Check for uncommitted secrets in .env
git check-ignore .env  # Should return .env (i.e., it's ignored)

# Get commit statistics
git shortlog -s -n  # Commits per author
```

**Python Wrapper:**
```python
import subprocess

def run_git_command(cmd, cwd):
    result = subprocess.run(
        cmd.split(),
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
```

---

### 6.3 File System Integration

**Safe File Reading:**
```python
def safe_read_file(file_path, max_size_mb=10):
    """Prevent reading excessively large files"""
    size = os.path.getsize(file_path)
    if size > max_size_mb * 1024 * 1024:
        raise ValueError(f"File {file_path} exceeds {max_size_mb}MB limit")

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
```

**Directory Traversal:**
```python
def find_code_files(project_path, extensions=['.py', '.js', '.ts']):
    code_files = []
    for root, dirs, files in os.walk(project_path):
        # Skip common ignore directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '.git', '__pycache__']]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))

    return code_files
```

---

## 7. Error Handling Strategy

### 7.1 Error Categories

| Error Type | Handling Strategy | Example |
|------------|-------------------|---------|
| **File Not Found** | Graceful degradation, log warning | README.md missing → deduct points but continue |
| **Git Not Initialized** | Skip git-related checks | No .git → git_score = 0, warn user |
| **LLM API Failure** | Retry with backoff, fallback to static analysis | Claude API down → use regex-based doc check |
| **Invalid File Format** | Skip file, log error | Corrupted .json → exclude from analysis |
| **Timeout** | Kill subprocess, mark check as incomplete | Code execution >60s → terminate |

### 7.2 Error Recovery Examples

```python
import time

def call_claude_with_retry(prompt, content, max_retries=3):
    for attempt in range(max_retries):
        try:
            return analyze_with_claude(prompt, content)
        except anthropic.RateLimitError:
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, retrying in {sleep_time}s...")
                time.sleep(sleep_time)
            else:
                print("LLM unavailable, using static analysis fallback")
                return None  # Caller should handle gracefully
```

---

## 8. Testing Strategy

### 8.1 Unit Tests (Per Component)

**Target Coverage**: ≥80% per component

**Example Test:**
```python
# tests/test_file_size_analyzer.py
import pytest
from src.analyzers.file_size_analyzer import check_file_sizes

def test_detects_oversized_file(tmp_path):
    # Create 200-line test file
    test_file = tmp_path / "large.py"
    test_file.write_text('\n'.join([f"# Line {i}" for i in range(200)]))

    violations = check_file_sizes(str(tmp_path))

    assert len(violations) == 1
    assert violations[0]['file'].endswith('large.py')
    assert violations[0]['lines'] == 200
    assert violations[0]['excess'] == 50

def test_allows_valid_file_size(tmp_path):
    # Create 100-line file (within limit)
    test_file = tmp_path / "small.py"
    test_file.write_text('\n'.join([f"# Line {i}" for i in range(100)]))

    violations = check_file_sizes(str(tmp_path))

    assert len(violations) == 0
```

---

### 8.2 Integration Tests

**Test Full Grading Workflow:**
```python
# tests/test_integration.py

def test_full_grading_workflow():
    # Setup: Create mock project with known issues
    project = create_mock_project({
        "missing_files": ["CLAUDE.md"],
        "oversized_files": ["src/main.py"],
        "hardcoded_secret": "src/config.py:12",
        "test_coverage": 0.65  # Below 70% threshold
    })

    # Execute grading
    result = grade_project(project.path)

    # Assertions
    assert result.overall_score < 70  # Should fail
    assert "CLAUDE.md" in [v.file for v in result.violations]
    assert any(v.type == "oversized_file" for v in result.violations)
    assert any(v.type == "hardcoded_secret" for v in result.violations)
```

---

### 8.3 Accuracy Benchmark Tests

**Methodology:**
1. Collect 20 diverse student projects
2. Have 3 expert graders evaluate each manually
3. Run auto-grader on same projects
4. Compare scores:

```python
def calculate_agreement(human_scores, auto_scores):
    """
    Target: ≥90% agreement (±5% variance)
    """
    agreements = []
    for human, auto in zip(human_scores, auto_scores):
        diff = abs(human - auto)
        variance_pct = (diff / human) * 100
        agreements.append(variance_pct <= 5.0)

    accuracy = sum(agreements) / len(agreements) * 100
    return accuracy

# Example:
human_scores = [85, 72, 90, 65, 78, ...]
auto_scores  = [87, 70, 88, 63, 80, ...]

accuracy = calculate_agreement(human_scores, auto_scores)
print(f"Accuracy: {accuracy}%")  # Target: ≥90%
```

---

## 9. Deployment Plan

### 9.1 Phase 1: Core Skills (P0 Features)

**Timeline**: First implementation phase
**Deliverables:**
- `/validate-docs`
- `/analyze-code`
- `/check-security`
- `/evaluate-tests`
- `/generate-report`
- `/grade-project` (quick mode only)

**Acceptance Criteria:**
- [ ] All skills have ≥80% test coverage
- [ ] Can grade a Python project in <5 minutes
- [ ] Generates valid JSON and HTML reports
- [ ] Detects critical issues (secrets, oversized files)

---

### 9.2 Phase 2: Advanced Analysis (P1 Features)

**Timeline**: Second implementation phase
**Deliverables:**
- `/assess-git`
- `/grade-research`
- `/check-ux`
- `/grade-project --deep`

**Acceptance Criteria:**
- [ ] LLM-based quality assessment operational
- [ ] Full grading completes in <15 minutes
- [ ] Accuracy benchmark ≥90%

---

### 9.3 Phase 3: Batch Processing (P2 Features)

**Timeline**: Third implementation phase
**Deliverables:**
- `/grade-batch` for multiple projects
- CSV export for instructor dashboards
- Comparative analytics

**Acceptance Criteria:**
- [ ] Can process 10 projects in parallel
- [ ] Generates aggregated summary report
- [ ] Cost stays under $0.20 per project

---

### 9.4 Installation Instructions

**For End Users (Students/Instructors):**
```bash
# 1. Install Claude Code CLI (if not already installed)
# Follow: https://docs.anthropic.com/claude/docs/cli

# 2. Install auto-grader skills
claude-code skills install academic-auto-grader

# 3. Navigate to project directory
cd /path/to/student/project

# 4. Run grading
claude-code /grade-project

# 5. View report
open grading_report.html
```

**For Developers:**
```bash
# Clone repository
git clone https://github.com/your-org/academic-auto-grader.git
cd academic-auto-grader

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ --cov=src

# Install skills locally
claude-code skills link .
```

---

## 10. Appendices

### 10.1 Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| **Skills Framework** | Claude Code CLI | Required by project scope |
| **Language** | Python 3.9+ | AST parsing, wide library support |
| **Code Parsing** | `ast` (Python), Tree-sitter (JS) | Accurate static analysis |
| **LLM** | Claude Sonnet 4 | Context window, instruction following |
| **Testing** | pytest, coverage.py | Industry standard |
| **Reporting** | Jinja2 (HTML templates), JSON | Human + machine readable |
| **Security Scanning** | Regex + `detect-secrets` library | Proven patterns |

---

### 10.2 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Claude API Downtime** | High - LLM checks fail | Graceful degradation to static analysis |
| **Student Code Malicious** | Critical - System compromise | No code execution, read-only access |
| **High API Costs** | Medium - Budget overrun | Hybrid approach, caching, batch optimization |
| **False Positives** | Medium - Student frustration | Clear error messages, manual override option |
| **Grading Inconsistency** | High - Unfair evaluation | Temperature=0 for determinism, benchmark tests |

---

**Document Version**: 1.0
**Last Updated**: 2025-01-25
**Status**: Approved for Implementation
**Next Review**: After Phase 1 completion
