# CLAUDE.md - Moodle Integration Development Guidelines

## Project Overview

**Moodle Assignment Submission Automation System** - A Claude Code Skills package that automates downloading student assignment submissions from Moodle, organizing them into a standardized folder structure, and integrating with the existing RamiAutoGrader system.

**Parent Project**: RamiAutoGrader
**Location**: `C:\Users\Guest1\CoOp\RamiAutoGrader\ExcelRW\`
**Architecture**: Claude Code Skills (not agents)

---

## CRITICAL REQUIREMENTS - Read This First

### Git Workflow (MANDATORY)

**⚠️ NEVER make just one commit** - Multiple commits throughout development are REQUIRED.

- Commit after each logical unit of work (skill completion, helper script, test, etc.)
- **Minimum 10-15 commits** for this project showing clear progression
- Each commit message must follow: `<type>(<scope>): <description> [TASK-ID]`
- Reference task IDs in commits: e.g., `feat(moodle): Add authentication skill [P2.1.1]`

**Good Commit Progression Example:**
```
feat: Initialize ExcelRW project structure with docs/
docs: Complete PRD for Moodle integration system
feat(skills): Add moodle-authenticate skill stub [P2.1.1]
feat(scripts): Implement moodle_auth.py helper [P2.1.1]
test(moodle): Add authentication tests [P3.1.1]
feat(skills): Add moodle-download-submissions skill [P2.2.1]
feat(scripts): Implement PDF download helper [P2.2.1]
feat(scripts): Add GitHub URL extraction from PDFs [P2.2.2]
refactor(scripts): Split download logic into smaller functions
test(download): Add tests for folder organization [P3.1.2]
docs(prompts): Document Selenium automation prompts
fix(download): Handle network timeout errors gracefully
feat(integration): Connect download skill to auto-grader [P2.3.1]
docs: Update README with Moodle setup instructions
chore: Add Selenium and PyPDF2 to requirements.txt
```

### Prompt Documentation (MANDATORY)

**📝 SAVE EVERY SIGNIFICANT PROMPT** to the `prompts/` directory as you work!

**Required Structure:**
```
ExcelRW/prompts/
├── README.md                           # Lessons learned, best practices
├── architecture/
│   ├── 001-skill-vs-script-design.md   # Why skills + helper scripts
│   ├── 002-folder-structure-design.md  # Assignments/Assignment_XX/ structure
│   └── 003-moodle-api-vs-selenium.md   # Decision: API or web scraping
├── code-generation/
│   ├── 001-selenium-moodle-navigation.md
│   ├── 002-pdf-github-url-extraction.md
│   ├── 003-batch-file-download.md
│   └── 004-error-handling-retry-logic.md
├── testing/
│   ├── 001-mock-moodle-responses.md
│   └── 002-integration-test-strategy.md
└── documentation/
    └── 001-skill-md-structure.md
```

**Each prompt file must include:**
- **Context**: Why you needed this prompt
- **Prompt Text**: Exact prompt used
- **Output Received**: What Claude generated
- **Iteration Notes**: What worked, what needed refinement
- **Lessons Learned**: Best practices for future

---

## Code Quality Standards

### File Size Limits (STRICTLY ENFORCED)

**Maximum file length: 150 lines** - **NO EXCEPTIONS**

When a file exceeds 150 lines:
1. Identify logical boundaries
2. Extract into separate modules
3. Use clear imports

**Example:**
```python
# BEFORE: moodle_downloader.py (280 lines) ❌

