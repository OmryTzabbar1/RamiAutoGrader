"""
Check UX Skill

Evaluates user experience quality for academic software projects.
Checks README usability, CLI help, and documentation clarity.

Delegates to:
- src/analyzers/ux_analyzer.py
- src/validators/readme_validator.py
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.ux_analyzer import evaluate_ux_quality


def run_ux_evaluation(project_path: str) -> dict:
    """
    Evaluate UX quality in a project.

    Args:
        project_path: Path to project directory

    Returns:
        dict: Evaluation results with score

    Example:
        >>> result = run_ux_evaluation('/path/to/project')
        >>> print(f"UX Score: {result['score']}/10")
    """
    print(f"[*] User Experience Evaluation: {project_path}")
    print("=" * 60)

    result = evaluate_ux_quality(project_path)

    # Display README results
    readme = result.get('readme_result', {})
    print(f"\n[*] README Analysis:")
    print(f"    Has README: {readme.get('has_readme', False)}")
    print(f"    Score: {readme.get('score', 0)}/4")

    if readme.get('has_readme'):
        print(f"    Sections: {len(readme.get('sections', []))}")
        print(f"    Has code examples: {readme.get('has_code_examples', False)}")

        if readme.get('issues'):
            print(f"    Issues:")
            for issue in readme['issues']:
                print(f"       - {issue}")

    # Display CLI results
    cli = result.get('cli_result', {})
    print(f"\n[*] CLI Help Analysis:")
    print(f"    Score: {cli.get('score', 0)}/3")
    print(f"    Has argparse: {cli.get('has_argparse', False)}")
    print(f"    Has help flag: {cli.get('has_help_flag', False)}")

    # Display message
    print(f"\n[*] {result['message']}")

    # Display score
    print("\n" + "=" * 60)
    print(f"UX Quality Score: {result['score']}/{result['max_score']}")

    if result['passed']:
        print("[+] PASSED - User experience is good")
    else:
        print("[X] FAILED - User experience needs improvement")

    return result


def main():
    """Skill entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='UX quality evaluator for academic projects'
    )
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    result = run_ux_evaluation(args.project_path)

    if args.json:
        print("\n" + json.dumps(result, indent=2, default=str))

    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
