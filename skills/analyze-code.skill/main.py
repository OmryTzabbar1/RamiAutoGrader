"""
Analyze Code Skill

Comprehensive code quality analysis for academic projects.
Enforces 150-line limit, docstring coverage, and naming conventions.

Delegates to:
- src/analyzers/file_size_analyzer.py
- src/analyzers/docstring_analyzer.py
- src/validators/naming_validator.py
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.file_size_analyzer import check_file_sizes, generate_size_report
from src.analyzers.docstring_analyzer import analyze_project_docstrings
from src.validators.naming_validator import analyze_project_naming


def analyze_code(project_path: str, language: str = 'python') -> dict:
    """
    Run comprehensive code quality analysis.

    Args:
        project_path: Path to project directory
        language: Programming language (default: 'python')

    Returns:
        dict: Analysis results with scores

    Example:
        >>> result = analyze_code('/path/to/project')
        >>> print(f"Code Quality Score: {result['score']}/30")
    """
    print(f"[*] Code Quality Analysis: {project_path}")
    print("=" * 60)

    results = {}
    max_score = 30
    score = max_score

    # 1. CRITICAL: Check file size limits (150 lines max)
    print("\n[*] Checking file size limits (150 lines max)...")
    size_violations = check_file_sizes(project_path, limit=150)

    if size_violations:
        print(f"\n[X] CRITICAL: {len(size_violations)} file(s) exceed 150-line limit!")
        for v in size_violations[:5]:  # Show first 5
            print(f"   {v}")
        if len(size_violations) > 5:
            print(f"   ... and {len(size_violations) - 5} more")

        # Heavy penalty for oversized files
        score -= len(size_violations) * 5
    else:
        print("[+] All files within 150-line limit")

    results['file_size'] = generate_size_report(size_violations)

    # 2. Check docstring coverage (90% target)
    print("\n[*] Analyzing docstring coverage (90% target)...")
    docstring_result = analyze_project_docstrings(project_path, min_coverage=0.9)

    coverage_pct = docstring_result['coverage'] * 100
    if docstring_result['passed']:
        print(f"[+] Docstring coverage: {coverage_pct:.1f}% (PASSED)")
    else:
        print(f"[!] Docstring coverage: {coverage_pct:.1f}% (target: 90%)")
        print(f"   Missing {docstring_result['missing']} docstrings")

        # Show some examples
        for v in docstring_result['violations'][:3]:
            print(f"   - {v.item_type} '{v.item_name}' in {v.file_path}:{v.line_number}")

        # Penalty based on how far from target
        coverage_gap = 0.9 - docstring_result['coverage']
        score -= coverage_gap * 20  # Up to 20 points penalty

    results['docstrings'] = docstring_result

    # 3. Check naming conventions
    print("\n[*] Validating naming conventions...")
    naming_result = analyze_project_naming(project_path)

    if naming_result['passed']:
        print("[+] All naming conventions followed")
    else:
        print(f"[!] Found {len(naming_result['violations'])} naming violations")

        # Show examples
        for v in naming_result['violations'][:3]:
            print(f"   - {v.item_type} '{v.item_name}' should use {v.expected_pattern}")

        # Minor penalty for naming
        score -= len(naming_result['violations']) * 0.5

    results['naming'] = naming_result

    # 4. Calculate final score
    score = max(0, min(score, max_score))  # Clamp to [0, max_score]

    # 5. Display summary
    print("\n" + "=" * 60)
    print(f"Code Quality Score: {score:.1f}/{max_score}")

    if score >= 27:  # 90%
        print("[+] EXCELLENT - High quality code")
    elif score >= 21:  # 70%
        print("[+] PASSED - Acceptable code quality")
    else:
        print("[X] FAILED - Significant quality issues")

    return {
        'score': score,
        'max_score': max_score,
        'passed': score >= 21,  # 70% threshold
        'file_size': results['file_size'],
        'docstrings': {
            'coverage': docstring_result['coverage'],
            'passed': docstring_result['passed'],
            'missing': docstring_result['missing']
        },
        'naming': {
            'violations': len(naming_result['violations']),
            'passed': naming_result['passed']
        }
    }


def main():
    """Skill entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Code quality analyzer for academic projects'
    )
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--language', default='python', help='Programming language')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    result = analyze_code(args.project_path, args.language)

    if args.json:
        print("\n" + json.dumps(result, indent=2))

    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
