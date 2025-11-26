---
name: validate-docs
description: Validates project documentation including PRD, README, PLANNING, TASKS, and architecture docs
version: 1.0.0
---

# Documentation Validation Skill

Evaluates documentation quality in academic software projects by checking:
- Required documents presence (PRD, README, PLANNING, TASKS)
- Document structure and completeness
- README quality and usability
- Architecture documentation

**Scoring:** 25 points maximum (critical for academic projects)

## Instructions

### 1. Check Required Documents

Use Glob to find required documentation files:

**Required Documents (Root Directory):**
- `PRD.md` - Product Requirements Document
- `README.md` - User manual and project overview
- `PLANNING.md` - Project planning and design
- `TASKS.md` - Task breakdown and tracking
- `CLAUDE.md` (optional) - Claude Code guidelines

**Required Architecture Docs (docs/ directory):**
- `docs/ARCHITECTURE.md` or similar C4 diagrams
- ADRs (Architecture Decision Records) in `docs/ADRs/`

```bash
# Check for required files
ls PRD.md README.md PLANNING.md TASKS.md CLAUDE.md

# Check for architecture docs
ls docs/ARCHITECTURE.md
ls docs/ADRs/
```

**Scoring:**
- Each missing document: -5 points
- Missing architecture docs: -3 points

### 2. Validate README.md Quality

The README is the most important document for usability. Check for:

**Required Sections:**
- Project title and description
- Installation instructions
- Usage examples
- Dependencies/Requirements
- Configuration guide
- Troubleshooting (optional but recommended)

**Quality Checks:**
- Has code examples/snippets
- Has clear formatting (headers, lists, code blocks)
- Minimum 300 words (brief READMEs are insufficient)
- No broken links (if any links present)

**Use Python helper:**
```bash
python src/validators/readme_validator.py <project_path>
```

The validator will:
1. Read README.md
2. Extract sections (H1, H2, H3 headers)
3. Check for code blocks
4. Count words
5. Validate completeness

**Scoring:**
- Missing README: -10 points (critical)
- Incomplete README (< 3 sections): -5 points
- No code examples: -2 points

### 3. Validate PRD.md Structure

The PRD should contain comprehensive requirements analysis:

**Required Sections:**
- **Problem Statement** - What problem does the project solve?
- **Functional Requirements** - Detailed feature list
- **Non-Functional Requirements** - Performance, security, usability
- **Success Metrics** - How to measure project success
- **Technical Constraints** - Limitations and boundaries

Use Grep to check for section headers:
```bash
grep -i "## Problem Statement" PRD.md
grep -i "## Functional Requirements" PRD.md
grep -i "## Non-Functional Requirements" PRD.md
grep -i "## Success Metrics" PRD.md
```

**Scoring:**
- Missing PRD: -5 points
- Missing key sections: -1 point per section

### 4. Validate PLANNING.md

Should contain project planning and design decisions:

**Expected Content:**
- Architecture diagrams (C4 Model: Context, Container, Component)
- Technology stack decisions
- Implementation phases
- Risk analysis (optional)

Use Read to check content:
```bash
# Read PLANNING.md and check for diagrams
grep -i "```mermaid" PLANNING.md || grep -i "```plantuml" PLANNING.md

# Check for C4 mentions
grep -i "C4\|context diagram\|container diagram\|component diagram" PLANNING.md
```

**Scoring:**
- Missing PLANNING.md: -3 points
- No architecture diagrams: -2 points

### 5. Validate TASKS.md

Should contain task breakdown with:

**Required Elements:**
- Hierarchical task structure (phases, sub-tasks)
- Task dependencies documented
- Acceptance criteria for each task
- Progress tracking (checkboxes)

Use Read and Grep:
```bash
# Check for task checkboxes
grep "\- \[ \]\|\- \[x\]" TASKS.md | wc -l

# Check for acceptance criteria mentions
grep -i "acceptance" TASKS.md | wc -l
```

