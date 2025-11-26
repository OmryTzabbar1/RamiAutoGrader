"""
Configuration file fixtures for testing.

Provides sample config files (.gitignore, .env.example, README).
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_readme(temp_dir):
    """Create a sample README.md file."""
    readme_path = Path(temp_dir) / "README.md"
    readme_path.write_text('''# Test Project

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from myproject import main
main.run()
```

## Configuration

Edit config.yaml to customize settings.

## Troubleshooting

### Issue: Module not found
**Solution:** Install dependencies first.
''')
    return str(readme_path)


@pytest.fixture
def sample_gitignore(temp_dir):
    """Create a sample .gitignore file."""
    gitignore_path = Path(temp_dir) / ".gitignore"
    gitignore_path.write_text('''# Python
__pycache__/
*.pyc
*.pyo
venv/
.env

# IDE
.vscode/
.idea/

# Security
*.key
*.pem
credentials.json
secrets.yaml
''')
    return str(gitignore_path)


@pytest.fixture
def sample_env_example(temp_dir):
    """Create a sample .env.example file."""
    env_example_path = Path(temp_dir) / ".env.example"
    env_example_path.write_text('''# API Configuration
API_KEY=your_key_here
API_URL=https://api.example.com

# Database
DB_HOST=localhost
DB_PORT=5432
''')
    return str(env_example_path)
