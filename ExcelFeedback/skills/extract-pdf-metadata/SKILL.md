---
name: extract-pdf-metadata
description: Extract student metadata from PDF submissions using Claude API
version: 1.0.0
---

# Extract PDF Metadata Skill

Extracts structured student information from unstructured PDF submissions using Claude's language understanding capabilities.

**Purpose**: Parse student ID, name, partner name, and assignment name from PDF text with confidence scoring.

**Scoring**: Returns confidence score (0.0-1.0) to flag uncertain extractions for manual review.

---

## Inputs

- `pdf_path` (str): Absolute path to student's PDF submission file

## Outputs

Returns JSON:
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

**Possible `extraction_status` values**:
- `SUCCESS`: All fields extracted with confidence ≥ 0.7
- `NEEDS_MANUAL_REVIEW`: Confidence < 0.7 or missing fields
- `FILE_NOT_FOUND`: PDF path does not exist
- `PDF_CORRUPTED`: PDF cannot be read
- `API_ERROR`: Claude API call failed after retries
- `PARSE_ERROR`: Claude returned invalid JSON

---

## Instructions

### 1. Validate PDF File Exists

Use Bash to check if PDF file exists:
```bash
test -f "${pdf_path}" && echo "EXISTS" || echo "NOT_FOUND"
```

If not found, return:
```json
{
  "student_id": "NOT_FOUND",
  "student_name": "NOT_FOUND",
  "partner_name": "NOT_FOUND",
  "assignment_name": "NOT_FOUND",
  "confidence": 0.0,
  "extraction_status": "FILE_NOT_FOUND"
}
```

### 2. Extract Text from PDF

Use `pdfplumber` to extract all text from the PDF:

**Python code** (in `scripts/extract_metadata.py`):
```python
import pdfplumber

def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract all text from PDF file.

    Args:
        pdf_path: Absolute path to PDF file

    Returns:
        Extracted text as string

    Raises:
        PDFError: If PDF is corrupted or cannot be read
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text.strip()
    except Exception as e:
        raise PDFError(f"Failed to extract text from PDF: {e}")
```

If extraction fails, return `extraction_status: "PDF_CORRUPTED"`.

### 3. Send Text to Claude API for Extraction

Use Claude API with structured extraction prompt:

**Claude Prompt Template**:
```markdown
Extract the following information from this student submission PDF text:

**Required fields:**
- student_id: The student's unique ID (usually 8 digits)
- student_name: The student's full name
- partner_name: The partner's full name (this is a group project of 2 students)
- assignment_name: The name/title of the assignment

**Instructions:**
- Return ONLY valid JSON with these exact field names
- If a field is not found or unclear, use "NOT_FOUND" as the value
- Do not include any markdown formatting or code blocks in your response
- Do not include explanations, just return the JSON object

**PDF Text:**
{pdf_text}

**Expected JSON format:**
{{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns"
}}
```

**API Call** (using anthropic SDK):
```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=500,
    temperature=0.0,  # Deterministic extraction
    messages=[
        {"role": "user", "content": prompt}
    ]
)

response_text = message.content[0].text
```

**Error Handling**:
- Retry up to 3 times with exponential backoff (1s, 2s, 4s)
- If all retries fail, return `extraction_status: "API_ERROR"`

### 4. Parse JSON Response

Parse Claude's response as JSON:

```python
import json

try:
    metadata = json.loads(response_text)
except json.JSONDecodeError:
    # Try to extract JSON from markdown code block
    import re
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if match:
        metadata = json.loads(match.group(1))
    else:
        # Return parse error
        return {
            "student_id": "NOT_FOUND",
            "student_name": "NOT_FOUND",
            "partner_name": "NOT_FOUND",
            "assignment_name": "NOT_FOUND",
            "confidence": 0.0,
            "extraction_status": "PARSE_ERROR"
        }
```

### 5. Calculate Confidence Score

Calculate confidence based on extracted data quality:

```python
def calculate_confidence(metadata: dict) -> float:
    """
    Calculate confidence score for extracted metadata.

    Confidence factors:
    - All required fields present (not "NOT_FOUND"): +0.4
    - Valid student_id format (8 digits): +0.2
    - Valid student_name format (2+ words): +0.2
    - Valid partner_name format (2+ words): +0.1
    - Valid assignment_name (non-empty, >3 chars): +0.1

    Returns:
        Float between 0.0 and 1.0
    """
    confidence = 0.0

    # Check all fields present
    required_fields = ["student_id", "student_name", "partner_name", "assignment_name"]
    fields_present = sum(1 for f in required_fields if metadata.get(f, "NOT_FOUND") != "NOT_FOUND")
    if fields_present == 4:
        confidence += 0.4

    # Validate student_id (8 digits)
    student_id = metadata.get("student_id", "")
    if student_id.isdigit() and len(student_id) == 8:
        confidence += 0.2

    # Validate student_name (2+ words)
    student_name = metadata.get("student_name", "")
    if student_name != "NOT_FOUND" and len(student_name.split()) >= 2:
        confidence += 0.2

    # Validate partner_name (2+ words)
    partner_name = metadata.get("partner_name", "")
    if partner_name != "NOT_FOUND" and len(partner_name.split()) >= 2:
        confidence += 0.1

    # Validate assignment_name (non-empty, >3 chars)
    assignment_name = metadata.get("assignment_name", "")
    if assignment_name != "NOT_FOUND" and len(assignment_name) > 3:
        confidence += 0.1

    return round(confidence, 2)
```

### 6. Determine Extraction Status

Based on confidence score, set extraction status:

```python
confidence = calculate_confidence(metadata)
metadata["confidence"] = confidence

if confidence >= 0.7:
    metadata["extraction_status"] = "SUCCESS"
else:
    metadata["extraction_status"] = "NEEDS_MANUAL_REVIEW"
```

**Threshold**: 0.7 (70% confidence) is the minimum for auto-acceptance.

### 7. Return Final Metadata

Return the complete metadata JSON:

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

---

## Error Handling

### File Not Found
```python
if not os.path.exists(pdf_path):
    return {
        "student_id": "NOT_FOUND",
        "student_name": "NOT_FOUND",
        "partner_name": "NOT_FOUND",
        "assignment_name": "NOT_FOUND",
        "confidence": 0.0,
        "extraction_status": "FILE_NOT_FOUND"
    }
```

### PDF Corrupted
```python
try:
    text = extract_pdf_text(pdf_path)
except PDFError:
    return {
        "student_id": "NOT_FOUND",
        "student_name": "NOT_FOUND",
        "partner_name": "NOT_FOUND",
        "assignment_name": "NOT_FOUND",
        "confidence": 0.0,
        "extraction_status": "PDF_CORRUPTED"
    }
```

### Claude API Error (After Retries)
```python
max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.messages.create(...)
        break
    except anthropic.APIError as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
        else:
            return {
                "student_id": "NOT_FOUND",
                "student_name": "NOT_FOUND",
                "partner_name": "NOT_FOUND",
                "assignment_name": "NOT_FOUND",
                "confidence": 0.0,
                "extraction_status": "API_ERROR"
            }
```

---

## Example Usage

**Input**:
```python
pdf_path = "results/john_doe/student_submission.pdf"
```

**PDF Content** (sample):
```
Student Submission - Design Patterns

Student ID: 12345678
Name: John Doe
Partner: Jane Smith

Assignment: Design Patterns Implementation

[Rest of PDF content...]
```

**Output**:
```json
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns Implementation",
  "confidence": 1.0,
  "extraction_status": "SUCCESS"
}
```

---

## Edge Cases

### Missing Partner Name

**PDF Content**:
```
Student ID: 12345678
Name: John Doe

Assignment: Solo Project
```