# AFTER: Refactor into focused modules ✅
scripts/
├── moodle_auth.py          # 95 lines - Authentication only
├── moodle_download.py      # 120 lines - Download logic
├── pdf_parser.py           # 65 lines - GitHub URL extraction
└── folder_organizer.py     # 80 lines - Create folder structure
```

### Code Organization

**Mandatory Directory Structure:**
```
ExcelRW/
├── .claude/
│   └── skills/
│       ├── moodle-authenticate/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── moodle_auth.py
│       ├── moodle-list-assignments/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── list_assignments.py
│       ├── moodle-download-submissions/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       ├── download_pdfs.py
│       │       ├── extract_github_urls.py
│       │       └── organize_folders.py
│       ├── github-clone-repos/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── batch_clone.py
│       └── generate-submission-report/
│           ├── SKILL.md
│           └── templates/
│               └── report_template.md
├── src/
│   ├── utils/
│   │   ├── moodle_client.py    # Reusable Moodle API/Selenium wrapper
│   │   ├── pdf_utils.py        # PDF parsing utilities
│   │   └── folder_utils.py     # Folder creation utilities
│   └── config/
│       └── moodle_config.py    # Configuration loader
├── tests/
│   ├── unit/
│   │   ├── test_moodle_auth.py
│   │   ├── test_pdf_extraction.py
│   │   └── test_folder_organization.py
│   ├── integration/
│   │   └── test_full_download_workflow.py
│   └── fixtures/
│       ├── sample_moodle_html/
│       └── sample_pdfs/
├── data/
│   └── .gitkeep               # Placeholder (data is in Assignments/)
├── Assignments/               # OUTPUT: All downloaded submissions
│   ├── .gitignore             # Ignore all downloaded content
│   └── README.md              # Explain folder structure
├── docs/
│   ├── PRD.md
│   ├── CLAUDE.md
│   ├── PLANNING.md
│   ├── TASKS.md
│   └── API.md                 # Moodle API endpoints used
├── prompts/                   # Prompt engineering log
│   ├── README.md
│   ├── architecture/
│   ├── code-generation/
│   ├── testing/
│   └── documentation/
├── config/
│   ├── .env.example           # Moodle credentials template
│   └── moodle_settings.yaml   # Course IDs, assignment mappings
├── README.md
├── requirements.txt
├── .env                       # Moodle credentials (GITIGNORED)
└── .gitignore
```

### Naming Conventions

**Python (primary language):**
- **Files**: `snake_case.py` (e.g., `moodle_auth.py`, `pdf_parser.py`)
- **Classes**: `PascalCase` (e.g., `MoodleClient`, `AssignmentDownloader`)
- **Functions/Methods**: `snake_case` (e.g., `download_submission()`, `extract_github_url()`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES = 3`, `ASSIGNMENTS_DIR = "Assignments"`)
- **Variables**: `snake_case` (e.g., `github_url`, `student_id`)

**SKILL.md files**: `kebab-case.md` (e.g., `moodle-authenticate/SKILL.md`)

---

## Documentation Requirements

### Every Function Must Have Docstrings

```python
def extract_github_url_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract GitHub repository URL from student submission PDF.

    Searches PDF text for patterns matching GitHub repository URLs.
    Handles cases where URL is hyperlinked or plain text.

    Args:
        pdf_path: Absolute path to PDF file

    Returns:
        GitHub URL if found, None if not found

    Raises:
        FileNotFoundError: If PDF file does not exist
        PDFReadError: If PDF is corrupted or unreadable

    Example:
        >>> url = extract_github_url_from_pdf("student_123/submission.pdf")
        >>> print(url)
        https://github.com/student123/project-repo
    """
```

### Every SKILL.md Must Follow This Structure

```markdown
# [Skill Name] Skill

## Purpose
[One sentence: What this skill does]

## When to Use
[When instructor should invoke this skill]

## Prerequisites
- [What must be set up before running]
- [e.g., Moodle credentials in .env]

## Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| course_id | string | Yes | - | Moodle course ID |
| assignment_num | int | Yes | - | Assignment number (1-12) |

## Instructions

### Step 1: [First Action]
[Detailed instructions for Claude to follow]

```bash
# Example command
python scripts/moodle_auth.py --course-id=12345
```

### Step 2: [Second Action]
[Continue with detailed steps...]

## Output

**Files Created:**
- `Assignments/Assignment_XX/download_report.txt`
- `Assignments/Assignment_XX/metadata.json`
- `Assignments/Assignment_XX/student_YYYY/submission.pdf`

**Success Criteria:**
- All submissions downloaded
- GitHub URLs extracted
- No errors in download_report.txt

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| AuthenticationError | Invalid Moodle credentials | Check .env file |
| NetworkError | Connection timeout | Retry with exponential backoff |
| PDFNotFoundError | Student didn't upload PDF | Log warning, skip student |

## Example Usage

```bash
# Invoke skill
/skill moodle-download-submissions

