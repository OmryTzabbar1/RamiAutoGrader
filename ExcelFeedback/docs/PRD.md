# Product Requirements Document (PRD)
# Excel Feedback Generation System

## 1. Project Overview & Background

**Project Name**: Excel Feedback Generation System
**Version**: 1.0
**Date**: 2025-11-27
**Author**: M.Sc. Computer Science - Course Instructor
**Parent Project**: RamiAutoGrader (Academic Software Auto-Grader System)

### 1.1 Problem Statement

After the RamiAutoGrader completes grading student submissions, instructors need a consolidated Excel spreadsheet with:
- Student identification information (ID, name, partner name)
- Assignment details
- GitHub repository links
- Final grades
- Summary feedback for each student

Currently, this information is scattered across:
- PDF submissions (student info, partner names)
- Metadata JSON files (GitHub URLs)
- Grading result files (scores, detailed reports)

**Manual consolidation is:**
- **Time-consuming**: 10-15 minutes per assignment for 30 students
- **Error-prone**: Copy-paste errors, missing information
- **Not scalable**: Becomes unmanageable with multiple assignments
- **Inefficient**: Same workflow repeated 12 times per course

### 1.2 Project Purpose

Build a **Claude Code Orchestrator Agent** (not a Python script) that:
1. **Extracts student metadata** from PDF submissions (student ID, name, partner name, assignment name)
2. **Reads grading results** from auto-grader output
3. **Generates executive summaries** from detailed grading reports
4. **Populates Excel spreadsheet** with all consolidated information
5. **Integrates seamlessly** with existing RamiAutoGrader workflow

**Key Constraint**: This MUST be a Claude Code agent that orchestrates existing or new skills, not a standalone Python project.

### 1.3 Target Audience & Stakeholders

| Stakeholder | Role | Interest | Priority |
|-------------|------|----------|----------|
| Course Instructors | Primary users | Quick overview of all student grades | P0 |
| Teaching Assistants | Secondary users | Review student performance | P1 |
| Students | Recipients | Receive feedback via Excel sheet | P2 |
| Academic Admin | Oversight | Final grade submission | P1 |

---

## 2. Objectives & Success Metrics

### 2.1 Project Goals

- [ ] **Goal 1**: Automate 100% of Excel feedback generation (no manual data entry)
- [ ] **Goal 2**: Reduce instructor time from 15 minutes to < 1 minute per assignment
- [ ] **Goal 3**: Zero transcription errors in final Excel sheet
- [ ] **Goal 4**: Generate human-readable summaries from detailed grading reports
- [ ] **Goal 5**: Support all 12 assignments for a course with 30-50 students

### 2.2 Key Performance Indicators (KPIs)

| KPI | Target | Measurement Method |
|-----|--------|-------------------|
| Metadata extraction accuracy | ≥ 98% | (Correct extractions / Total submissions) × 100 |
| Time to generate Excel sheet | < 2 minutes | Elapsed time from invocation to completion |
| Summary quality score | ≥ 4/5 | Instructor rating of generated summaries |
| Integration success rate | 100% | Works with all RamiAutoGrader outputs |

### 2.3 Acceptance Criteria

- [ ] Agent extracts student ID, name, partner name, assignment name from PDFs
- [ ] Agent reads grading results from RamiAutoGrader output files
- [ ] Agent generates 2-3 sentence summaries from detailed reports
- [ ] Agent populates Excel with all required columns
- [ ] Excel sheet is properly formatted (headers, column widths, borders)
- [ ] Agent integrates with RamiAutoGrader agent (called automatically after grading)
- [ ] Handles missing data gracefully (flags for manual review)

---

## 3. Functional Requirements

### 3.1 Feature List (Prioritized)

| Priority | Feature | Description | User Story |
|----------|---------|-------------|------------|
| P0 (Must) | PDF Metadata Extraction | Extract student ID, name, partner name, assignment name from PDFs | As an instructor, I want student info automatically extracted so I don't have to type it manually |
| P0 (Must) | GitHub URL Population | Read GitHub URLs from ExcelRW metadata | As an instructor, I want GitHub links pre-populated in the Excel sheet |
| P0 (Must) | Grade Extraction | Read final scores from grading_results.json | As an instructor, I want grades automatically populated |
| P0 (Must) | Summary Generation | Generate 2-3 sentence summaries from detailed reports | As an instructor, I want concise feedback I can share with students |
| P0 (Must) | Excel Sheet Generation | Create formatted Excel file with all columns | As an instructor, I want a professional-looking Excel sheet |
| P1 (Should) | Error Handling | Flag missing/invalid data for manual review | As an instructor, I want to know which entries need attention |
| P1 (Should) | Column Formatting | Auto-size columns, add borders, freeze header row | As an instructor, I want a polished, easy-to-read spreadsheet |
| P2 (Nice) | Multiple Format Support | Export as .xlsx, .csv, Google Sheets | As an instructor, I want flexibility in file formats |

