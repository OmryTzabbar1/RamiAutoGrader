"""
Validate Documentation Skill

Validates required documentation for academic software projects.
Checks for README, PRD, PLANNING, TASKS, and CLAUDE.md files.

Delegates to:
- src/validators/document_validator.py
- src/analyzers/documentation_checker.py
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.documentation_checker import check_project_documentation


def validate_docs(project_path: str) -> dict:
    """
    Validate all required documentation in a project.

    Args:
        project_path: Path to project directory

    Returns:
        dict: Validation results with score

    Example:
        >>> result = validate_docs('/path/to/project')
        >>> print(f"Documentation Score: {result['score']}/25")
    """
    print(f"[*] Documentation Validation: {project_path}")
    print("=" * 60)

    result = check_project_documentation(project_path)

    # Display results
    print(f"\n[*] Checking required documents...")
    print(f"    Total documents: {result['total_docs']}")
    print(f"    Passed: {result['docs_passed']}")
    print(f"    Missing: {result['docs_missing']}")
    print(f"    Incomplete: {result['docs_incomplete']}")

    # Show detailed results
    for doc_name, doc_result in result['results'].items():
        if not doc_result.get('exists'):
            print(f"\n[X] {doc_name} - MISSING")
        elif not doc_result['passed']:
            print(f"\n[!] {doc_name} - INCOMPLETE")
            print(f"    Word count: {doc_result['word_count']}")

            for issue in doc_result.get('issues', []):
                print(f"    - {issue.details}")
        else:
            print(f"\n[+] {doc_name} - PASSED")
            print(f"    Word count: {doc_result['word_count']}")
            print(f"    Sections: {len(doc_result['sections_found'])}")

    # Display score
    print("\n" + "=" * 60)
    print(f"Documentation Score: {result['score']}/{result['max_score']}")

    if result['passed']:
        print("[+] PASSED - Documentation is adequate")
    else:
        print("[X] FAILED - Documentation needs improvement")

    return result


def main():
    """Skill entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Documentation validator for academic projects'
    )
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    result = validate_docs(args.project_path)

    if args.json:
        # Convert issues to dict for JSON serialization
        json_result = dict(result)
        json_result['issues'] = [
            {
                'doc_name': issue.doc_name,
                'issue_type': issue.issue_type,
                'details': issue.details,
                'severity': issue.severity
            }
            for issue in result.get('issues', [])
        ]
        # Convert nested results
        for doc_name in json_result.get('results', {}):
            doc_issues = json_result['results'][doc_name].get('issues', [])
            json_result['results'][doc_name]['issues'] = [
                {
                    'doc_name': issue.doc_name,
                    'issue_type': issue.issue_type,
                    'details': issue.details,
                    'severity': issue.severity
                }
                for issue in doc_issues
            ]

        print("\n" + json.dumps(json_result, indent=2))

    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
