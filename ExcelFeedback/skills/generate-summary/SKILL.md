---
name: generate-summary
description: Generate concise 2-3 sentence feedback summary from grading report
version: 1.0.0
---

# Generate Summary Skill

Generates human-readable feedback summaries from detailed grading reports using Claude's language understanding capabilities.

**Purpose**: Transform technical grading results into concise, professional feedback for instructors.

**Output**: 2-3 sentence summary (30-50 words) highlighting score, strengths, and key improvements.

---

## Inputs

- `grading_report_path` (str): Absolute path to student's `grading_results.json` file

## Outputs

Returns string (30-50 words):
```
"Score: 77/100. Strong documentation (25/25) and excellent security practices (10/10). Code quality needs improvement: 2 files exceed 150-line limit (src/analyzer.py, src/parser.py). Increase test coverage from 67% to ≥70% minimum."
```

---

## Instructions

### 1. Validate Grading Report File Exists

Check if grading_results.json exists:
```bash
test -f "${grading_report_path}" && echo "EXISTS" || echo "NOT_FOUND"
```

If not found, return error summary:
```
"Error: Grading report not found. Cannot generate feedback summary."
```

### 2. Read and Parse Grading Report JSON

Read the grading_results.json file:

**Python code** (in `scripts/summarize_report.py`):
```python
import json

def load_grading_report(report_path: str) -> dict:
    """
    Load grading report JSON file.

    Args:
        report_path: Absolute path to grading_results.json

    Returns:
        Dictionary with grading data

    Raises:
        FileNotFoundError: If report file does not exist
        JSONDecodeError: If file is not valid JSON
    """
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

**Expected JSON structure**:
```json
{
  "total_score": 77,
  "max_score": 100,
  "category_scores": {
    "documentation": 25,
    "code_quality": 20,
    "testing": 10,
    "security": 10,
    "git": 7,
    "research": 5
  },
  "violations": [
    "src/analyzer.py: 182 lines (exceeds 150 limit)",
    "src/parser.py: 165 lines (exceeds 150 limit)",
    "Test coverage: 67% (below 70% minimum)",
    "Missing docstrings: 3 functions"
  ],
  "strengths": [
    "Excellent documentation coverage (100%)",
    "No hardcoded secrets found",
    "Clean git history (23 commits)"
  ]
}
```

### 3. Send Report to Claude API for Summarization

Use Claude API with structured summarization prompt:

**Claude Prompt Template**:
```markdown
Summarize this grading report in 2-3 sentences for instructor review.

**Requirements:**
- Start with overall score out of 100
- Mention main strengths (categories with high scores)
- Highlight key areas for improvement (specific actionable items)
- Professional but encouraging tone
- Length: 30-50 words STRICT
- Format: Plain text, no markdown

**Grading Report:**
Total Score: {total_score}/{max_score}

Category Scores:
{category_scores_formatted}

Violations:
{violations_list}

Strengths:
{strengths_list}

**Example Output:**
"Score: 77/100. Strong documentation (25/25) and security (10/10). Fix: 2 files exceed 150 lines; increase test coverage to 70%+."

**Your Summary (30-50 words):**
```

**API Call** (using anthropic SDK):
```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=200,
    temperature=0.3,  # Slight creativity for professional tone
    messages=[
        {"role": "user", "content": prompt}
    ]
)

summary = message.content[0].text.strip()
```

### 4. Validate Summary Quality

Validate the generated summary meets requirements:

```python
def validate_summary(summary: str) -> dict:
    """
    Validate summary meets quality requirements.

    Requirements:
    - Length: 30-50 words
    - Starts with "Score:"
    - Professional tone (no slang, emojis)
    - Plain text (no markdown)

    Args:
        summary: Generated summary text

    Returns:
        dict: {
            "valid": bool,
            "word_count": int,
            "issues": list[str]
        }
    """
    word_count = len(summary.split())
    issues = []

    if word_count < 30:
        issues.append(f"Too short ({word_count} words, need 30+)")
    if word_count > 50:
        issues.append(f"Too long ({word_count} words, max 50)")

    if not summary.startswith("Score:"):
        issues.append("Does not start with 'Score:'")

    # Check for markdown
    if any(md in summary for md in ['**', '##', '```', '[', ']']):
        issues.append("Contains markdown formatting")

    # Check for emojis (basic check)
    if any(ord(c) > 127 for c in summary):
        issues.append("Contains non-ASCII characters (emojis?)")

    return {
        "valid": len(issues) == 0,
        "word_count": word_count,
        "issues": issues
    }
```

If validation fails, retry with adjusted prompt (max 2 retries).

### 5. Return Final Summary

Return the validated summary as plain text string:

```python
summary = "Score: 77/100. Strong documentation (25/25) and excellent security practices (10/10). Code quality needs improvement: 2 files exceed 150-line limit. Increase test coverage from 67% to ≥70%."

return summary
```

---

## Error Handling

### Grading Report Not Found
```python
if not os.path.exists(report_path):
    return "Error: Grading report not found. Cannot generate feedback summary."
```

### Invalid JSON Format
```python
try:
    report = json.load(f)
except json.JSONDecodeError:
    return "Error: Grading report is corrupted. Cannot parse JSON."
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
            time.sleep(2 ** attempt)
            continue
        else:
            return f"Error: Failed to generate summary after {max_retries} attempts."
```

### Summary Validation Failure
```python
validation = validate_summary(summary)
if not validation["valid"]:
    # Retry with adjusted prompt
    if retry_count < 2:
        return generate_summary_with_retry(...)
    else:
        # Return fallback summary
        return f"Score: {total_score}/{max_score}. See detailed report for complete analysis."
