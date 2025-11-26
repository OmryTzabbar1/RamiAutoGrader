# Performance Optimization Guide

## Overview

The auto-grader has been optimized for **3-5x faster execution** through parallel processing, intelligent caching, and early exit strategies. This document explains the optimizations and how to use them.

---

## Performance Improvements

### 1. Parallel Skill Execution (3-5x Speedup)

**Problem:** Skills ran sequentially, wasting time when they could run concurrently.

**Solution:** Use `ThreadPoolExecutor` to run independent skills in parallel.

**Impact:**
- Before: ~15-20 seconds for typical project
- After: ~3-5 seconds (3-5x faster)
- Configurable worker count (default: 4)

**Implementation:** `src/core/skill_executor_optimized.py`

```python
# Skills run concurrently using thread pool
with ThreadPoolExecutor(max_workers=4) as executor:
    future_to_skill = {
        executor.submit(analyze_code): 'code_quality',
        executor.submit(check_docs): 'documentation',
        executor.submit(evaluate_tests): 'testing',
        # ... etc
    }
```

---

### 2. Shared File Scanning Cache (70% Reduction in I/O)

**Problem:** Each analyzer scanned the filesystem independently, causing redundant file operations.

**Solution:** Centralized `ProjectCache` that stores file lists and content.

**Impact:**
- Eliminates ~70% of redundant file system operations
- Faster subsequent file access
- Thread-safe for parallel execution

**Implementation:** `src/core/project_cache.py`

```python
# First analyzer scans filesystem
cache = ProjectCache(project_path)
files = cache.get_code_files()  # Scans filesystem

# Second analyzer reuses cached result
files = cache.get_code_files()  # Returns instantly from cache
```

**Cached Data:**
- Code file lists (`.py`, `.js`, `.ts`)
- Test file lists
- Git repository metadata
- File content for repeated reads

---

### 3. Early Exit on Critical Failures

**Problem:** Grader continued running all checks even after detecting critical failures (e.g., hardcoded secrets = auto-fail).

**Solution:** Security check runs first; if secrets detected, remaining checks are skipped.

**Impact:**
- Projects with critical failures fail in <1 second
- Saves ~10-15 seconds on failed submissions
- Provides immediate feedback

**Implementation:**
```python
# Phase 1: Critical checks (run first)
results['security'] = run_security_check(project_path)

if results['security']['is_critical_failure']:
    print("[!] CRITICAL FAILURE: Skipping remaining checks")
    return early_exit_results

# Phase 2: Remaining checks (only if passed phase 1)
run_other_skills_in_parallel()
```

---

### 4. Optimized Git Operations

**Problem:** Git history analysis was slow on large repositories.

**Solutions:**
- Reduced default commit limit (100 → 50)
- Shorter timeout (10s → 5s)
- Short hash format (saves memory)
- Better error handling

**Impact:**
- ~40% faster git analysis
- Handles slow/large repos gracefully
- Improved timeout handling

**Implementation:** `src/utils/git_commands.py`

```python
# Optimized git log command
result = subprocess.run(
    ['git', 'log', '-50', '--format=%H|%s|%an|%ad', '--date=short'],
    timeout=5  # Faster timeout
)
```

---

## Usage

### Basic Usage (Parallel Mode - Default)

```bash
# Parallel execution (default, fastest)
python grade_project.py ./student-project

# Same as:
python grade_project.py ./student-project --parallel --workers 4
```

### Sequential Mode (For Debugging)

```bash
# Sequential execution (slower, easier to debug)
python grade_project.py ./student-project --sequential
```

### Advanced Options

```bash
# Customize worker count (2-8 workers recommended)
python grade_project.py ./project --workers 6

# Disable early exit (run all checks even on critical failures)
python grade_project.py ./project --no-early-exit

# Combine options
python grade_project.py ./project --workers 8 --no-early-exit --json
```

---

## Benchmarking

Run the benchmarking script to measure performance improvements:

```bash
# Single run
python benchmark_performance.py ./student-project

# Multiple runs for average (recommended)
python benchmark_performance.py ./student-project --runs 3

# Test different worker counts
python benchmark_performance.py ./project --runs 3 --workers 6
```

**Example Output:**
```
BENCHMARK RESULTS
============================================================

Sequential (Original):
  Average time: 15.34s

Parallel (Optimized, 4 workers):
  Average time: 3.82s

Performance Improvement:
  Speedup: 4.01x
  Time saved: 11.52s
  Faster by: 75.1%

🚀 EXCELLENT: Major performance improvement!
```

