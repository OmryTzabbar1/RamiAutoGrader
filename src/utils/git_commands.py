"""
Git Command Utilities

Wrapper functions for executing git commands and parsing output.
Used by git analyzer to inspect repository history.
"""

import subprocess
from typing import List
from dataclasses import dataclass


@dataclass
class CommitInfo:
    """Information about a git commit."""
    hash: str
    message: str
    author: str
    date: str

    @property
    def message_length(self) -> int:
        """Get commit message length."""
        return len(self.message)

    @property
    def is_meaningful(self) -> bool:
        """Check if commit message is meaningful (not vague)."""
        import re
        vague_patterns = [
            r'^update',
            r'^fix',
            r'^wip',
            r'^tmp',
            r'^test',
            r'^\.',
        ]
        message_lower = self.message.lower()
        return not any(re.match(pattern, message_lower) for pattern in vague_patterns)


def check_git_repo(project_path: str) -> bool:
    """
    Check if directory is a git repository.

    Args:
        project_path: Path to check

    Returns:
        bool: True if git repo exists
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def get_commit_history(project_path: str, limit: int = 100) -> List[CommitInfo]:
    """
    Get git commit history.

    Args:
        project_path: Root directory of git repo
        limit: Maximum commits to fetch (default: 100)

    Returns:
        List[CommitInfo]: Commit information

    Example:
        >>> commits = get_commit_history('/path/to/repo')
        >>> print(f"Found {len(commits)} commits")
    """
    try:
        # Get commit log with custom format
        result = subprocess.run(
            ['git', 'log', f'-{limit}', '--format=%H|%s|%an|%ad'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|', 3)
            if len(parts) == 4:
                commits.append(CommitInfo(
                    hash=parts[0],
                    message=parts[1],
                    author=parts[2],
                    date=parts[3]
                ))

        return commits
    except Exception:
        return []
