# Project Tasks & Progress Tracker
# Moodle Assignment Submission Automation System

**Project**: ExcelRW - Moodle Integration for RamiAutoGrader
**Start Date**: 2025-11-27
**Target Completion**: 2 weeks (2025-12-11)
**Status**: 🟡 Planning Complete → Development Starting

---

## Task Status Legend

- 🔴 **Not Started** - Task not begun
- 🟡 **In Progress** - Currently being worked on
- 🟢 **Completed** - Task finished and verified
- ⏸️ **Blocked** - Cannot proceed (waiting on dependency or decision)
- 🔵 **In Review** - Done, awaiting verification/testing

---

## IMPORTANT CLARIFICATIONS (2025-11-27)

**User Requirements Clarified:**

1. **Instructor Access**: Assume instructor-level access to Moodle. Authentication setup will be handled separately.

2. **GitHub Link Extraction**: GitHub URLs are **clickable hyperlinks** in PDFs (not plain text).
   - Use PDF hyperlink extraction (PyPDF2/pikepdf annotations)
   - Fallback to text search only if no hyperlinks found

3. **Self-Grade Extraction**: Self-assigned grades are in PDF (specific field or text).
   - May need additional script/skill to parse this field reliably
   - Note: Higher claimed self-grades → stricter auto-grading evaluation

4. **Moodle API Available**: Confirmed Moodle REST API is available.
   - Prioritize API approach over Selenium
   - API setup steps: Enable web services, create external service, add functions, generate token
   - Use POST requests with token authentication

5. **Adaptive Grading Strictness**: **NEW FEATURE**
   - Higher self-grade claims → more critical evaluation
   - Formula: `strictness = 1.0 + (self_grade / 100) * 0.3`
   - Example: self_grade=95 → strictness=1.285 (28.5% stricter penalties)
   - Configurable via `.env` (GRADING_STRICTNESS_MULTIPLIER)

6. **Folder Naming**: Use **student_name** (not student_id)
   - Format: `Assignments/Assignment_XX/student_John_Doe/`
   - Sanitize names: replace spaces with underscores, remove special characters

**Documentation Updates Applied:**
- ✅ PRD.md: Updated folder structure, added grading strictness feature
- ✅ PLANNING.md: Added ADR-006 (grading strictness), updated ADR-003 (hyperlink extraction), ADR-004 (folder naming)
- ✅ CLAUDE.md: Updated PDF parsing strategy
- ✅ .env.example: Added grading strictness configuration

**Implementation Priorities (Updated 2025-11-27):**

**P0 (Critical - MVP):**
- ✅ Download PDFs from Moodle
- ✅ Extract GitHub URLs from PDF hyperlinks
- ✅ Organize into folder structure

**P1 (Important):**
- Self-grade extraction using Claude/LLM
- Implement strictness parameter in RamiAutoGrader grading skills
- Integration testing

**P2 (Nice to Have):**
- Moodle authentication (can be manual for now)
- Report generation
- Advanced error handling

**Notes:**
- GitHub clone skill: Already exists in RamiAutoGrader (reuse it, no need to rebuild)
- Self-grade extraction: Use Claude Code to read PDF and extract grade (handle unstructured text)
- Name collisions: Not an issue for this use case
- Timeline: No urgency - focus on quality over speed

---

## Progress Overview

| Phase | Tasks | Completed | Progress | Status |
|-------|-------|-----------|----------|--------|
| Phase 1: Planning & Setup | 10 | 10 | 100% | 🟢 Completed |
| **Phase 2A: MVP (P0 Features)** | **8** | **0** | **0%** | 🔴 Not Started |
| Phase 2B: Enhanced Features (P1) | 6 | 0 | 0% | 🔴 Not Started |
| Phase 2C: Moodle Integration (P2) | 5 | 0 | 0% | 🔴 Not Started |
| Phase 3: Integration & Testing | 8 | 0 | 0% | 🔴 Not Started |
| Phase 4: Documentation & Deployment | 6 | 0 | 0% | 🔴 Not Started |
| **TOTAL** | **43** | **10** | **23%** | 🟡 In Progress |

