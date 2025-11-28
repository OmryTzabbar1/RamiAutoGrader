---
name: populate-excel
description: Create formatted Excel workbook with student feedback data
version: 1.0.0
---

# Populate Excel Skill

Creates professionally formatted Excel workbooks (.xlsx) with student feedback data for instructor review.

**Purpose**: Aggregate metadata, grading results, and summaries into a single Excel file with rich formatting.

**Output**: .xlsx file with headers, borders, column widths, text wrapping, and clickable hyperlinks.

---

## Inputs

- `student_data` (list): List of dictionaries with student information
- `assignment_name` (str): Name of assignment for filename
- `output_dir` (str, optional): Output directory (default: "results/")

## Outputs

Returns string (path to created Excel file):
```
"results/FinalFeedback_DesignPatterns.xlsx"
```

---

## Student Data Structure

Each item in `student_data` list:
```json
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns",
  "github_url": "https://github.com/student/project",
  "grade": "77/100",
  "summary": "Score: 77/100. Strong docs...",
  "notes": "NEEDS_MANUAL_REVIEW"
}
```

---

## Instructions

### 1. Validate Input Data

Check that student_data is not empty:
```python
if not student_data or len(student_data) == 0:
    raise ValueError("student_data cannot be empty")
```

### 2. Create Excel Workbook

Use openpyxl to create workbook:

**Python code** (in `scripts/create_excel.py`):
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

def create_workbook():
    """Create new Excel workbook."""
    return Workbook()
```

### 3. Define Column Structure

Define 8 columns with headers and widths:

```python
COLUMNS = [
    {"header": "Student ID", "width": 12, "key": "student_id"},
    {"header": "Student Name", "width": 20, "key": "student_name"},
    {"header": "Partner Name", "width": 20, "key": "partner_name"},
    {"header": "Assignment Name", "width": 25, "key": "assignment_name"},
    {"header": "GitHub URL", "width": 40, "key": "github_url"},
    {"header": "Grade", "width": 10, "key": "grade"},
    {"header": "Summary", "width": 60, "key": "summary"},
    {"header": "Notes", "width": 15, "key": "notes"}
]
```

###  4. Add Header Row

Create header row with formatting:

```python
def add_header_row(ws, columns):
    """
    Add formatted header row to worksheet.

    Args:
        ws: openpyxl Worksheet object
        columns: List of column definitions
    """
    # Header style
    header_font = Font(bold=True, size=11, name='Calibri')
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Add headers
    for idx, col in enumerate(columns, start=1):
        cell = ws.cell(row=1, column=idx)
        cell.value = col["header"]
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border

        # Set column width
        ws.column_dimensions[get_column_letter(idx)].width = col["width"]
