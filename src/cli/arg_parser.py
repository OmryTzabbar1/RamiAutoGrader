"""
CLI Argument Parser for grade_from_git script.

Defines command-line arguments and usage examples.
"""

import argparse


def create_arg_parser():
    """
    Create and configure argument parser for grade_from_git.

    Returns:
        argparse.ArgumentParser: Configured parser

    Example:
        >>> parser = create_arg_parser()
        >>> args = parser.parse_args(['https://github.com/user/repo.git'])
        >>> print(args.repo_url)
        https://github.com/user/repo.git
    """
    parser = argparse.ArgumentParser(
        description='Clone and grade a Git repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Grade a repository (default branch)
  python grade_from_git.py https://github.com/user/project.git

  # Grade specific branch
  python grade_from_git.py https://github.com/user/project.git main

  # Save results to file
  python grade_from_git.py https://github.com/user/project.git --output report.json

  # Keep cloned repository for manual review
  python grade_from_git.py https://github.com/user/project.git --no-cleanup

  # Full example
  python grade_from_git.py https://github.com/user/project.git develop --output results/project.json
        """
    )

    parser.add_argument(
        'repo_url',
        help='Git repository URL (https:// or git@)'
    )

    parser.add_argument(
        'branch',
        nargs='?',
        default=None,
        help='Branch to clone (optional, uses default branch if not specified)'
    )

    parser.add_argument(
        '--output',
        '-o',
        help='Save grading report to JSON file'
    )

    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help='Keep cloned repository after grading (default: cleanup)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output only JSON results (no summary)'
    )

    return parser
