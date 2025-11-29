# Excel Feedback Integration Guide

## Overview

The RamiAutoGrader now supports **individual Excel feedback generation** for each student grading session. This allows you to run multiple grading instances in parallel and generate separate Excel files for each student.

---

## Quick Start

### Single Student Grading with Excel Output

```bash
# 1. Grade a repository
claude /skill grade-from-git
# URL: https://github.com/student/project.git
# Claimed grade: 80

# 2. Generate Excel feedback (after grading completes)
python scripts/create_single_student_excel.py \
  --student-name "Student Name" \
  --github-url "https://github.com/student/project.git" \
  --claimed-grade "80/100" \
  --actual-grade "87/100" \
  --status "PASSED" \
  --summary "Score: 87/100 (B). Excellent: Security, Documentation..." \
  --notes "Underestimated by 7 points"

# Output: results/Student_Name_Feedback.xlsx
```

---

## Parallel Grading Workflow

### Terminal 1: Grade Student A
```bash
cd /path/to/RamiAutoGrader
claude /skill grade-from-git
# Grade student A's repository
# Generate Excel: StudentA_Feedback.xlsx
```

### Terminal 2: Grade Student B
```bash
cd /path/to/RamiAutoGrader
claude /skill grade-from-git
# Grade student B's repository
# Generate Excel: StudentB_Feedback.xlsx
```

### Terminal 3: Grade Student C
```bash
cd /path/to/RamiAutoGrader
claude /skill grade-from-git
# Grade student C's repository
# Generate Excel: StudentC_Feedback.xlsx
```

**Result**: 3 independent Excel files in `results/` directory

---

## Excel File Structure

Each Excel file contains a single row with 7 columns:

