"""
Detailed Report Generator Module

Generates comprehensive, actionable grading reports with specific
file paths, line numbers, and fix recommendations.
"""

from typing import Dict, List
from pathlib import Path


def generate_detailed_report(results: Dict, project_path: str) -> str:
    """
    Generate detailed grading report with specific issues and fixes.

    Args:
        results: Complete grading results from run_all_skills()
        project_path: Path to graded project

    Returns:
        str: Formatted detailed report
    """
    lines = []
    project_name = Path(project_path).name

    # Header
    lines.append("\n" + "=" * 80)
    lines.append(f"DETAILED GRADING REPORT: {project_name}")
    lines.append("=" * 80)
    lines.append(f"\nTotal Score: {results['total_score']:.1f}/100")
    lines.append(f"Grade: {results['grade']}")
    lines.append(f"Status: {'PASSED' if results['passed'] else 'FAILED'}")
    lines.append("")

    res = results['results']

    # Security Details
    lines.extend(_format_security_details(res['security']))

    # Code Quality Details
    lines.extend(_format_code_quality_details(res['code_quality']))

    # Documentation Details
    lines.extend(_format_documentation_details(res['documentation']))

    # Testing Details
    lines.extend(_format_testing_details(res['testing']))

    # Git Workflow Details
    lines.extend(_format_git_details(res['git']))

    # Research Details
    lines.extend(_format_research_details(res['research']))

    # Summary of Action Items
    lines.extend(_format_action_items(results))

    lines.append("=" * 80)
    return '\n'.join(lines)


def _format_security_details(security: Dict) -> List[str]:
    """Format detailed security findings."""
    lines = []
    lines.append("-" * 80)
    lines.append(f"SECURITY: {security['score']}/10")
    lines.append("-" * 80)

    if security['score'] == 10:
        lines.append("✓ PERFECT - No security issues found")
    else:
        if security['secrets_found'] > 0:
            lines.append(f"✗ CRITICAL: {security['secrets_found']} hardcoded secret(s) detected!")
            lines.append("  This is an automatic fail. Remove all hardcoded credentials.")
            lines.append("")

        if not security.get('gitignore_valid'):
            lines.append("✗ .gitignore incomplete or missing")
            lines.append("  Required patterns: .env, *.key, *.pem, __pycache__, etc.")
            lines.append("")

        if not security.get('env_valid'):
            lines.append("✗ Missing .env.example template")
            lines.append("  Create .env.example with placeholder values")
            lines.append("")

    lines.append("")
    return lines


def _format_code_quality_details(code: Dict) -> List[str]:
    """Format detailed code quality findings."""
    lines = []
    lines.append("-" * 80)
    lines.append(f"CODE QUALITY: {code['score']}/30")
    lines.append("-" * 80)

    violations = code.get('file_size_violations', 0)
    if violations > 0:
        lines.append(f"✗ FILE SIZE VIOLATIONS: {violations} file(s) exceed 150-line limit")
        lines.append(f"  Penalty: -{violations * 5} points")
        lines.append("")
        lines.append("  FILES TO REFACTOR:")
        # Note: Detailed file list would come from full results
        lines.append("  Run: python -c \"from src.analyzers.file_size_analyzer import check_file_sizes; ")
        lines.append("       violations = check_file_sizes('.', 150);")
        lines.append("       for v in violations: print(f'{v.file_path}: {v.line_count} lines')\"")
        lines.append("")
    else:
        lines.append("✓ All files under 150-line limit")
        lines.append("")

    coverage = code.get('docstring_coverage', 0)
    if coverage < 0.9:
        lines.append(f"✗ DOCSTRING COVERAGE: {coverage:.1%} (minimum: 90%)")
        missing_count = code.get('docstrings', {}).get('missing', [])
        if isinstance(missing_count, list):
            lines.append(f"  {len(missing_count)} functions/classes missing docstrings")
        lines.append("")
    else:
        lines.append(f"✓ Docstring coverage: {coverage:.1%}")
        lines.append("")

    naming_violations = code.get('naming_violations', 0)
    if naming_violations > 0:
        lines.append(f"⚠ NAMING VIOLATIONS: {naming_violations}")
        lines.append("  Follow conventions: snake_case, PascalCase, UPPER_SNAKE_CASE")
        lines.append("")

    lines.append("")
    return lines