```

### 5. Add Data Rows

Add student data rows with formatting:

```python
def add_data_rows(ws, student_data, columns):
    """
    Add student data rows to worksheet.

    Args:
        ws: openpyxl Worksheet object
        student_data: List of student dictionaries
        columns: List of column definitions
    """
    cell_font = Font(size=11, name='Calibri')
    cell_alignment = Alignment(horizontal="left", vertical="top", wrap_text=False)
    summary_alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for row_idx, student in enumerate(student_data, start=2):
        for col_idx, col in enumerate(columns, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            value = student.get(col["key"], "")

            # Handle GitHub URL as hyperlink
            if col["key"] == "github_url" and value:
                cell.hyperlink = value
                cell.value = "Link"
                cell.font = Font(color="0563C1", underline="single", size=11)
            else:
                cell.value = value
                cell.font = cell_font

            # Apply formatting
            if col["key"] == "summary":
                cell.alignment = summary_alignment  # Enable text wrapping for summary
            else:
                cell.alignment = cell_alignment

            cell.border = thin_border
```

### 6. Save Excel File

Save workbook to output directory:

```python
def save_workbook(wb, assignment_name, output_dir="results/"):
    """
    Save Excel workbook to file.

    Args:
        wb: openpyxl Workbook object
        assignment_name: Name of assignment
        output_dir: Output directory path

    Returns:
        Path to saved file
    """
    import os

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Sanitize assignment name for filename
    safe_name = "".join(c for c in assignment_name if c.isalnum() or c in (' ', '-', '_'))
    safe_name = safe_name.replace(' ', '')

    filename = f"FinalFeedback_{safe_name}.xlsx"
    filepath = os.path.join(output_dir, filename)

    wb.save(filepath)
    return filepath
```

### 7. Complete Workflow

```python
def populate_excel(student_data, assignment_name, output_dir="results/"):
    """
    Create formatted Excel workbook with student feedback.

    Args:
        student_data: List of student dictionaries
        assignment_name: Name of assignment
        output_dir: Output directory path

    Returns:
        Path to created Excel file
    """
    if not student_data:
        raise ValueError("student_data cannot be empty")

    wb = create_workbook()
    ws = wb.active
    ws.title = "FinalFeedback"

    add_header_row(ws, COLUMNS)
    add_data_rows(ws, student_data, COLUMNS)

    filepath = save_workbook(wb, assignment_name, output_dir)
    return filepath
```

---

## Error Handling

### Empty Student Data
```python
if not student_data or len(student_data) == 0:
    raise ValueError("student_data cannot be empty. Need at least 1 student.")
```

### Invalid Output Directory
```python
import os

try:
    os.makedirs(output_dir, exist_ok=True)
except PermissionError:
    raise PermissionError(f"Cannot create output directory: {output_dir}. Check permissions.")
```

### Workbook Save Failure
```python
try:
    wb.save(filepath)
except Exception as e:
    raise IOError(f"Failed to save Excel file to {filepath}: {e}")
```

---

## Example Usage

**Input**:
```python
student_data = [
    {
        "student_id": "12345678",
        "student_name": "John Doe",
        "partner_name": "Jane Smith",
        "assignment_name": "Design Patterns",
        "github_url": "https://github.com/johndoe/design-patterns",
        "grade": "77/100",
        "summary": "Score: 77/100. Strong documentation (25/25) and excellent security practices (10/10). Code quality needs improvement: 2 files exceed 150-line limit.",
        "notes": ""
    },
    {
        "student_id": "87654321",
        "student_name": "Alice Johnson",
        "partner_name": "Bob Williams",
        "assignment_name": "Design Patterns",
        "github_url": "https://github.com/alicejohnson/patterns",
        "grade": "92/100",
        "summary": "Score: 92/100. Exceptional code quality (28/30) and perfect test coverage (15/15). Minor: add 2 more ADRs to docs.",
        "notes": ""
    },
    {
        "student_id": "11223344",
        "student_name": "Charlie Brown",
        "partner_name": "NOT_FOUND",
        "assignment_name": "Design Patterns",
        "github_url": "https://github.com/charliebrown/dp-project",
        "grade": "85/100",
        "summary": "Score: 85/100. Strong overall (85%). Excellent git workflow (10/10). Improve: test coverage from 75% to 90%.",
        "notes": "LOW_CONFIDENCE_REVIEW"
    }
]

assignment_name = "Design Patterns"
output_dir = "results/"
```

**Output**:
```
"results/FinalFeedback_DesignPatterns.xlsx"
```

**Excel File Structure**:

| Student ID | Student Name | Partner Name | Assignment Name | GitHub URL | Grade | Summary | Notes |
|------------|--------------|--------------|-----------------|------------|-------|---------|-------|
| 12345678 | John Doe | Jane Smith | Design Patterns | [Link](https://github.com/johndoe/design-patterns) | 77/100 | Score: 77/100. Strong documentation (25/25)... | |
| 87654321 | Alice Johnson | Bob Williams | Design Patterns | [Link](https://github.com/alicejohnson/patterns) | 92/100 | Score: 92/100. Exceptional code quality (28/30)... | |
| 11223344 | Charlie Brown | NOT_FOUND | Design Patterns | [Link](https://github.com/charliebrown/dp-project) | 85/100 | Score: 85/100. Strong overall (85%)... | LOW_CONFIDENCE_REVIEW |

**Formatting Applied**:
- Header: Bold, light blue background (#D9E1F2), centered
- Borders: Thin borders on all cells
- Column widths: Student ID (12), Student Name (20), Summary (60)
- Text wrapping: Enabled for Summary column
- GitHub URL: Clickable hyperlink (blue, underlined)

---

## Edge Cases

### Single Student

**Input**: 1 student in list

**Output**: Excel file with header + 1 data row

---

### Missing GitHub URL

**Input**:
```json
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns",
  "github_url": "",
  "grade": "0/100",
  "summary": "Error: GitHub URL not found in submission.",
  "notes": "PDF_MISSING"
}
```

**Output**: GitHub URL cell shows empty (no hyperlink)

---

### Long Summary (>60 characters per line)

**Input**: Summary with 80+ words

**Handling**: Text wrapping enabled for Summary column, so long text wraps to multiple lines

---

### Special Characters in Assignment Name

**Input**: `assignment_name = "Design Patterns - Fall 2025 (CS401)"`

**Filename Sanitization**: `FinalFeedback_DesignPatterns-Fall2025CS401.xlsx`

(Remove special characters like parentheses, keep alphanumeric, spaces, hyphens, underscores)

---

### Large Dataset (100+ students)

**Input**: 150 students

**Handling**: Excel supports 1,048,576 rows, so 150 students is no problem

**Performance**: ~0.5 seconds to create workbook

---

## Testing

### Unit Tests Required

1. **test_create_excel_valid_data**: Create Excel with 3 students
2. **test_create_excel_single_student**: Create Excel with 1 student
3. **test_create_excel_many_students**: Create Excel with 30 students
4. **test_header_formatting**: Verify header row formatting (bold, color, alignment)
5. **test_column_widths**: Verify column widths set correctly
6. **test_hyperlink_creation**: Verify GitHub URL is clickable hyperlink
7. **test_text_wrapping**: Verify Summary column has text wrapping enabled
8. **test_borders**: Verify all cells have borders
9. **test_empty_student_data**: Verify error raised for empty list
10. **test_output_directory_creation**: Verify output directory created if missing
11. **test_filename_sanitization**: Verify special characters removed from filename

### Manual Testing (Open in Excel)

- ✅ File opens correctly in Microsoft Excel
- ✅ Headers are bold with light blue background
- ✅ All cells have borders
- ✅ Column widths are appropriate (no truncated text)
- ✅ GitHub URLs are clickable (blue, underlined)
- ✅ Summary text wraps to multiple lines if needed
- ✅ Instructor can sort/filter data
- ✅ No formatting issues (alignment, fonts, colors)

---

## Dependencies

- `openpyxl>=3.1.0`: Excel file creation and formatting

---

## Configuration

**Default Output Directory**: `results/`

**Column Widths** (customizable in `COLUMNS`):
- Student ID: 12
- Student Name: 20
- Partner Name: 20
- Assignment Name: 25
- GitHub URL: 40
- Grade: 10
- Summary: 60
- Notes: 15

**Formatting Constants**:
```python
HEADER_FONT = Font(bold=True, size=11, name='Calibri')
HEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
CELL_FONT = Font(size=11, name='Calibri')
HYPERLINK_FONT = Font(color="0563C1", underline="single", size=11)
```

---

## Success Criteria

- ✅ Creates Excel file with correct filename
- ✅ Header row: Bold, light blue background, centered
- ✅ All cells have thin borders
- ✅ Column widths set appropriately (no truncation)
- ✅ GitHub URLs are clickable hyperlinks
- ✅ Summary column has text wrapping enabled
- ✅ Handles 1-100+ students correctly
- ✅ Output directory created if missing
- ✅ File opens correctly in Microsoft Excel
- ✅ Instructor can sort/filter data

---

## Performance

**Single Student**: ~0.1 seconds

**30 Students**: ~0.3 seconds

**100 Students**: ~0.8 seconds

**Bottleneck**: openpyxl cell formatting (applying styles to each cell)

**Optimization**: Could use batch formatting if > 1000 students

---

## Common Issues

1. **Excel shows "Repair needed"**: Usually caused by invalid hyperlink URLs - validate URLs before adding
2. **Text truncated in cells**: Column width too narrow - increase width in COLUMNS definition
3. **File locked (cannot save)**: Excel file already open - close Excel before regenerating
4. **Summary text not wrapping**: Ensure `wrap_text=True` in alignment for Summary column

---

## Future Enhancements

- Conditional formatting (red for grades <70, green for ≥90)
- Charts showing grade distribution
- Multiple sheets (one per assignment type)
- Auto-filter enabled on header row
- Freeze header row (always visible when scrolling)
- Data validation on Notes column (dropdown with predefined values)
