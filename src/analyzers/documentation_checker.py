"""
Documentation Checker Module

Project-wide documentation validation and scoring.
Checks all required documents and calculates overall documentation score.
"""

import os
from typing import Dict, List

from ..validators.document_validator import validate_document
from ..validators.document_requirements import DEFAULT_DOC_REQUIREMENTS


def _validate_all_docs(project_path: str, required_docs: List[Dict]) -> tuple:
    """Validate all required documents and collect results."""
    results = {}
    all_issues = []
    docs_passed = 0

    for doc_spec in required_docs:
        doc_name = doc_spec['name']
        doc_path = os.path.join(project_path, doc_name)

        result = validate_document(
            doc_path,
            doc_spec.get('required_sections', []),
            doc_spec.get('min_words', 0)
        )

        results[doc_name] = result
        all_issues.extend(result.get('issues', []))

        if result['passed']:
            docs_passed += 1

    return results, all_issues, docs_passed


def _calculate_doc_score(results: Dict) -> Dict:
    """Calculate documentation score from validation results."""
    max_score = 25
    missing_count = sum(1 for r in results.values() if not r.get('exists', False))
    incomplete_count = sum(1 for r in results.values() if r.get('exists') and not r['passed'])

    score = max_score - (missing_count * 10) - (incomplete_count * 5)
    score = max(0, score)

    return {
        'score': score,
        'max_score': max_score,
        'passed': score >= 17.5,
        'docs_missing': missing_count,
        'docs_incomplete': incomplete_count
    }


def check_project_documentation(project_path: str, config: Dict = None) -> Dict:
    """
    Validate all required documentation in a project.

    Args:
        project_path: Root directory of project
        config: Grading config dict (if None, uses defaults)

    Returns:
        Dict with overall validation results and score

    Example:
        >>> result = check_project_documentation('/path/to/project')
        >>> print(f"Documentation Score: {result['score']}/25")
    """
    if config is None:
        config = DEFAULT_DOC_REQUIREMENTS

    required_docs = config.get('required_documents', [])
    results, all_issues, docs_passed = _validate_all_docs(project_path, required_docs)
    score_info = _calculate_doc_score(results)

    return {
        **score_info,
        'total_docs': len(required_docs),
        'docs_passed': docs_passed,
        'results': results,
        'issues': all_issues
    }
