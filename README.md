# Academic Software Auto-Grader System

An intelligent auto-grading system for M.Sc. Computer Science project submissions, built as a collection of Claude Code CLI skills and orchestrated by a conversational AI agent.

## Overview

This system evaluates academic software projects against ISO/IEC 25010 quality standards and academic excellence criteria, providing comprehensive, automated grading with actionable feedback.

## Architecture

- **Claude Code Skills**: Modular grading components (documentation validation, code analysis, security scanning, etc.)
- **Orchestrator Agent**: Intelligent coordinator with natural language interface
- **Hybrid Analysis**: Static analysis for objective checks + LLM for subjective quality assessment

## Key Features

- 📝 **Documentation Analysis**: PRD, README, Architecture, CLAUDE.md validation
- 💻 **Code Quality**: File size limits, naming conventions, docstring coverage, complexity metrics
- 🔒 **Security Scanning**: Hardcoded secrets detection, .gitignore validation
- ✅ **Test Coverage**: Coverage analysis (70% minimum requirement)
- 📊 **Git History**: Commit quality and workflow evaluation
- 🎨 **UX Assessment**: Nielsen's heuristics evaluation
- 🔬 **Research Quality**: Parameter exploration and analysis depth
- 🌐 **GitHub Integration**: Grade repositories directly from GitHub URLs

## Grading Criteria

- **Documentation (25%)**: Completeness and quality of project documentation
- **Code Quality (30%)**: Structure, naming, comments, complexity
- **Testing (15%)**: Coverage and test quality
- **Security (10%)**: No secrets, proper .gitignore
- **Git Workflow (10%)**: Commit history quality
- **Research Quality (10%)**: Analysis depth and methodology

## Installation

```bash
# Clone repository
git clone https://github.com/OmryTzabbar1/RamiAutoGrader.git
cd RamiAutoGrader

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Grade a local project
/grade-project /path/to/student/project

# Grade a GitHub repository
/grade-github-project https://github.com/username/project.git

# Run specific checks
/validate-docs /path/to/project
/analyze-code /path/to/project
/check-security /path/to/project
```

## Project Status

🚧 **Under Development** - Phase 1: Infrastructure Setup

See [TASKS.MD](TASKS.MD) for detailed task breakdown and progress tracking.

## Documentation

- [PRD.md](PRD.md) - Product Requirements Document
- [PLANNING.MD](PLANNING.MD) - Technical Architecture & ADRs
- [CLAUDE.MD](CLAUDE.MD) - Development Guidelines
- [TASKS.MD](TASKS.MD) - Task Breakdown & Progress

## Development Guidelines

- **File Size Limit**: 150 lines maximum (STRICTLY ENFORCED)
- **Commit Frequency**: 15-25+ commits showing clear progression
- **Commit Format**: `<type>(<scope>): <description> [TASK-ID]`
- **Documentation**: Every function, class, and module must have docstrings
- **Testing**: 70% minimum coverage (80%+ for core grading logic)

## License

Academic project for M.Sc. Computer Science program.

## Contact

Repository: https://github.com/OmryTzabbar1/RamiAutoGrader.git