---

## Phase 1: Planning & Setup (100% Complete) ✅

### 1.1 Project Initialization

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P1.1.1 | Create ExcelRW project directory | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed |
| P1.1.2 | Initialize docs/ folder | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed |
| P1.1.3 | Create .gitignore for Assignments/ folder | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - Ignores Assignments/, .env, temp_* |
| P1.1.4 | Set up .env.example with Moodle credentials template | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - Includes strictness config |
| P1.1.5 | Create requirements.txt with dependencies | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - PyPDF2, pikepdf, pdfplumber, etc. |
| P1.1.6 | Create directory structure (src/, tests/, etc.) | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - All directories created |

**Acceptance Criteria (P1.1)**:
- [ ] Directory structure matches CLAUDE.md specification
- [ ] .gitignore excludes Assignments/, .env, *.log
- [ ] .env.example has all required variables with examples

---

### 1.2 Documentation

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P1.2.1 | Complete PRD.md | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - 9 sections, 450 lines |
| P1.2.2 | Complete CLAUDE.md | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - Development guidelines |
| P1.2.3 | Complete PLANNING.md | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - C4 diagrams, 6 ADRs |
| P1.2.4 | Complete TASKS.md | P0 | 🟢 | Claude | 2025-11-27 | ✅ Completed - Updated with clarifications |

**Acceptance Criteria (P1.2)**:
- [x] PRD includes all 9 mandatory sections
- [x] CLAUDE.md has code quality standards, testing requirements
- [ ] PLANNING.md has C4 diagrams (Context, Container, Component)
- [ ] PLANNING.md has 5+ ADRs documenting key decisions
- [ ] TASKS.md has all phases with task breakdown

---

## Phase 2A: MVP - Core Download Functionality (P0 Features) (0% Complete)

**Goal**: Download PDFs from Moodle and extract GitHub URLs (minimum viable product)

### 2A.1 PDF Download & Organization

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2A.1.1 | Create download-pdfs skill structure | P0 | 🔴 | - | TBD | .claude/skills/download-pdfs/ |
| P2A.1.2 | Write SKILL.md for manual PDF download workflow | P0 | 🔴 | - | TBD | Instructions for organizing manually downloaded PDFs |
| P2A.1.3 | Implement organize_folders.py | P0 | 🔴 | - | TBD | Create Assignments/Assignment_XX/student_name/ structure |
| P2A.1.4 | Implement sanitize_names.py | P0 | 🔴 | - | TBD | Convert "John Doe" → "student_John_Doe" |
| P2A.1.5 | Add folder validation checks | P0 | 🔴 | - | TBD | Verify structure matches expected format |

**Acceptance Criteria (P2A.1)**:
- [ ] SKILL.md explains how to manually download PDFs from Moodle
- [ ] organize_folders.py creates correct structure: `Assignments/Assignment_XX/student_name/`
- [ ] Name sanitization handles spaces, special chars, unicode
- [ ] Validates that all expected files exist (submission.pdf)
- [ ] All scripts < 150 lines
- [ ] Docstrings on all functions
- [ ] Unit tests for folder organization

**Estimated Effort**: 3-4 hours

---

### 2A.2 GitHub URL Extraction from PDFs

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2A.2.1 | Create extract-github-urls skill | P0 | 🔴 | - | TBD | .claude/skills/extract-github-urls/ |
| P2A.2.2 | Write SKILL.md for GitHub extraction | P0 | 🔴 | - | TBD | Instructions for batch URL extraction |
| P2A.2.3 | Implement extract_hyperlinks.py | P0 | 🔴 | - | TBD | Extract hyperlinks from PDF annotations (PyPDF2/pikepdf) |
| P2A.2.4 | Implement extract_text_urls.py (fallback) | P0 | 🔴 | - | TBD | Text search for github.com patterns (pdfplumber) |
| P2A.2.5 | Implement url_validator.py | P0 | 🔴 | - | TBD | Validate and normalize GitHub URLs |
| P2A.2.6 | Create metadata writer | P0 | 🔴 | - | TBD | Save student_name, github_url to metadata.json |

