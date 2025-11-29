# Generate Excel Feedback Skill

Creates a professionally formatted Excel file with grading results for a single student.

**Purpose**: Convert grading results into an instructor-facing Excel feedback sheet.

**Scoring**: N/A (output generation, not grading)

## Instructions

### 1. Collect Grading Data

Gather all grading results from the previous skills:
- Security score
- Code quality score
- Documentation score
- Testing score
- Git workflow score
- Research score
- UX score
- Total score and grade

### 2. Extract Student Information

From the grading context, extract:
- Student name (from GitHub URL or repository name)
- GitHub repository URL
- Claimed grade (if provided)
- Actual grade (calculated total)

### 3. Generate Summary

Create a concise 2-3 sentence summary highlighting:
- Total score and letter grade
- Categories where student excelled (perfect or near-perfect scores)
- Categories needing improvement (below 70% or with violations)
- Quick win recommendations (easy fixes for biggest impact)

**Format**:
```
Score: X/100 (Grade). Excellent: [perfect categories]. Strong: [good categories].
Needs work: [weak categories] - specific issue. Quick fix to improve score.
```

**Example**:
```
Score: 87/100 (B). Excellent: Security (10/10), Documentation (25/25), Testing (15/15), UX (10/10).
Strong: Git Workflow (9/10), Research (8/10). Needs work: Code Quality (20/30) - 2 files exceed 150-line limit.
Refactor detailed_reporter.py (298 lines) and execution_tracer.py (209 lines) to reach 96%.
```

### 4. Prepare Excel Data

Create a dictionary with all required fields:

```python
student_data = {
    "student_name": "Student Name",
    "github_url": "https://github.com/user/repo",
    "claimed_grade": "80/100" or "Not specified",
    "actual_grade": "87/100",
    "status": "PASSED" or "FAILED",
    "summary": "Generated summary from step 3",
    "notes": "Underestimated by 7 points" or ""
}
```

### 5. Call Python Script

Use the Bash tool to call the Excel generation script:

```bash
cd C:/Users/Guest1/CoOp/RamiAutoGrader
python scripts/create_single_student_excel.py \
  --student-name "Student Name" \
  --github-url "https://github.com/user/repo" \
  --claimed-grade "80/100" \
  --actual-grade "87/100" \
  --status "PASSED" \
  --summary "Summary text" \
  --notes "Notes text"
```

OR create a temporary JSON file and pass it:

```bash
# Create JSON with student data
cat > /tmp/student_grading.json <<EOF
{
  "student_name": "Omry Tzabbar",
  "github_url": "https://github.com/OmryTzabbar1/RamiAutoGrader.git",
  "claimed_grade": "80/100",
  "actual_grade": "87/100",
  "status": "PASSED",
  "summary": "Score: 87/100...",
  "notes": "Underestimated by 7 points"
}
EOF

# Generate Excel
python scripts/create_single_student_excel.py --json /tmp/student_grading.json
```

### 6. Verify Output

Check that Excel file was created:

```bash
ls -lh results/*_Feedback.xlsx
```

### 7. Report Results

Output the path to the created Excel file:

```
✅ Excel feedback generated successfully!

File: results/StudentName_Feedback.xlsx
Size: 5.7 KB

The Excel file contains:
- Student name and GitHub link
- Claimed vs actual grade comparison
- Pass/fail status
- Detailed summary of strengths and weaknesses
- Notes for instructor review

You can open this file in Microsoft Excel or Google Sheets.
```

## Success Criteria

- ✅ Excel file created with correct filename
- ✅ File contains all 7 columns with proper formatting
- ✅ GitHub URL is clickable hyperlink
- ✅ Summary is wrapped and readable
- ✅ Headers are bold with blue background
- ✅ All cells have borders

## Example Usage

```bash
# After running all grading skills
/skill generate-excel-feedback

# Provide grading context (from previous skills):
# - Total score: 87/100
# - GitHub URL: https://github.com/OmryTzabbar1/RamiAutoGrader.git
# - Claimed grade: 80/100
# - Student name: Omry Tzabbar

# Output: results/Omry_Tzabbar_Feedback.xlsx
```

## Output Format

The generated Excel file has 7 columns:

| Column | Example Value |
|--------|---------------|
| Student Name | Omry Tzabbar |
| GitHub URL | [Link](https://github.com/...) |
| Claimed Grade | 80/100 |
| Actual Grade | 87/100 |
| Status | PASSED |
| Summary | Score: 87/100 (B). Excellent: Security... |
| Notes | Underestimated by 7 points |

**Formatting**:
- Header row: Bold, light blue (#D9E1F2), centered
- Borders: Thin on all cells
- GitHub URL: Clickable hyperlink (blue, underlined)
- Summary column: Text wrapping enabled (80 chars wide)
- File size: ~5-6 KB

## Error Handling

**Issue**: Python script not found

**Solution**:
```bash
# Check if script exists
ls scripts/create_single_student_excel.py

# If missing, the script should be at:
# C:/Users/Guest1/CoOp/RamiAutoGrader/scripts/create_single_student_excel.py
```

**Issue**: openpyxl not installed

**Solution**:
```bash
pip install openpyxl
```

**Issue**: Permission denied writing to results/

**Solution**:
```bash
mkdir -p results
chmod 755 results
```
