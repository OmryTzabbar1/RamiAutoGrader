"""
Grade Research Skill

Evaluates research quality for academic software projects.
Checks for parameter exploration, statistical analysis, and research artifacts.

Delegates to:
- src/analyzers/research_analyzer.py
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.research_analyzer import evaluate_research_quality


def run_research_evaluation(project_path: str) -> dict:
    """
    Evaluate research quality in a project.

    Args:
        project_path: Path to project directory

    Returns:
        dict: Evaluation results with score

    Example:
        >>> result = run_research_evaluation('/path/to/project')
        >>> print(f"Research Score: {result['score']}/10")
    """
    print(f"[*] Research Quality Evaluation: {project_path}")
    print("=" * 60)

    result = evaluate_research_quality(project_path)

    # Display findings
    print(f"\n[*] Research Documentation: {len(result.get('research_docs', []))}")
    if result.get('research_docs'):
        for doc in result['research_docs'][:3]:
            print(f"   [+] {doc}")

    print(f"\n[*] Parameter/Config Files: {len(result.get('param_files', []))}")
    if result.get('param_files'):
        for pfile in result['param_files'][:3]:
            print(f"   [+] {pfile}")

    print(f"\n[*] Analysis Scripts: {len(result.get('analysis_scripts', []))}")
    if result.get('analysis_scripts'):
        for script in result['analysis_scripts'][:3]:
            print(f"   [+] {script}")

    # Display message
    print(f"\n[*] {result['message']}")

    # Display score
    print("\n" + "=" * 60)
    print(f"Research Quality Score: {result['score']}/{result['max_score']}")

    if result['passed']:
        print("[+] PASSED - Research quality is adequate")
    else:
        print("[X] FAILED - Research quality needs improvement")

    return result


def main():
    """Skill entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Research quality evaluator for academic projects'
    )
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    result = run_research_evaluation(args.project_path)

    if args.json:
        print("\n" + json.dumps(result, indent=2, default=str))

    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