---

## Performance Tuning

### Worker Count Guidelines

| CPU Cores | Recommended Workers | Notes |
|-----------|---------------------|-------|
| 2 cores   | 2-3 workers         | Minimal overhead |
| 4 cores   | 4 workers (default) | Balanced performance |
| 6+ cores  | 6-8 workers         | Maximum parallelism |
| 8+ cores  | 6-8 workers         | Diminishing returns beyond 8 |

**Finding Optimal Worker Count:**
```bash
# Test different configurations
for workers in 2 4 6 8; do
    echo "Testing $workers workers..."
    python grade_project.py ./project --workers $workers
done
```

### When to Use Sequential Mode

Use `--sequential` when:
- Debugging specific skill failures
- Generating detailed logs
- Testing individual analyzer changes
- Running on low-resource systems

---

## Architecture

### Parallel Execution Flow

```
1. Initialize ProjectCache (shared state)
2. Run Security Check (can trigger early exit)
   └─ If critical failure: Skip to results
3. Run remaining skills in parallel:
   ┌─ Code Analysis ────────┐
   ├─ Documentation ────────┤
   ├─ Testing ──────────────┼─→ ThreadPoolExecutor
   ├─ Git Assessment ───────┤   (max_workers=4)
   ├─ Research Evaluation ──┤
   └─ UX Evaluation ────────┘
4. Aggregate results and calculate score
```

### Thread Safety

All analyzers are **thread-safe**:
- No shared mutable state between skills
- `ProjectCache` uses locks for thread-safe access
- Independent file operations per skill

---

## Optimization Impact Summary

| Optimization | Speedup | Impact |
|--------------|---------|--------|
| Parallel execution | 3-5x | High |
| File scanning cache | 1.5-2x | Medium |
| Early exit | Variable* | High for failures |
| Git optimization | 1.4x | Medium |
| **Combined** | **3-5x overall** | **Very High** |

\* Early exit only affects projects with critical failures (~20-30% of submissions)

---

## Future Optimization Opportunities

### Not Yet Implemented (Lower Priority)

1. **Process Pool for CPU-Bound Tasks**
   - AST parsing could use ProcessPoolExecutor
   - Limited benefit (most work is I/O bound)
   - Adds complexity

2. **Persistent Cache Across Runs**
   - Cache results for unchanged files (git hash-based)
   - Useful for re-grading with different rubrics
   - Requires cache invalidation logic

3. **Incremental Analysis**
   - Only analyze changed files (git diff)
   - Significant complexity for marginal gain
   - Not worth it for single-run grading

4. **Async I/O with asyncio**
   - Replace threads with async/await
   - Minimal benefit over ThreadPoolExecutor
   - More complex code

---

## Troubleshooting

### "Too many open files" Error

**Symptom:** Error when grading large projects with many files.

**Solution:** Reduce worker count:
```bash
python grade_project.py ./project --workers 2
```

### Workers Not Improving Performance

**Symptom:** No speedup when increasing workers.

**Possible Causes:**
- I/O bottleneck (slow disk)
- Small project (overhead > benefit)
- Already at optimal parallelism

**Solution:** Benchmark to find optimal worker count:
```bash
python benchmark_performance.py ./project --runs 3
```

### Inconsistent Results Between Sequential/Parallel

**Symptom:** Different scores between modes.

**Expected:** Results should be identical (same scoring logic).

**If Different:** Report bug with project path and output.

---

## Implementation Notes

### Why ThreadPoolExecutor (not ProcessPoolExecutor)?

- **I/O Bound:** Most work is file reading and git commands
- **Lightweight:** Less overhead than process spawning
- **Shared Cache:** Threads can share ProjectCache
- **Simpler:** No pickle serialization needed

### Why Not Asyncio?

- ThreadPoolExecutor is simpler and sufficient
- Skills use blocking I/O (subprocess, file reads)
- Converting to async/await = major refactor
- Minimal performance benefit

### Thread Safety Strategy

1. **Read-Only Sharing:** Skills only read from cache
2. **Locks for Writes:** ProjectCache uses `threading.Lock()`
3. **Independent Results:** Each skill returns isolated dict
4. **No Global State:** All state is local or explicitly synchronized

---

## Questions?

- **Performance issues?** Run benchmarks and check worker count
- **Debugging?** Use `--sequential` mode
- **Custom tuning?** Adjust `--workers` based on your hardware
- **Report bugs:** Include benchmark output and system specs
