"""
Test Analyzer Module

Evaluates test coverage and quality in academic software projects.
Analyzes test files and provides scoring based on test presence and quality.

Target: 70% minimum coverage, 90% for critical paths.
"""

from typing import Dict

from ..utils.file_finder import find_test_files
from .test_counter import analyze_test_file


def evaluate_tests(project_path: str, language: str = 'python') -> Dict:
    """
    Evaluate test suite quality and coverage.

    Args:
        project_path: Root directory of project
        language: Programming language (default: 'python')

    Returns:
        Dict with test evaluation results and score (out of 15)

    Example:
        >>> result = evaluate_tests('/path/to/project')
        >>> print(f"Test Score: {result['score']}/15")
        Test Score: 12/15
    """
    test_files = find_test_files(project_path, language)

    if not test_files:
        return {
            'score': 0,
            'max_score': 15,
            'passed': False,
            'test_files_found': 0,
            'total_tests': 0,
            'has_tests': False,
            'message': 'No test files found'
        }

    # Analyze all test files
    total_tests = 0
    total_assertions = 0
    file_results = []

    for test_file in test_files:
        result = analyze_test_file(test_file)
        file_results.append(result)

        if 'num_tests' in result:
            total_tests += result['num_tests']
            total_assertions += result.get('num_assertions', 0)

    # Calculate score using helper
    score, message = _calculate_test_score(total_tests, total_assertions)

    return {
        'score': score,
        'max_score': 15,
        'passed': score >= 10.5,  # 70% threshold
        'test_files_found': len(test_files),
        'total_tests': total_tests,
        'total_assertions': total_assertions,
        'has_tests': total_tests > 0,
        'file_results': file_results,
        'message': message
    }


def _calculate_test_score(total_tests: int, total_assertions: int) -> tuple:
    """Calculate score and message based on test metrics."""
    max_score = 15
    score = max_score

    # Penalty for no tests
    if total_tests == 0:
        return 0, 'No tests found in test files'

    # Penalty for too few tests
    if total_tests < 5:
        score -= 5
        message = f'Only {total_tests} tests found (minimum 5 recommended)'
    # Penalty for low assertion count
    elif total_assertions < total_tests:
        score -= 3
        message = f'Low assertion count ({total_assertions} assertions for {total_tests} tests)'
    else:
        message = f'Found {total_tests} tests with {total_assertions} assertions'

    return max(0, score), message
