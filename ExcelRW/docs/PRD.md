# Product Requirements Document (PRD)
# Moodle Assignment Submission Automation System

## 1. Project Overview & Background

**Project Name**: Moodle Assignment Submission Automation System
**Version**: 1.0
**Date**: 2025-11-27
**Author**: M.Sc. Computer Science - Course Instructor
**Parent Project**: RamiAutoGrader (Academic Software Auto-Grader System)

### 1.1 Problem Statement

Instructors teaching M.Sc. Computer Science courses face significant manual overhead when collecting and organizing student assignment submissions from Moodle. Currently, instructors must:
- Manually download each student's PDF submission
- Extract GitHub repository links from PDFs or submission forms
- Create folder structures manually for 12 assignments
- Copy student self-assessment grades
- Organize hundreds of files across multiple assignments

This manual process is:
- **Time-consuming**: 15-30 minutes per assignment for a class of 30 students
- **Error-prone**: Risk of missing submissions, incorrect folder organization
- **Not scalable**: Becomes unmanageable with larger classes or multiple sections
- **Repetitive**: Same workflow repeated 12 times per course

### 1.2 Project Purpose

Build an automated system using Claude Code Skills to:
1. **Connect to Moodle** and authenticate securely
2. **Navigate to assignments** for a specific course
3. **Download student submissions** (PDFs, GitHub links, self-grades)
4. **Organize downloads** into a standardized folder structure (`Assignments/Assignment_XX/`)
5. **Extract metadata** (student ID, GitHub URL, self-grade) for downstream processing
6. **Integrate with existing auto-grader** to enable automated grading workflow

This automation will reduce instructor workload from ~6 hours per course (12 assignments × 30 min) to ~30 minutes total.

### 1.3 Market Analysis

**Similar Tools:**
| Tool | Strengths | Weaknesses | Cost |
|------|-----------|------------|------|
| Moodle Grade Export | Built-in, simple | No file organization, no GitHub integration | Free |
| Canvas SpeedGrader | Good UI | Different LMS, no auto-grading | Paid |
| Manual Scripts | Customizable | Brittle, breaks on Moodle updates | Free |

**Competitive Advantages:**
- **Skill-based architecture**: Modular, maintainable, reusable
- **Integration with auto-grader**: End-to-end automation from submission to grade
- **Robustness**: Error handling, retry logic, detailed logging
- **Documentation**: Claude Code skills are self-documenting

### 1.4 Target Audience & Stakeholders

| Stakeholder | Role | Interest | Priority |
|-------------|------|----------|----------|
| Course Instructors | Primary users | Reduce manual work, faster grading | P0 |
| Teaching Assistants | Secondary users | Organize submissions, verify downloads | P1 |
| Students | Indirect users | Receive feedback faster | P2 |
| IT Department | Support | Ensure security, Moodle compliance | P1 |

---

## 2. Objectives & Success Metrics

### 2.1 Project Goals

- [ ] **Goal 1**: Automate 95%+ of submission download workflow
- [ ] **Goal 2**: Reduce instructor time spent on submission organization from 6 hours to < 30 minutes per course
- [ ] **Goal 3**: Zero missed submissions due to automation errors
- [ ] **Goal 4**: Integrate seamlessly with existing RamiAutoGrader system
- [ ] **Goal 5**: Handle all 12 assignments for a course with 30-50 students

### 2.2 Key Performance Indicators (KPIs)

| KPI | Target | Measurement Method |
|-----|--------|-------------------|
| Download success rate | ≥ 99% | (Successful downloads / Total submissions) × 100 |
| Time to process 1 assignment | < 5 minutes | Elapsed time from skill start to completion |
| False negative rate (missed submissions) | 0% | Manual verification against Moodle |
| Folder organization accuracy | 100% | Correct folder structure for all assignments |
| GitHub link extraction accuracy | ≥ 95% | Successfully parsed links / Total submissions |

### 2.3 Acceptance Criteria

