#!/usr/bin/env python
"""
Git Clone Skill

Clones a Git repository with full history for comprehensive grading.
This skill is designed to be called by the grade-project agent.

Usage:
    /skill git-clone <github_url>

Example:
    /skill git-clone https://github.com/user/repo.git
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.git_clone import clone_repository


def main():
    """Main entry point for git-clone skill."""
    if len(sys.argv) < 2:
        print("Usage: /skill git-clone <github_url>")
        print("\nExample:")
        print("  /skill git-clone https://github.com/user/repo.git")
        sys.exit(1)

    github_url = sys.argv[1]

    # Validate URL
    if not github_url.startswith(('http://', 'https://')):
        print(f"Error: Invalid GitHub URL: {github_url}")
        print("URL must start with http:// or https://")
        sys.exit(1)

    if 'github.com' not in github_url:
        print(f"Error: Not a GitHub URL: {github_url}")
        sys.exit(1)

    print(f"Cloning repository: {github_url}")
    print("Using full clone (depth=None) to preserve git history...\n")

    try:
        # Clone with full history for git workflow assessment
        result = clone_repository(github_url, depth=None)

        print(f"[OK] Repository cloned successfully!")
        print(f"\nCloned to: {result['path']}")
        print(f"Branch: {result.get('branch', 'N/A')}")
        print(f"Temp directory: {result.get('temp_dir', 'N/A')}")

        # Output in format agent can parse
        print(f"\n__CLONED_PATH__={result['path']}")

    except Exception as e:
        print(f"[FAIL] Clone error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
