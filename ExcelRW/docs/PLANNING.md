# Technical Planning & Architecture Document
# Moodle Assignment Submission Automation System

**Version**: 1.0
**Date**: 2025-11-27
**Status**: Planning Complete → Ready for Development

---

## 1. System Overview

### 1.1 High-Level Architecture

The Moodle Assignment Submission Automation System is a **Skill-Based Architecture** built on Claude Code's skill framework. It automates the download and organization of student assignment submissions from Moodle LMS, integrating seamlessly with the existing RamiAutoGrader system.

**Core Components:**
1. **Authentication Layer**: Connect to Moodle (API or Selenium)
2. **Download Layer**: Fetch PDF submissions and metadata
3. **Extraction Layer**: Parse GitHub URLs from PDFs
4. **Organization Layer**: Create standardized folder structure
5. **Integration Layer**: Clone repos and trigger auto-grading

### 1.2 Architecture Style

**Skill-Based Microservices Architecture**

- **Pattern**: Each skill is an independent, composable unit with a single responsibility
- **Communication**: Skills communicate via filesystem (JSON metadata files)
- **Orchestration**: Manual (instructor invokes skills) or automated (shell script)
- **State Management**: File-based (metadata.json per assignment)

**Rationale**:
- ✅ **Modularity**: Each skill can be developed, tested, deployed independently
- ✅ **Reusability**: Skills can be reused across different courses/semesters
- ✅ **Maintainability**: Clear separation of concerns, easy to debug
- ✅ **Discoverability**: Skills are self-documenting via SKILL.md
- ✅ **Composability**: Can combine skills in different workflows

---

## 2. C4 Model Diagrams

### 2.1 Context Diagram (Level 1)

```
┌─────────────────┐
│   Instructor    │───────────┐
│  (Primary User) │           │
└─────────────────┘           │
                              │ Invokes Skills
                              ▼
┌─────────────────────────────────────────────┐
│                                             │
│  Moodle Submission Automation System        │
│                                             │
│  Downloads & organizes student assignments  │
│  from Moodle, integrates with auto-grader  │
│                                             │
└─────────────────────────────────────────────┘
        │                    │                │
        │                    │                │
        ▼                    ▼                ▼
┌──────────────┐    ┌──────────────┐  ┌─────────────────┐
│   Moodle LMS │    │  GitHub API  │  │ RamiAutoGrader  │
│  (External)  │    │  (External)  │  │   (Existing)    │
└──────────────┘    └──────────────┘  └─────────────────┘
```

**Description**:
- **Instructor** invokes Claude Code skills to automate submission downloads
- **System** connects to **Moodle** to fetch submissions, **GitHub** to clone repos, and **RamiAutoGrader** to grade projects
- All interactions are read-only except for local filesystem writes

---

### 2.2 Container Diagram (Level 2)

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Moodle Submission Automation System                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐      ┌──────────────────┐                    │
│  │  Claude Code     │      │  Helper Scripts  │                    │
│  │  Skills          │──────│  (Python)        │                    │
│  │  (SKILL.md)      │      │  - moodle_auth.py│                    │
│  │                  │      │  - download_pdfs │                    │
│  └──────────────────┘      │  - extract_urls  │                    │
│                            └──────────────────┘                    │
│                                     │                               │
│                                     │                               │
│                                     ▼                               │
│  ┌──────────────────────────────────────────┐                      │
│  │         Filesystem Storage               │                      │
│  │  Assignments/                            │                      │
│  │  ├── Assignment_01/                      │                      │
│  │  │   ├── metadata.json                   │                      │
│  │  │   └── student_*/                      │                      │
│  │  │       ├── submission.pdf              │                      │
│  │  │       └── repo/                       │                      │
│  └──────────────────────────────────────────┘                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
         │                      │                       │
         ▼                      ▼                       ▼
    ┌────────┐          ┌─────────────┐      ┌──────────────────┐
    │ Moodle │          │   GitHub    │      │  RamiAutoGrader  │
    │  API   │          │     API     │      │     System       │
    └────────┘          └─────────────┘      └──────────────────┘
