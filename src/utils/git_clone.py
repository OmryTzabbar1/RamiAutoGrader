"""
Git Clone Utilities

Helper functions for cloning Git repositories for grading.
Supports HTTPS and SSH URLs, branch selection, and cleanup.
"""

import subprocess
import tempfile
import shutil
import re
from pathlib import Path
from typing import Dict, Optional


def is_git_url(url: str) -> bool:
    """
    Check if string is a valid Git URL.

    Args:
        url: String to check

    Returns:
        bool: True if valid Git URL

    Example:
        >>> is_git_url("https://github.com/user/repo.git")
        True
        >>> is_git_url("/local/path")
        False
    """
    git_patterns = [
        r'^https?://github\.com/.+/.+',
        r'^git@github\.com:.+/.+',
        r'^https?://gitlab\.com/.+/.+',
        r'^git@gitlab\.com:.+/.+',
        r'^https?://bitbucket\.org/.+/.+',
        r'\.git$'
    ]

    return any(re.search(pattern, url) for pattern in git_patterns)


def extract_repo_name(url: str) -> str:
    """
    Extract repository name from Git URL.

    Args:
        url: Git repository URL

    Returns:
        str: Repository name

    Example:
        >>> extract_repo_name("https://github.com/user/my-project.git")
        'my-project'
    """
    # Remove .git suffix if present
    url = url.rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]

    # Extract last part of path
    parts = url.split('/')
    return parts[-1]


def clone_repository(
    repo_url: str,
    target_dir: Optional[str] = None,
    branch: Optional[str] = None,
    depth: int = 1
) -> Dict:
    """
    Clone a Git repository to a target directory.

    Args:
        repo_url: Git repository URL (HTTPS or SSH)
        target_dir: Directory to clone into (creates temp if None)
        branch: Branch to clone (default branch if None)
        depth: Clone depth (1 for shallow clone, None for full)

    Returns:
        dict: {
            'success': bool,
            'path': str (path to cloned repo),
            'message': str,
            'temp': bool (True if using temp directory)
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

    try:
        # Run git clone
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            return {
                'success': True,
                'path': clone_path,
                'message': f'Successfully cloned {repo_url}',
                'temp': is_temp,
                'repo_name': repo_name
            }
        else:
            return {
                'success': False,
                'path': None,
                'message': f'Git clone failed: {result.stderr}',
                'temp': is_temp,
                'repo_name': repo_name
            }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'path': None,
            'message': 'Git clone timed out (>5 minutes)',
            'temp': is_temp,
            'repo_name': repo_name
        }
    except FileNotFoundError:
        return {
            'success': False,
            'path': None,
            'message': 'Git command not found. Please install Git.',
            'temp': is_temp,
            'repo_name': repo_name
        }
    except Exception as e:
        return {
            'success': False,
            'path': None,
            'message': f'Error cloning repository: {str(e)}',
            'temp': is_temp,
            'repo_name': repo_name
        }


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