# When prompted, provide:
# Course ID: 54321
# Assignment Number: 5
```

## Integration Points

**Upstream**: [What calls this skill]
**Downstream**: [What this skill calls]
**Output Used By**: [Which other skills/systems consume this output]
```

---

## Configuration Management

### Environment Variables (.env)

**NEVER hardcode Moodle credentials!**

```bash
# .env (GITIGNORED)
MOODLE_URL=https://moodle.university.edu
MOODLE_USERNAME=instructor@university.edu
MOODLE_PASSWORD=your_secure_password_here
MOODLE_API_TOKEN=abc123def456...  # If using API instead of scraping

# Optional: GitHub access for private repos
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Configuration
ASSIGNMENTS_DIR=Assignments
MAX_RETRIES=3
DOWNLOAD_TIMEOUT=30
```

**Create .env.example:**
```bash
# .env.example (COMMITTED TO GIT)
MOODLE_URL=https://moodle.your-university.edu
MOODLE_USERNAME=your_username
MOODLE_PASSWORD=your_password
MOODLE_API_TOKEN=your_api_token_if_using_api

GITHUB_TOKEN=your_github_token_for_private_repos

ASSIGNMENTS_DIR=Assignments
MAX_RETRIES=3
DOWNLOAD_TIMEOUT=30
```

### Configuration Files

**`config/moodle_settings.yaml`:**
```yaml
# Course Configuration
course_id: "54321"
course_name: "Advanced Software Engineering"
semester: "Fall 2025"

# Assignment Configuration
assignments:
  - number: 1
    name: "Design Patterns Implementation"
    moodle_assignment_id: "12345"
  - number: 2
    name: "Testing and CI/CD"
    moodle_assignment_id: "12346"
  # ... up to 12

# Download Settings
max_concurrent_downloads: 5
retry_attempts: 3
retry_delay_seconds: 5

# Folder Naming
student_folder_pattern: "student_{student_id}"
assignment_folder_pattern: "Assignment_{number:02d}"
```

---

## Testing Requirements

### Coverage Targets
- **Minimum**: 70% code coverage
- **Critical paths** (authentication, download, PDF parsing): 90%+
- **Helper scripts**: 80%+

### Test Types Required

1. **Unit Tests** - Test each function in isolation
   ```python
   def test_extract_github_url_from_pdf_success():
       """Test GitHub URL extraction from valid PDF."""
       pdf_path = "tests/fixtures/sample_pdfs/valid_submission.pdf"
       url = extract_github_url_from_pdf(pdf_path)
       assert url == "https://github.com/testuser/testrepo"
   ```

2. **Edge Case Tests**
   ```python
   def test_extract_github_url_multiple_urls_in_pdf():
       """Test extraction when PDF has multiple GitHub URLs."""
       pdf_path = "tests/fixtures/sample_pdfs/multiple_urls.pdf"
       url = extract_github_url_from_pdf(pdf_path)
       # Should return first URL found
       assert url is not None
   ```

3. **Error Handling Tests**
   ```python
   def test_download_submission_network_timeout():
       """Test retry logic when network times out."""
       with pytest.raises(NetworkError):
           download_submission(url="http://fake-moodle.com", timeout=0.001)
   ```

4. **Integration Tests**
   ```python
   def test_full_download_workflow():
       """Test complete workflow: authenticate → download → organize."""
       # Use mock Moodle server or recorded HTTP responses
       result = run_full_download(course_id="12345", assignment_num=1)
       assert result.success == True
       assert len(result.students) > 0
       assert os.path.exists("Assignments/Assignment_01/metadata.json")
   ```

### Mocking External Services

**Use `responses` library to mock Moodle HTTP calls:**
```python
import responses

@responses.activate
def test_moodle_authentication_success():
    responses.add(
        responses.POST,
        "https://moodle.university.edu/login/index.php",
        json={"success": True, "session_id": "abc123"},
        status=200
    )

    client = MoodleClient()
    success = client.authenticate("user", "pass")
    assert success == True
```

---

## Error Handling

### Required Practices

1. **Defensive Programming**: Validate all inputs
   ```python
   def download_submission(student_id: str, assignment_num: int):
       if not student_id or not student_id.isdigit():
           raise ValueError(f"Invalid student_id: {student_id}")
       if assignment_num < 1 or assignment_num > 12:
           raise ValueError(f"Assignment number must be 1-12, got {assignment_num}")
   ```