```

**Description**:
- **Claude Code Skills**: User-facing layer (SKILL.md files), orchestrate workflow
- **Helper Scripts**: Python utilities for heavy lifting (Selenium, PDF parsing, file I/O)
- **Filesystem Storage**: Persistent storage of submissions in organized folder structure
- **External Services**: Moodle (source), GitHub (repos), RamiAutoGrader (grading engine)

---

### 2.3 Component Diagram (Level 3) - Download Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│         moodle-download-submissions Skill                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  SKILL.md ────┐                                                  │
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────┐     ┌──────────────────────┐         │
│   │  Orchestration      │────▶│  Authentication      │         │
│   │  Logic (Claude)     │     │  (moodle_auth.py)    │         │
│   └─────────────────────┘     └──────────────────────┘         │
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────┐     ┌──────────────────────┐         │
│   │  Download Manager   │────▶│  PDF Downloader      │         │
│   │  (download_pdfs.py) │     │  (requests/Selenium) │         │
│   └─────────────────────┘     └──────────────────────┘         │
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────┐     ┌──────────────────────┐         │
│   │  URL Extractor      │────▶│  PDF Parser          │         │
│   │(extract_github_urls)│     │  (PyPDF2/pdfplumber) │         │
│   └─────────────────────┘     └──────────────────────┘         │
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────┐     ┌──────────────────────┐         │
│   │  Folder Organizer   │────▶│  Filesystem Utils    │         │
│   │(organize_folders.py)│     │  (pathlib/os)        │         │
│   └─────────────────────┘     └──────────────────────┘         │
│               │                                                  │
│               ▼                                                  │
│   ┌─────────────────────┐                                       │
│   │  Metadata Writer    │                                       │
│   │  (JSON serializer)  │                                       │
│   └─────────────────────┘                                       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Component Responsibilities**:
- **Orchestration Logic**: SKILL.md instructions read by Claude, coordinates execution
- **Authentication**: Login to Moodle, maintain session
- **Download Manager**: Fetch PDFs from Moodle, handle retries
- **URL Extractor**: Parse GitHub URLs from PDF text
- **Folder Organizer**: Create `Assignments/Assignment_XX/student_YY/` structure
- **Metadata Writer**: Save student_id, github_url, self_grade to JSON

---

## 3. Architecture Decision Records (ADRs)

### ADR-001: Skill-Based vs Monolithic Script

**Status**: ✅ Accepted
**Date**: 2025-11-27

**Context**:
Need to decide whether to build this as:
- **Option A**: Single monolithic Python script
- **Option B**: Claude Code Skills (SKILL.md + helper scripts)

**Decision**: Use **Skill-Based Architecture** (Option B)

**Consequences**:
✅ **Pros**:
- Each skill is discoverable (`/skill <name>`)
- Self-documenting via SKILL.md
- Composable (can combine skills in different workflows)
- Testable in isolation
- Maintainable (clear separation of concerns)
- Aligns with parent RamiAutoGrader architecture

❌ **Cons**:
- More files to manage (SKILL.md + scripts)
- Requires understanding of Claude Code Skills framework
- Slight overhead in skill invocation vs direct script

**Alternatives Considered**:
| Alternative | Pros | Cons |
|-------------|------|------|
| Single Python script | Simple, one file | Hard to maintain, not composable, poor documentation |
| Flask web app | Nice UI, accessible from browser | Overkill, adds complexity, deployment overhead |
| Jupyter Notebook | Interactive, good for exploration | Not production-ready, hard to automate |

**Rationale**: Skill-based architecture wins because it aligns with project goals (modularity, reusability, academic excellence) and integrates naturally with existing RamiAutoGrader system.

---

### ADR-002: Moodle API vs Selenium Web Scraping

**Status**: ✅ Accepted (Hybrid Approach)
**Date**: 2025-11-27

**Context**:
Moodle can be accessed via:
- **Option A**: Moodle Web Services API (if enabled)
- **Option B**: Selenium browser automation (web scraping)

**Decision**: Implement **both**, prefer API, fall back to Selenium

```python
class MoodleClient:
    def __init__(self):
        if self._check_api_available():
            self.backend = MoodleAPIBackend()
        else:
            self.backend = MoodleSeleniumBackend()
