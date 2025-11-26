"""
Git Helper Functions

URL validation, name extraction, and command execution.
"""

import subprocess
import re
from typing import Dict


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


def execute_git_clone(cmd: list, repo_url: str, repo_name: str) -> Dict:
    """
    Execute git clone command and handle errors.

    Args:
        cmd: Git clone command as list
        repo_url: Repository URL (for error messages)
        repo_name: Repository name (for error messages)

    Returns:
        dict: Result with success status and message
    """
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
                'message': f'Successfully cloned {repo_url}'
            }
        else:
            return {
                'success': False,
                'message': f'Git clone failed: {result.stderr}'
            }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'message': 'Git clone timed out (>5 minutes)'
        }
    except FileNotFoundError:
        return {
            'success': False,
            'message': 'Git command not found. Please install Git.'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error cloning repository: {str(e)}'
        }