- [ ] System authenticates to Moodle successfully (supports username/password and API token)
- [ ] Downloads all student submissions for a given assignment number (1-12)
- [ ] Creates folder structure: `Assignments/Assignment_XX/student_name/` (where name is from Moodle)
- [ ] Extracts GitHub URL from PDF hyperlinks (not text parsing)
- [ ] Extracts self-assigned grade from PDF (specific field or text)
- [ ] Stores metadata (student name, GitHub URL, self-grade) in JSON format
- [ ] Adjusts grading strictness based on self-grade (higher claimed grade = more critical evaluation)
- [ ] Handles errors gracefully (missing PDFs, invalid GitHub links, network issues)
- [ ] Generates summary report of download status
- [ ] Integrates with existing auto-grader to trigger grading workflow

---

## 3. Functional Requirements

### 3.1 Feature List (Prioritized)

| Priority | Feature | Description | User Story |
|----------|---------|-------------|------------|
| P0 (Must) | Moodle Authentication | Connect to Moodle using credentials or API token | As an instructor, I want to authenticate to Moodle so that I can access course assignments |
| P0 (Must) | Assignment Navigation | Navigate to specific assignment by number (1-12) | As an instructor, I want to select Assignment 5 so that I can download all student submissions for that assignment |
| P0 (Must) | Submission Download | Download all student PDFs and metadata | As an instructor, I want to download all submissions automatically so that I don't have to click each one manually |
| P0 (Must) | Folder Organization | Create `Assignments/Assignment_XX/student_name/` structure | As an instructor, I want submissions organized by assignment and student so that I can find them easily |
| P0 (Must) | GitHub Link Extraction | Extract GitHub URLs from PDF hyperlinks (not text parsing) | As an instructor, I want GitHub links extracted from hyperlinks so that I can clone student repos |
| P1 (Should) | Metadata Export | Save student name, GitHub URL, self-grade to JSON | As an instructor, I want metadata in JSON format so that I can feed it to the auto-grader |
| P1 (Should) | Self-Grade Extraction | Parse self-assigned grade from PDF text or field | As an instructor, I want self-grades extracted so I can compare with auto-grades |
| P1 (Should) | Adaptive Grading Strictness | Increase grading rigor when student claims high self-grade | As an instructor, I want students who claim 95+ to be evaluated more critically to ensure accuracy |
| P1 (Should) | Error Handling | Retry failed downloads, log errors | As an instructor, I want the system to handle errors gracefully so that I can fix issues manually if needed |
| P1 (Should) | Progress Reporting | Show download progress (X/N students) | As an instructor, I want to see progress so that I know the system is working |
| P2 (Nice) | GitHub Auto-Clone | Automatically clone GitHub repos to assignment folder | As an instructor, I want repos cloned automatically so that I can run the auto-grader immediately |
| P2 (Nice) | Self-Grade Comparison | Compare self-grade vs auto-grader score | As an instructor, I want to see discrepancies between self-assessment and actual grade |

### 3.2 Use Cases

#### Use Case 1: Download Assignment Submissions

**Actor**: Course Instructor
**Preconditions**:
- Instructor has Moodle credentials
- Assignment is published on Moodle
- Students have submitted their work

**Main Flow**:
1. Instructor invokes skill: `/skill moodle-download-assignment`
2. System prompts for: Moodle API token, course ID, assignment number (1-12)
3. System authenticates to Moodle via REST API
4. System navigates to assignment page
5. System iterates through each student submission:
   - Downloads PDF to `Assignments/Assignment_XX/student_name/submission.pdf`
   - Extracts GitHub URL from PDF hyperlinks (not text parsing)
   - Extracts self-submitted grade from PDF text
   - Saves metadata to `metadata.json`
6. System generates summary report: `Assignments/Assignment_XX/download_report.txt`

**Postconditions**:
- All submissions downloaded
- Folder structure created
- Metadata extracted
- Summary report generated

