"""
Git Analyzer Module

Analyzes git repository history and workflow quality.
Evaluates commit count, message quality, and development progression.

Requirements: Minimum 10 commits with meaningful messages.
"""

from typing import Dict

from ..utils.git_commands import check_git_repo, get_commit_history


def assess_git_workflow(project_path: str, min_commits: int = 10) -> Dict:
    """
    Assess git workflow quality.

    Args:
        project_path: Root directory of project
        min_commits: Minimum required commits (default: 10)

    Returns:
        Dict with git assessment results and score (out of 10)

    Example:
        >>> result = assess_git_workflow('/path/to/repo')
        >>> print(f"Git Score: {result['score']}/10")
    """
    # Check if git repo exists
    if not check_git_repo(project_path):
        return {
            'score': 0,
            'max_score': 10,
            'passed': False,
            'is_git_repo': False,
            'message': 'Not a git repository'
        }

    # Get commit history
    commits = get_commit_history(project_path)

    if not commits:
        return {
            'score': 0,
            'max_score': 10,
            'passed': False,
            'is_git_repo': True,
            'commit_count': 0,
            'message': 'No commits found'
        }

    # Analyze commits
    total_commits = len(commits)
    short_messages = sum(1 for c in commits if c.message_length < 10)
    vague_messages = sum(1 for c in commits if not c.is_meaningful)

    # Calculate score
    score, message = _calculate_git_score(
        total_commits, min_commits, short_messages, vague_messages
    )

    return {
        'score': score,
        'max_score': 10,
        'passed': score >= 7,  # 70% threshold
        'is_git_repo': True,
        'commit_count': total_commits,
        'short_messages': short_messages,
        'vague_messages': vague_messages,
        'commits': commits[:10],  # First 10 for display
        'message': message
    }


def _calculate_git_score(total: int, min_req: int, short: int, vague: int) -> tuple:
    """Calculate git score and build message."""
    max_score = 10
    score = max_score

    # Penalty for insufficient commits
    if total < min_req:
        score -= 5
        message = f'Only {total} commits (minimum: {min_req})'
    # Penalty for short messages (> 20%)
    elif short > total * 0.2:
        score -= 2
        message = f'{short} commits have short messages (< 10 chars)'
    # Penalty for vague messages (> 30%)
    elif vague > total * 0.3:
        score -= 2
        message = f'{vague} commits have vague messages'
    else:
        message = f'{total} commits with good message quality'

    return max(0, score), message
