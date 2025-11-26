"""
Integration tests for full grading workflow.

Tests the complete end-to-end grading process.
"""

import pytest
from pathlib import Path
from src.core.skill_executor import run_all_skills
from src.core.grading_utils import calculate_grade


@pytest.fixture
def sample_project(temp_dir):
    """Create a complete sample project for testing."""
    project_path = Path(temp_dir)

    # Create source files
    (project_path / "src").mkdir()
    (project_path / "src" / "__init__.py").write_text("")
    (project_path / "src" / "main.py").write_text('''"""
Main module for sample project.
"""


def main():
    """Run the main application."""
    print("Hello, World!")


if __name__ == "__main__":
    main()
''')

    # Create documentation
    (project_path / "README.md").write_text('''# Sample Project

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
python src/main.py
```
''')

    (project_path / "PRD.md").write_text('''# Product Requirements Document

## Problem Statement
This is a sample project.

## Functional Requirements
- Feature 1
- Feature 2
''')

    (project_path / "PLANNING.md").write_text('''# Planning Document

## Architecture
System design here.
''')

    (project_path / "TASKS.md").write_text('''# Tasks

- [x] Task 1
- [ ] Task 2
''')

    # Create .gitignore
    (project_path / ".gitignore").write_text('''.env
*.key
*.pem
credentials.json
secrets.yaml
__pycache__/
''')

    # Create .env.example
    (project_path / ".env.example").write_text('''API_KEY=your_key_here
''')

    # Initialize git
    import subprocess
    subprocess.run(['git', 'init'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'feat: Initial commit'], cwd=project_path, capture_output=True)

    return str(project_path)


class TestFullGradingWorkflow:
    """Integration tests for complete grading workflow."""

    def test_run_all_skills_returns_results(self, sample_project):
        """Test that run_all_skills returns complete results."""
        results = run_all_skills(sample_project)

        assert 'results' in results
        assert 'total_score' in results
        assert 'max_score' in results
        assert 'percentage' in results
        assert 'grade' in results
        assert 'passed' in results

    def test_all_categories_evaluated(self, sample_project):
        """Test that all grading categories are evaluated."""
        results = run_all_skills(sample_project)

        assert 'security' in results['results']
        assert 'code_quality' in results['results']
        assert 'documentation' in results['results']
        assert 'testing' in results['results']
        assert 'git' in results['results']
        assert 'research' in results['results']

    def test_each_category_has_score(self, sample_project):
        """Test that each category has a score."""
        results = run_all_skills(sample_project)

        for category, result in results['results'].items():
            assert 'score' in result
            assert 'max_score' in result
            assert 'passed' in result
            assert result['score'] >= 0
            assert result['score'] <= result['max_score']

    def test_total_score_calculation(self, sample_project):
        """Test that total score is calculated correctly."""
        results = run_all_skills(sample_project)

        expected_total = sum(
            results['results'][cat]['score']
            for cat in ['security', 'code_quality', 'documentation', 'testing', 'git', 'research']
        )

        assert results['total_score'] == pytest.approx(expected_total, rel=0.01)

    def test_percentage_calculation(self, sample_project):
        """Test that percentage is calculated correctly."""
        results = run_all_skills(sample_project)

        expected_percentage = (results['total_score'] / results['max_score']) * 100
        assert results['percentage'] == pytest.approx(expected_percentage, rel=0.01)

    def test_grade_assignment(self, sample_project):
        """Test that grade is assigned correctly."""
        results = run_all_skills(sample_project)

        expected_grade = calculate_grade(results['total_score'])
        assert results['grade'] == expected_grade

    def test_pass_fail_determination(self, sample_project):
        """Test that pass/fail is determined correctly."""
        results = run_all_skills(sample_project)

        expected_passed = results['total_score'] >= 70
        assert results['passed'] == expected_passed

    def test_max_score_is_100(self, sample_project):
        """Test that maximum score is 100."""
        results = run_all_skills(sample_project)

        assert results['max_score'] == 100

    def test_security_category_works(self, sample_project):
        """Test that security check runs successfully."""
        results = run_all_skills(sample_project)
        security = results['results']['security']

        assert 'secrets_found' in security
        assert 'gitignore_valid' in security
        assert 'env_valid' in security

    def test_code_quality_category_works(self, sample_project):
        """Test that code quality check runs successfully."""
        results = run_all_skills(sample_project)
        code_quality = results['results']['code_quality']

        assert 'file_size_violations' in code_quality
        assert 'docstring_coverage' in code_quality
        assert 'naming_violations' in code_quality

    def test_git_category_works(self, sample_project):
        """Test that git workflow check runs successfully."""
        results = run_all_skills(sample_project)
        git = results['results']['git']

        assert 'is_git_repo' in git
        assert 'commit_count' in git
        assert git['is_git_repo'] is True