**Alternative Flows**:
- **3a**: Authentication fails → Prompt for credentials again, retry 3 times, then abort
- **5a**: PDF not found for student → Log warning, continue with next student
- **5b**: GitHub URL not found → Log warning, set URL to "NOT_FOUND" in metadata
- **5c**: Network error → Retry 3 times with exponential backoff, then skip student and log error

---

#### Use Case 2: Extract GitHub Repository Links

**Actor**: System (automated)
**Preconditions**: PDF downloaded to student folder

**Main Flow**:
1. Open PDF file using PyPDF2 or pdfplumber
2. Extract hyperlinks from PDF annotations (not text parsing)
3. Filter for URLs matching GitHub pattern: `https://github.com/[username]/[repo]`
4. Validate URL format
5. Save to metadata.json

**Postconditions**: GitHub URL extracted and stored

**Alternative Flows**:
- **2a**: Multiple GitHub URLs found → Take the first one, log warning
- **2b**: No hyperlinks found → Fallback to text search for "github.com", log as "MANUAL_REVIEW_NEEDED"
- **4a**: Invalid URL format → Log error, save as "INVALID_URL"

**Note**: PDF submissions have GitHub links as clickable hyperlinks, not plain text.

---

#### Use Case 3: Integrate with Auto-Grader

**Actor**: System (automated)
**Preconditions**:
- Submissions downloaded
- GitHub URLs extracted
- Auto-grader system available

**Main Flow**:
1. Read metadata.json for assignment
2. For each student:
   - Clone GitHub repository (if not already cloned)
   - Invoke auto-grader: `/skill grade-from-git <github_url>`
   - Save grading results to `student_YYYY/grading_results.json`
   - Compare auto-grade vs self-grade
   - Generate discrepancy report if difference > 10 points
3. Generate course-level summary: all students' grades + discrepancies

**Postconditions**:
- All repos graded
- Results saved
- Discrepancies identified

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements

- **Download speed**: Process 30 students in < 5 minutes (10 seconds per student average)
- **GitHub cloning**: Clone 30 repos in < 10 minutes (20 seconds per repo average)
- **PDF parsing**: Extract URL in < 2 seconds per PDF
- **Concurrent downloads**: Support up to 5 parallel downloads without overwhelming Moodle

### 4.2 Security Requirements

- **Authentication**: Support both username/password (encrypted) and API tokens
- **Credential storage**: Never hardcode credentials, use .env file (ignored by git)
- **Network security**: Use HTTPS for all Moodle connections
- **Data privacy**: Student data stays local, no external uploads
- **Access control**: Only authenticated instructors can run skills

### 4.3 Scalability Requirements

- **Class size**: Support 10-100 students per assignment
- **Concurrent assignments**: Handle multiple assignments being processed simultaneously
- **Semester load**: Support 12 assignments × 100 students = 1,200 total submissions
- **Multi-course**: Support running for multiple courses (separate invocations)

### 4.4 Availability & Reliability

- **Uptime dependency**: Relies on Moodle availability (out of our control)
- **Retry logic**: 3 retries with exponential backoff for network errors
- **Graceful degradation**: If Moodle API unavailable, fall back to web scraping
- **Error recovery**: Resume downloads from last successful student (checkpoint file)

### 4.5 Usability Requirements

- **Skill invocation**: Simple command with minimal parameters
- **Progress feedback**: Show "Downloading student X/N..."
- **Error messages**: Clear, actionable (e.g., "Authentication failed. Check credentials in .env")
- **Documentation**: Each skill has comprehensive SKILL.md with examples

---

## 5. Assumptions, Dependencies & Constraints

### 5.1 Assumptions

