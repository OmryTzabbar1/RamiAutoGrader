# ADR-007: Strictness Parameter Design

**Status**: ✅ Accepted
**Date**: 2025-11-27
**Context**: Implement adaptive grading strictness based on student self-grades

---

## Problem Statement

Students submit self-assigned grades along with their projects. Students who claim higher grades (e.g., 95+) should face more critical evaluation to prevent grade inflation and ensure accuracy.

---

## Decision

Implement a **strictness multiplier** parameter that scales:
1. **Penalty values** (deductions for violations)
2. **Quality thresholds** (minimum requirements for passing)

---

## Strictness Formula

```python
strictness = 1.0 + (self_grade / 100) * 0.3

# Examples:
# self_grade = 70  → strictness = 1.21  (baseline)
# self_grade = 85  → strictness = 1.255 (25.5% stricter)
# self_grade = 95  → strictness = 1.285 (28.5% stricter)
# self_grade = 100 → strictness = 1.30  (30% stricter)
```

---

## Implementation Details

### 1. SKILL.md Parameter Section

Add to each grading skill:

```markdown
## Strictness Parameter (Optional)

This skill accepts an optional `strictness` multiplier to adjust grading rigor.

**Usage:**
- Default: `strictness=1.0` (standard grading)
- Adaptive: `strictness=1.0 to 1.3` (based on student self-grade)

**How strictness affects grading:**
- **Penalties are multiplied** by strictness value
- **Quality thresholds are raised** for higher strictness

Example:
- Standard: -5 points for file size violation
- Strictness 1.3: -6.5 points for file size violation (5 × 1.3)
```

### 2. Penalty Scaling

**analyze-code** (30 points max):
```python
# Standard penalties
file_size_penalty = -5 * strictness
naming_violation_penalty = -0.5 * strictness
docstring_penalty = -(0.9 - coverage) * 20 * strictness
```

**evaluate-tests** (15 points max):
```python
# Standard penalties
no_test_files_penalty = -15 * strictness  # Auto-fail gets worse
few_test_files_penalty = -5 * strictness
insufficient_tests_penalty = -3 * strictness
```

**check-security** (10 points max):
```python
# Standard penalties (critical violations don't scale - always 0)
hardcoded_secrets_penalty = 0  # Critical failure (no scaling)
gitignore_penalty = -3 * strictness
env_config_penalty = -2 * strictness
```

**validate-docs** (25 points max):
```python
# Standard penalties
missing_prd_penalty = -10 * strictness
missing_readme_penalty = -8 * strictness
missing_architecture_penalty = -5 * strictness
```

### 3. Threshold Adjustments

**Docstring Coverage** (analyze-code):
```python
# Base threshold: 90%
# Adjusted threshold: 90% + (strictness - 1.0) * 20%

strictness = 1.0  → threshold = 90%
strictness = 1.2  → threshold = 94%  (90% + 0.2 * 20%)
strictness = 1.3  → threshold = 96%  (90% + 0.3 * 20%)
```

**Test Coverage** (evaluate-tests):
```python
# Base threshold: 70%
# Adjusted threshold: 70% + (strictness - 1.0) * 40%

strictness = 1.0  → threshold = 70%
strictness = 1.2  → threshold = 78%  (70% + 0.2 * 40%)
strictness = 1.3  → threshold = 82%  (70% + 0.3 * 40%)
```

**Minimum Test Count** (evaluate-tests):
```python
# Base: 10 tests minimum
# Adjusted: 10 + (strictness - 1.0) * 20

strictness = 1.0  → min_tests = 10
strictness = 1.2  → min_tests = 14  (10 + 0.2 * 20)
strictness = 1.3  → min_tests = 16  (10 + 0.3 * 20)
```

---

## Parameter Passing Mechanism

### Option A: Environment Variable (Simple)
```bash
export GRADING_STRICTNESS=1.285
/skill analyze-code
```

**Pros**: Simple, no SKILL.md changes needed
**Cons**: Not explicit, hard to trace per-student

### Option B: CLI Argument (Explicit)
```bash
/skill analyze-code --strictness=1.285
```

**Pros**: Explicit, traceable
**Cons**: Requires SKILL.md updates, Claude must parse args