```

**Consequences**:
✅ **Pros**:
- API: Fast, reliable, structured JSON responses
- Selenium: Works even if API disabled, handles SSO/complex auth
- Fallback ensures system works in all scenarios

❌ **Cons**:
- More code to maintain (two implementations)
- Need to test both paths

**Alternatives Considered**:
| Alternative | Pros | Cons |
|-------------|------|------|
| API-only | Clean, fast | Breaks if API disabled |
| Selenium-only | Always works | Slow, brittle, breaks on UI changes |
| Manual download | No code needed | Defeats purpose of automation |

**Rationale**: Hybrid approach provides best of both worlds - speed of API when available, robustness of Selenium as fallback.

---

### ADR-003: PDF Parsing Library Selection

**Status**: ✅ Accepted (Multi-Library Fallback with Hyperlink Extraction)
**Date**: 2025-11-27
**Updated**: 2025-11-27 (added hyperlink extraction priority)

**Context**:
Need to extract GitHub URLs from student submission PDFs. GitHub links are embedded as **clickable hyperlinks** (not plain text), which requires extracting PDF annotations rather than text parsing.

**Decision**: Use **multi-library fallback** strategy with **hyperlink extraction priority**:
1. Try PyPDF2/pikepdf first - extract hyperlinks from PDF annotations (fast, accurate)
2. If no hyperlinks found, try pdfplumber - search text for "github.com" patterns
3. If fails, try pdfminer - most thorough text extraction
4. If all fail, flag for manual review

**Consequences**:
✅ **Pros**:
- Handles diverse PDF formats
- Maximizes extraction success rate
- Degrades gracefully

❌ **Cons**:
- Dependency bloat (3 PDF libraries)
- Slower if fallbacks needed

**Alternatives Considered**:
| Alternative | Pros | Cons |
|-------------|------|------|
| PyPDF2 only | Lightweight | Fails on scanned/image PDFs |
| OCR (Tesseract) | Handles any PDF | Very slow, high error rate |
| Require text file | Simple | Extra burden on students |

**Rationale**: Multi-library fallback maximizes success rate while keeping reasonable performance.

---

### ADR-004: Folder Naming Convention

**Status**: ✅ Accepted
**Date**: 2025-11-27

**Context**:
Need to decide folder structure for organizing student submissions.

**Decision**:
```
Assignments/
├── Assignment_01/          # Zero-padded assignment number (01-12)
│   ├── metadata.json       # All students' metadata
│   ├── download_report.txt # Summary report
│   └── student_John_Doe/   # Student name (sanitized: underscores for spaces)
│       ├── submission.pdf
│       ├── metadata.json   # Individual student metadata
│       └── repo/           # Cloned GitHub repo
```

**Rationale**:
- **Zero-padding** (01-12): Ensures correct alphabetical sort order
- **Student name** in folder name: Human-readable, easy to navigate, matches instructor expectations
- **Name sanitization**: Replace spaces with underscores, remove special characters
- **Flat structure** (not nested): Easy to navigate, works with auto-grader
- **metadata.json at both levels**: Assignment-level summary + per-student details

**Alternatives Considered**:
| Alternative | Pros | Cons |
|-------------|------|------|
| Assignment1/ (no padding) | Shorter | Breaks sort order (1, 10, 11, 2, 3...) |
| student_12345678/ (ID) | Unique, no spaces | Not human-readable, privacy concerns |
| Nested by date | Chronological | Hard to find specific assignment |

**Update (2025-11-27)**: Changed from `student_id` to `student_name` based on user requirements for better readability.

---

### ADR-005: Metadata Format (JSON vs CSV vs YAML)

**Status**: ✅ Accepted (JSON)
**Date**: 2025-11-27

**Context**:
Need to store metadata (student_id, github_url, self_grade, etc.) for each submission.

**Decision**: Use **JSON** format

```json
{
  "assignment_number": 1,
  "students": [
    {
      "student_id": "12345678",
      "github_url": "https://github.com/user/repo",
      "self_grade": 85,
      "auto_grade": null,
      "download_status": "success"
    }
  ]
}
```

**Consequences**:
✅ **Pros**:
- Structured, supports nested data
- Native Python support (`json` module)
- Easy to parse in auto-grader
- Human-readable

❌ **Cons**:
- Slightly more verbose than CSV

**Alternatives Considered**:
| Alternative | Pros | Cons |
|-------------|------|------|
| CSV | Compact, Excel-compatible | No nested structure, quoting issues |
| YAML | Very readable | Whitespace-sensitive, parsing errors |
| SQLite | Queryable | Overkill for small dataset |

**Rationale**: JSON strikes best balance of structure, simplicity, and Python support.

---

### ADR-006: Adaptive Grading Strictness Based on Self-Grade

**Status**: ✅ Accepted
**Date**: 2025-11-27

**Context**:
Students submit self-assigned grades along with their projects. Higher self-grades require more critical evaluation to ensure accuracy and prevent grade inflation.

**Decision**: Implement **adaptive grading strictness algorithm**

**Formula**:
```python
base_strictness = 1.0
strictness_multiplier = 0.3  # Configurable in .env

