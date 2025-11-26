"""
Git Clone Utilities

Helper functions for cloning Git repositories for grading.
Supports HTTPS and SSH URLs, branch selection, and cleanup.
"""

import tempfile
import shutil
from pathlib import Path
from typing import Dict, Optional

from .git_helpers import extract_repo_name, execute_git_clone, is_git_url


def clone_repository(
    repo_url: str,
    target_dir: Optional[str] = None,
    branch: Optional[str] = None,
    depth: Optional[int] = None
) -> Dict:
    """
    Clone a Git repository to a target directory.

    Args:
        repo_url: Git repository URL (HTTPS or SSH)
        target_dir: Directory to clone into (creates temp if None)
        branch: Branch to clone (default branch if None)
        depth: Clone depth (None for full clone, 1 for shallow - default: None for grading)

    Returns:
        dict: {
            'success': bool,
            'path': str (path to cloned repo),
            'message': str,
            'temp': bool (True if using temp directory),
            'repo_name': str
        }

    Example:
        >>> result = clone_repository("https://github.com/user/repo.git")
        >>> print(result['path'])
        /tmp/tmp_xyz/repo
    """
    repo_name = extract_repo_name(repo_url)

    # Create target directory
    if target_dir:
        clone_path = Path(target_dir) / repo_name
        is_temp = False
    else:
        temp_base = tempfile.mkdtemp(prefix='autograder_')
        clone_path = Path(temp_base) / repo_name
        is_temp = True

    clone_path = str(clone_path)

    # Build git clone command
    cmd = ['git', 'clone']

    if depth:
        cmd.extend(['--depth', str(depth)])

    if branch:
        cmd.extend(['--branch', branch])

    cmd.extend([repo_url, clone_path])

    # Execute git clone
    result = execute_git_clone(cmd, repo_url, repo_name)

    # Add path and temp info to result
    if result['success']:
        result['path'] = clone_path
    else:
        result['path'] = None

    result['temp'] = is_temp
    result['repo_name'] = repo_name

    return result


def cleanup_clone(path: str) -> bool:
    """
    Clean up cloned repository directory.

    Args:
        path: Path to cloned repository

    Returns:
        bool: True if cleanup successful

    Example:
        >>> cleanup_clone('/tmp/tmp_xyz/repo')
        True
    """
    try:
        shutil.rmtree(path, ignore_errors=True)
        return True
    except Exception:
        return False
