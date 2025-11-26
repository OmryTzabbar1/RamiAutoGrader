"""
Assess Git Skill

Assesses git workflow quality for academic software projects.
Analyzes commit history, message quality, and development practices.

Delegates to:
- src/analyzers/git_analyzer.py
- src/utils/git_commands.py
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.git_analyzer import assess_git_workflow


def run_git_assessment(project_path: str, min_commits: int = 10) -> dict:
    """
    Assess git workflow in a project.

    Args:
        project_path: Path to project directory
        min_commits: Minimum required commits (default: 10)

    Returns:
        dict: Assessment results with score

    Example:
        >>> result = run_git_assessment('/path/to/project')
        >>> print(f"Git Score: {result['score']}/10")
    """
    print(f"[*] Git Workflow Assessment: {project_path}")
    print("=" * 60)

    result = assess_git_workflow(project_path, min_commits)

    # Display summary
    if not result['is_git_repo']:
        print("\n[X] Not a git repository")
    else:
        print(f"\n[*] Total commits: {result.get('commit_count', 0)}")
        print(f"[*] Short messages (< 10 chars): {result.get('short_messages', 0)}")
        print(f"[*] Vague messages: {result.get('vague_messages', 0)}")

        # Show recent commits
        if result.get('commits'):
            print(f"\n[*] Recent commits:")
            for commit in result['commits'][:5]:  # Show first 5
                msg = commit.message[:60] + '...' if len(commit.message) > 60 else commit.message
                print(f"   - {commit.hash[:7]}: {msg}")

            if len(result['commits']) > 5:
                print(f"   ... and {len(result['commits']) - 5} more")

    # Display message
    print(f"\n[*] {result['message']}")

    # Display score
    print("\n" + "=" * 60)
    print(f"Git Workflow Score: {result['score']}/{result['max_score']}")

    if result['passed']:
        print("[+] PASSED - Git workflow is good")
    else:
        print("[X] FAILED - Git workflow needs improvement")

    return result


def main():
    """Skill entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Git workflow assessor for academic projects'
    )
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--min-commits', type=int, default=10, help='Minimum commits required')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    result = run_git_assessment(args.project_path, args.min_commits)

    if args.json:
        # Convert commits for JSON serialization
        json_result = dict(result)
        if 'commits' in json_result:
            json_result['commits'] = [
                {
                    'hash': c.hash,
                    'message': c.message,
                    'author': c.author,
                    'date': c.date
                }
                for c in result['commits']
            ]
        print("\n" + json.dumps(json_result, indent=2))

    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