grading_strictness = base_strictness + (self_grade / 100) * strictness_multiplier

# Examples:
# Self-grade = 70 → strictness = 1.0 + (70/100) * 0.3 = 1.21
# Self-grade = 85 → strictness = 1.0 + (85/100) * 0.3 = 1.255
# Self-grade = 95 → strictness = 1.0 + (95/100) * 0.3 = 1.285
```

**Implementation**:
```python
def calculate_grading_strictness(self_grade: int) -> float:
    """
    Calculate grading strictness multiplier based on self-grade.

    Higher self-grades → More critical evaluation
    - Standard strictness (1.0) for self-grade ≤ 70
    - Up to 1.3x strictness for self-grade = 100

    Args:
        self_grade: Student's self-assessed grade (0-100)

    Returns:
        Strictness multiplier (1.0 to 1.3)
    """
    base = float(os.getenv("GRADING_STRICTNESS_BASE", "1.0"))
    multiplier = float(os.getenv("GRADING_STRICTNESS_MULTIPLIER", "0.3"))

    return base + (self_grade / 100) * multiplier
```

**Integration with Auto-Grader**:
When invoking the auto-grader, pass strictness as parameter:
```python
result = grade_project(
    repo_path=student.repo_path,
    strictness=student.grading_strictness
)
```

The auto-grader will:
- Apply stricter penalty thresholds (e.g., -2 points per missing docstring instead of -1)
- Require higher test coverage (e.g., 80% instead of 70%)
- Be more critical of code quality violations

**Consequences**:
✅ **Pros**:
- Encourages accurate self-assessment
- Prevents grade inflation (students claiming 95+ must truly earn it)
- Fair: students who honestly assess lower grades get standard evaluation
- Configurable via `.env` (instructors can adjust multiplier)

❌ **Cons**:
- Adds complexity to grading logic
- May discourage students from being ambitious (mitigated by transparency)

**Alternatives Considered**:
| Alternative | Pros | Cons |
|-------------|------|------|
| Ignore self-grade | Simpler | Misses opportunity to validate student judgment |
| Fixed penalty for high self-grades | Simple | Not granular, discourages ambition |
| Use self-grade as baseline | Intuitive | Grade inflation, students game the system |

**Rationale**: Adaptive strictness balances fairness with accuracy. Students who claim excellence must demonstrate it, while average students aren't penalized for honesty.

---

## 4. Data Architecture

### 4.1 Data Models

**Student Submission Model**:
```python
@dataclass
class StudentSubmission:
    student_name: str              # Primary identifier (used for folder naming)
    github_url: str                # Extracted from PDF hyperlinks
    self_grade: int                # Self-assessed grade (0-100)
    grading_strictness: float      # Calculated strictness multiplier (1.0-1.3)
    submission_date: datetime
    pdf_path: str                  # Path to submission.pdf
    repo_path: Optional[str]       # Path to cloned repo (if GitHub URL found)
    auto_grade: Optional[int]      # Auto-grader score (null until graded)
    download_status: str           # "success", "failed", "partial"
    extraction_method: str         # "hyperlink", "text_search", or "manual"
    warnings: List[str]            # Any issues encountered

@dataclass
class AssignmentMetadata:
    assignment_number: int
    assignment_name: str
    total_students: int
    successful_downloads: int
    failed_downloads: int
    students: List[StudentSubmission]
    download_timestamp: datetime
