"""
Skill Executor Module

Executes individual grading skills and collects results.
Provides a unified interface for running all skills.
"""

import os
import sys
from pathlib import Path
from typing import Dict

# Import all skill functions
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.analyzers.file_size_analyzer import check_file_sizes, generate_size_report
from src.analyzers.docstring_analyzer import analyze_project_docstrings
from src.validators.naming_validator import analyze_project_naming
from src.analyzers.security_scanner import scan_for_secrets
from src.validators.gitignore_validator import validate_gitignore
from src.validators.env_validator import check_env_template
from src.analyzers.documentation_checker import check_project_documentation
from src.analyzers.test_analyzer import evaluate_tests
from src.analyzers.git_analyzer import assess_git_workflow
from src.analyzers.research_analyzer import evaluate_research_quality
from src.analyzers.ux_analyzer import evaluate_ux_quality
from .grading_utils import calculate_grade


def run_security_check(project_path: str) -> Dict:
    """Run security validation skill."""
    secrets = scan_for_secrets(project_path)
    gitignore = validate_gitignore(project_path)
    env = check_env_template(project_path)

    has_secrets = len(secrets) > 0
    score = 10 if not has_secrets and gitignore['passed'] and env['passed'] else 0

    if has_secrets:
        score = 0
    elif not gitignore['passed']:
        score -= 3
    elif not env['passed']:
        score -= 2

    return {
        'score': max(0, score),
        'max_score': 10,
        'passed': score >= 7,
        'secrets_found': len(secrets),
        'gitignore_valid': gitignore['passed'],
        'env_valid': env['passed']
    }


def run_code_analysis(project_path: str) -> Dict:
    """Run code quality analysis skill."""
    size_violations = check_file_sizes(project_path, limit=150)
    docstring_result = analyze_project_docstrings(project_path, min_coverage=0.9)
    naming_result = analyze_project_naming(project_path)

    max_score = 30
    score = max_score

    # File size violations
    score -= len(size_violations) * 5

    # Docstring coverage
    if not docstring_result['passed']:
        coverage_gap = 0.9 - docstring_result['coverage']
        score -= coverage_gap * 20

    # Naming violations
    score -= len(naming_result['violations']) * 0.5

    score = max(0, min(score, max_score))

    return {
        'score': score,
        'max_score': max_score,
        'passed': score >= 21,
        'file_size_violations': len(size_violations),
        'docstring_coverage': docstring_result['coverage'],
        'naming_violations': len(naming_result['violations'])
    }


def run_all_skills(project_path: str) -> Dict:
    """
    Run all grading skills and aggregate results.

    Args:
        project_path: Root directory of project to grade

    Returns:
        Dict with all skill results and total score

    Example:
        >>> results = run_all_skills('/path/to/project')
        >>> print(f"Total Score: {results['total_score']}/100")
    """
    print(f"[*] Running comprehensive auto-grader on: {project_path}\n")

    results = {}

    # Run all skills
    print("[*] Security check...")
    results['security'] = run_security_check(project_path)

    print("[*] Code analysis...")
    results['code_quality'] = run_code_analysis(project_path)

    print("[*] Documentation validation...")
    results['documentation'] = check_project_documentation(project_path)

    print("[*] Test evaluation...")
    results['testing'] = evaluate_tests(project_path)

    print("[*] Git assessment...")
    results['git'] = assess_git_workflow(project_path)

    print("[*] Research evaluation...")
    results['research'] = evaluate_research_quality(project_path)

    print("[*] UX evaluation...")
    results['ux'] = evaluate_ux_quality(project_path)

    # Calculate total
    total = (
        results['security']['score'] +
        results['code_quality']['score'] +
        results['documentation']['score'] +
        results['testing']['score'] +
        results['git']['score'] +
        results['research']['score']
    )

    return {
        'results': results,
        'total_score': total,
        'max_score': 100,
        'percentage': (total / 100) * 100,
        'passed': total >= 70,
        'grade': calculate_grade(total)
    }
