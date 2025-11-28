# ExcelFeedback - Excel Feedback Generation Layer

**Version**: 1.0.0

**Purpose**: Final layer that ties RamiAutoGrader together by generating instructor-facing Excel feedback sheets after auto-grading completes.

---

## Overview

ExcelFeedback is a Claude Code agent system that transforms grading results into professionally formatted Excel files for instructor review. It extracts student metadata from PDFs, generates concise feedback summaries, and creates formatted Excel workbooks with clickable hyperlinks and rich formatting.

**Architecture**: Agent-based orchestration (NOT Python script)

---

## Key Features

✅ **PDF Metadata Extraction**: Uses Claude API to extract student ID, name, partner name, and assignment name from unstructured PDF text

✅ **AI-Powered Summaries**: Generates 2-3 sentence feedback summaries (30-50 words) from detailed grading reports

✅ **Professional Excel Output**: Creates .xlsx files with:
- Rich formatting (headers, borders, colors, column widths)
- Clickable GitHub hyperlinks
- Text wrapping for long summaries
- Manual review flags for low-confidence extractions

✅ **Error Handling**: Gracefully handles missing PDFs, API failures, and low-confidence extractions

✅ **Integration**: Automatically triggered by RamiAutoGrader after grading completes

---

## Architecture

```
excel-feedback-generator (Agent)
├── extract-pdf-metadata (Skill)  → Extract student information
├── generate-summary (Skill)       → Create concise feedback
└── populate-excel (Skill)         → Generate formatted .xlsx
```

**Data Flow**:
```
Student PDFs → Claude API → Metadata
Grading Results → Claude API → Summary
Both → openpyxl → Excel File
```

---

## Installation

### Prerequisites

- Python 3.10+
- Claude Code CLI
- Anthropic API key

### Setup

```bash
# Navigate to ExcelFeedback directory
cd ExcelFeedback/

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
nano .env  # Add ANTHROPIC_API_KEY
```

**.env** file:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
CONFIDENCE_THRESHOLD=0.7
EXCEL_OUTPUT_DIR=results/
```

---

## Usage

### Automatic Execution (Recommended)

ExcelFeedback is automatically triggered by RamiAutoGrader after grading completes.

**No manual steps needed!**

---

### Manual Execution

If you need to regenerate Excel feedback manually:

```bash
cd agents/excel-feedback-generator/

# Run agent with Claude Code
claude-code run agent.yaml \
  --input grading_results_dir=../../results \
  --input pdf_submissions_dir=../../results \
  --input assignment_name="Design Patterns"
