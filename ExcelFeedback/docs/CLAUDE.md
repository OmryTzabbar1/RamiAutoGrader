# CLAUDE.md - ExcelFeedback Development Guidelines

## Project Overview

**ExcelFeedback** is the final layer of the RamiAutoGrader system that generates instructor-facing Excel feedback sheets after auto-grading completes. This is a **Claude Code agent orchestration project** (NOT a Python script project) that ties together the entire grading workflow.

**Key Architecture Decision**: Implemented as a **Claude Code agent** that orchestrates specialized skills for maximum flexibility and maintainability.

---

## CRITICAL REQUIREMENTS - Read This First

### Agent Architecture (NOT Python Script)

**⚠️ This is NOT a standalone Python project** - it's a Claude Code agent that orchestrates skills.

**Why Agent Architecture?**
- Flexible orchestration of LLM-based tasks (PDF extraction, summary generation)
- Native integration with RamiAutoGrader agent workflow
- No CLI interface needed - called automatically after grading
- Leverages Claude API directly for unstructured data extraction

**Project Type**: Claude Code Agent + Skills (not standalone Python application)

---

## Agent Structure

### Main Agent: `excel-feedback-generator`

**Location**: `ExcelFeedback/agents/excel-feedback-generator/`

**Purpose**: Orchestrate post-grading Excel sheet generation

**Workflow**:
1. Receive grading results from RamiAutoGrader agent
2. For each student submission:
   - Extract student metadata from PDF (via `extract-pdf-metadata` skill)
   - Generate human-readable summary (via `generate-summary` skill)
   - Populate Excel row with all data
3. Create final Excel workbook (via `populate-excel` skill)
4. Save to `results/FinalFeedback_<assignment>.xlsx`

**Agent Configuration** (`agent.yaml`):
```yaml
name: excel-feedback-generator
version: 1.0.0
description: Generate instructor-facing Excel feedback sheets after auto-grading

skills:
  - extract-pdf-metadata
  - generate-summary
  - populate-excel

workflow:
  - step: validate_inputs
    description: Verify grading results and PDF paths exist

  - step: extract_all_metadata
    skill: extract-pdf-metadata
    for_each: student_submission
    inputs:
      pdf_path: ${submission.pdf_path}
    outputs:
      metadata: ${student.metadata}

  - step: generate_all_summaries
    skill: generate-summary
    for_each: student_submission
    inputs:
      grading_report: ${submission.grading_results.json}
    outputs:
      summary: ${student.summary}

  - step: create_excel
    skill: populate-excel
    inputs:
      student_data: ${all_students}
      assignment_name: ${assignment_name}
    outputs:
      excel_path: ${output_path}

outputs:
  excel_file: results/FinalFeedback_${assignment_name}.xlsx
```

---

## Skill Specifications

### Skill 1: `extract-pdf-metadata`

**Purpose**: Extract student information from unstructured PDF submissions using Claude API

**Location**: `ExcelFeedback/skills/extract-pdf-metadata/`

**Inputs**:
- `pdf_path` (str): Path to student's PDF submission

**Outputs** (JSON):
```json
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns Implementation",
  "confidence": 0.95,
  "extraction_status": "SUCCESS"
}
```

**Claude Prompt Template**:
```markdown
Extract the following information from this student submission PDF:

Required fields:
- student_id: The student's unique ID (usually 8 digits)
- student_name: The student's full name
- partner_name: The partner's full name (this is a group project of 2)
- assignment_name: The name/title of the assignment

Instructions:
- Return valid JSON with these exact field names
- If a field is not found, use "NOT_FOUND" as the value
- Provide a confidence score (0.0-1.0) for extraction quality
- If confidence < 0.7, set extraction_status to "NEEDS_MANUAL_REVIEW"

PDF Text:
{pdf_text}
```

**Implementation Guidelines**:
```python
# SKILL.md should specify:
# 1. Use pdfplumber to extract text from PDF
# 2. Send text to Claude API with extraction prompt
# 3. Parse JSON response
# 4. Validate required fields
# 5. Flag low-confidence extractions for manual review
```

**Error Handling**:
- PDF not found: Return `extraction_status: "FILE_NOT_FOUND"`
- Claude API failure: Return `extraction_status: "API_ERROR"`
- Invalid JSON response: Return `extraction_status: "PARSE_ERROR"`
- Low confidence (<0.7): Return `extraction_status: "NEEDS_MANUAL_REVIEW"`

---

### Skill 2: `generate-summary`