**Output**:
```json
{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "NOT_FOUND",
  "assignment_name": "Solo Project",
  "confidence": 0.6,
  "extraction_status": "NEEDS_MANUAL_REVIEW"
}
```

### Invalid Student ID Format

**PDF Content**:
```
Student ID: ABC123 (invalid)
Name: John Doe
Partner: Jane Smith
Assignment: Design Patterns
```

**Output**:
```json
{
  "student_id": "ABC123",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns",
  "confidence": 0.6,
  "extraction_status": "NEEDS_MANUAL_REVIEW"
}
```

### Completely Unstructured PDF

**PDF Content**:
```
This is a project about design patterns.
I worked with my classmate.
[No clear student info...]
```

**Output**:
```json
{
  "student_id": "NOT_FOUND",
  "student_name": "NOT_FOUND",
  "partner_name": "NOT_FOUND",
  "assignment_name": "NOT_FOUND",
  "confidence": 0.0,
  "extraction_status": "NEEDS_MANUAL_REVIEW"
}
```

---

## Testing

### Unit Tests Required

1. **test_extract_valid_pdf**: Extract from well-formatted PDF
2. **test_extract_missing_partner**: Handle missing partner name
3. **test_extract_invalid_student_id**: Handle non-8-digit student ID
4. **test_extract_file_not_found**: Handle missing PDF file
5. **test_extract_corrupted_pdf**: Handle corrupted PDF
6. **test_api_retry_on_error**: Verify retry logic works
7. **test_confidence_calculation**: Verify confidence scoring
8. **test_parse_error_handling**: Handle invalid JSON from Claude

### Confidence Score Test Cases

| Scenario | Expected Confidence | Status |
|----------|-------------------|--------|
| All fields valid | 1.0 | SUCCESS |
| Missing partner | 0.6 | NEEDS_MANUAL_REVIEW |
| Invalid student_id | 0.6 | NEEDS_MANUAL_REVIEW |
| All fields missing | 0.0 | NEEDS_MANUAL_REVIEW |
| 3/4 fields valid | 0.7-0.9 | SUCCESS or REVIEW |

---

## Dependencies

- `pdfplumber>=0.10.0`: PDF text extraction
- `anthropic>=0.40.0`: Claude API client
- `python-dotenv>=1.0.0`: Environment variables

---

## Configuration

**Environment Variables** (from `.env`):
```bash
ANTHROPIC_API_KEY=sk-ant-...
CONFIDENCE_THRESHOLD=0.7
```

**Model**: `claude-sonnet-4-5-20250929` (latest Sonnet)

**Temperature**: `0.0` (deterministic extraction)

**Max Tokens**: `500` (JSON response is small)

---

## Success Criteria

- ✅ Extracts metadata from 80%+ of PDFs with confidence ≥ 0.7
- ✅ Handles missing PDFs gracefully (returns FILE_NOT_FOUND)
- ✅ Handles corrupted PDFs gracefully (returns PDF_CORRUPTED)
- ✅ Retries Claude API failures (3× with exponential backoff)
- ✅ Flags low-confidence extractions for manual review
- ✅ Returns valid JSON for all scenarios
- ✅ No hardcoded values (uses environment variables)

---

## Performance

**Per Student**:
- PDF text extraction: ~1-2 seconds
- Claude API call: ~3-5 seconds
- Total: ~4-7 seconds

**For 30 Students** (sequential):
- Total time: ~2-4 minutes

**Optimization**: Can be parallelized (5 concurrent calls) → ~1 minute total

---

## Common Issues

1. **PDF has no text (scanned image)**: Returns confidence 0.0, flags for manual review
2. **Student name in different format**: Claude's flexibility handles variations
3. **Assignment name is very long**: Claude truncates to key information
4. **Multiple students listed**: Claude extracts first student by default

---

## Future Enhancements

- OCR support for scanned PDFs (using pytesseract)
- Multi-language support (detect language, adjust prompt)
- Fuzzy matching against student roster (validate student IDs)
- Historical data learning (improve extraction based on past submissions)
