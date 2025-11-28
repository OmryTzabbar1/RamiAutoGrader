# TASKS.md - ExcelFeedback Task Breakdown

## Project Overview

**ExcelFeedback** is a Claude Code agent that generates instructor-facing Excel feedback sheets after RamiAutoGrader completes grading. This task list tracks all implementation tasks organized by priority and phase.

**Implementation Approach**: Agent-based orchestration (NOT Python script)

---

## Task Status Legend

| Symbol | Status | Description |
|--------|--------|-------------|
| 🔴 | Not Started | Task not yet begun |
| 🟡 | In Progress | Currently being worked on |
| 🟢 | Completed | Task finished and tested |
| ⏸️ | Blocked | Waiting on dependency |
| ⚠️ | Needs Review | Complete but requires validation |

---

## Phase Overview

| Phase | Description | Tasks | Estimated Time | Status |
|-------|-------------|-------|----------------|--------|
| **Phase 0** | Documentation & Planning | 4 | 2-3 hours | 🟢 Completed |
| **Phase 1** | Skill Development | 12 | 6-8 hours | 🔴 Not Started |
| **Phase 2** | Agent Development | 8 | 4-6 hours | 🔴 Not Started |
| **Phase 3** | Integration & Testing | 7 | 3-4 hours | 🔴 Not Started |
| **Phase 4** | Documentation & Finalization | 3 | 1-2 hours | 🔴 Not Started |

**Total Tasks**: 34
**Total Estimated Time**: 16-23 hours

---

## Phase 0: Documentation & Planning (2-3 hours)

**Goal**: Create complete project documentation before implementation

| ID | Task | Status | Time | Notes |
|----|------|--------|------|-------|
| P0.1 | Write PRD.md with requirements and architecture | 🟢 | 1h | Complete |
| P0.2 | Write CLAUDE.md with development guidelines | 🟢 | 0.5h | Complete |
| P0.3 | Write PLANNING.md with C4 diagrams and ADRs | 🟢 | 1h | Complete |
| P0.4 | Write TASKS.md with task breakdown | 🟢 | 0.5h | This file |

**Phase 0 Progress**: 4/4 tasks completed (100%)
**Phase 0 Status**: ✅ Complete

---

## Phase 1: Skill Development (6-8 hours)

**Goal**: Implement the 3 core skills (extract-pdf-metadata, generate-summary, populate-excel)

### 1.1 Skill: extract-pdf-metadata (2-3 hours)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P1.1.1 | Create skill directory structure | 🔴 | 0.25h | None | `skills/extract-pdf-metadata/` |
| P1.1.2 | Write SKILL.md with instructions | 🔴 | 0.5h | P1.1.1 | Detailed Claude instructions |
| P1.1.3 | Create skill.json manifest | 🔴 | 0.25h | P1.1.1 | Define inputs/outputs |
| P1.1.4 | Implement PDF text extraction (pdfplumber) | 🔴 | 0.5h | P1.1.3 | Handle corrupted PDFs |
| P1.1.5 | Implement Claude API client for metadata extraction | 🔴 | 1h | P1.1.4 | Structured prompt, JSON parsing |
| P1.1.6 | Implement confidence scoring logic | 🔴 | 0.5h | P1.1.5 | Score 0.0-1.0 |
| P1.1.7 | Write unit tests for PDF extraction | 🔴 | 0.5h | P1.1.4 | Test valid/corrupted PDFs |
| P1.1.8 | Write unit tests for Claude API integration | 🔴 | 0.5h | P1.1.5 | Mock API responses |
| P1.1.9 | Write unit tests for confidence scoring | 🔴 | 0.25h | P1.1.6 | Edge cases |

**Subtask Progress**: 0/9 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ Skill extracts student_id, student_name, partner_name, assignment_name from PDF
- ✅ Returns JSON with all fields (or "NOT_FOUND" for missing)
- ✅ Confidence score calculated correctly (0.0-1.0)
- ✅ Handles missing PDFs gracefully (returns FILE_NOT_FOUND status)
- ✅ Handles Claude API failures gracefully (retries 3×)
- ✅ Unit tests cover 90%+ of code
- ✅ All files under 150 lines

---