### 3.2 Use Cases

#### Use Case 1: Generate Excel Feedback Sheet

**Actor**: RamiAutoGrader Agent (automated invocation)
**Preconditions**:
- All students graded for a specific assignment
- Grading results saved to `Assignments/Assignment_XX/student_name/grading_results.json`
- PDF submissions available in `Assignments/Assignment_XX/student_name/submission.pdf`
- Metadata.json exists with GitHub URLs

**Main Flow**:
1. RamiAutoGrader agent completes grading all students
2. RamiAutoGrader agent invokes **excel-feedback-generator** agent
3. excel-feedback-generator agent invokes **extract-pdf-metadata** skill for each student
4. Skill extracts: student_id, student_name, partner_name, assignment_name
5. Agent reads GitHub URLs from `metadata.json`
6. Agent reads final grades from `grading_results.json` for each student
7. Agent invokes **generate-summary** skill to create concise feedback
8. Agent invokes **populate-excel** skill to create Excel sheet
9. Excel sheet saved to `Assignments/Assignment_XX/FinalFeedback.xlsx`
10. Agent reports completion to user

**Postconditions**:
- Excel sheet created with all columns populated
- Missing data flagged in "Notes" column
- File ready for distribution to students

**Alternative Flows**:
- **3a**: PDF metadata extraction fails → Log warning, mark as "NEEDS_MANUAL_REVIEW", continue
- **6a**: Grading results not found → Use "PENDING" as grade, flag for review
- **7a**: Summary generation fails → Use generic template summary, flag for review

---

#### Use Case 2: Extract Student Metadata from PDF

**Actor**: extract-pdf-metadata skill (invoked by agent)
**Preconditions**: PDF submission exists

**Main Flow**:
1. Read PDF text using pdfplumber/PyPDF2
2. Use Claude API to extract structured data:
   - Prompt: "Extract student_id, student_name, partner_name, assignment_name from this PDF"
3. Validate extracted fields (non-empty, proper format)
4. Return structured JSON:
   ```json
   {
     "student_id": "12345678",
     "student_name": "John Doe",
     "partner_name": "Jane Smith",
     "assignment_name": "Design Patterns Project"
   }
   ```

**Postconditions**: Metadata available for Excel population

**Alternative Flows**:
- **2a**: Claude cannot extract all fields → Return partial data, flag missing fields
- **3a**: Validation fails → Return error, mark for manual review

---

#### Use Case 3: Generate Summary from Grading Report

**Actor**: generate-summary skill (invoked by agent)
**Preconditions**: Detailed grading report exists

**Main Flow**:
1. Read detailed grading report (markdown/JSON)
2. Use Claude API with prompt:
   ```
   Summarize this grading report in 2-3 sentences for student feedback.
   Include: overall score, main strengths, key areas for improvement.
   Format: Professional but encouraging tone.
   ```
3. Validate summary (length, tone, completeness)
4. Return summary text

**Example Output**:
```
Score: 77/100 (C+). Strong documentation and security practices.
Main areas for improvement: 3 files exceed 150-line limit, requiring refactoring.
Test coverage report is missing - recommend adding pytest-cov.
```

**Postconditions**: Human-readable summary available for Excel

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements

- **Metadata extraction**: < 5 seconds per PDF
- **Summary generation**: < 10 seconds per report
- **Excel generation**: < 30 seconds for 30 students
- **Total time**: < 5 minutes for entire assignment (30 students)

### 4.2 Usability Requirements

- **Agent invocation**: Automatic (called by RamiAutoGrader agent)
- **Manual invocation**: Simple command: `/agent excel-feedback-generator assignment_number=5`
- **Error messages**: Clear, actionable (e.g., "Missing PDF for student_John_Doe")
- **Output**: Excel file immediately ready to distribute (no post-processing)

### 4.3 Reliability Requirements

- **Graceful degradation**: Continue processing even if some extractions fail
- **Error logging**: All failures logged to `FinalFeedback_errors.log`
- **Partial success**: Generate Excel with partial data, flag incomplete rows

### 4.4 Security Requirements

- **Data privacy**: Student data stays local, not uploaded to external services (Claude API is acceptable)
- **No secrets**: No API keys in agent code (use .env)
- **File permissions**: Excel files readable only by instructor