**Acceptance Criteria (P2A.2)**:
- [ ] Extracts GitHub URLs from PDF hyperlinks (primary method)
- [ ] Falls back to text search if no hyperlinks found
- [ ] Normalizes URLs (handles github.com, www.github.com, /tree/main, etc.)
- [ ] Validates URL format before saving
- [ ] Saves metadata.json with student_name, github_url, extraction_method
- [ ] Logs PDFs where GitHub URL not found (for manual review)
- [ ] All scripts < 150 lines
- [ ] 90%+ test coverage with sample PDFs

**Estimated Effort**: 5-6 hours

---

### 2A.3 Integration with Existing RamiAutoGrader

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2A.3.1 | Test github-clone skill with ExcelRW metadata | P0 | 🔴 | - | TBD | Verify existing skill works with our folder structure |
| P2A.3.2 | Create batch-grade-submissions skill | P0 | 🔴 | - | TBD | Invoke grade-from-git for all students |

**Acceptance Criteria (P2A.3)**:
- [ ] Existing github-clone skill successfully clones repos to student_name/repo/
- [ ] batch-grade-submissions reads metadata.json and grades all repos
- [ ] Results saved to student_name/grading_results.json

**Estimated Effort**: 2-3 hours

---

## Phase 2B: Enhanced Features (P1 Features) (0% Complete)

**Goal**: Add self-grade extraction and adaptive grading strictness

### 2B.1 Self-Grade Extraction Using Claude

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2B.1.1 | Create extract-self-grades skill | P1 | 🔴 | - | TBD | .claude/skills/extract-self-grades/ |
| P2B.1.2 | Write SKILL.md for LLM-based extraction | P1 | 🔴 | - | TBD | Instructions for Claude to read PDF and extract grade |
| P2B.1.3 | Implement pdf_to_text.py | P1 | 🔴 | - | TBD | Extract full text from PDF for Claude |
| P2B.1.4 | Create self_grade_prompt.txt | P1 | 🔴 | - | TBD | Prompt template for Claude to extract grade |
| P2B.1.5 | Implement grade_extractor.py | P1 | 🔴 | - | TBD | Use Claude API to extract self-grade from text |
| P2B.1.6 | Add validation and fallback | P1 | 🔴 | - | TBD | Validate extracted grade (0-100), handle failures |

**Acceptance Criteria (P2B.1)**:
- [ ] Extracts self-grade from unstructured PDF text using Claude/LLM
- [ ] Handles various formats ("85", "85/100", "I deserve 85", etc.)
- [ ] Validates extracted grade is in range 0-100
- [ ] Flags PDFs where grade cannot be extracted (manual review)
- [ ] Updates metadata.json with self_grade field
- [ ] All scripts < 150 lines
- [ ] Test with sample PDFs with various self-grade formats

**Estimated Effort**: 4-5 hours

---

### 2B.2 Implement Strictness Parameter in RamiAutoGrader

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2B.2.1 | Design strictness parameter interface | P1 | 🔴 | - | TBD | How to pass strictness to grading skills |
| P2B.2.2 | Update analyze-code skill to accept strictness | P1 | 🔴 | - | TBD | Apply stricter penalties based on multiplier |
| P2B.2.3 | Update evaluate-tests skill to accept strictness | P1 | 🔴 | - | TBD | Require higher coverage (e.g., 80% vs 70%) |
| P2B.2.4 | Update check-security skill to accept strictness | P1 | 🔴 | - | TBD | More critical of potential vulnerabilities |
| P2B.2.5 | Update validate-docs skill to accept strictness | P1 | 🔴 | - | TBD | Require more comprehensive documentation |
| P2B.2.6 | Calculate strictness in batch-grade-submissions | P1 | 🔴 | - | TBD | Use formula: 1.0 + (self_grade / 100) * 0.3 |
| P2B.2.7 | Test strictness scaling with sample projects | P1 | 🔴 | - | TBD | Verify higher self-grades → lower scores |

