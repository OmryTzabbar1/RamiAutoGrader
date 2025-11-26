"""
End-to-end test for the entire grading system.

Tests the complete workflow by grading the auto-grader project itself.
"""

import pytest
from pathlib import Path
from src.core.skill_executor import run_all_skills


def test_grade_self():
    """
    End-to-end test: Grade the auto-grader project itself.

    This test exercises all grading skills and provides comprehensive
    coverage of the entire codebase.
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Run the grader on itself
    results = run_all_skills(str(project_root))

    # Verify basic structure
    assert 'results' in results
    assert 'total_score' in results
    assert 'grade' in results
    assert 'passed' in results

    # Verify all categories were evaluated
    assert 'security' in results['results']
    assert 'code_quality' in results['results']
    assert 'documentation' in results['results']
    assert 'testing' in results['results']
    assert 'git' in results['results']
    assert 'research' in results['results']

    # Verify scores are in valid ranges
    assert 0 <= results['total_score'] <= 100
    assert results['grade'] in ['A', 'B', 'C', 'D', 'F']

    # Auto-grader should pass its own tests
    # (After we complete the test suite, this should be True!)
    print(f"\nAuto-Grader Self-Assessment: {results['total_score']}/100 ({results['grade']})")
    print(f"Passed: {results['passed']}")


def test_all_skills_return_scores():
    """Test that all skills return valid scores."""
    project_root = Path(__file__).parent.parent
    results = run_all_skills(str(project_root))

    for category, result in results['results'].items():
        assert 'score' in result, f"{category} missing score"
        assert 'max_score' in result, f"{category} missing max_score"
        assert 'passed' in result, f"{category} missing passed status"

        # Verify score is within valid range
        assert 0 <= result['score'] <= result['max_score'], \
            f"{category} score {result['score']} out of range [0, {result['max_score']}]"