def _format_documentation_details(docs: Dict) -> List[str]:
    """Format detailed documentation findings."""
    lines = []
    lines.append("-" * 80)
    lines.append(f"DOCUMENTATION: {docs['score']}/25")
    lines.append("-" * 80)

    lines.append(f"Documents Found: {docs.get('docs_passed', 0)}/{docs.get('total_docs', 5)}")
    lines.append("")

    missing = docs.get('docs_missing', 0)
    if missing > 0:
        lines.append(f"✗ MISSING DOCUMENTS: {missing}")
        lines.append("  Required: PRD.md, README.md, PLANNING.md, TASKS.md, CLAUDE.md")
        lines.append("")

    incomplete = docs.get('docs_incomplete', 0)
    if incomplete > 0:
        lines.append(f"⚠ INCOMPLETE DOCUMENTS: {incomplete}")
        results_dict = docs.get('results', {})
        for doc_name, doc_result in results_dict.items():
            if not doc_result.get('passed') and doc_result.get('exists'):
                wc = doc_result.get('word_count', 0)
                lines.append(f"  • {doc_name}: {wc} words (needs more detail)")
        lines.append("")

    lines.append("")
    return lines


def _format_testing_details(testing: Dict) -> List[str]:
    """Format detailed testing findings."""
    lines = []
    lines.append("-" * 80)
    lines.append(f"TESTING: {testing['score']}/15")
    lines.append("-" * 80)

    if not testing.get('has_tests'):
        lines.append("✗ NO TESTS FOUND")
        lines.append("  Create test files in tests/ directory")
        lines.append("")
    else:
        test_count = testing.get('total_tests', 0)
        lines.append(f"Tests Found: {test_count}")

        if test_count < 5:
            lines.append("⚠ Insufficient test coverage (minimum: 5 tests recommended)")
        else:
            lines.append("✓ Adequate test count")
        lines.append("")

    lines.append("")
    return lines


def _format_git_details(git: Dict) -> List[str]:
    """Format detailed git workflow findings."""
    lines = []
    lines.append("-" * 80)
    lines.append(f"GIT WORKFLOW: {git['score']}/10")
    lines.append("-" * 80)

    if not git.get('is_git_repo'):
        lines.append("✗ NOT A GIT REPOSITORY")
        lines.append("  Initialize: git init")
        lines.append("")
    else:
        commit_count = git.get('commit_count', 0)
        lines.append(f"Commits: {commit_count}")

        if commit_count < 10:
            lines.append(f"⚠ Only {commit_count} commits (minimum: 10, recommended: 15-25)")
            lines.append("  Make atomic commits showing development progression")
        else:
            lines.append("✓ Good commit history")
        lines.append("")

        short_msgs = git.get('short_messages', 0)
        if short_msgs > 0:
            lines.append(f"⚠ {short_msgs} commit(s) with short messages (<10 chars)")
            lines.append("")

    lines.append("")
    return lines


def _format_research_details(research: Dict) -> List[str]:
    """Format detailed research findings."""
    lines = []
    lines.append("-" * 80)
    lines.append(f"RESEARCH: {research['score']}/10")
    lines.append("-" * 80)

    if research['score'] < 10:
        lines.append("⚠ RESEARCH DOCUMENTATION INCOMPLETE")
        lines.append("  Expected:")
        lines.append("  • prompts/ directory with prompt examples")
        lines.append("  • Parameter exploration analysis")
        lines.append("  • Comparative analysis of approaches")
        lines.append("")

    lines.append("")
    return lines


def _format_action_items(results: Dict) -> List[str]:
    """Format actionable items to improve score."""
    lines = []
    lines.append("-" * 80)
    lines.append("ACTION ITEMS TO IMPROVE SCORE")
    lines.append("-" * 80)

    res = results['results']
    items = []

    # Prioritize by point value
    code_score = res['code_quality']['score']
    if code_score < 30:
        potential = 30 - code_score
        items.append((potential, "CODE QUALITY", [
            "Refactor files exceeding 150 lines",
            "Add missing docstrings",
            "Fix naming convention violations"
        ]))

    doc_score = res['documentation']['score']
    if doc_score < 25:
        potential = 25 - doc_score
        items.append((potential, "DOCUMENTATION", [
            "Complete PLANNING.md with design decisions",
            "Expand TASKS.md with all development tasks",
            "Add architecture diagrams"
        ]))

    test_score = res['testing']['score']
    if test_score < 15:
        potential = 15 - test_score
        items.append((potential, "TESTING", [
            "Add more test cases (aim for 30+)",
            "Improve coverage to 70%+",
            "Test edge cases"
        ]))

    git_score = res['git']['score']
    if git_score < 10:
        potential = 10 - git_score
        items.append((potential, "GIT WORKFLOW", [
            "Create 15-25 atomic commits",
            "Use conventional commit format",
            "Show development progression"
        ]))

    # Sort by potential points (highest first)
    items.sort(reverse=True, key=lambda x: x[0])

    if not items:
        lines.append("✓ Excellent work! No major improvements needed.")
    else:
        for potential, category, actions in items:
            lines.append(f"\n{category} (+{potential:.0f} points potential):")
            for action in actions:
                lines.append(f"  □ {action}")

    lines.append("")
    return lines
