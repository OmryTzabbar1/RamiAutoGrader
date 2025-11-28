"""
Generate concise feedback summaries from grading reports using Claude API.

This module transforms technical grading results into human-readable 2-3 sentence
summaries (30-50 words) for instructor review.
"""

import os
import json
import time
from typing import Dict
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

load_dotenv()


def load_grading_report(report_path: str) -> Dict:
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


def validate_summary(summary: str) -> Dict:
    """
    Validate summary meets quality requirements.

    Args:
        summary: Generated summary text

    Returns:
        Dictionary with validation results
    """
    word_count = len(summary.split())
    issues = []

    if word_count < 30:
        issues.append(f"Too short ({word_count} words, need 30+)")
    if word_count > 50:
        issues.append(f"Too long ({word_count} words, max 50)")

    if not summary.startswith("Score:"):
        issues.append("Does not start with 'Score:'")

    if any(md in summary for md in ['**', '##', '```', '[', ']']):
        issues.append("Contains markdown formatting")

    return {
        "valid": len(issues) == 0,
        "word_count": word_count,
        "issues": issues
    }


def format_prompt(report: Dict) -> str:
    """
    Format grading report into Claude prompt.

    Args:
        report: Grading report dictionary

    Returns:
        Formatted prompt string
    """
    total = report.get("total_score", 0)
    max_score = report.get("max_score", 100)
    categories = report.get("category_scores", {})
    violations = report.get("violations", [])
    strengths = report.get("strengths", [])

    categories_formatted = "\n".join([f"- {k}: {v}" for k, v in categories.items()])
    violations_formatted = "\n".join([f"- {v}" for v in violations]) if violations else "None"
    strengths_formatted = "\n".join([f"- {s}" for s in strengths]) if strengths else "None"

    return f"""Summarize this grading report in 2-3 sentences for instructor review.

**Requirements:**
- Start with overall score out of {max_score}
- Mention main strengths (categories with high scores)
- Highlight key areas for improvement (specific actionable items)
- Professional but encouraging tone
- Length: 30-50 words STRICT
- Format: Plain text, no markdown

**Grading Report:**
Total Score: {total}/{max_score}

Category Scores:
{categories_formatted}

Violations:
{violations_formatted}

Strengths:
{strengths_formatted}

**Example Output:**
"Score: 77/100. Strong documentation (25/25) and security (10/10). Fix: 2 files exceed 150 lines; increase test coverage to 70%+."

**Your Summary (30-50 words):**"""


def generate_summary(grading_report_path: str) -> str:
    """
    Generate feedback summary from grading report using Claude API.

    Args:
        grading_report_path: Absolute path to grading_results.json

    Returns:
        Summary string (30-50 words)
    """
    if not os.path.exists(grading_report_path):
        return "Error: Grading report not found. Cannot generate feedback summary."

    try:
        report = load_grading_report(grading_report_path)
    except json.JSONDecodeError:
        return "Error: Grading report is corrupted. Cannot parse JSON."

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")

    client = Anthropic(api_key=api_key)
    prompt = format_prompt(report)
    max_retries = 3
    summary = None

    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=200,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            summary = message.content[0].text.strip()
            validation = validate_summary(summary)

            if validation["valid"]:
                return summary
            elif attempt < max_retries - 1:
                continue
            else:
                total = report.get("total_score", 0)
                max_score = report.get("max_score", 100)
                return f"Score: {total}/{max_score}. See detailed report for complete analysis."

        except APIError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            else:
                return f"Error: Failed to generate summary after {max_retries} attempts."

    return summary or "Error: Summary generation failed."