```

### 4.2 Data Flow

```
Moodle → Download → Extract → Organize → Clone → Grade → Report
  ↓         ↓          ↓          ↓         ↓       ↓        ↓
 Auth    PDFs+meta  github_url  folders   repos  results  summary
```

**Stage-by-Stage Data**:
1. **Auth**: Session token
2. **Download**: PDF bytes + Moodle metadata
3. **Extract**: GitHub URL string
4. **Organize**: File paths in folder structure
5. **Clone**: Git repository on disk
6. **Grade**: JSON results from auto-grader
7. **Report**: Markdown summary

### 4.3 Data Storage

| Data Type | Storage | Retention | Access Pattern |
|-----------|---------|-----------|----------------|
| PDFs | Filesystem (`Assignments/Assignment_XX/student_YY/submission.pdf`) | Permanent (semester) | Write-once, read during grading |
| Metadata | JSON files | Permanent | Write-once, read for reporting |
| GitHub repos | Filesystem (cloned) | Permanent | Write-once, read during grading |
| Logs | Text files (`download.log`) | 1 semester | Append-only |
| Moodle credentials | .env file (encrypted) | Permanent | Read-only |

---

## 5. API Design

### 5.1 Moodle Web Services API

**If API enabled**, use these endpoints:

| Endpoint | Purpose | Request | Response |
|----------|---------|---------|----------|
| `/login/token.php` | Get auth token | `{username, password, service}` | `{token: "..."}` |
| `/webservice/rest/server.php` | Generic API call | `{wstoken, wsfunction, ...}` | JSON |
| Function: `core_course_get_courses` | List courses | `{wstoken}` | `[{id, fullname, ...}]` |
| Function: `mod_assign_get_assignments` | List assignments | `{courseids: [123]}` | `[{id, name, duedate, ...}]` |
| Function: `mod_assign_get_submissions` | Get submissions | `{assignmentids: [456]}` | `[{userid, status, ...}]` |
| Function: `core_files_get_files` | Download file | `{contextid, component, filearea, itemid, filepath, filename}` | Binary data |

**Example API Call (Python)**:
```python
import requests

def get_assignment_submissions(token, assignment_id):
    url = "https://moodle.university.edu/webservice/rest/server.php"
    params = {
        'wstoken': token,
        'wsfunction': 'mod_assign_get_submissions',
        'moodlewsrestformat': 'json',
        'assignmentids[0]': assignment_id
    }
    response = requests.get(url, params=params)
    return response.json()
```

### 5.2 Selenium Selectors (Fallback)

**If API unavailable**, use Selenium with these CSS selectors:

| Element | Selector | Purpose |
|---------|----------|---------|
| Login form | `#login form` | Submit credentials |
| Username field | `#username` | Enter username |
| Password field | `#password` | Enter password |
| Course link | `.course-link[data-course-id="123"]` | Navigate to course |
| Assignment list | `.activity.assign` | Find assignments |
| Submission link | `.submissionstatussubmitted a` | Download PDF |

**Selenium Error Handling**:
```python
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
except TimeoutException:
    logging.error("Login page did not load in time")
    raise MoodleConnectionError("Timeout waiting for login page")
```

---

## 6. Infrastructure & Deployment

### 6.1 Deployment Architecture

**Local Development Environment**:
```
Instructor's Machine
├── Python 3.9+
├── Chrome/Firefox browser (for Selenium)
├── Git
└── Claude Code CLI
```

**Dependencies**:
- Python libraries: Selenium, PyPDF2, pdfplumber, requests, beautifulsoup4
- System: ChromeDriver (for Selenium)

### 6.2 Environment Configuration

| Environment | Purpose | Config Source |
|-------------|---------|---------------|
| Development | Local testing | `.env.dev` |
| Production | Real courses | `.env` |

**No staging environment needed** (only one instructor, low risk)

### 6.3 Installation Script

```bash
#!/bin/bash
# install.sh

# Install Python dependencies
pip install -r requirements.txt

# Download ChromeDriver (for Selenium)
python scripts/setup_chromedriver.py

# Create folder structure
mkdir -p Assignments
mkdir -p prompts/{architecture,code-generation,testing,documentation}

# Copy environment template
cp config/.env.example .env

echo "Setup complete! Edit .env with your Moodle credentials."
```