2. **Retry Logic with Exponential Backoff**
   ```python
   import time

   MAX_RETRIES = 3

   def download_with_retry(url: str) -> bytes:
       for attempt in range(MAX_RETRIES):
           try:
               response = requests.get(url, timeout=30)
               response.raise_for_status()
               return response.content
           except requests.RequestException as e:
               if attempt == MAX_RETRIES - 1:
                   raise NetworkError(f"Failed after {MAX_RETRIES} attempts: {e}")
               delay = 2 ** attempt  # 1s, 2s, 4s
               logging.warning(f"Attempt {attempt+1} failed, retrying in {delay}s...")
               time.sleep(delay)
   ```

3. **Graceful Degradation**
   ```python
   def extract_github_url_from_pdf(pdf_path: str) -> Optional[str]:
       try:
           url = _extract_with_pypdf2(pdf_path)
           if url:
               return url
       except Exception as e:
           logging.warning(f"PyPDF2 failed, trying pdfplumber: {e}")

       try:
           url = _extract_with_pdfplumber(pdf_path)
           if url:
               return url
       except Exception as e:
           logging.error(f"Both PDF parsers failed: {e}")

       return None  # Manual review needed
   ```

4. **Detailed Logging**
   ```python
   import logging

   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('Assignments/download.log'),
           logging.StreamHandler()
       ]
   )

   logger = logging.getLogger(__name__)

   logger.info(f"Starting download for Assignment {assignment_num}")
   logger.warning(f"GitHub URL not found for student {student_id}")
   logger.error(f"Authentication failed: {error_message}")
   ```

---

## Git Practices

### IMPORTANT: Frequent Commits Required

- **NEVER make just one large commit** - this is unacceptable!
- Make **multiple commits throughout development** as you complete each logical unit of work
- Commit after completing each skill, helper script, test file, or documentation update
- Each commit should represent a single logical change
- Aim for **10-15+ commits minimum** for this project
- Build up a clear history showing evolution from planning → development → testing → deployment

### Commit Message Format

```
<type>(<scope>): <short description> [TASK-ID]

<optional longer description>

<optional references to issues/tasks>
```

**Types:**
- `feat`: New skill or helper script
- `fix`: Bug fix
- `docs`: Documentation changes (SKILL.md, README, prompts)
- `test`: Adding or updating tests
- `refactor`: Code restructuring (no behavior change)
- `chore`: Dependencies, config files, .gitignore

**Examples:**
```bash
feat(skills): Add moodle-authenticate skill with login flow [P2.1.1]
feat(scripts): Implement PDF GitHub URL extraction [P2.2.2]
test(download): Add unit tests for folder organization [P3.1.2]
docs(prompts): Document Selenium automation strategy [P5.2.1]
fix(auth): Handle session timeout with token refresh [P2.1.1]
refactor(download): Split 200-line script into 4 modules [P2.2.1]
chore: Add Selenium and PyPDF2 to requirements.txt
```

---

## Special Considerations for Moodle Integration

### 1. Selenium vs Moodle API

**Decision:** Try Moodle API first, fall back to Selenium if unavailable.

**Moodle API Pros:**
- More reliable (structured JSON responses)
- Faster (no browser overhead)
- Less brittle (API stable across Moodle versions)

**Selenium Pros:**
- Works even if API disabled
- Can handle complex authentication flows (SSO)
- Can capture screenshots for debugging

**Implementation:**
```python
class MoodleClient:
    def __init__(self):
        self.api_available = self._check_api_availability()
        if self.api_available:
            self.backend = MoodleAPIBackend()
        else:
            self.backend = MoodleSeleniumBackend()
```

### 2. PDF Parsing Strategies

**Approach:** Hyperlink extraction first, then text search fallback

**Important**: GitHub URLs are embedded as **clickable hyperlinks** in PDFs, not plain text!

