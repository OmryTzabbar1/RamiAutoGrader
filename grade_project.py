"""
Auto-Grader Orchestrator

Main entry point for the Academic Software Auto-Grader System.
Coordinates all grading skills and generates comprehensive reports.

Usage:
    python grade_project.py <project_path>
    python grade_project.py <project_path> --json
    python grade_project.py <project_path> --output report.json

Example:
    python grade_project.py ../student-project
"""

import sys
import json
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.skill_executor import run_all_skills
from src.core.grading_utils import format_results_summary


def main():
    """Main orchestrator entry point."""
    parser = argparse.ArgumentParser(
        description='Academic Software Auto-Grader - Comprehensive project evaluation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python grade_project.py ./my-project
  python grade_project.py ./my-project --json
  python grade_project.py ./my-project --output report.json

Categories (100 points total):
  Security:       10 points
  Code Quality:   30 points
  Documentation:  25 points
  Testing:        15 points
  Git Workflow:   10 points
  Research:       10 points

Grading Scale:
  A: 90-100  (Excellence)
  B: 80-89   (Very Good)
  C: 70-79   (Passing)
  D: 60-69   (Poor)
  F: 0-59    (Failing)
        """
    )

    parser.add_argument(
        'project_path',
        help='Path to project directory to grade'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    parser.add_argument(
        '--output',
        '-o',
        help='Save report to file (JSON format)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed output from each skill'
    )

    args = parser.parse_args()

    # Run all grading skills
    print("\n" + "=" * 60)
    print("ACADEMIC SOFTWARE AUTO-GRADER")
    print("=" * 60 + "\n")

    results = run_all_skills(args.project_path)

    # Display summary
    print("\n" + format_results_summary(results))

    # JSON output
    if args.json or args.output:
        # Convert results to JSON-serializable format
        json_results = {
            'total_score': results['total_score'],
            'max_score': results['max_score'],
            'percentage': results['percentage'],
            'grade': results['grade'],
            'passed': results['passed'],
            'categories': {
                'security': results['results']['security'],
                'code_quality': results['results']['code_quality'],
                'documentation': results['results']['documentation'],
                'testing': results['results']['testing'],
                'git': results['results']['git'],
                'research': results['results']['research'],
                'ux': results['results']['ux']
            }
        }

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(json_results, f, indent=2, default=str)
            print(f"\n[+] Report saved to: {args.output}")
        else:
            print("\n" + json.dumps(json_results, indent=2, default=str))

    # Exit with appropriate code
    sys.exit(0 if results['passed'] else 1)


if __name__ == '__main__':
    main()