**Acceptance Criteria (P2B.2)**:
- [ ] All grading skills accept optional `strictness` parameter (default: 1.0)
- [ ] Strictness multiplier applied to penalties (e.g., -2 instead of -1 at 1.5x)
- [ ] Test coverage thresholds scale with strictness
- [ ] Strictness value saved to grading_results.json for transparency
- [ ] batch-grade-submissions calculates strictness from self_grade
- [ ] Verified: self_grade=95 results in more critical evaluation than self_grade=70
- [ ] All changes maintain < 150 lines per file

**Estimated Effort**: 6-8 hours

---

## Phase 2C: Moodle Integration (P2 Features) (0% Complete)

**Goal**: Automate Moodle authentication and download (can be deferred)

### 2C.1 Moodle Authentication Skill

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2C.1.1 | Create moodle-authenticate skill structure | P2 | 🔴 | - | TBD | .claude/skills/moodle-authenticate/ |
| P2C.1.2 | Write SKILL.md for moodle-authenticate | P2 | 🔴 | - | TBD | Include prerequisites, parameters, instructions |
| P2C.1.3 | Implement moodle_auth.py (API version) | P2 | 🔴 | - | TBD | Use Moodle Web Services API |
| P2C.1.4 | Implement moodle_auth_selenium.py (fallback) | P2 | 🔴 | - | TBD | Use Selenium for web login |
| P2C.1.5 | Add session caching (save cookies) | P2 | 🔴 | - | TBD | Avoid repeated logins |

**Acceptance Criteria (P2C.1)**:
- [ ] SKILL.md has examples, error handling, success criteria
- [ ] moodle_auth.py successfully authenticates with API token
- [ ] Fallback to Selenium works if API unavailable
- [ ] Session cookies cached to avoid repeated logins
- [ ] All files < 150 lines
- [ ] Docstrings on all functions
- [ ] Unit tests for both API and Selenium paths

**Estimated Effort**: 4-6 hours

**Note**: Can be deferred - manual download is acceptable for MVP

---

## Phase 3: Integration & Testing (0% Complete)

### 3.1 Unit Tests

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P3.1.1 | Test moodle_auth.py (API path) | P0 | 🔴 | - | 2025-12-05 | Mock Moodle API responses |
| P3.1.2 | Test moodle_auth_selenium.py | P1 | 🔴 | - | 2025-12-05 | Use Selenium test fixtures |
| P3.1.3 | Test extract_github_urls.py | P0 | 🔴 | - | 2025-12-06 | Use sample PDF fixtures |
| P3.1.4 | Test organize_folders.py | P0 | 🔴 | - | 2025-12-06 | Verify folder structure created |
| P3.1.5 | Test batch_clone.py | P1 | 🔴 | - | 2025-12-06 | Mock Git clone operations |

**Acceptance Criteria (P3.1)**:
- [ ] All unit tests pass
- [ ] Coverage ≥ 80% for helper scripts
- [ ] Tests use fixtures (sample PDFs, mock Moodle HTML)
- [ ] Tests documented with docstrings

**Estimated Effort**: 4-5 hours

---

### 3.2 Integration Tests

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P3.2.1 | Set up mock Moodle server (Flask) | P0 | 🔴 | - | 2025-12-07 | Simulate Moodle API endpoints |
| P3.2.2 | Test full workflow: auth → download → organize | P0 | 🔴 | - | 2025-12-07 | End-to-end test |
| P3.2.3 | Test with real Moodle (old assignment) | P0 | 🔴 | - | 2025-12-08 | Use past course data |