---

## 7. Security Architecture

### 7.1 Authentication

**Moodle Credentials Storage**:
```python
import os
from cryptography.fernet import Fernet

# Load encryption key from secure location
key = os.environ.get("ENCRYPTION_KEY")
cipher = Fernet(key)

# Encrypt password before storing
encrypted_password = cipher.encrypt(password.encode())

# Decrypt when needed
password = cipher.decrypt(encrypted_password).decode()
```

### 7.2 Authorization

**Access Control**:
- Only authenticated instructors can run skills
- Skills check for valid Moodle session before proceeding
- No external network access except Moodle and GitHub

### 7.3 Data Protection

**Student Privacy**:
- All data stored locally (no cloud uploads)
- Student names not used in folder names (use IDs)
- PDFs not committed to Git (in `.gitignore`)
- Logs sanitized (no passwords, no personal info)

### 7.4 API Security

**Moodle API Token Handling**:
```python
# WRONG (hardcoded) ❌
MOODLE_TOKEN = "abc123def456"

# CORRECT (.env file) ✅
import os
from dotenv import load_dotenv

load_dotenv()
MOODLE_TOKEN = os.environ.get("MOODLE_API_TOKEN")
if not MOODLE_TOKEN:
    raise ValueError("MOODLE_API_TOKEN not set in .env")
```

---

## 8. Performance Considerations

### 8.1 Bottlenecks Identified

| Area | Bottleneck | Mitigation |
|------|------------|------------|
| PDF Download | Network I/O | Concurrent downloads (5 threads) |
| PDF Parsing | CPU-bound | Multi-library fallback (fail fast) |
| GitHub Cloning | Network I/O | Shallow clone (`--depth 1`) |
| Large PDFs (> 10 MB) | Memory | Stream processing, don't load entire PDF |

### 8.2 Caching Strategy

**Cache Moodle Session**:
```python
# Save session cookies to avoid repeated logins
import pickle

def save_session(session, filename="moodle_session.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(session.cookies, f)

def load_session(filename="moodle_session.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)
```

### 8.3 Scalability Strategy

**Handle Large Classes (100+ students)**:
- Use concurrent downloads (ThreadPoolExecutor)
- Paginate Moodle API calls if needed
- Process in batches of 20 students
- Show progress bar (`tqdm` library)

---

## 9. Monitoring & Observability

### 9.1 Logging

**Log Levels**:
- **DEBUG**: Detailed trace (Selenium actions, HTTP requests)
- **INFO**: High-level progress ("Downloading student 5/30...")
- **WARNING**: Non-fatal issues ("GitHub URL not found")
- **ERROR**: Failed operations ("PDF download failed after 3 retries")
- **CRITICAL**: System failures ("Moodle authentication failed")

**Log Format**:
```
2025-11-27 20:30:15 - moodle_download - INFO - Starting download for Assignment 5
2025-11-27 20:30:16 - moodle_download - INFO - Authenticated successfully
2025-11-27 20:30:20 - moodle_download - INFO - Downloading student 1/30...
2025-11-27 20:30:22 - moodle_download - WARNING - GitHub URL not found for student 12345678
2025-11-27 20:30:45 - moodle_download - INFO - Download complete: 28/30 successful
```

### 9.2 Metrics

**Track in `download_report.txt`**:
- Total students
- Successful downloads
- Failed downloads
- GitHub URLs found vs not found
- Average download time per student
- Errors encountered

**Example Report**:
```
Assignment 5 Download Report
Generated: 2025-11-27 20:45:00

Summary:
- Total Students: 30
- Successful Downloads: 28 (93.3%)
- Failed Downloads: 2 (6.7%)
- GitHub URLs Found: 27 (90.0%)
- Average Download Time: 5.2 seconds

Errors:
- student_11111111: PDF not found
- student_22222222: Network timeout after 3 retries

Warnings:
- student_33333333: GitHub URL not found in PDF (flagged for manual review)
```

### 9.3 Alerting