**Purpose**: Generate concise 2-3 sentence feedback summary from detailed grading report

**Location**: `ExcelFeedback/skills/generate-summary/`

**Inputs**:
- `grading_report_path` (str): Path to student's `grading_results.json`

**Outputs** (str):
```
"Strong documentation (25/25) and excellent security practices (10/10). Code quality needs improvement: 2 files exceed 150-line limit (src/analyzer.py, src/parser.py). Increase test coverage from 67% to ≥70% minimum."
```

**Claude Prompt Template**:
```markdown
Summarize this grading report in 2-3 sentences for instructor review.

Requirements:
- Start with overall score out of 100
- Mention main strengths (categories with high scores)
- Highlight key areas for improvement (specific actionable items)
- Professional but encouraging tone
- Length: 30-50 words
- Format: Plain text, no markdown

Grading Report:
{grading_results_json}

Example Output:
"Score: 77/100. Strong documentation (25/25) and security (10/10). Fix: 2 files exceed 150 lines; increase test coverage to 70%+."
```

**Implementation Guidelines**:
```python
# SKILL.md should specify:
# 1. Read grading_results.json
# 2. Extract total score, category scores, violations
# 3. Send to Claude API with summary prompt
# 4. Validate response length (30-50 words)
# 5. Return plain text summary
```

**Quality Checks**:
- Summary must start with score (e.g., "Score: 77/100")
- Must mention at least 1 strength
- Must mention at least 1 improvement area
- Length: 30-50 words (strict enforcement)
- No markdown formatting (plain text only)

---

### Skill 3: `populate-excel`

**Purpose**: Create formatted Excel workbook with all student feedback

**Location**: `ExcelFeedback/skills/populate-excel/`

**Inputs**:
- `student_data` (list): Combined metadata, grading results, summaries
- `assignment_name` (str): Name of assignment for filename

**Outputs**:
- `results/FinalFeedback_<assignment_name>.xlsx`

**Excel Sheet Structure**:

| Column | Width | Format | Example |
|--------|-------|--------|---------|
| Student ID | 12 | Text | 12345678 |
| Student Name | 20 | Text | John Doe |
| Partner Name | 20 | Text | Jane Smith |
| Assignment Name | 25 | Text | Design Patterns |
| GitHub URL | 40 | Hyperlink | [Link](https://github.com/...) |
| Grade | 10 | Number | 77/100 |
| Summary | 60 | Text (wrapped) | Strong docs, fix file sizes... |
| Notes | 15 | Text | NEEDS_MANUAL_REVIEW |

**Formatting Requirements**:
```python
# openpyxl formatting:
- Header row: Bold, light blue background (#D9E1F2), centered
- Column widths: Auto-adjust to content (min widths specified above)
- Text wrapping: Enabled for Summary column
- Borders: Thin borders on all cells
- Font: Calibri 11pt
- Alignment: Top-left for text, center for headers
- GitHub URL: Active hyperlink (formula: =HYPERLINK(url, "Link"))
```

**Implementation Guidelines**:
```python
# SKILL.md should specify:
# 1. Create new Excel workbook using openpyxl
# 2. Add header row with formatting
# 3. For each student, add row with data
# 4. Apply formatting (borders, colors, fonts)
# 5. Auto-adjust column widths
# 6. Save to results/ directory
```

**Data Sources**:
```python
student_row = {
    "student_id": metadata["student_id"],
    "student_name": metadata["student_name"],
    "partner_name": metadata["partner_name"],
    "assignment_name": metadata["assignment_name"],
    "github_url": grading_results["github_url"],  # From metadata.json
    "grade": f"{grading_results['total_score']}/{grading_results['max_score']}",
    "summary": summary,  # From generate-summary skill
    "notes": "NEEDS_MANUAL_REVIEW" if metadata["confidence"] < 0.7 else ""
}
```

---

## Integration with RamiAutoGrader

### Post-Grading Hook

**Modify**: `RamiAutoGrader/agents/grader-orchestrator/agent.yaml`

**Add this section**:
```yaml
post_grading_steps:
  - agent: excel-feedback-generator
    trigger: after_all_students_graded
    inputs:
      grading_results_dir: ${output_dir}
      pdf_submissions_dir: ${pdf_dir}
      assignment_name: ${assignment_name}
    outputs:
      excel_file: results/FinalFeedback_${assignment_name}.xlsx
```

**Workflow Sequence**:
1. RamiAutoGrader agent grades all students
2. Results saved to `results/<student_name>/grading_results.json`
3. RamiAutoGrader agent triggers `excel-feedback-generator` agent
4. ExcelFeedback agent processes all results
5. Final Excel file saved to `results/FinalFeedback_<assignment>.xlsx`

---

## Data Flow

```
RamiAutoGrader Agent Completes
         ↓
   Trigger Hook
         ↓
excel-feedback-generator Agent Starts
         ↓
For Each Student:
   ├─→ extract-pdf-metadata skill
   │     ├─ Input: student_submission.pdf
   │     ├─ Process: Claude API extraction
   │     └─ Output: {student_id, name, partner_name, assignment_name}
   │
   ├─→ generate-summary skill
   │     ├─ Input: grading_results.json
   │     ├─ Process: Claude API summarization
   │     └─ Output: "Score: 77/100. Strong docs, fix files..."
   │
   └─→ Collect data for Excel row
         ↓
populate-excel skill
   ├─ Input: All student data
   ├─ Process: Create formatted .xlsx
   └─ Output: results/FinalFeedback_<assignment>.xlsx
```

---

## File Structure

```
ExcelFeedback/
├── agents/
│   └── excel-feedback-generator/
│       ├── agent.yaml              # Agent configuration
│       └── README.md               # Agent documentation
├── skills/
│   ├── extract-pdf-metadata/
│   │   ├── SKILL.md                # Skill instructions
│   │   ├── skill.json              # Skill manifest
│   │   └── scripts/
│   │       └── extract_metadata.py # Python helper (if needed)
│   ├── generate-summary/
│   │   ├── SKILL.md
│   │   ├── skill.json
│   │   └── scripts/
│   │       └── summarize_report.py
│   └── populate-excel/
│       ├── SKILL.md
│       ├── skill.json
│       └── scripts/
│           └── create_excel.py
├── docs/
│   ├── PRD.md                      # Product requirements
│   ├── CLAUDE.md                   # This file
│   ├── PLANNING.md                 # Architecture & ADRs
│   └── TASKS.md                    # Task breakdown
├── tests/
│   ├── unit/
│   │   ├── test_extract_metadata.py
│   │   ├── test_generate_summary.py
│   │   └── test_populate_excel.py
│   ├── integration/
│   │   └── test_full_workflow.py
│   └── fixtures/
│       ├── sample_submission.pdf
│       └── sample_grading_results.json
├── config/
│   ├── .env.example
│   └── agent_config.yaml
├── results/                        # Output directory (auto-generated)
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Code Quality Standards

### Agent Development Standards

**Agent Configuration (agent.yaml)**:
- Clear workflow steps with descriptions
- Explicit input/output definitions
- Error handling strategies documented
- Timeout configurations for LLM calls

**Skill Development Standards**:
- Each skill has comprehensive SKILL.md documentation
- Clear input/output contracts
- Edge case handling documented
- LLM prompts version-controlled

### File Size Limits

**Maximum file length: 150 lines** - NO EXCEPTIONS

**For Skills**:
- `SKILL.md`: Can exceed 150 lines (documentation)
- `scripts/*.py`: Must stay under 150 lines
- If script exceeds 150 lines, split into utilities module

**Example**:
```
# BEFORE: extract_metadata.py (215 lines) ❌

# AFTER: Refactor ✅
scripts/
├── extract_metadata.py      # Main logic (95 lines)
└── utils/
    ├── pdf_parser.py         # PDF extraction (78 lines)
    └── claude_client.py      # Claude API calls (62 lines)
```

### Documentation Requirements

**Every Skill SKILL.md Must Have**:
```markdown
# Skill Name

## Purpose
[What this skill does and why it exists]

## Inputs
- param_name (type): Description

## Outputs
- output_name (type): Description
- Example JSON structure

## Instructions
Step-by-step Claude Code instructions:
1. Read input file
2. Process data
3. Call Claude API with prompt
4. Validate output
5. Return result

## Claude Prompt Template
[Exact prompt to use with variables marked as {variable_name}]

## Error Handling
- Scenario 1: Action to take
- Scenario 2: Action to take

## Example Usage
[Concrete example with sample inputs/outputs]
```

**Every Function Must Have**:
```python
def extract_student_metadata(pdf_path: str) -> dict:
    """
    Extract student information from PDF using Claude API.

    This function reads the PDF text, sends it to Claude with a structured
    extraction prompt, and returns validated metadata. If extraction fails
    or confidence is low, the function flags the record for manual review.

    Args:
        pdf_path: Absolute path to student's PDF submission

    Returns:
        dict: {
            'student_id': str,
            'student_name': str,
            'partner_name': str,
            'assignment_name': str,
            'confidence': float (0.0-1.0),
            'extraction_status': str (SUCCESS | NEEDS_MANUAL_REVIEW | ERROR)
        }

    Raises:
        FileNotFoundError: If pdf_path does not exist
        RuntimeError: If Claude API call fails

    Example:
        >>> result = extract_student_metadata('submission.pdf')
        >>> print(result['student_name'])
        'John Doe'
    """
```

---

## Testing Requirements

### Coverage Targets
- **Minimum**: 70% overall code coverage
- **Critical Paths**: 90%+ for skills (metadata extraction, Excel generation)
- **LLM Integration**: Mock Claude API responses for unit tests

### Test Types Required

1. **Unit Tests** - Test each skill in isolation with mocked dependencies
2. **Integration Tests** - Test full agent workflow with sample data
3. **Edge Case Tests** - Malformed PDFs, missing data, API failures
4. **Output Validation** - Verify Excel format, data accuracy

### Example Test Structure

```python
def test_extract_metadata_valid_pdf():
    """
    Test that extract_student_metadata successfully extracts all fields
    from a well-formatted PDF submission.
    """
    # Arrange
    sample_pdf = "tests/fixtures/valid_submission.pdf"
    expected = {
        "student_id": "12345678",
        "student_name": "John Doe",
        "partner_name": "Jane Smith",
        "assignment_name": "Design Patterns",
        "confidence": 0.95,
        "extraction_status": "SUCCESS"
    }

    # Act
    result = extract_student_metadata(sample_pdf)

    # Assert
    assert result == expected
    assert result["confidence"] >= 0.7


def test_extract_metadata_missing_partner_name():
    """
    Test that extract_student_metadata handles PDFs with missing partner
    information by returning NOT_FOUND and flagging for manual review.
    """
    # Arrange
    sample_pdf = "tests/fixtures/missing_partner.pdf"

    # Act
    result = extract_student_metadata(sample_pdf)

    # Assert
    assert result["partner_name"] == "NOT_FOUND"
    assert result["extraction_status"] == "NEEDS_MANUAL_REVIEW"
    assert result["confidence"] < 0.7
```

---

## Configuration Management

### Environment Variables

**Required `.env` variables**:
```bash
# Claude API (inherited from Claude Code)
ANTHROPIC_API_KEY=sk-ant-...

# Excel Feedback Configuration
EXCEL_OUTPUT_DIR=results/
CONFIDENCE_THRESHOLD=0.7

# LLM Model Selection
CLAUDE_MODEL=claude-sonnet-4-5-20250929
```

**Create `.env.example`**:
```bash
# Claude API Key (required)
ANTHROPIC_API_KEY=your_key_here

# Excel Feedback Configuration
EXCEL_OUTPUT_DIR=results/
CONFIDENCE_THRESHOLD=0.7

# Model Selection
CLAUDE_MODEL=claude-sonnet-4-5-20250929
```

### Agent Configuration

**`config/agent_config.yaml`**:
```yaml
# Excel Feedback Generator Configuration
version: "1.0"

agent:
  name: excel-feedback-generator
  timeout: 600  # 10 minutes max for all students
  retry_policy:
    max_retries: 3
    backoff: exponential

skills:
  extract_pdf_metadata:
    timeout: 30  # 30 seconds per student
    confidence_threshold: 0.7
    model: claude-sonnet-4-5-20250929

  generate_summary:
    timeout: 20
    max_words: 50
    min_words: 30
    model: claude-sonnet-4-5-20250929

  populate_excel:
    timeout: 60
    output_format: xlsx
    header_style:
      font: Calibri 11pt Bold
      background: "#D9E1F2"

excel_columns:
  - name: Student ID
    width: 12
  - name: Student Name
    width: 20
  - name: Partner Name
    width: 20
  - name: Assignment Name
    width: 25
  - name: GitHub URL
    width: 40
  - name: Grade
    width: 10
  - name: Summary
    width: 60
  - name: Notes
    width: 15
```

---

## Error Handling

### Required Error Handling Strategies

1. **PDF Extraction Failures**:
   - Action: Flag row with `extraction_status: "FILE_NOT_FOUND"`
   - Excel Notes column: "PDF_MISSING"
   - Continue processing other students

2. **Claude API Failures**:
   - Action: Retry up to 3 times with exponential backoff
   - If still fails: Use placeholder data + flag for manual review
   - Excel Notes column: "API_ERROR_MANUAL_REVIEW"

3. **Low Confidence Extraction**:
   - Action: Accept extraction but flag for verification
   - Excel Notes column: "LOW_CONFIDENCE_REVIEW"

4. **Invalid JSON Response from Claude**:
   - Action: Log error, use default structure with "NOT_FOUND" values
   - Excel Notes column: "PARSE_ERROR"

5. **Excel Generation Failures**:
   - Action: Log error, save partial Excel if possible
   - Output error report to `results/errors_<timestamp>.log`

---

## Git Practices

### Commit Frequency

**⚠️ NEVER make just one large commit** - this is an agent orchestration project requiring careful incremental development.

**Recommended Commit Progression**:
```
feat(agent): Initialize excel-feedback-generator agent structure
feat(skills): Add extract-pdf-metadata skill stub [P1.1]
test(skills): Add unit tests for PDF metadata extraction
feat(skills): Implement Claude API integration for metadata extraction
docs(skills): Document PDF extraction prompt template
feat(skills): Add generate-summary skill [P1.2]
test(skills): Add summary generation tests with mocked Claude responses
feat(skills): Add populate-excel skill [P1.3]
test(skills): Add Excel formatting validation tests
feat(agent): Implement agent workflow orchestration
test(integration): Add end-to-end workflow test
feat(integration): Add post-grading hook to RamiAutoGrader agent
docs: Update README with usage examples
fix: Handle edge case where partner_name is missing from PDF
refactor: Extract Claude API client to shared utility
```

**Minimum commits**: 15-20 commits showing clear development progression

### Commit Messages

**Format**:
```
<type>(<scope>): <short description> [TASK-ID]
```

**Types**:
- `feat`: New feature (skill, agent configuration)
- `fix`: Bug fix
- `docs`: Documentation (SKILL.md, README)
- `test`: Adding or updating tests
- `refactor`: Code restructuring
- `chore`: Dependencies, config

---

## Quality Checklist Before Completion

### Agent Quality
- [ ] Agent workflow clearly defined in agent.yaml
- [ ] All skills properly orchestrated
- [ ] Error handling at agent level (timeouts, retries)
- [ ] Integration with RamiAutoGrader agent tested

### Skills Quality
- [ ] All 3 skills implemented (extract-pdf-metadata, generate-summary, populate-excel)
- [ ] SKILL.md comprehensive for each skill
- [ ] Claude prompts documented and version-controlled
- [ ] Input/output contracts validated

### Code Quality
- [ ] All files under 150 lines
- [ ] Docstrings on all functions/classes/modules
- [ ] No hardcoded secrets or paths
- [ ] 70%+ test coverage

### Git & Version Control
- [ ] 15-20+ commits with clear progression
- [ ] Commit messages follow format
- [ ] Commits reference TASKS.md task IDs

### Documentation
- [ ] README complete with usage examples
- [ ] CLAUDE.md finalized (this file)
- [ ] PLANNING.md with architecture diagrams
- [ ] TASKS.md tracking all tasks

### Testing
- [ ] Unit tests for all skills
- [ ] Integration test for full agent workflow
- [ ] Edge case tests (malformed PDFs, API failures)
- [ ] Output validation (Excel format, data accuracy)
- [ ] All tests pass

### Configuration
- [ ] `.env.example` created
- [ ] `agent_config.yaml` documented
- [ ] No hardcoded values

### Integration
- [ ] Post-grading hook added to RamiAutoGrader
- [ ] End-to-end test with real grading results
- [ ] Excel output manually verified

---

## Success Criteria

**Functional**:
- ✅ Agent automatically triggered after RamiAutoGrader completes
- ✅ All student metadata extracted from PDFs with ≥70% confidence
- ✅ Summaries generated for all students (30-50 words each)
- ✅ Excel file created with proper formatting
- ✅ Manual review flags set for low-confidence extractions

**Quality**:
- ✅ All skills pass unit tests
- ✅ Integration test passes with 10+ sample students
- ✅ Excel output validated (columns, formatting, hyperlinks)
- ✅ Error handling tested (missing PDFs, API failures)

**Documentation**:
- ✅ All SKILL.md files comprehensive
- ✅ Agent workflow documented
- ✅ README provides clear usage instructions
- ✅ Prompt templates version-controlled

---

**Remember**: This is a **Claude Code agent project**, not a standalone Python application. The agent orchestrates skills that leverage Claude's LLM capabilities for unstructured data extraction and summarization. Every decision should demonstrate understanding of agent-based architectures and prompt engineering best practices.
