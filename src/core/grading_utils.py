"""
Grading Utilities Module

Helper functions for calculating grades and formatting results.
"""

from typing import Dict


def calculate_grade(score: float) -> str:
    """
    Calculate letter grade from numerical score.

    Args:
        score: Numerical score (0-100)

    Returns:
        str: Letter grade (A, B, C, D, or F)

    Example:
        >>> grade = calculate_grade(85)
        >>> print(grade)
        B
    """
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def format_results_summary(results: Dict) -> str:
    """
    Format grading results into a readable summary.

    Args:
        results: Grading results from run_all_skills()

    Returns:
        str: Formatted summary string
    """
    lines = []
    lines.append("=" * 60)
    lines.append("GRADING SUMMARY")
    lines.append("=" * 60)

    res = results['results']
    lines.append(f"Security:       {res['security']['score']:>5.1f} / 10")
    lines.append(f"Code Quality:   {res['code_quality']['score']:>5.1f} / 30")
    lines.append(f"Documentation:  {res['documentation']['score']:>5.1f} / 25")
    lines.append(f"Testing:        {res['testing']['score']:>5.1f} / 15")
    lines.append(f"Git Workflow:   {res['git']['score']:>5.1f} / 10")
    lines.append(f"Research:       {res['research']['score']:>5.1f} / 10")
    lines.append("-" * 60)
    lines.append(f"TOTAL:          {results['total_score']:>5.1f} / 100")
    lines.append(f"GRADE:          {results['grade']}")
    lines.append(f"STATUS:         {'PASSED' if results['passed'] else 'FAILED'}")
    lines.append("=" * 60)

    return '\n'.join(lines)