**Critical Alerts** (email instructor):
- Authentication failure (Moodle credentials invalid)
- > 20% download failure rate
- All downloads fail (Moodle down)

**Warning Alerts** (log only):
- GitHub URL not found (< 20% of students)
- Network slowness (> 10s per download)

---

## 10. Testing Strategy

### 10.1 Unit Tests

**Test Pyramid**:
```
      /\
     /  \  E2E (1)
    /────\
   / Unit  \ Integration (5)
  /  (15)   \
 /───────────\
```

**Unit Test Examples**:
```python
def test_extract_github_url_from_valid_pdf():
    url = extract_github_url("tests/fixtures/valid.pdf")
    assert url == "https://github.com/user/repo"

def test_extract_github_url_from_pdf_with_no_url():
    url = extract_github_url("tests/fixtures/no_url.pdf")
    assert url is None

def test_create_assignment_folder_structure():
    create_folders(assignment_num=1, student_ids=["123", "456"])
    assert os.path.exists("Assignments/Assignment_01/student_123")
    assert os.path.exists("Assignments/Assignment_01/student_456")
```

### 10.2 Integration Tests

**Test Full Workflow with Mock Moodle**:
```python
@pytest.fixture
def mock_moodle_server():
    # Start local Flask server simulating Moodle
    server = MockMoodleServer(port=5000)
    server.start()
    yield server
    server.stop()

def test_full_download_workflow(mock_moodle_server):
    # Test: authenticate → download → extract → organize
    result = download_assignment(
        moodle_url="http://localhost:5000",
        course_id="123",
        assignment_num=1
    )
    assert result.success == True
    assert len(result.students) == 3  # Mock server returns 3 students
    assert os.path.exists("Assignments/Assignment_01/metadata.json")
```

### 10.3 Edge Case Tests

```python
def test_pdf_with_multiple_github_urls():
    # Should return first URL
    url = extract_github_url("tests/fixtures/multiple_urls.pdf")
    assert url.startswith("https://github.com/")

def test_corrupted_pdf():
    # Should handle gracefully
    with pytest.raises(PDFReadError):
        extract_github_url("tests/fixtures/corrupted.pdf")

def test_network_timeout_retry():
    # Should retry 3 times
    with pytest.raises(NetworkError):
        download_with_retry(url="http://fake-url.com", max_retries=3)
```

---

## 11. Extensibility Design

### 11.1 Extension Points

| Extension Point | Purpose | Interface |
|-----------------|---------|-----------|
| PDF Parser | Support new PDF libraries | `def extract_text(pdf_path: str) -> str` |
| Moodle Backend | Add new Moodle versions | `class MoodleBackend(ABC)` with abstract methods |
| Metadata Format | Support XML, YAML | `class MetadataSerializer(ABC)` |
| Report Generator | Custom report formats | `def generate_report(data: dict, format: str) -> str` |

### 11.2 Plugin Architecture

**Allow custom extractors**:
```python
# plugins/custom_extractor.py
class CustomGitHubExtractor:
    def extract(self, pdf_path: str) -> Optional[str]:
        # Custom logic for specific PDF format
        pass

# Register plugin
register_extractor("custom", CustomGitHubExtractor())
```

---

## 12. Migration & Rollback Plan

**Migration from Manual to Automated**:
1. **Week 1**: Test with old assignment (known data)
2. **Week 2**: Run in parallel with manual (verify consistency)
3. **Week 3**: Use for new assignment, have manual backup ready
4. **Week 4+**: Fully automated, no manual process

**Rollback Plan**:
- If automation fails, instructor manually downloads from Moodle
- Logs provide audit trail of what failed
- Partial downloads can be resumed (skip already-downloaded students)

---

## 13. Future Enhancements (Out of Scope for V1)

- [ ] Web dashboard for monitoring downloads
- [ ] Email notifications when downloads complete
- [ ] Support for non-PDF submissions (Word docs, ZIP files)
- [ ] GitLab/Bitbucket support (not just GitHub)
- [ ] Automatic grade sync back to Moodle
- [ ] Parallel grading of multiple assignments
- [ ] Student-facing portal to view auto-grades

---

**Planning Status**: ✅ Complete - Ready to begin implementation (see TASKS.md)