---

## 5. System Architecture

### 5.1 Agent Architecture

```
excel-feedback-generator (Agent)
├── orchestrates:
│   ├── extract-pdf-metadata (Skill)
│   │   └── scripts/extract_student_info.py
│   ├── generate-summary (Skill)
│   │   └── scripts/summarize_report.py
│   └── populate-excel (Skill)
│       └── scripts/create_excel_sheet.py
```

**Integration Point**:
```python
# RamiAutoGrader agent (agent.yaml) - ADD THIS:
post_grading_steps:
  - agent: excel-feedback-generator
    trigger: after_all_students_graded
    params:
      assignment_number: ${assignment_number}
```

### 5.2 Excel Sheet Structure

| Column | Source | Example | Notes |
|--------|--------|---------|-------|
| **Student ID** | PDF extraction | 12345678 | Unique identifier |
| **Student Name** | PDF extraction | John Doe | Full name |
| **Partner Name** | PDF extraction | Jane Smith | Group partner |
| **Assignment Name** | PDF extraction | Design Patterns | Assignment title |
| **GitHub URL** | metadata.json | https://github.com/... | Pre-populated by ExcelRW |
| **Grade** | grading_results.json | 77/100 | Final score |
| **Summary** | Generated by Claude | Strong docs, fix file sizes... | 2-3 sentences |
| **Notes** | Agent-generated | NEEDS_MANUAL_REVIEW | Flags for attention |

### 5.3 File Locations

**Input Files**:
```
Assignments/Assignment_05/
├── metadata.json                    # GitHub URLs
├── student_John_Doe/
│   ├── submission.pdf               # Student metadata source
│   ├── grading_results.json         # Grade source
│   └── detailed_report.md           # Summary source
└── student_Jane_Smith/
    └── ...
```

**Output Files**:
```
Assignments/Assignment_05/
├── FinalFeedback.xlsx               # Generated Excel sheet
└── FinalFeedback_errors.log         # Extraction errors
```

---

## 6. Data Models

### 6.1 Student Metadata (Extracted from PDF)

```json
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns Project",
  "extraction_method": "claude_api",
  "confidence": 0.95
}
```

### 6.2 Grading Results (Read from grading_results.json)

```json
{
  "total_score": 77,
  "max_score": 100,
  "percentage": 77.0,
  "letter_grade": "C+",
  "passed": true,
  "category_scores": {
    "code_quality": 20,
    "tests": 10,
    "security": 10,
    "documentation": 25,
    "git_workflow": 10,
    "research": 2
  }
}
```

### 6.3 Summary (Generated by Claude)

```json
{
  "summary_text": "Score: 77/100 (C+). Strong documentation and security practices. Main areas for improvement: 3 files exceed 150-line limit, requiring refactoring. Test coverage report is missing - recommend adding pytest-cov.",
  "word_count": 31,
  "tone": "professional_encouraging",
  "key_points": [
    "Strong: documentation, security",
    "Improve: file sizes, test coverage"
  ]
}
```

---

## 7. Integration with RamiAutoGrader

### 7.1 Current Workflow

```
1. User: /agent grade-project assignment_number=5
2. RamiAutoGrader agent:
   - Grades all students
   - Generates detailed_report.md
   - Saves grading_results.json
3. Done.
```

### 7.2 Updated Workflow (with Excel Feedback)

```
1. User: /agent grade-project assignment_number=5
2. RamiAutoGrader agent:
   - Grades all students
   - Generates detailed_report.md
   - Saves grading_results.json
   - ✨ Invokes excel-feedback-generator agent
3. excel-feedback-generator agent:
   - Extracts PDF metadata for all students
   - Generates summaries
   - Creates FinalFeedback.xlsx
4. Done.
```

**Implementation**: Update `grader-orchestrator/agent.yaml`:
```yaml
post_execution:
  - name: generate_excel_feedback
    agent: excel-feedback-generator
    params:
      assignment_number: ${assignment_number}
    condition: all_students_graded
```

---

## 8. Assumptions & Constraints

### 8.1 Assumptions

- PDF submissions contain student ID, name, partner name, assignment name in a parsable format
- Claude API can reliably extract structured data from PDFs (95%+ accuracy)
- All students have grading_results.json after RamiAutoGrader completes
- Excel file format (.xlsx) is acceptable (not Google Sheets API)

### 8.2 Constraints

