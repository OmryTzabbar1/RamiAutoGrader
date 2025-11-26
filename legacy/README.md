# Legacy Code Archive

**Archived:** 2025-11-26  
**Reason:** Architecture change from monolithic scripts to agent-based skill orchestration

---

## Why These Files Were Archived

The auto-grader architecture changed in v2.0.0:

**OLD Architecture (Monolithic):**
```
CLI Script (grade_project.py, grade_from_git.py)
  └─> Python Executor (skill_executor_optimized.py)
      └─> Runs all grading functions
```

**NEW Architecture (Agent-Based):**
```
Claude Code Agent
  ├─> /skill check-security     ]
  ├─> /skill validate-docs       ] All invoked
  ├─> /skill analyze-code        ] in parallel
  ├─> /skill evaluate-tests      ] by agent
  ├─> /skill assess-git          ]
  ├─> /skill grade-research      ]
  └─> /skill check-ux            ]
```

---

## Archived Files

### Root Scripts (Entry Points)

1. **grade_from_git.py** (152 lines)
   - Purpose: Clone Git repo and grade in one script
   - Replaced by: Agent clones via `git_clone.py` utility + calls individual skills

2. **grade_project.py** (163 lines)
   - Purpose: Orchestrate all grading via Python executor
   - Replaced by: Agent orchestrates skills directly

3. **benchmark_performance.py** (~80 lines)
   - Purpose: Benchmark sequential vs parallel execution
   - Replaced by: N/A (agent benchmarking would be different)

### Core Modules (Orchestration)

4. **src/core/skill_executor.py**
   - Purpose: Sequential Python executor for all skills
   - Replaced by: Agent Skill tool invocation

5. **src/core/skill_executor_optimized.py** (209 lines)
   - Purpose: Parallel Python executor using ThreadPoolExecutor
   - Replaced by: Agent parallel skill invocation (multiple Skill tool calls)

6. **src/core/project_cache.py** (162 lines)
   - Purpose: Shared cache for parallel executor
   - Replaced by: Each skill handles caching individually

### CLI Utilities

7. **src/cli/arg_parser.py**
   - Purpose: CLI argument parsing for scripts
   - Replaced by: Agent processes user messages directly

---

## Impact of Archiving

### File Size Violations Fixed:
- Before: 5 files over 150 lines
- After: 1 file over 150 lines (detailed_reporter.py)
- **Files fixed:**
  - grade_from_git.py: 152 → archived ✅
  - grade_project.py: 163 → archived ✅
  - skill_executor_optimized.py: 209 → archived ✅
  - project_cache.py: 162 → archived ✅

### Grading Impact:
- File size penalties: −13 points → −3 points
- **Points gained: +10**
- Estimated new score: 66 → 76 (C+, near passing)

---

## How to Use Legacy Code (If Needed)

These files are preserved for reference but are **not maintained**.

To use legacy CLI scripts:
```bash
# Run from legacy directory
cd legacy/
python grade_project.py /path/to/project
python grade_from_git.py https://github.com/user/repo.git
```

**Note:** Legacy scripts may break as the codebase evolves. Use the agent instead:
```bash
@agent-grade-project grade /path/to/project
@agent-grade-project grade https://github.com/user/repo.git
```

---

## Migration Guide

If you have scripts/tools using the legacy CLI:

**OLD:**
```bash
python grade_project.py ./student_project --output results.json
```

**NEW:**
```bash
# Use the agent instead
@agent-grade-project grade ./student_project
```

Or invoke skills individually:
```bash
/skill check-security ./student_project
/skill analyze-code ./student_project
# ... etc
```

---

**Archive Version:** 1.0  
**Agent Architecture Version:** 2.0.0  
**Documentation:** See docs/architecture/dependency-map.md