```python
def extract_github_url(pdf_path: str) -> Tuple[Optional[str], str]:
    """
    Extract GitHub URL from PDF.

    Returns:
        (url, extraction_method) where method is "hyperlink", "text_search", or "manual"
    """
    # Try 1: Extract hyperlinks from PDF annotations (PyPDF2/pikepdf)
    url = _extract_hyperlinks(pdf_path)
    if url:
        return (url, "hyperlink")

    # Try 2: Text search as fallback (pdfplumber)
    url = _try_pdfplumber_text_search(pdf_path)
    if url:
        return (url, "text_search")

    # Try 3: pdfminer (most thorough text extraction)
    url = _try_pdfminer(pdf_path)
    if url:
        return (url, "text_search")

    # Give up, flag for manual review
    return (None, "manual")
```

### 3. Concurrent Downloads

**Use ThreadPoolExecutor for parallel downloads:**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_all_submissions(students, assignment_num):
    results = []
    max_workers = 5  # Don't overwhelm Moodle

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_student_submission, s, assignment_num): s
            for s in students
        }

        for future in as_completed(futures):
            student = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logging.error(f"Failed for {student.id}: {e}")

    return results
```

### 4. Folder Organization Best Practices

**Create all folders upfront:**

```python
def create_assignment_structure(assignment_num: int, students: List[Student]):
    base_dir = Path(f"Assignments/Assignment_{assignment_num:02d}")
    base_dir.mkdir(parents=True, exist_ok=True)

    for student in students:
        student_dir = base_dir / f"student_{student.id}"
        student_dir.mkdir(parents=True, exist_ok=True)

        # Create placeholder files
        (student_dir / ".gitkeep").touch()

    logging.info(f"Created folder structure for {len(students)} students")
```

---

## Integration with RamiAutoGrader

### Workflow After Download

```python
# After downloads complete, trigger auto-grading
def grade_all_submissions(assignment_num: int):
    metadata_file = f"Assignments/Assignment_{assignment_num:02d}/metadata.json"
    with open(metadata_file) as f:
        data = json.load(f)

    for student in data['students']:
        if student['github_url'] != "NOT_FOUND":
            # Clone repo
            clone_repo(student['github_url'], student['repo_path'])

            # Run auto-grader (from parent RamiAutoGrader system)
            result = grade_project(student['repo_path'])

            # Save results
            save_grading_results(student, result)

            # Compare with self-grade
            if abs(result['score'] - student['self_grade']) > 10:
                flag_discrepancy(student, result)
```

---

## Quality Checklist Before Completion

### Code Quality
- [ ] All files under 150 lines (use `find . -name "*.py" -exec wc -l {} \; | awk '{if ($1 > 150) print}'`)
- [ ] Docstrings on all functions/classes
- [ ] No hardcoded Moodle credentials (check with `grep -r "password"`)
- [ ] 70%+ test coverage (`pytest --cov=src`)
- [ ] Error handling for all external calls (Moodle, filesystem, GitHub)

### Git & Version Control
- [ ] 10-15+ commits showing clear progression
- [ ] Each commit follows `<type>(<scope>): <description>` format
- [ ] Commits reference task IDs from TASKS.md
- [ ] No sensitive data in git history (`git log -p | grep -i password`)

### Documentation
- [ ] README explains Moodle setup process
- [ ] All SKILL.md files complete with examples
- [ ] prompts/ directory has 5+ documented prompts
- [ ] prompts/README.md has lessons learned
- [ ] .env.example has all required variables

### Testing
- [ ] Unit tests for authentication, download, PDF parsing
- [ ] Integration test for full workflow
- [ ] Test with sample Moodle course (old assignments)
- [ ] Edge case tests (missing PDF, invalid GitHub URL, network errors)

### Security
- [ ] .env in .gitignore
- [ ] No API keys in code
- [ ] Student data stays local (not uploaded anywhere)
- [ ] Moodle credentials encrypted at rest (if stored)

---

## Deployment Checklist

Before using on real assignments:

- [ ] Test with past assignment (known good data)
- [ ] Verify folder structure matches expected format
- [ ] Check GitHub URL extraction accuracy (> 95%)
- [ ] Run on small batch (5-10 students) first
- [ ] Generate summary report, verify student count
- [ ] Dry run auto-grading on 2-3 repos
- [ ] Document any manual steps needed
- [ ] Create troubleshooting guide for common errors

---

**Remember**: This is part of an academic project. Every decision should demonstrate professional software engineering practices, thorough testing, and comprehensive documentation.
