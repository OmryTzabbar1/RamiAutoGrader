# Module Dependency Map

**Generated:** 2025-11-26  
**Purpose:** Identify used vs unused code after agent architecture change

---

## Entry Points

### 1. Claude Code Skills (Primary Entry Points - USED)

**Location:** `skills/*.skill/main.py`

These are invoked by the agent via `/skill <name>`:

- **analyze-code**: `skills/analyze-code.skill/main.py`
- **assess-git**: `skills/assess-git.skill/main.py`
- **check-security**: `skills/check-security.skill/main.py`
- **check-ux**: `skills/check-ux.skill/main.py`
- **evaluate-tests**: `skills/evaluate-tests.skill/main.py`
- **grade-research**: `skills/grade-research.skill/main.py`
- **validate-docs**: `skills/validate-docs.skill/main.py`

### 2. Legacy CLI Scripts (POTENTIALLY UNUSED)

**Location:** Root directory

These were CLI entry points before agent architecture:

- **grade_from_git.py**: Clone + grade in one script (152 lines)
- **grade_project.py**: Orchestrate all grading (163 lines)  
- **benchmark_performance.py**: Performance testing

---

## Dependency Analysis

### Skills → Dependencies

#### check-security skill imports:
import sys
import os
import json
from src.analyzers.security_scanner import scan_for_secrets
from src.validators.gitignore_validator import validate_gitignore
from src.validators.env_validator import check_env_template
from src.reporters.security_reporter import generate_security_report

#### analyze-code skill imports:
import sys
import json
from src.analyzers.file_size_analyzer import check_file_sizes, generate_size_report
from src.analyzers.docstring_analyzer import analyze_project_docstrings
from src.validators.naming_validator import analyze_project_naming

#### validate-docs skill imports:
import sys
import json
from src.analyzers.documentation_checker import check_project_documentation

### Legacy Scripts → Dependencies

#### grade_from_git.py imports:
import sys
import json
from src.utils.git_clone import clone_repository, cleanup_clone
from src.utils.git_helpers import is_git_url
from src.core.skill_executor import run_all_skills
from src.core.skill_executor_optimized import run_all_skills_parallel
from src.core.grading_utils import format_results_summary
from src.cli.arg_parser import create_arg_parser

#### grade_project.py imports:
import sys
import json
import argparse
from src.core.skill_executor import run_all_skills
from src.core.skill_executor_optimized import run_all_skills_parallel
from src.core.grading_utils import format_results_summary

#### benchmark_performance.py imports:
import sys
import time
import argparse
from src.core.skill_executor import run_all_skills
from src.core.skill_executor_optimized import run_all_skills_parallel

---

## Module Usage Matrix

| Module | Used by Skills | Used by Scripts | Status |
|--------|----------------|-----------------|--------|
| `src/analyzers/file_size_analyzer.py` | analyze-code | - | ✅ USED |
| `src/analyzers/security_scanner.py` | check-security | - | ✅ USED |
| `src/core/skill_executor.py` | - | grade_project, benchmark | ❌ UNUSED |
| `src/core/skill_executor_optimized.py` | - | grade_from_git, grade_project, benchmark | ❌ UNUSED |
| `src/core/project_cache.py` | - | skill_executor_optimized | ❌ UNUSED |
| `src/cli/arg_parser.py` | - | grade_from_git, grade_project | ❌ UNUSED |
| `src/utils/git_clone.py` | - | grade_from_git, agent | ✅ USED (by agent) |

---

## Summary & Recommendations

### ✅ KEEP - Used by Skills (Current Architecture)

**Core Analyzers:**
- `src/analyzers/file_size_analyzer.py`
- `src/analyzers/docstring_analyzer.py`
- `src/analyzers/security_scanner.py`
- `src/analyzers/documentation_checker.py`
- `src/analyzers/test_analyzer.py`
- `src/analyzers/git_analyzer.py`
- `src/analyzers/research_analyzer.py`
- `src/analyzers/ux_analyzer.py`

**Validators:**
- `src/validators/gitignore_validator.py`
- `src/validators/env_validator.py`
- `src/validators/naming_validator.py`

**Reporters:**
- `src/reporters/security_reporter.py`
- `src/reporters/detailed_reporter.py` (needs refactoring - 298 lines)

**Utilities:**
- `src/utils/git_clone.py` ✅ **Used by agent for cloning**
- `src/utils/file_finder.py`
- `src/utils/line_counter.py`
- All other utils/* (used internally)

**Parsers:**
- `src/parsers/python_parser.py`

---

### ❌ ARCHIVE - Only Used by Legacy Scripts

**To Archive:**

1. **grade_from_git.py** (152 lines)
   - Reason: Agent now clones via `clone_repository()` + calls individual skills
   - Replaced by: Agent orchestration

2. **grade_project.py** (163 lines)
   - Reason: Agent orchestrates skills directly
   - Replaced by: Agent orchestration

3. **src/core/skill_executor.py** (~150 lines)
   - Reason: Agent calls skills via Skill tool, not Python
   - Replaced by: Agent parallel skill invocation

4. **src/core/skill_executor_optimized.py** (209 lines)
   - Reason: Same as above
   - Replaced by: Agent parallel skill invocation

5. **src/core/project_cache.py** (162 lines)
   - Reason: Only used by skill_executor_optimized.py
   - Replaced by: N/A (each skill handles its own caching if needed)

6. **src/cli/arg_parser.py** (~50 lines)
   - Reason: Only used by grade_from_git.py and grade_project.py
   - Replaced by: Agent processes user input

---

### ❓ DECIDE - Special Cases

1. **benchmark_performance.py** (~80 lines)
   - Uses: skill_executor_optimized.py
   - Options:
     - A) Archive (no longer needed)
     - B) Refactor to benchmark agent performance instead
   - **Recommendation**: Archive (agent benchmarking can be done differently)

2. **src/core/grading_utils.py**
   - Uses: Only `calculate_grade()` and `format_results_summary()`
   - Used by: Legacy scripts only
   - **Recommendation**: Keep but verify if agent needs these functions

---

## Impact of Archiving

### Files to Move to `legacy/`:
- `grade_from_git.py`
- `grade_project.py`
- `benchmark_performance.py`
- `src/core/skill_executor.py`
- `src/core/skill_executor_optimized.py`
- `src/core/project_cache.py`
- `src/cli/arg_parser.py`

### File Size Violations Fixed:
- grade_from_git.py: 152 lines → archived ✅
- grade_project.py: 163 lines → archived ✅
- skill_executor_optimized.py: 209 lines → archived ✅
- project_cache.py: 162 lines → archived ✅

**Result:** 4 out of 5 file size violations eliminated!

**Remaining violation:**
- `src/reporters/detailed_reporter.py` (298 lines) - needs refactoring

### Grading Impact:
- File size violations: 5 → 1 (-13 points → -3 points) = **+10 points**
- Cleaner codebase: +1-2 bonus points
- **Total:** +11-12 points from archiving alone!

---

**Document Status:** COMPLETE  
**Next Step:** P7.1.2 - Create unused code audit document
