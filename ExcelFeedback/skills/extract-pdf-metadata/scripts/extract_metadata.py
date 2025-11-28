"""
Extract student metadata from PDF submissions using Claude API.

This module provides functionality to extract structured student information
(student ID, name, partner name, assignment name) from unstructured PDF
submissions using Claude's language understanding capabilities.
"""

import os
import json
import time
import re
from typing import Dict
import pdfplumber
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

load_dotenv()


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract all text from PDF file.

    Args:
        pdf_path: Absolute path to PDF file

    Returns:
        Extracted text as string

    Raises:
        Exception: If PDF is corrupted or cannot be read
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text.strip()


def calculate_confidence(metadata: Dict[str, str]) -> float:
    """
    Calculate confidence score for extracted metadata.

    Args:
        metadata: Dictionary with extracted fields

    Returns:
        Float between 0.0 and 1.0
    """
    confidence = 0.0
    required_fields = ["student_id", "student_name", "partner_name", "assignment_name"]
    fields_present = sum(1 for f in required_fields if metadata.get(f, "NOT_FOUND") != "NOT_FOUND")

    if fields_present == 4:
        confidence += 0.4

    student_id = metadata.get("student_id", "")
    if student_id.isdigit() and len(student_id) == 8:
        confidence += 0.2

    student_name = metadata.get("student_name", "")
    if student_name != "NOT_FOUND" and len(student_name.split()) >= 2:
        confidence += 0.2

    partner_name = metadata.get("partner_name", "")
    if partner_name != "NOT_FOUND" and len(partner_name.split()) >= 2:
        confidence += 0.1

    assignment_name = metadata.get("assignment_name", "")
    if assignment_name != "NOT_FOUND" and len(assignment_name) > 3:
        confidence += 0.1

    return round(confidence, 2)


def extract_metadata(pdf_path: str) -> Dict:
    """
    Extract student metadata from PDF using Claude API.

    Args:
        pdf_path: Absolute path to student's PDF submission

    Returns:
        Dictionary with extracted metadata and confidence score
    """
    default_response = {
        "student_id": "NOT_FOUND",
        "student_name": "NOT_FOUND",
        "partner_name": "NOT_FOUND",
        "assignment_name": "NOT_FOUND",
        "confidence": 0.0,
        "extraction_status": "FILE_NOT_FOUND"
    }

    if not os.path.exists(pdf_path):
        return default_response

    try:
        pdf_text = extract_pdf_text(pdf_path)
    except Exception:
        default_response["extraction_status"] = "PDF_CORRUPTED"
        return default_response

    prompt = f"""Extract the following information from this student submission PDF text:

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
{pdf_text[:2000]}

**Expected JSON format:**
{{
  "student_id": "12345678",
  "student_name": "John Doe",
  "partner_name": "Jane Smith",
  "assignment_name": "Design Patterns"
}}"""

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")

    client = Anthropic(api_key=api_key)
    max_retries = 3
    response_text = None

    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = message.content[0].text
            break
        except APIError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            else:
                default_response["extraction_status"] = "API_ERROR"
                return default_response

    try:
        metadata = json.loads(response_text)
    except json.JSONDecodeError:
        match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if match:
            metadata = json.loads(match.group(1))
        else:
            default_response["extraction_status"] = "PARSE_ERROR"
            return default_response

    confidence = calculate_confidence(metadata)
    metadata["confidence"] = confidence
    metadata["extraction_status"] = "SUCCESS" if confidence >= 0.7 else "NEEDS_MANUAL_REVIEW"

    return metadata
