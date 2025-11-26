#!/usr/bin/env python
"""
Grade From Git - Clone and grade Git repositories

Usage:
    python grade_from_git.py <repo_url> [branch] [--output FILE] [--no-cleanup]

Examples:
    python grade_from_git.py https://github.com/user/project.git
    python grade_from_git.py https://github.com/user/project.git main
    python grade_from_git.py https://github.com/user/project.git --output results.json
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.git_clone import clone_repository, cleanup_clone
from src.utils.git_helpers import is_git_url
from src.core.skill_executor import run_all_skills
from src.core.grading_utils import format_results_summary
from src.cli.arg_parser import create_arg_parser


def grade_from_git(repo_url, branch=None, output_file=None, cleanup=True):
    """
    Clone a Git repository and grade it.

    Args:
        repo_url: Git repository URL
        branch: Branch to clone (optional)
        output_file: Path to save results JSON (optional)
        cleanup: Whether to cleanup after grading

    Returns:
        dict: Grading results or None on failure
    """
    # Validate URL
    if not is_git_url(repo_url):
        print(f"\n[X] Error: '{repo_url}' is not a valid Git URL")
        print("\nExpected format:")
        print("  https://github.com/user/repo.git")
        print("  git@github.com:user/repo.git")
        return None

    print("\n" + "=" * 60)
    print("GRADE FROM GIT")
    print("=" * 60)
    print(f"\nRepository: {repo_url}")
    if branch:
        print(f"Branch: {branch}")

    # Clone repository
    print(f"\n[*] Cloning repository...")
    clone_result = clone_repository(repo_url, branch=branch, depth=1)

    if not clone_result['success']:
        print(f"\n[X] Clone failed: {clone_result['message']}")
        return None

    cloned_path = clone_result['path']
    repo_name = clone_result['repo_name']

    print(f"[+] Successfully cloned to: {cloned_path}")

    # Grade the repository
    print(f"\n[*] Running auto-grader on {repo_name}...\n")
    results = run_all_skills(cloned_path)

    # Add repository metadata
    results['repository'] = {
        'url': repo_url,
        'name': repo_name,
        'branch': branch,
        'cloned_path': cloned_path
    }

    # Display summary
    print("\n" + format_results_summary(results))

    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n[+] Full report saved to: {output_file}")

    # Cleanup if requested
    if cleanup:
        print(f"\n[*] Cleaning up cloned repository...")
        cleanup_clone(cloned_path)
        print("[+] Cleanup complete")
    else:
        print(f"\n[*] Repository kept at: {cloned_path}")

    return results


def main():
    """Main entry point."""
    parser = create_arg_parser()
    args = parser.parse_args()

    # Run grading
    result = grade_from_git(
        repo_url=args.repo_url,
        branch=args.branch,
        output_file=args.output,
        cleanup=not args.no_cleanup
    )

    # JSON output mode
    if args.json and result:
        print("\n" + json.dumps(result, indent=2, default=str))

    # Exit with appropriate code
    if result:
        sys.exit(0 if result['passed'] else 1)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