### Option C: Prompt-Based (Recommended) ✅
Update SKILL.md instructions:

```markdown
## Instructions

**BEFORE STARTING**: Check if strictness parameter is specified.

If no strictness specified, use default: `strictness = 1.0`

If strictness is specified (e.g., in grading metadata or user prompt):
- Read strictness value
- Apply to all penalty calculations
- Note strictness in final report
```

User invokes:
```
Grade this project with strictness 1.285 (self-grade: 95)
```

**Pros**: Natural language, flexible, no code changes
**Cons**: Relies on Claude parsing user input correctly

---

## Decision: Option C (Prompt-Based)

Use **prompt-based strictness** because:
- ✅ No code changes needed (only SKILL.md updates)
- ✅ Natural language interface
- ✅ Claude excels at parsing structured prompts
- ✅ Easy to test and iterate
- ✅ Maintains skill modularity

---

## Transparency & Reporting

All grading reports must include:

```json
{
  "score": 23.5,
  "max_score": 30,
  "strictness": 1.285,
  "strictness_reason": "Student self-grade: 95/100",
  "penalties_applied": {
    "file_size_violations": -6.5,  // Was -5, scaled by 1.3
    "docstring_coverage": -3.2,    // Was -2.5, scaled by 1.3
    "naming_violations": -0.65     // Was -0.5, scaled by 1.3
  },
  "thresholds_used": {
    "docstring_coverage_required": 0.96,  // Was 0.90, raised by strictness
    "test_coverage_required": 0.82        // Was 0.70, raised by strictness
  }
}
```

---

## Testing Strategy

1. **Baseline Test**: Grade a sample project with strictness=1.0
2. **High Strictness Test**: Grade same project with strictness=1.3
3. **Verify**: Score with strictness=1.3 should be lower (more penalties, higher thresholds)
4. **Edge Case**: Verify strictness=1.0 produces identical results to current grading

---

## Migration Path

**Phase 1**: Update SKILL.md files (no functional changes)
- Add strictness parameter documentation
- Add instructions for applying strictness

**Phase 2**: Test manually
- Grade RamiAutoGrader with strictness=1.0 (baseline)
- Grade RamiAutoGrader with strictness=1.3 (verify differences)

**Phase 3**: Integrate with ExcelRW
- Calculate strictness from self-grade
- Pass to batch-grade-submissions skill
- Include in grading reports

---

## Example: analyze-code with Strictness

**Current SKILL.md (partial):**
```markdown
**Penalty:** -5 points per violation
```

**Updated SKILL.md (partial):**
```markdown
**Strictness Parameter**: If specified, multiply penalties by strictness value.

**Default Penalty (strictness=1.0):** -5 points per violation
**Adjusted Penalty:** -5 × strictness points per violation

Examples:
- strictness=1.0: -5 points
- strictness=1.2: -6 points
- strictness=1.3: -6.5 points
```

---

## Consequences

✅ **Pros:**
- Encourages accurate self-assessment
- Prevents grade inflation
- Fair: students who honestly assess lower grades get standard evaluation
- Fully transparent (strictness value in report)
- Configurable per student

❌ **Cons:**
- Adds complexity to grading logic
- Requires careful testing
- May discourage students from being ambitious (mitigated by transparency)
- Claude must correctly parse and apply strictness in prompts

---

## Alternatives Considered

**Fixed Penalty for High Self-Grades**:
- Pro: Simple
- Con: Not granular, binary approach

**Ignore Self-Grade**:
- Pro: Simpler
- Con: Misses opportunity to validate student judgment

**Use Self-Grade as Baseline**:
- Pro: Intuitive
- Con: Grade inflation, students game the system

---

## Acceptance Criteria

- [ ] All 4 grading skills updated with strictness parameter documentation
- [ ] Penalties scaled by strictness multiplier
- [ ] Thresholds adjusted for higher strictness
- [ ] Strictness value included in grading reports
- [ ] Tested with RamiAutoGrader project (strictness=1.0 vs 1.3)
- [ ] Verified: Higher strictness → lower scores for same project
- [ ] All files remain < 150 lines

---

**Rationale**: Prompt-based strictness provides the best balance of simplicity, flexibility, and maintainability while ensuring transparent, fair grading.