| Column | Description | Example |
|--------|-------------|---------|
| **Student Name** | Extracted from repo or manual input | Omry Tzabbar |
| **GitHub URL** | Repository link (clickable) | [Link](https://github.com/...) |
| **Claimed Grade** | Student's self-assessment | 80/100 |
| **Actual Grade** | Auto-grader result | 87/100 |
| **Status** | PASSED or FAILED | PASSED |
| **Summary** | 2-3 sentence feedback | Score: 87/100 (B). Excellent: Security... |
| **Notes** | Comparison notes | Underestimated by 7 points |

### Formatting Features

- ✅ Header row: Bold, light blue background (#D9E1F2), centered
- ✅ Borders: Thin on all cells
- ✅ GitHub URL: Clickable hyperlink (blue, underlined)
- ✅ Summary column: Text wrapping enabled (80 chars wide)
- ✅ Professional fonts: Calibri 11pt
- ✅ File size: ~5-6 KB

---

## Command-Line Options

### Using CLI Arguments

```bash
python scripts/create_single_student_excel.py \
  --student-name "John Doe" \
  --github-url "https://github.com/johndoe/project" \
  --claimed-grade "85/100" \
  --actual-grade "92/100" \
  --status "PASSED" \
  --summary "Excellent work! Strong in all areas." \
  --notes "Exceeded expectations" \
  --output-dir "results/"
```

### Using JSON File

```bash
# Create JSON with grading data
cat > student_grading.json <<EOF
{
  "student_name": "Jane Smith",
  "github_url": "https://github.com/janesmith/project",
  "claimed_grade": "75/100",
  "actual_grade": "88/100",
  "status": "PASSED",
  "summary": "Score: 88/100 (B+). Excellent: Documentation, Testing. Needs work: Code Quality.",
  "notes": "Underestimated by 13 points"
}
EOF

# Generate Excel from JSON
python scripts/create_single_student_excel.py --json student_grading.json
```

---

## Integration with Claude Code Skill

### Using the `generate-excel-feedback` Skill

```bash
# After running all grading skills
claude /skill generate-excel-feedback

# The skill will:
# 1. Collect grading results from all previous skills
# 2. Generate a concise summary
# 3. Create the Excel file automatically
# 4. Output the file path
```

---

## Batch Processing Multiple Students

### Option 1: Sequential Processing

```bash
#!/bin/bash
# grade_all_students.sh

REPOS=(
  "https://github.com/student1/project"
  "https://github.com/student2/project"
  "https://github.com/student3/project"
)

CLAIMED_GRADES=(80 85 90)

for i in "${!REPOS[@]}"; do
  REPO="${REPOS[$i]}"
  CLAIMED="${CLAIMED_GRADES[$i]}"

  echo "Grading: $REPO"

  # Grade repository
  # (Manual: run grade-from-git skill)

  # Generate Excel
  # (Manual: run generate-excel-feedback skill)

  echo "Completed: $i"
done
```

### Option 2: Parallel Processing

```bash
#!/bin/bash
# grade_parallel.sh

REPOS=(
  "https://github.com/student1/project"
  "https://github.com/student2/project"
  "https://github.com/student3/project"
)

# Run in parallel (GNU parallel or xargs)
printf '%s\n' "${REPOS[@]}" | parallel -j 4 'echo "Grading {}"'

# Or manually: Open 4 terminals and grade 1 student per terminal
```

---

## Aggregating Results

After grading all students, you can aggregate individual Excel files:

### Manual Aggregation (Excel/Google Sheets)

1. Open first Excel file
2. Copy all rows from other Excel files
3. Paste into first file
4. Save as `FinalFeedback_All Students.xlsx`

### Python Aggregation Script (Future)

```python
# aggregate_excel_files.py (to be implemented)
import glob
from openpyxl import load_workbook, Workbook

def aggregate_excel_files(input_pattern="results/*_Feedback.xlsx"):
    """Combine all individual Excel files into one master file."""
    wb_master = Workbook()
    ws_master = wb_master.active

    # Copy header from first file
    # Copy all data rows from all files
    # Save as FinalFeedback_AllStudents.xlsx

    pass
```

---

## Troubleshooting

### Issue: Excel file not created

**Symptoms**: Script runs but no file in `results/`

**Solutions**:
```bash
# Check permissions
ls -ld results/
mkdir -p results
chmod 755 results

# Check Python version (need 3.8+)
python --version

# Verify openpyxl installed
pip install openpyxl
```

### Issue: Unicode errors on Windows

**Symptoms**: `UnicodeEncodeError: 'charmap' codec can't encode...`

**Solution**: Already fixed in script (removed emoji characters)

### Issue: Long summaries truncated

**Symptoms**: Summary text cut off in Excel

**Solution**: Summary column has text wrapping enabled. Adjust row height in Excel:
- Select row
- Right-click → Row Height
- Set to 50 or Auto

---

## File Locations

```
RamiAutoGrader/
├── scripts/
│   └── create_single_student_excel.py    # Main Excel generation script
├── .claude/
│   └── skills/
│       └── generate-excel-feedback/
│           └── SKILL.md                   # Claude Code skill
├── results/
│   ├── Student1_Feedback.xlsx            # Generated Excel files
│   ├── Student2_Feedback.xlsx
│   └── Student3_Feedback.xlsx
└── docs/
    └── EXCEL_FEEDBACK_INTEGRATION.md     # This file
```

---

## Example Output

**File**: `results/Omry_Tzabbar_Feedback.xlsx`

| Student Name | GitHub URL | Claimed Grade | Actual Grade | Status | Summary | Notes |
|--------------|------------|---------------|--------------|--------|---------|-------|
| Omry Tzabbar | [Link](https://github.com/OmryTzabbar1/RamiAutoGrader.git) | 80/100 | 87/100 | PASSED | Score: 87/100 (B). Excellent: Security (10/10), Documentation (25/25), Testing (15/15), UX (10/10). Strong: Git Workflow (9/10), Research (8/10). Needs work: Code Quality (20/30) - 2 files exceed 150-line limit. | Underestimated by 7 points |

---

## Next Steps

1. ✅ Single-student Excel generation implemented
2. ✅ Command-line interface working
3. ✅ Claude Code skill created
4. ⏳ Test with multiple students in parallel
5. ⏳ Create aggregation script (optional)
6. ⏳ Add to main README documentation

---

## Dependencies

- Python 3.8+
- openpyxl >= 3.1.0

Install with:
```bash
pip install openpyxl
```

---

**Last Updated**: 2025-11-29
**Status**: ✅ Ready for production use