### 1.2 Skill: generate-summary (1-2 hours)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P1.2.1 | Create skill directory structure | 🔴 | 0.25h | None | `skills/generate-summary/` |
| P1.2.2 | Write SKILL.md with instructions | 🔴 | 0.5h | P1.2.1 | Summary prompt template |
| P1.2.3 | Create skill.json manifest | 🔴 | 0.25h | P1.2.1 | Define inputs/outputs |
| P1.2.4 | Implement grading report JSON parser | 🔴 | 0.5h | P1.2.3 | Extract scores, violations |
| P1.2.5 | Implement Claude API client for summarization | 🔴 | 0.75h | P1.2.4 | Structured prompt, 30-50 words |
| P1.2.6 | Implement summary validator (word count, format) | 🔴 | 0.25h | P1.2.5 | Ensure professional tone |
| P1.2.7 | Write unit tests for JSON parsing | 🔴 | 0.25h | P1.2.4 | Test edge cases |
| P1.2.8 | Write unit tests for Claude API integration | 🔴 | 0.5h | P1.2.5 | Mock API responses |

**Subtask Progress**: 0/8 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ Skill generates 2-3 sentence summary from grading_results.json
- ✅ Summary starts with score (e.g., "Score: 77/100")
- ✅ Summary mentions main strengths and improvement areas
- ✅ Summary length: 30-50 words (strict enforcement)
- ✅ Professional but encouraging tone
- ✅ Handles edge cases (0/100 score, 100/100 score)
- ✅ Unit tests cover 85%+ of code
- ✅ All files under 150 lines

---

### 1.3 Skill: populate-excel (2-3 hours)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P1.3.1 | Create skill directory structure | 🔴 | 0.25h | None | `skills/populate-excel/` |
| P1.3.2 | Write SKILL.md with instructions | 🔴 | 0.5h | P1.3.1 | Excel format specs |
| P1.3.3 | Create skill.json manifest | 🔴 | 0.25h | P1.3.1 | Define inputs/outputs |
| P1.3.4 | Implement data aggregator (merge metadata + results) | 🔴 | 0.5h | P1.3.3 | Combine all data sources |
| P1.3.5 | Implement Excel workbook creation (openpyxl) | 🔴 | 1h | P1.3.4 | Headers, rows, formulas |
| P1.3.6 | Implement Excel formatting (styles, borders, widths) | 🔴 | 1h | P1.3.5 | Colors, fonts, wrapping |
| P1.3.7 | Implement hyperlink formula for GitHub URLs | 🔴 | 0.5h | P1.3.5 | `=HYPERLINK(url, "Link")` |
| P1.3.8 | Write unit tests for data aggregation | 🔴 | 0.25h | P1.3.4 | Test merging logic |
| P1.3.9 | Write unit tests for Excel generation | 🔴 | 0.5h | P1.3.5 | Verify row/column structure |
| P1.3.10 | Write unit tests for Excel formatting | 🔴 | 0.5h | P1.3.6 | Verify styles applied |