```

---

## Example Usage

**Input**:
```python
grading_report_path = "results/john_doe/grading_results.json"
```

**Grading Report Content**:
```json
{
  "total_score": 77,
  "max_score": 100,
  "category_scores": {
    "documentation": 25,
    "code_quality": 20,
    "testing": 10,
    "security": 10,
    "git": 7,
    "research": 5
  },
  "violations": [
    "src/analyzer.py: 182 lines (exceeds 150 limit)",
    "src/parser.py: 165 lines (exceeds 150 limit)",
    "Test coverage: 67% (below 70% minimum)"
  ],
  "strengths": [
    "Excellent documentation coverage (100%)",
    "No hardcoded secrets found"
  ]
}
```

**Output**:
```
"Score: 77/100. Strong documentation (25/25) and excellent security practices (10/10). Code quality needs improvement: 2 files exceed 150-line limit (src/analyzer.py, src/parser.py). Increase test coverage from 67% to ≥70% minimum."
```

**Word Count**: 38 words ✅

---

## Edge Cases

### Perfect Score (100/100)

**Grading Report**:
```json
{
  "total_score": 100,
  "max_score": 100,
  "category_scores": {
    "documentation": 25,
    "code_quality": 30,
    "testing": 15,
    "security": 10,
    "git": 10,
    "research": 10
  },
  "violations": [],
  "strengths": [
    "Exceptional code quality",
    "100% test coverage",
    "Perfect documentation"
  ]
}
```

**Output**:
```
"Score: 100/100 - Exceptional work! Outstanding code quality (30/30), perfect test coverage (15/15), and comprehensive documentation (25/25). Exemplary academic project demonstrating mastery of software engineering principles."
```

### Failing Score (< 70%)

**Grading Report**:
```json
{
  "total_score": 45,
  "max_score": 100,
  "category_scores": {
    "documentation": 10,
    "code_quality": 15,
    "testing": 5,
    "security": 10,
    "git": 3,
    "research": 2
  },
  "violations": [
    "Missing README.md (critical)",
    "6 files exceed 150 lines",
    "No unit tests found",
    "Only 3 git commits"
  ]
}
```

**Output**:
```
"Score: 45/100 - Requires significant improvement. Critical issues: missing README (10/25 docs), no unit tests (5/15 testing), insufficient commits (3/10 git). Focus on documentation, test coverage, and code modularity."
```

### Missing Category Scores

**Grading Report**:
```json
{
  "total_score": 65,
  "max_score": 80,
  "category_scores": {
    "documentation": 20,
    "code_quality": 25,
    "testing": 12,
    "security": 8
  },
  "violations": ["Test coverage: 72% (acceptable but could improve)"]
}
```

**Output**:
```
"Score: 65/80. Good documentation (20/25) and code structure (25/30). Security excellent (8/10). Minor improvement: increase test coverage from 72% to 90% for excellence threshold."
```

---

## Testing

### Unit Tests Required

1. **test_generate_summary_valid_report**: Generate summary from valid grading report
2. **test_generate_summary_perfect_score**: Handle 100/100 score
3. **test_generate_summary_failing_score**: Handle low score (<70%)
4. **test_generate_summary_file_not_found**: Handle missing grading report
5. **test_generate_summary_invalid_json**: Handle corrupted JSON
6. **test_validate_summary_valid**: Validate correct summary
7. **test_validate_summary_too_short**: Validate summary length (too short)
8. **test_validate_summary_too_long**: Validate summary length (too long)
9. **test_validate_summary_missing_score**: Validate starts with "Score:"
10. **test_validate_summary_has_markdown**: Validate no markdown

### Word Count Test Cases

| Scenario | Expected Word Count | Valid |
|----------|-------------------|-------|
| Typical summary | 35-45 words | ✅ |
| Minimum acceptable | 30 words | ✅ |
| Maximum acceptable | 50 words | ✅ |
| Too short | < 30 words | ❌ |
| Too long | > 50 words | ❌ |

---

## Dependencies

- `anthropic>=0.40.0`: Claude API client
- `python-dotenv>=1.0.0`: Environment variables

---

## Configuration

**Environment Variables** (from `.env`):
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

**Model**: `claude-sonnet-4-5-20250929` (latest Sonnet)

**Temperature**: `0.3` (slightly creative for professional tone)

**Max Tokens**: `200` (summary is short)

---

## Success Criteria

- ✅ Generates 30-50 word summaries for all grading reports
- ✅ Always starts with "Score: X/Y"
- ✅ Mentions at least 1 strength and 1 improvement area
- ✅ Professional tone (no slang, emojis, or markdown)
- ✅ Handles edge cases (perfect score, failing score)
- ✅ Retries Claude API failures (3× with exponential backoff)
- ✅ Validates summary quality before returning
- ✅ Returns error message for missing/corrupted reports

---

## Performance

**Per Student**:
- JSON loading: ~0.1 seconds
- Claude API call: ~2-4 seconds
- Validation: ~0.1 seconds
- Total: ~2-5 seconds

**For 30 Students** (sequential):
- Total time: ~1-3 minutes

**Optimization**: Can be parallelized with extract-pdf-metadata skill

---

## Common Issues

1. **Summary too generic**: Claude sometimes generates vague summaries - add more context to prompt
2. **Summary exceeds 50 words**: Prompt emphasizes "STRICT" limit, but retries may be needed
3. **Missing specific violations**: Ensure violations list is included in prompt
4. **Tone too negative**: Temperature=0.3 balances professionalism with encouragement

---

## Future Enhancements

- Customizable tone (strict, encouraging, neutral)
- Multi-language summaries (support non-English instructors)
- Category-specific feedback templates
- Historical comparison ("Improved from previous assignment")