- **Architecture constraint**: MUST be a Claude Code agent (not standalone Python)
- **Integration constraint**: Must work with existing RamiAutoGrader agent
- **No GUI**: Command-line only (Claude Code environment)
- **Local execution**: All processing happens locally (no cloud deployment)

### 8.3 Out-of-Scope

- ❌ Email distribution of Excel sheets (manual distribution)
- ❌ Google Sheets API integration (use .xlsx export)
- ❌ Student portal for viewing feedback (Excel is final format)
- ❌ Historical grade tracking (one Excel per assignment)
- ❌ Grade curve calculation (instructor does manually)

---

## 9. Timeline & Deliverables

### 9.1 Phase 1: Skill Development (Estimated: 6-8 hours)

| Task | Deliverable | Estimated Time |
|------|-------------|----------------|
| Create extract-pdf-metadata skill | SKILL.md + extract_student_info.py | 3 hours |
| Create generate-summary skill | SKILL.md + summarize_report.py | 2 hours |
| Create populate-excel skill | SKILL.md + create_excel_sheet.py | 2-3 hours |

### 9.2 Phase 2: Agent Development (Estimated: 4-6 hours)

| Task | Deliverable | Estimated Time |
|------|-------------|----------------|
| Create excel-feedback-generator agent | agent.yaml + orchestration logic | 2 hours |
| Integrate with RamiAutoGrader agent | Update grader-orchestrator/agent.yaml | 1 hour |
| Test with sample assignment | FinalFeedback.xlsx for Assignment_01 | 2-3 hours |

### 9.3 Phase 3: Testing & Documentation (Estimated: 3-4 hours)

| Task | Deliverable | Estimated Time |
|------|-------------|----------------|
| Unit tests for all skills | tests/test_excel_feedback.py | 2 hours |
| Integration test (end-to-end) | Test with full assignment | 1 hour |
| README documentation | Usage instructions, troubleshooting | 1 hour |

**Total Estimated Time**: 13-18 hours

---

## 10. Success Criteria

### 10.1 Functional Completeness

- [ ] Excel sheet generated with all 8 columns
- [ ] Student metadata extracted from 95%+ of PDFs
- [ ] Summaries generated for all students
- [ ] Excel properly formatted (headers, borders, column widths)
- [ ] Agent automatically invoked after RamiAutoGrader completes

### 10.2 Quality Metrics

- [ ] Metadata extraction accuracy: ≥ 98%
- [ ] Summary quality: Rated 4+/5 by instructor
- [ ] Zero manual data entry required (except flagged items)
- [ ] All scripts < 150 lines (following CLAUDE.md standards)
- [ ] 70%+ test coverage

### 10.3 Integration Success

- [ ] Works seamlessly with RamiAutoGrader agent
- [ ] No breaking changes to existing grading workflow
- [ ] Error logs provide clear troubleshooting guidance
- [ ] Excel file ready to distribute immediately (no post-processing)

---

## Appendix A: Example Excel Output

| Student ID | Student Name | Partner Name | Assignment Name | GitHub URL | Grade | Summary | Notes |
|------------|--------------|--------------|-----------------|------------|-------|---------|-------|
| 12345678 | John Doe | Jane Smith | Design Patterns | https://github.com/john/project | 77/100 | Strong docs, fix file sizes, add test coverage | |
| 87654321 | Jane Smith | John Doe | Design Patterns | https://github.com/jane/project | 85/100 | Excellent code quality, minor naming violations | |
| 11111111 | Bob Lee | Alice Wu | Design Patterns | NOT_FOUND | PENDING | GitHub URL not found in PDF | NEEDS_MANUAL_REVIEW |

---

## Appendix B: Prompt Templates

### B.1 PDF Metadata Extraction Prompt

```
Extract the following information from this student submission PDF:

Required fields:
- student_id: The student's unique ID (usually 8 digits)
- student_name: The student's full name
- partner_name: The partner's full name (this is a group project)
- assignment_name: The name/title of the assignment

Return a JSON object with these exact keys. If a field is not found, use "NOT_FOUND".

Example response:
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns Project"
}

PDF Text:
[PDF content here]
```

### B.2 Summary Generation Prompt

```
Summarize this grading report in 2-3 sentences for student feedback.

Requirements:
- Include: overall score, main strengths, key areas for improvement
- Format: Professional but encouraging tone
- Length: 30-50 words
- Focus on actionable feedback

Grading Report:
[Report content here]
```

---

**Document Status**: ✅ Complete - Ready for development
**Next Steps**:
1. Review PRD with instructor
2. Generate CLAUDE.md, PLANNING.md, TASKS.md
3. Begin skill development (Phase 1)