**Subtask Progress**: 0/10 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ Skill creates Excel file with 8 columns (Student ID, Name, Partner, Assignment, GitHub URL, Grade, Summary, Notes)
- ✅ Header row: Bold, light blue background (#D9E1F2), centered
- ✅ Borders: Thin borders on all cells
- ✅ Column widths: Auto-adjusted (Student ID: 12, Summary: 60)
- ✅ Text wrapping: Enabled for Summary column
- ✅ GitHub URL: Clickable hyperlink (formula)
- ✅ Handles 1-100 students correctly
- ✅ Unit tests cover 90%+ of code
- ✅ All files under 150 lines

---

## Phase 2: Agent Development (4-6 hours)

**Goal**: Implement the excel-feedback-generator agent that orchestrates the 3 skills

### 2.1 Agent Configuration (1-2 hours)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P2.1.1 | Create agent directory structure | 🔴 | 0.25h | Phase 1 complete | `agents/excel-feedback-generator/` |
| P2.1.2 | Write agent.yaml configuration | 🔴 | 1h | P2.1.1 | Define workflow steps |
| P2.1.3 | Document agent workflow in README.md | 🔴 | 0.5h | P2.1.2 | Usage examples |
| P2.1.4 | Create config/agent_config.yaml | 🔴 | 0.5h | P2.1.2 | Timeouts, retries |

**Subtask Progress**: 0/4 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ agent.yaml defines workflow with 3 steps (extract, summarize, populate)
- ✅ For-each loop for extract and summarize (per student)
- ✅ Error handling strategies documented
- ✅ Timeout configurations set (30s per student for extract, 20s for summary)
- ✅ Retry policy defined (3× with exponential backoff)

---

### 2.2 Agent Integration (1-2 hours)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P2.2.1 | Modify RamiAutoGrader agent.yaml | 🔴 | 0.5h | P2.1.4 | Add post_grading_steps |
| P2.2.2 | Implement data passing (results_dir → agent) | 🔴 | 0.5h | P2.2.1 | Input mapping |
| P2.2.3 | Test agent orchestration (mock skills) | 🔴 | 0.5h | P2.2.2 | Verify workflow runs |
| P2.2.4 | Test error handling (skill failure scenarios) | 🔴 | 0.5h | P2.2.3 | Verify retries work |

**Subtask Progress**: 0/4 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ RamiAutoGrader agent triggers ExcelFeedback after grading
- ✅ Data passed correctly (grading_results_dir, pdf_dir, assignment_name)
- ✅ Agent orchestration works with mock skills
- ✅ Error handling tested (API failure, skill timeout)
- ✅ Post-grading hook does NOT fail entire grading if Excel generation fails

---

## Phase 3: Integration & Testing (3-4 hours)

**Goal**: Test full workflow with real data and validate output

### 3.1 Integration Testing (1-2 hours)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P3.1.1 | Create test fixtures (sample PDFs, grading results) | 🔴 | 0.5h | None | 3 students, various scenarios |
| P3.1.2 | Write integration test: Full workflow (3 students) | 🔴 | 0.5h | P3.1.1, Phase 2 | All valid data |
| P3.1.3 | Write integration test: 1 student with missing PDF | 🔴 | 0.25h | P3.1.1 | Verify flagging works |
| P3.1.4 | Write integration test: 1 student with low confidence | 🔴 | 0.25h | P3.1.1 | Verify manual review flag |
| P3.1.5 | Write integration test: Claude API retry on failure | 🔴 | 0.5h | P3.1.1 | Mock API error |

**Subtask Progress**: 0/5 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ Integration test passes with 3 valid students
- ✅ Excel file created with correct data
- ✅ Missing PDF flagged correctly (Notes: "PDF_MISSING")
- ✅ Low confidence extraction flagged (Notes: "LOW_CONFIDENCE_REVIEW")
- ✅ Claude API retry works (3× with backoff)

---

### 3.2 End-to-End Testing (1-2 hours)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P3.2.1 | Run RamiAutoGrader on sample project | 🔴 | 0.5h | P3.1.5 | Generate real grading results |
| P3.2.2 | Verify ExcelFeedback triggered automatically | 🔴 | 0.25h | P3.2.1 | Check post-grading hook |
| P3.2.3 | Manually validate Excel output (open in Excel) | 🔴 | 0.5h | P3.2.2 | Check formatting, hyperlinks |
| P3.2.4 | Test with 10+ students (performance test) | 🔴 | 0.5h | P3.2.3 | Verify <5 min completion |

**Subtask Progress**: 0/4 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ ExcelFeedback triggered automatically after grading
- ✅ Excel file opens correctly in Microsoft Excel
- ✅ Hyperlinks are clickable
- ✅ Text is readable (no truncation)
- ✅ 10 students processed in <5 minutes
- ✅ Instructor can sort/filter data

---

## Phase 4: Documentation & Finalization (1-2 hours)

**Goal**: Complete documentation and prepare for deployment

### 4.1 Documentation (0.5-1 hour)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P4.1.1 | Write README.md for ExcelFeedback project | 🔴 | 0.5h | Phase 3 complete | Installation, usage, examples |
| P4.1.2 | Update RamiAutoGrader README with ExcelFeedback | 🔴 | 0.25h | P4.1.1 | Document integration |
| P4.1.3 | Create .env.example file | 🔴 | 0.25h | None | ANTHROPIC_API_KEY, config |

**Subtask Progress**: 0/3 tasks completed
**Subtask Status**: 🔴 Not Started

**Acceptance Criteria**:
- ✅ README.md complete with installation steps
- ✅ Usage examples provided (how to trigger agent)
- ✅ .env.example created with all required variables
- ✅ RamiAutoGrader README updated with integration info

---

### 4.2 Code Quality & Review (0.5-1 hour)

| ID | Task | Status | Time | Dependencies | Notes |
|----|------|--------|------|--------------|-------|
| P4.2.1 | Run code quality checks (lint, type check) | ⏸️ | 0.25h | All code complete | flake8, mypy |
| P4.2.2 | Verify all files under 150 lines | ⏸️ | 0.25h | All code complete | Check file sizes |
| P4.2.3 | Verify test coverage ≥70% | ⏸️ | 0.25h | All tests written | pytest --cov |
| P4.2.4 | Refactor any oversized files | ⏸️ | 0.5h | P4.2.2 | Split if needed |

**Subtask Progress**: 0/4 tasks completed
**Subtask Status**: ⏸️ Blocked (waiting on code completion)

**Acceptance Criteria**:
- ✅ All files under 150 lines
- ✅ No linting errors (flake8)
- ✅ Type checking passes (mypy)
- ✅ Test coverage ≥70% overall, ≥90% for critical paths
- ✅ All tests passing

---

## Git Commit Tracking

**Required**: 15-20+ commits showing clear development progression

**Recommended Commit Progression**:

| Commit # | Type | Scope | Message | Task ID |
|----------|------|-------|---------|---------|
| 1 | docs | project | Create PRD, CLAUDE, PLANNING, TASKS docs | P0.1-P0.4 |
| 2 | feat | skills | Add extract-pdf-metadata skill stub | P1.1.1-P1.1.3 |
| 3 | feat | skills | Implement PDF text extraction (pdfplumber) | P1.1.4 |
| 4 | feat | skills | Implement Claude API metadata extraction | P1.1.5 |
| 5 | feat | skills | Add confidence scoring logic | P1.1.6 |
| 6 | test | skills | Add unit tests for extract-pdf-metadata | P1.1.7-P1.1.9 |
| 7 | feat | skills | Add generate-summary skill stub | P1.2.1-P1.2.3 |
| 8 | feat | skills | Implement Claude API summarization | P1.2.4-P1.2.5 |
| 9 | feat | skills | Add summary validator (word count) | P1.2.6 |
| 10 | test | skills | Add unit tests for generate-summary | P1.2.7-P1.2.8 |
| 11 | feat | skills | Add populate-excel skill stub | P1.3.1-P1.3.3 |
| 12 | feat | skills | Implement data aggregator | P1.3.4 |
| 13 | feat | skills | Implement Excel workbook creation | P1.3.5 |
| 14 | feat | skills | Implement Excel formatting (styles, borders) | P1.3.6 |
| 15 | feat | skills | Add hyperlink formula for GitHub URLs | P1.3.7 |
| 16 | test | skills | Add unit tests for populate-excel | P1.3.8-P1.3.10 |
| 17 | feat | agent | Create agent configuration (agent.yaml) | P2.1.1-P2.1.2 |
| 18 | docs | agent | Document agent workflow in README | P2.1.3-P2.1.4 |
| 19 | feat | integration | Add post-grading hook to RamiAutoGrader | P2.2.1-P2.2.2 |
| 20 | test | integration | Add integration tests for agent workflow | P3.1.1-P3.1.5 |
| 21 | test | e2e | Add end-to-end test with RamiAutoGrader | P3.2.1-P3.2.4 |
| 22 | docs | project | Write README.md and .env.example | P4.1.1-P4.1.3 |
| 23 | refactor | code | Refactor oversized files if needed | P4.2.4 |
| 24 | chore | project | Final code quality checks and cleanup | P4.2.1-P4.2.3 |

**Commit Message Format**:
```
<type>(<scope>): <short description> [TASK-ID]

<optional longer description>
```

**Types**: feat, fix, docs, test, refactor, chore

---

## Daily Progress Log

### 2025-11-28 (Session Start)

**Tasks Completed**:
- ✅ P0.1: Created PRD.md (500+ lines)
- ✅ P0.2: Created CLAUDE.md (600+ lines)
- ✅ P0.3: Created PLANNING.md (700+ lines)
- ✅ P0.4: Created TASKS.md (this file)

**Phase 0 Status**: 🟢 Complete (4/4 tasks)

**Next Steps**:
- Begin Phase 1: Skill Development
- Start with P1.1: extract-pdf-metadata skill

**Blockers**: None

**Notes**:
- All documentation complete before implementation (best practice)
- Ready to start coding Phase 1

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Claude API rate limits (50 req/min) | Medium | Medium | Implement exponential backoff, batch processing |
| PDF format variations | High | High | Use LLM extraction (flexible), confidence scoring |
| Low extraction accuracy | Medium | Low | Manual review workflow for low-confidence extractions |
| Excel formatting issues | Low | Low | Extensive testing with Microsoft Excel |
| Agent orchestration complexity | Medium | Medium | Start with simple workflow, add error handling incrementally |

---

## Dependencies

### External Dependencies

| Dependency | Version | Purpose | Installation |
|------------|---------|---------|--------------|
| anthropic | ≥0.40.0 | Claude API client | `pip install anthropic` |
| pdfplumber | ≥0.10.0 | PDF text extraction | `pip install pdfplumber` |
| openpyxl | ≥3.1.0 | Excel generation | `pip install openpyxl` |
| pytest | ≥7.0.0 | Testing framework | `pip install pytest` |
| python-dotenv | ≥1.0.0 | Environment variables | `pip install python-dotenv` |

### Internal Dependencies

| Component | Depends On | Type |
|-----------|-----------|------|
| generate-summary skill | extract-pdf-metadata skill | Sequential (per student) |
| populate-excel skill | Both other skills | Sequential (after all students) |
| Agent | All 3 skills | Orchestration |
| Integration tests | Agent + Skills | Testing |

---

## Success Criteria (Final Checklist)

### Functional Requirements
- [ ] All 3 skills implemented (extract-pdf-metadata, generate-summary, populate-excel)
- [ ] Agent orchestration working (agent.yaml)
- [ ] Integration with RamiAutoGrader (post-grading hook)
- [ ] Excel file generated with correct format (8 columns, formatting)
- [ ] Metadata extraction ≥80% accuracy (confidence ≥ 0.7)
- [ ] Summaries generated for all students (30-50 words each)
- [ ] Manual review flags set correctly (low confidence, errors)

### Quality Requirements
- [ ] All files under 150 lines
- [ ] Docstrings on all functions/classes/modules
- [ ] No hardcoded secrets or paths
- [ ] 70%+ overall test coverage
- [ ] 90%+ test coverage for critical paths (skills)
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] E2E test passes