- Students submit assignments in the expected format (PDF + GitHub link)
- Moodle interface remains relatively stable (won't break selectors frequently)
- GitHub repositories are public or instructor has access
- Course has 12 assignments (can be configured)
- Assignment numbers are 1-12 (zero-padded: Assignment_01, Assignment_02, etc.)

### 5.2 External Dependencies

| Dependency | Type | Risk Level | Mitigation |
|------------|------|------------|------------|
| Moodle LMS | External | High | Cache Moodle HTML structure, implement fallback scraping |
| GitHub API | External | Medium | Use API with rate limit handling, fall back to manual clone |
| Internet connection | External | Medium | Retry logic, offline mode for already-downloaded data |
| Python libraries (Selenium, PyPDF2) | External | Low | Pin versions in requirements.txt |

### 5.3 Technical Constraints

- Must use Claude Code Skills architecture (SKILL.md + optional scripts)
- Cannot execute student code (security risk)
- Limited to static analysis and file operations
- Must integrate with existing RamiAutoGrader folder structure
- Windows environment (PowerShell/CMD compatibility)

### 5.4 Organizational Constraints

- **Timeline**: Must be ready before next assignment deadline (2-3 weeks)
- **Budget**: No external API costs (use free Moodle/GitHub access)
- **Resources**: Single developer (instructor), Claude Code assistance

### 5.5 Out-of-Scope Items

- ❌ Automatic grading of PDFs (only organize files, don't analyze PDF content beyond GitHub URL)
- ❌ Moodle gradebook updates (read-only access to submissions)
- ❌ Email notifications to students
- ❌ Real-time monitoring dashboard
- ❌ Support for non-GitHub version control (GitLab, Bitbucket)
- ❌ Support for assignment types other than "PDF + GitHub link"

---

## 6. System Architecture & Technical Design

### 6.1 Skill-Based Architecture

```
.claude/skills/
├── moodle-authenticate/
│   ├── SKILL.md                    # Authentication instructions
│   └── scripts/
│       └── moodle_auth.py          # Helper: Login to Moodle
│
├── moodle-list-assignments/
│   ├── SKILL.md                    # List available assignments
│   └── scripts/
│       └── parse_assignments.py    # Helper: Parse assignment list
│
├── moodle-download-submissions/
│   ├── SKILL.md                    # Download all submissions for assignment
│   └── scripts/
│       ├── download_pdfs.py        # Helper: Download files
│       ├── extract_github_urls.py  # Helper: Parse PDFs for URLs
│       └── organize_folders.py     # Helper: Create folder structure
│
├── github-clone-repos/
│   ├── SKILL.md                    # Clone student GitHub repos
│   └── scripts/
│       └── batch_clone.py          # Helper: Clone multiple repos
│
└── generate-submission-report/
    ├── SKILL.md                    # Generate summary report
    └── templates/
        └── report_template.md      # Report format
```

### 6.2 Data Flow

```
Moodle → Download PDFs → Extract GitHub URLs → Organize Folders → Clone Repos → Grade Repos → Compare Grades
   ↓           ↓                 ↓                    ↓               ↓            ↓              ↓
  Auth    submissions/    metadata.json       Assignments/    student_repos/  results.json   report.md
```

### 6.3 Folder Structure Output

```
Assignments/
├── Assignment_01/
│   ├── download_report.txt         # Summary: 28/30 downloaded, 2 errors
│   ├── metadata.json                # All students' metadata
│   ├── student_12345678/
│   │   ├── submission.pdf
│   │   ├── metadata.json            # {student_id, github_url, self_grade}
│   │   ├── repo/                    # Cloned GitHub repo
│   │   └── grading_results.json    # Auto-grader output
│   ├── student_87654321/
│   │   └── ...
│   └── ...
├── Assignment_02/
│   └── ...
...
└── Assignment_12/
    └── ...
```

---

## 7. Timeline & Milestones

### 7.1 Project Schedule

| Phase | Start | End | Deliverables | Status |
|-------|-------|-----|--------------|--------|
| Phase 1: Planning | Week 1 | Week 1 | PRD, CLAUDE.md, PLANNING.md, TASKS.md | 🟡 In Progress |
| Phase 2: Core Skills | Week 1 | Week 2 | moodle-authenticate, moodle-download-submissions | 🔴 Not Started |
| Phase 3: Integration | Week 2 | Week 2 | github-clone-repos, integrate with auto-grader | 🔴 Not Started |
| Phase 4: Testing | Week 2 | Week 3 | Test with real Moodle course (past assignments) | 🔴 Not Started |
| Phase 5: Documentation | Week 3 | Week 3 | README, usage guides, troubleshooting | 🔴 Not Started |
| Phase 6: Deployment | Week 3 | Week 3 | Use for next assignment deadline | 🔴 Not Started |

### 7.2 Checkpoint Reviews

- [ ] **Checkpoint 1** (End of Week 1): Review SKILL.md files, test authentication on Moodle
- [ ] **Checkpoint 2** (Mid Week 2): Test download of 1 assignment (5-10 students), verify folder structure
- [ ] **Checkpoint 3** (End of Week 2): Test full workflow (download → clone → grade) on sample assignment
- [ ] **Checkpoint 4** (End of Week 3): Dry run on upcoming assignment, fix any issues

---

## 8. Risks & Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Moodle interface changes | Medium | High | Use Moodle API if available, test with multiple Moodle versions |
| PDF format inconsistency | High | Medium | Support multiple PDF parsing libraries, manual fallback |
| GitHub repository private | Medium | Medium | Prompt instructor to request access, log as error |
| Network failures during download | Low | Medium | Implement retry logic, checkpoint resume |
| Student submits wrong file | High | Low | Log warnings, generate report for manual review |

---

## 9. Appendices

### 9.1 Glossary

| Term | Definition |
|------|------------|
| **Moodle** | Open-source Learning Management System (LMS) |
| **Assignment** | A course task with a due date, submission requirements |
| **Submission** | Student's uploaded PDF + metadata (GitHub link, self-grade) |
| **Self-Grade** | Student's self-assessment score (0-100) |
| **Auto-Grader** | Existing RamiAutoGrader system that evaluates student GitHub repos |
| **Skill** | Claude Code modular capability (SKILL.md + optional scripts) |

### 9.2 References

- [Moodle Web Services API Documentation](https://docs.moodle.org/dev/Web_services)
- [Selenium WebDriver Docs](https://selenium-python.readthedocs.io/)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [GitHub API v3](https://docs.github.com/en/rest)
- [RamiAutoGrader Repository](https://github.com/OmryTzabbar1/RamiAutoGrader)

### 9.3 Sample Submission Metadata

```json
{
  "assignment_number": 1,
  "assignment_name": "Software Design Patterns",
  "total_students": 30,
  "successful_downloads": 28,
  "failed_downloads": 2,
  "students": [
    {
      "student_name": "John Doe",
      "github_url": "https://github.com/johndoe/design-patterns-project",
      "self_grade": 85,
      "grading_strictness": 1.255,
      "auto_grade": null,
      "submission_date": "2025-11-20T14:30:00Z",
      "pdf_path": "Assignments/Assignment_01/student_John_Doe/submission.pdf",
      "repo_path": "Assignments/Assignment_01/student_John_Doe/repo/",
      "download_status": "success",
      "extraction_method": "hyperlink"
    },
    {
      "student_name": "Jane Smith",
      "github_url": "NOT_FOUND",
      "self_grade": 90,
      "grading_strictness": 1.27,
      "auto_grade": null,
      "submission_date": "2025-11-21T09:15:00Z",
      "pdf_path": "Assignments/Assignment_01/student_Jane_Smith/submission.pdf",
      "repo_path": null,
      "download_status": "success",
      "extraction_method": "text_search",
      "warnings": ["GitHub URL not found in PDF hyperlinks, text search also failed"]
    }
  ],
  "download_timestamp": "2025-11-27T20:00:00Z"
}
```

---

**Document Status**: ✅ Complete - Ready for development
**Next Steps**: Review PRD with stakeholders → Generate CLAUDE.md and PLANNING.md → Begin skill development
