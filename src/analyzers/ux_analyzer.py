"""
User Experience (UX) Analyzer Module

Evaluates user experience quality in academic software projects.
Checks for clear documentation, CLI help availability, and usability.

Focus: Command-line tools, documentation clarity, error handling.
"""

from typing import Dict

from ..validators.readme_validator import check_readme_usability
from ..utils.file_finder import find_code_files


def check_cli_help(project_path: str) -> Dict:
    """
    Check for CLI help implementation in Python files.

    Args:
        project_path: Root directory of project

    Returns:
        Dict with CLI help metrics (score out of 3)

    Example:
        >>> result = check_cli_help('/path/to/project')
        >>> print(f"CLI help score: {result['score']}/3")
    """
    py_files = find_code_files(project_path, extensions=['.py'])
    has_argparse = False
    has_help_flag = False

    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Check for argparse usage
            if 'argparse' in content or 'ArgumentParser' in content:
                has_argparse = True

            # Check for help flags
            if '--help' in content or 'add_help' in content:
                has_help_flag = True

            if has_argparse and has_help_flag:
                break
        except Exception:
            continue

    score = 0
    if has_argparse:
        score += 2
    if has_help_flag:
        score += 1

    return {
        'score': score,
        'has_argparse': has_argparse,
        'has_help_flag': has_help_flag
    }


def evaluate_ux_quality(project_path: str) -> Dict:
    """
    Evaluate overall UX quality.

    Args:
        project_path: Root directory of project

    Returns:
        Dict with UX evaluation results and score (out of 10)

    Example:
        >>> result = evaluate_ux_quality('/path/to/project')
        >>> print(f"UX Score: {result['score']}/10")
    """
    # Check README usability (max 4 points)
    readme_result = check_readme_usability(project_path)

    # Check CLI help (max 3 points)
    cli_result = check_cli_help(project_path)

    # Calculate total score
    score = readme_result['score'] + cli_result['score']

    # Bonus points for excellent documentation (max 3 points)
    if readme_result.get('has_code_examples'):
        score += 2
    if len(readme_result.get('sections', [])) >= 5:
        score += 1

    score = min(10, score)  # Cap at 10

    return {
        'score': score,
        'max_score': 10,
        'passed': score >= 7,  # 70% threshold
        'readme_result': readme_result,
        'cli_result': cli_result,
        'message': _build_ux_message(readme_result, cli_result, score)
    }


def _build_ux_message(readme: Dict, cli: Dict, score: int) -> str:
    """Build UX evaluation message."""
    if not readme['has_readme']:
        return 'No README found - critical UX issue'
    if score >= 8:
        return 'Excellent user experience - clear documentation and help'
    if score >= 7:
        return 'Good user experience - adequate documentation'
    return 'UX needs improvement - enhance documentation and help'