### Git & Version Control
- [ ] 15-20+ commits with clear progression
- [ ] Commit messages follow format: `<type>(<scope>): <description> [TASK-ID]`
- [ ] Commits reference task IDs from TASKS.md
- [ ] Clean, meaningful development history

### Documentation
- [ ] README.md complete (installation, usage, examples)
- [ ] All SKILL.md files comprehensive
- [ ] Agent workflow documented (agent.yaml + README)
- [ ] .env.example created
- [ ] RamiAutoGrader README updated with integration info

### Performance
- [ ] Process 30 students in <5 minutes
- [ ] Claude API success rate ≥95%
- [ ] No memory leaks or resource exhaustion

### User Experience
- [ ] Excel file opens correctly in Microsoft Excel
- [ ] Hyperlinks are clickable
- [ ] Text is readable (no truncation)
- [ ] Instructor can sort/filter data
- [ ] Flagged records clearly visible in "Notes" column

---

## Notes for Future Phases

### Phase 5: Enhancements (Post-MVP)

**Potential Tasks**:
- Conditional formatting (red for low grades, green for high)
- Summary chart showing grade distribution
- Multi-sheet support (different assignment types)
- Email integration (auto-email feedback to students)
- Historical tracking (grades across multiple assignments)

**Estimated Time**: 8-12 hours

**Priority**: Low (after core functionality stable)

---

**End of TASKS.md**

This task list provides a comprehensive roadmap for implementing the ExcelFeedback agent. All tasks are organized by phase, with clear dependencies, time estimates, and acceptance criteria. Update task statuses as work progresses!
