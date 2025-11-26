"""
Sample project fixture for integration testing.

Creates a complete project structure for grading tests.
"""

import pytest
import subprocess
from pathlib import Path


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
    subprocess.run(['git', 'init'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=project_path, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'feat: Initial commit'], cwd=project_path, capture_output=True)

    return str(project_path)