**Scoring:**
- Missing TASKS.md: -3 points
- Fewer than 20 tasks: -2 points (insufficient breakdown)
- No acceptance criteria: -1 point

### 6. Use Python Helper for Complete Analysis

For comprehensive validation, run the document checker:

```bash
python src/analyzers/documentation_checker.py <project_path>
```

This will:
1. Check all required documents
2. Validate README structure
3. Analyze PRD completeness
4. Verify architecture documentation
5. Calculate documentation score

### 7. Calculate Documentation Score

**Scoring Formula:**
```
Base Score: 25 points

Deductions:
- Missing README: -10 points
- Missing PRD: -5 points
- Missing PLANNING.md: -3 points
- Missing TASKS.md: -3 points
- Missing architecture docs: -3 points
- Incomplete README: -5 points
- Missing PRD sections: -1 point each
- No code examples in README: -2 points

Final Score: max(0, min(Base Score - Deductions, 25))
```

**Passing Threshold:** 17.5/25 (70%)

### 8. Generate Report

Output a structured report:

```json
{
  "score": 20.0,
  "max_score": 25,
  "passed": true,
  "details": {
    "required_docs": {
      "readme": {"present": true, "score": 4, "issues": []},
      "prd": {"present": true, "score": 5, "issues": ["Missing 'Success Metrics' section"]},
      "planning": {"present": true, "score": 3, "issues": []},
      "tasks": {"present": true, "score": 3, "issues": []},
      "architecture": {"present": true, "score": 3, "issues": []}
    },
    "readme_analysis": {
      "sections": 6,
      "has_code_examples": true,
      "word_count": 842,
      "quality": "good"
    },
    "missing_documents": [],
    "recommendations": [
      "Add 'Success Metrics' section to PRD.md",
      "Consider adding troubleshooting section to README.md"
    ]
  }
}
```

## Example Usage

```bash
# Run the documentation validation skill
/skill validate-docs

# When prompted, provide project path
/path/to/student/project
```

## Python Helpers Available

1. **documentation_checker.py** - Complete documentation analysis
   ```bash
   python src/analyzers/documentation_checker.py <path>
   ```

2. **readme_validator.py** - Detailed README analysis
   ```bash
   python src/validators/readme_validator.py <path>
   ```

3. **document_validator.py** - Check required documents
   ```bash
   python src/validators/document_validator.py <path>
   ```

4. **markdown_utils.py** - Parse markdown structure
   ```bash
   python src/utils/markdown_utils.py <file>
   ```

## Success Criteria

- ✅ All required documents present
- ✅ README has all essential sections
- ✅ PRD contains comprehensive requirements
- ✅ PLANNING.md has architecture diagrams
- ✅ TASKS.md has detailed task breakdown
- ✅ Score ≥ 17.5/25 to pass

## Common Issues

1. **README too brief** - Often just a title and one paragraph
2. **No code examples** - Critical for usability
3. **Missing PRD** - Students skip requirements analysis
4. **TASKS.md too high-level** - Not enough detail
5. **No architecture diagrams** - Planning lacks visual structure

## Recommendations Format

Provide actionable feedback:
```
[+] Documentation Issues Found:

    1. README.md (4/4 points):
       ✓ All required sections present
       ✓ Has code examples
       ✓ Well-formatted and comprehensive

    2. PRD.md (4/5 points):
       ⚠ Missing section: "Success Metrics"

       Add a section defining how to measure project success:
       ## Success Metrics
       - User satisfaction: >4.5/5 average rating
       - Grading accuracy: ≥90% agreement with human graders
       - Performance: <30 seconds per project

    3. PLANNING.md (3/3 points):
       ✓ Contains architecture diagrams
       ✓ Covers technology stack decisions

    4. TASKS.md (3/3 points):
       ✓ Comprehensive task breakdown (87 tasks)
       ✓ Clear acceptance criteria

    5. Architecture Documentation (3/3 points):
       ✓ docs/ARCHITECTURE.md present
       ✓ ADRs documented

    Final Score: 20/25 (80%) - PASSED
```
