"""
Document Validator Module

Validates required documentation for academic software projects.
Checks for existence, completeness, and quality of documentation files.

Required Documents:
- README.md, PRD.md, PLANNING.md, TASKS.md, CLAUDE.md
"""

import os
from typing import Dict, List

from ..models.code_models import DocumentIssue
from ..utils.markdown_utils import count_words, extract_sections


def validate_document(
    doc_path: str,
    required_sections: List[str],
    min_words: int
) -> Dict:
    """
    Validate a single documentation file.

    Args:
        doc_path: Path to documentation file
        required_sections: List of required section names
        min_words: Minimum word count

    Returns:
        Dict with validation results

    Example:
        >>> result = validate_document('README.md', ['Installation'], 200)
        >>> if result['passed']:
        ...     print("README is valid")
    """
    issues = []

    # Check if file exists
    if not os.path.exists(doc_path):
        return {
            'passed': False,
            'exists': False,
            'word_count': 0,
            'sections_found': [],
            'issues': [DocumentIssue(
                doc_name=os.path.basename(doc_path),
                issue_type='missing',
                details=f'File not found: {doc_path}',
                severity='critical'
            )]
        }

    # Read content
    try:
        with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {
            'passed': False,
            'exists': True,
            'error': str(e),
            'issues': []
        }

    # Count words
    word_count = count_words(content)
    if word_count < min_words:
        issues.append(DocumentIssue(
            doc_name=os.path.basename(doc_path),
            issue_type='too_short',
            details=f'Only {word_count} words (minimum: {min_words})',
            severity='major'
        ))

    # Extract and check sections
    sections = extract_sections(content)
    sections_lower = [s.lower() for s in sections]

    for req_section in required_sections:
        if not any(req_section.lower() in s for s in sections_lower):
            issues.append(DocumentIssue(
                doc_name=os.path.basename(doc_path),
                issue_type='missing_section',
                details=f'Missing required section: {req_section}',
                severity='major'
            ))

    return {
        'passed': len(issues) == 0,
        'exists': True,
        'word_count': word_count,
        'sections_found': sections,
        'issues': issues
    }