```

**Output**: `results/FinalFeedback_DesignPatterns.xlsx`

---

## Excel Output Structure

The generated Excel file contains 8 columns:

| Column | Source | Example |
|--------|--------|---------|
| Student ID | PDF extraction | 12345678 |
| Student Name | PDF extraction | John Doe |
| Partner Name | PDF extraction | Jane Smith |
| Assignment Name | PDF extraction | Design Patterns |
| GitHub URL | metadata.json | [Link](https://github.com/...) |
| Grade | grading_results.json | 77/100 |
| Summary | AI-generated | "Score: 77/100. Strong docs..." |
| Notes | Auto-flagged | LOW_CONFIDENCE_REVIEW |

**Formatting**:
- Header row: Bold, light blue background (#D9E1F2), centered
- Borders: Thin borders on all cells
- Column widths: Student ID (12), Summary (60)
- Text wrapping: Enabled for Summary column
- GitHub URL: Clickable hyperlink (blue, underlined)

---

## Manual Review Flags

The **Notes** column contains flags for records requiring instructor attention:

| Flag | Meaning | Action Required |
|------|---------|-----------------|
| `LOW_CONFIDENCE_REVIEW` | Metadata extraction confidence < 70% | Verify student ID, name, partner |
| `PDF_MISSING` | Student PDF not found | Check if student submitted PDF |
| `EXTRACTION_ERROR` | Claude API failed after retries | Manual data entry needed |
| *(empty)* | All data extracted successfully | No action needed |

---

## Project Structure

```
ExcelFeedback/
├── agents/
│   └── excel-feedback-generator/    # Main orchestrator agent
│       ├── agent.yaml                # Workflow definition
│       └── README.md                 # Agent documentation
│
├── skills/
│   ├── extract-pdf-metadata/         # PDF → Student info
│   │   ├── SKILL.md                  # Skill instructions
│   │   ├── skill.json                # Skill manifest
│   │   └── scripts/
│   │       └── extract_metadata.py   # Core implementation
│   │
│   ├── generate-summary/             # Grading report → Summary
│   │   ├── SKILL.md
│   │   ├── skill.json
│   │   └── scripts/
│   │       └── summarize_report.py
│   │
│   └── populate-excel/               # All data → Excel file
│       ├── SKILL.md
│       ├── skill.json
│       └── scripts/
│           └── create_excel.py
│
├── tests/
│   ├── unit/                         # Unit tests for skills
│   │   ├── test_extract_metadata.py
│   │   ├── test_generate_summary.py
│   │   └── test_populate_excel.py
│   └── fixtures/                     # Test data
│
├── config/
│   ├── .env.example                  # Environment template
│   └── agent_config.yaml             # Configuration settings
│
├── docs/
│   ├── PRD.md                        # Product requirements
│   ├── CLAUDE.md                     # Development guidelines
│   ├── PLANNING.md                   # Architecture & ADRs
│   └── TASKS.md                      # Task breakdown
│
├── results/                          # Output directory (auto-generated)
│   └── FinalFeedback_*.xlsx          # Generated Excel files
│
├── README.md                         # This file
├── requirements.txt                  # Python dependencies
└── .gitignore                        # Git ignore patterns
```

---

## Skills

### 1. extract-pdf-metadata

**Purpose**: Extract student metadata from PDFs using Claude API

**Features**:
- PDF text extraction (pdfplumber)
- Claude API for unstructured data parsing
- Confidence scoring (0.0-1.0)
- Flags low-confidence extractions

**Input**: `student_submission.pdf`

**Output**: `pdf_metadata.json`
```json
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns",
  "confidence": 0.95,
  "extraction_status": "SUCCESS"
}
```

**Performance**: ~4-7 seconds per student

---

### 2. generate-summary

**Purpose**: Generate 2-3 sentence feedback summaries

**Features**:
- Grading report JSON parsing
- Claude API for summarization
- Summary validation (30-50 words, professional tone)
- Handles perfect scores (100/100) and failing scores

**Input**: `grading_results.json`

**Output**: `summary.txt`
```
Score: 77/100. Strong documentation (25/25) and excellent security practices (10/10).
Code quality needs improvement: 2 files exceed 150-line limit. Increase test coverage from 67% to 70%.
```

**Performance**: ~2-5 seconds per student

---

### 3. populate-excel

**Purpose**: Create formatted Excel workbooks

**Features**:
- 8 columns with rich formatting
- Headers: Bold, light blue background, centered
- Clickable GitHub hyperlinks
- Text wrapping for long summaries
- Thin borders on all cells

**Input**: `student_data` (list of dictionaries)

**Output**: `FinalFeedback_DesignPatterns.xlsx`

**Performance**: ~0.3 seconds for 30 students

---

## Configuration

### Environment Variables

**Required**:
- `ANTHROPIC_API_KEY`: Claude API key from Anthropic

**Optional**:
- `CONFIDENCE_THRESHOLD`: Minimum confidence for auto-acceptance (default: 0.7)
- `EXCEL_OUTPUT_DIR`: Output directory path (default: results/)

---

### Agent Configuration

**File**: `config/agent_config.yaml`

**Key Settings**:
```yaml
agent:
  timeout: 600  # 10 minutes

skills:
  extract_pdf_metadata:
    timeout: 30
    confidence_threshold: 0.7
    model: claude-sonnet-4-5-20250929

  generate_summary:
    timeout: 20
    word_count:
      min: 30
      max: 50

  populate_excel:
    timeout: 60
    output_format: xlsx
