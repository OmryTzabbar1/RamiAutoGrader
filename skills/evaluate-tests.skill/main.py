"""
Evaluate Tests Skill

Evaluates test suite quality and coverage for academic software projects.
Analyzes test files, counts tests, and assesses test quality.

Delegates to:
- src/analyzers/test_analyzer.py
- src/analyzers/test_counter.py
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.test_analyzer import evaluate_tests


def run_test_evaluation(project_path: str, language: str = 'python') -> dict:
    """
    Evaluate test suite in a project.

    Args:
        project_path: Path to project directory
        language: Programming language (default: 'python')

    Returns:
        dict: Evaluation results with score

    Example:
        >>> result = run_test_evaluation('/path/to/project')
        >>> print(f"Test Score: {result['score']}/15")
    """
    print(f"[*] Test Evaluation: {project_path}")
    print("=" * 60)

    result = evaluate_tests(project_path, language)

    # Display summary
    print(f"\n[*] Test files found: {result['test_files_found']}")
    print(f"[*] Total tests: {result['total_tests']}")
    print(f"[*] Total assertions: {result['total_assertions']}")

    # Show detailed file results
    if result.get('file_results'):
        print(f"\n[*] Test file details:")
        for file_result in result['file_results'][:5]:  # Show first 5
            if 'error' in file_result:
                print(f"   [!] {file_result['file_path']}: {file_result['error']}")
            else:
                tests = file_result.get('num_tests', 0)
                assertions = file_result.get('num_assertions', 0)
                print(f"   [+] {file_result['file_path']}: {tests} tests, {assertions} assertions")

        if len(result['file_results']) > 5:
            print(f"   ... and {len(result['file_results']) - 5} more files")

    # Display message
    print(f"\n[*] {result['message']}")

    # Display score
    print("\n" + "=" * 60)
    print(f"Test Score: {result['score']}/{result['max_score']}")

    if result['passed']:
        print("[+] PASSED - Test suite is adequate")
    else:
        print("[X] FAILED - Test suite needs improvement")

    return result


def main():
    """Skill entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Test suite evaluator for academic projects'
    )
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--language', default='python', help='Programming language')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    result = run_test_evaluation(args.project_path, args.language)

    if args.json:
        # Convert file_results for JSON serialization
        json_result = dict(result)
        print("\n" + json.dumps(json_result, indent=2, default=str))

    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