**Acceptance Criteria (P3.2)**:
- [ ] Mock server returns realistic Moodle responses
- [ ] Full workflow test passes (auth → download → organize)
- [ ] Test with real Moodle completes successfully
- [ ] All downloaded files match expected structure

**Estimated Effort**: 3-4 hours

---

## Phase 4: Documentation & Deployment (0% Complete)

### 4.1 README & User Docs

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P4.1.1 | Write README.md for ExcelRW | P0 | 🔴 | - | 2025-12-09 | Installation, usage, troubleshooting |
| P4.1.2 | Document Moodle setup requirements | P0 | 🔴 | - | 2025-12-09 | API token generation, permissions |
| P4.1.3 | Create usage examples in README | P0 | 🔴 | - | 2025-12-09 | Show skill invocation for each workflow |
| P4.1.4 | Write troubleshooting guide | P1 | 🔴 | - | 2025-12-09 | Common errors and solutions |

**Acceptance Criteria (P4.1)**:
- [ ] README has installation steps (requirements, ChromeDriver, .env setup)
- [ ] README has usage examples for each skill
- [ ] Troubleshooting section covers top 10 errors
- [ ] README includes screenshots/diagrams

**Estimated Effort**: 2-3 hours

---

### 4.2 Prompt Engineering Log

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P4.2.1 | Document architecture decision prompts | P0 | 🔴 | - | 2025-12-10 | prompts/architecture/ (5+ files) |
| P4.2.2 | Document code generation prompts | P0 | 🔴 | - | 2025-12-10 | prompts/code-generation/ (5+ files) |
| P4.2.3 | Document testing prompts | P1 | 🔴 | - | 2025-12-10 | prompts/testing/ (3+ files) |
| P4.2.4 | Write prompts/README.md with lessons learned | P0 | 🔴 | - | 2025-12-10 | Best practices, what worked |

**Acceptance Criteria (P4.2)**:
- [ ] 5+ architecture prompts documented
- [ ] 5+ code generation prompts documented
- [ ] 3+ testing prompts documented
- [ ] prompts/README.md has lessons learned section
- [ ] Each prompt file includes: context, prompt text, output, iterations

**Estimated Effort**: 3-4 hours

---

### 4.3 Final Verification

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P4.3.1 | Verify all files < 150 lines | P0 | 🔴 | - | 2025-12-11 | Run line count check |
| P4.3.2 | Verify test coverage ≥ 70% | P0 | 🔴 | - | 2025-12-11 | pytest --cov=src |
| P4.3.3 | Verify no hardcoded secrets | P0 | 🔴 | - | 2025-12-11 | grep -r "password\|token" |
| P4.3.4 | Verify git history (10-15+ commits) | P0 | 🔴 | - | 2025-12-11 | git log --oneline \| wc -l |
| P4.3.5 | Run full workflow on upcoming assignment | P0 | 🔴 | - | 2025-12-11 | Dry run before real use |

**Acceptance Criteria (P4.3)**:
- [ ] All Python files ≤ 150 lines
- [ ] Test coverage ≥ 70% (target: 80%)
- [ ] No secrets in codebase or git history
- [ ] Git log shows 10-15+ commits with meaningful messages
- [ ] Dry run completes successfully with sample data

**Estimated Effort**: 2-3 hours

---

## Blockers & Issues

| ID | Issue | Blocking Tasks | Status | Resolution | Date |
|----|-------|----------------|--------|------------|------|
| B001 | Moodle API availability unknown | P2.1.3 | 🟡 Open | Contact IT to check if API enabled | 2025-11-27 |
| B002 | Sample PDFs for testing not available | P3.1.3 | 🟡 Open | Use past assignments or generate test PDFs | 2025-11-27 |

**Add new blockers here as they arise**

---

## Daily Progress Log

### 2025-11-27