```

---

## Performance

**Typical Execution Time** (30 students):

| Step | Sequential | Parallel (Future) |
|------|-----------|------------------|
| Extract metadata | 2-4 minutes | ~1 minute |
| Generate summaries | 1-3 minutes | ~30 seconds |
| Aggregate data | < 1 second | < 1 second |
| Create Excel | < 1 second | < 1 second |
| **Total** | **3-8 minutes** | **1-2 minutes** |

**Optimization**: Parallel processing of API calls (5 concurrent requests)

---

## Testing

### Run Unit Tests

```bash
# Run all tests
pytest tests/unit/

# Run with coverage
pytest tests/unit/ --cov=skills --cov-report=html

# Run specific test file
pytest tests/unit/test_extract_metadata.py -v
```

### Manual Testing

1. Grade a sample project with RamiAutoGrader
2. Verify `results/FinalFeedback_*.xlsx` created
3. Open in Microsoft Excel
4. Check formatting, hyperlinks, data accuracy

---

## Troubleshooting

### Issue: Excel file not created

**Symptoms**: Workflow completes but no Excel file found

**Solutions**:
```bash
# Check permissions
ls -ld results/

# Check logs
cat results/excel_generation_errors.log

# Verify dependencies installed
pip install -r requirements.txt
```

---

### Issue: "LOW_CONFIDENCE_REVIEW" for many students

**Symptoms**: > 50% of students flagged

**Causes**:
- PDFs have inconsistent formatting
- Student IDs not 8 digits
- Partner names missing (solo projects)

**Solutions**:
- Update PDF extraction prompt in `extract_metadata.py`
- Adjust confidence threshold in `agent_config.yaml`
- For solo projects, accept "NOT_FOUND" for partner_name

---

### Issue: Claude API rate limits

**Symptoms**: "Error: Failed to generate summary after 3 attempts"

**Solutions**:
- Reduce concurrent requests in `agent_config.yaml`
- Add rate limiting: 45 requests/minute (leave buffer)

---

## Development

### Code Quality Standards

- **File size limit**: 150 lines maximum (strictly enforced)
- **Docstrings**: Required on all functions/classes/modules
- **Test coverage**: 70%+ overall, 90%+ for critical paths
- **No hardcoded secrets**: Use environment variables
- **Git commits**: 15-20+ commits showing progression

### Running Quality Checks

```bash
# Linting
flake8 skills/

# Type checking
mypy skills/

# Test coverage
pytest --cov=skills --cov-report=term-missing
```

---

## Documentation

### Key Documents

- **PRD.md**: Product requirements and objectives
- **CLAUDE.md**: Development guidelines (agent architecture, code standards)
- **PLANNING.md**: Architecture diagrams and ADRs
- **TASKS.md**: Task breakdown (34 tasks across 4 phases)

### Architecture Decision Records (ADRs)

- **ADR-001**: Agent vs Python script (agent selected)
- **ADR-002**: Claude API for metadata extraction
- **ADR-003**: Excel format vs CSV/JSON
- **ADR-004**: Prompt-based orchestration
- **ADR-005**: Confidence scoring for manual review
- **ADR-006**: Post-grading hook integration

---

## Dependencies

**Python Packages** (from `requirements.txt`):
- `anthropic>=0.40.0` - Claude API client
- `pdfplumber>=0.10.0` - PDF text extraction
- `openpyxl>=3.1.0` - Excel generation
- `python-dotenv>=1.0.0` - Environment variables
- `pytest>=7.0.0` - Testing framework

---

## Contributing

### Development Workflow

1. Create feature branch
2. Implement changes (follow 150-line limit)
3. Write unit tests (70%+ coverage)
4. Run quality checks (flake8, mypy)
5. Commit frequently (clear messages)
6. Submit for review

---

## License

Academic project for M.Sc. Computer Science program.

---

## Support

**Documentation**: See `docs/` directory

**Issues**: Report to project maintainer

**Questions**: Refer to skill SKILL.md files and agent README.md

---

**Last Updated**: 2025-11-28

**Status**: Phase 1 & 2 Complete (Skills + Agent) | Phase 3 Pending (Integration Testing)
