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

---

## Progress Overview

| Phase | Tasks | Completed | Progress | Status |
|-------|-------|-----------|----------|--------|
| Phase 1: Planning & Setup | 10 | 10 | 100% | 🟢 Completed |
| Phase 2: Core Skills Development | 12 | 0 | 0% | 🔴 Not Started |
| Phase 3: Integration & Testing | 8 | 0 | 0% | 🔴 Not Started |
| Phase 4: Documentation & Deployment | 6 | 0 | 0% | 🔴 Not Started |
| **TOTAL** | **36** | **10** | **28%** | 🟡 In Progress |

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

## Phase 2: Core Skills Development (0% Complete)

### 2.1 Authentication Skill

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2.1.1 | Create moodle-authenticate skill structure | P0 | 🔴 | - | 2025-11-28 | .claude/skills/moodle-authenticate/ |
| P2.1.2 | Write SKILL.md for moodle-authenticate | P0 | 🔴 | - | 2025-11-28 | Include prerequisites, parameters, instructions |
| P2.1.3 | Implement moodle_auth.py (API version) | P0 | 🔴 | - | 2025-11-28 | Use Moodle Web Services API |
| P2.1.4 | Implement moodle_auth_selenium.py (fallback) | P1 | 🔴 | - | 2025-11-29 | Use Selenium for web login |
| P2.1.5 | Add session caching (save cookies) | P2 | 🔴 | - | 2025-11-29 | Avoid repeated logins |

**Acceptance Criteria (P2.1)**:
- [ ] SKILL.md has examples, error handling, success criteria
- [ ] moodle_auth.py successfully authenticates with API token
- [ ] Fallback to Selenium works if API unavailable
- [ ] Session cookies cached to avoid repeated logins
- [ ] All files < 150 lines
- [ ] Docstrings on all functions
- [ ] Unit tests for both API and Selenium paths

**Estimated Effort**: 4-6 hours

---

### 2.2 Download Submissions Skill

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2.2.1 | Create moodle-download-submissions skill | P0 | 🔴 | - | 2025-11-30 | .claude/skills/moodle-download-submissions/ |
| P2.2.2 | Write SKILL.md for download workflow | P0 | 🔴 | - | 2025-11-30 | Orchestration instructions for Claude |
| P2.2.3 | Implement download_pdfs.py | P0 | 🔴 | - | 2025-12-01 | Fetch PDFs from Moodle |
| P2.2.4 | Implement extract_github_urls.py | P0 | 🔴 | - | 2025-12-01 | Parse GitHub URLs from PDFs |
| P2.2.5 | Implement organize_folders.py | P0 | 🔴 | - | 2025-12-01 | Create Assignments/Assignment_XX/ structure |
| P2.2.6 | Add concurrent download support | P1 | 🔴 | - | 2025-12-02 | ThreadPoolExecutor, max 5 concurrent |
| P2.2.7 | Add retry logic with exponential backoff | P0 | 🔴 | - | 2025-12-02 | 3 retries, 1s → 2s → 4s |

**Acceptance Criteria (P2.2)**:
- [ ] Downloads all PDFs for a given assignment number
- [ ] Creates folder structure: `Assignments/Assignment_XX/student_YYYY/`
- [ ] Extracts GitHub URL from each PDF
- [ ] Saves metadata.json with student_id, github_url, self_grade
- [ ] Generates download_report.txt summary
- [ ] Handles errors gracefully (missing PDF, network timeout)
- [ ] All helper scripts < 150 lines each
- [ ] 90%+ test coverage

**Estimated Effort**: 8-10 hours

---

### 2.3 GitHub Clone Skill

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2.3.1 | Create github-clone-repos skill | P1 | 🔴 | - | 2025-12-03 | .claude/skills/github-clone-repos/ |
| P2.3.2 | Write SKILL.md for batch cloning | P1 | 🔴 | - | 2025-12-03 | Instructions for cloning all student repos |
| P2.3.3 | Implement batch_clone.py | P1 | 🔴 | - | 2025-12-03 | Clone repos to student_YYYY/repo/ |
| P2.3.4 | Add shallow clone optimization | P2 | 🔴 | - | 2025-12-04 | --depth 1 for speed |
| P2.3.5 | Handle private repos (GitHub token) | P2 | 🔴 | - | 2025-12-04 | Use GITHUB_TOKEN from .env |

**Acceptance Criteria (P2.3)**:
- [ ] Clones all GitHub repos from metadata.json
- [ ] Repos saved to correct student folders
- [ ] Handles clone failures gracefully (repo doesn't exist, private)
- [ ] Uses shallow clone for speed
- [ ] All code < 150 lines
- [ ] Unit tests with mock Git

**Estimated Effort**: 3-4 hours

---

### 2.4 Report Generation Skill

| ID | Task | Priority | Status | Assignee | Due Date | Notes |
|----|------|----------|--------|----------|----------|-------|
| P2.4.1 | Create generate-submission-report skill | P1 | 🔴 | - | 2025-12-04 | .claude/skills/generate-submission-report/ |
| P2.4.2 | Write SKILL.md for reporting | P1 | 🔴 | - | 2025-12-04 | Generate summary of downloads |
| P2.4.3 | Create report_template.md | P1 | 🔴 | - | 2025-12-04 | Markdown template for reports |
| P2.4.4 | Implement report generation logic | P1 | 🔴 | - | 2025-12-05 | Read metadata, format report |

**Acceptance Criteria (P2.4)**:
- [ ] Generates markdown report with download statistics
- [ ] Includes student count, success rate, errors, warnings
- [ ] Lists students with missing GitHub URLs
- [ ] Lists students with download failures
- [ ] Saved to `Assignments/Assignment_XX/download_report.md`

**Estimated Effort**: 2-3 hours

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