**Completed**:
- [P1.1.1]: Created ExcelRW project directory structure
- [P1.1.2]: Initialized docs/ folder
- [P1.2.1]: Completed PRD.md (9 sections, 450 lines)
- [P1.2.2]: Completed CLAUDE.md (development guidelines)

**In Progress**:
- [P1.2.3]: Writing PLANNING.md (70% complete - C4 diagrams done, ADRs in progress)
- [P1.2.4]: Writing TASKS.md (this file - 90% complete)

**Blockers**:
- Need to verify Moodle API availability (B001)
- Need sample PDFs for testing (B002)

**Notes**:
- Documentation phase going well, on track for 2-week timeline
- Next: Complete PLANNING.md, then begin skill development tomorrow

---

### [Add new date entries here as work progresses]

**Template**:
```
### YYYY-MM-DD

**Completed**:
- [Task ID]: Brief description

**In Progress**:
- [Task ID]: Current status, % complete

**Blockers**:
- [Blocker ID]: Status update

**Notes**:
- Any important observations or decisions made today
```

---

## Submission Checklist (ISO/IEC 25010 Compliance)

### Functional Suitability
- [ ] Completeness: All features from PRD implemented
- [ ] Correctness: Downloads match expected data (verified with test run)
- [ ] Appropriateness: Fits instructor workflow needs

### Performance Efficiency
- [ ] Time behavior: Downloads 30 students in < 5 minutes
- [ ] Resource utilization: Memory usage < 500 MB
- [ ] Capacity: Handles 100+ students per assignment

### Usability
- [ ] Learnability: Instructor can use after reading README
- [ ] Operability: Skills easy to invoke (clear parameters)
- [ ] Error messages: Clear, actionable
- [ ] Documentation: README is comprehensive user manual

### Reliability
- [ ] Maturity: Tested on 2+ real assignments
- [ ] Fault tolerance: Handles network errors, missing PDFs
- [ ] Recoverability: Can resume failed downloads

### Security
- [ ] Confidentiality: Credentials encrypted, student data local
- [ ] Integrity: Downloaded PDFs match Moodle originals
- [ ] No secrets in code or git history

### Maintainability
- [ ] Modularity: Each skill is independent
- [ ] Analyzability: Code well-documented with docstrings
- [ ] Modifiability: Easy to add new skills
- [ ] Testability: 70%+ test coverage

---

## Timeline Summary

| Week | Focus | Deliverables |
|------|-------|--------------|
| Week 1 (Nov 27 - Dec 3) | Planning + Core Skills | PRD, CLAUDE, PLANNING, TASKS, moodle-authenticate, moodle-download-submissions |
| Week 2 (Dec 4 - Dec 11) | Integration + Testing + Docs | github-clone-repos, tests, README, prompts, final verification |

**Key Milestones**:
- ✅ **Day 1 (Nov 27)**: Documentation complete (PRD, CLAUDE, PLANNING, TASKS)
- 🔴 **Day 3 (Nov 29)**: Authentication skill working
- 🔴 **Day 7 (Dec 3)**: Download skill working end-to-end
- 🔴 **Day 10 (Dec 6)**: All tests passing
- 🔴 **Day 14 (Dec 11)**: Production-ready, dry run complete

---

## Risk Register

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Moodle API disabled | Medium | High | Implement Selenium fallback | Developer |
| PDF format changes | Low | Medium | Multi-library parsing strategy | Developer |
| Network unreliable | Low | Medium | Retry logic, checkpointing | Developer |
| Students submit wrong format | High | Low | Validation, clear error messages | Instructor |
| Timeline slips | Medium | Medium | Prioritize P0 tasks, cut P2 features if needed | Developer |

---

**Next Steps** (for tomorrow, 2025-11-28):
1. Complete PLANNING.md (finish ADRs)
2. Create .gitignore for Assignments/
3. Create .env.example
4. Begin moodle-authenticate skill (P2.1.1)

**Status**: 📝 Planning phase 50% complete, ready to begin development!
