"""
README Validator Module

Validates README usability and completeness.
Checks for key sections and code examples.
"""

import os
import re
from typing import Dict

from ..utils.markdown_utils import extract_sections


def check_readme_usability(project_path: str) -> Dict:
    """
    Check README for user-friendly content.

    Args:
        project_path: Root directory of project

    Returns:
        Dict with README usability metrics (score out of 4)

    Example:
        >>> result = check_readme_usability('/path/to/project')
        >>> print(f"README score: {result['score']}/4")
    """
    readme_path = os.path.join(project_path, 'README.md')

    if not os.path.exists(readme_path):
        return {
            'score': 0,
            'has_readme': False,
            'issues': ['README.md not found']
        }

    try:
        with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        sections = extract_sections(content)
        sections_lower = [s.lower() for s in sections]

        score = 4
        issues = []

        # Check for key sections
        required = {
            'installation': 'Installation or Setup section',
            'usage': 'Usage or Getting Started section',
            'example': 'Examples section'
        }

        for keyword, description in required.items():
            if not any(keyword in s for s in sections_lower):
                score -= 1
                issues.append(f'Missing {description}')

        # Check for code examples
        has_code_blocks = bool(re.search(r'```', content))
        if not has_code_blocks:
            issues.append('No code examples found')

        return {
            'score': max(0, score),
            'has_readme': True,
            'sections': sections,
            'has_code_examples': has_code_blocks,
            'issues': issues
        }
    except Exception as e:
        return {
            'score': 0,
            'has_readme': True,
            'error': str(e),
            'issues': ['Error reading README']
        }
