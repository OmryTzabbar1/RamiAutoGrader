"""
Line Counter Utility Module

Counts lines of code with optional filtering for comments and blank lines.
Supports multiple programming languages with different comment styles.

Key Features:
- Accurate line counting
- Comment filtering by language
- Blank line detection
"""

import os
import re
from typing import Dict


# Comment patterns for different languages
COMMENT_PATTERNS = {
    'python': {
        'single_line': r'^\s*#',
        'docstring': r'^\s*("""|\'\'\').*\1\s*$'
    },
    'javascript': {
        'single_line': r'^\s*//',
        'multi_line_start': r'^\s*/\*',
        'multi_line_end': r'\*/\s*$'
    },
    'typescript': {
        'single_line': r'^\s*//',
        'multi_line_start': r'^\s*/\*',
        'multi_line_end': r'\*/\s*$'
    },
}


def count_lines(
    file_path: str,
    exclude_comments: bool = False,
    exclude_blank: bool = False
) -> int:
    """
    Count lines in a file with optional filtering.

    Args:
        file_path: Path to file
        exclude_comments: If True, don't count comment-only lines
        exclude_blank: If True, don't count blank lines

    Returns:
        int: Number of lines (after applying filters)

    Raises:
        FileNotFoundError: If file doesn't exist

    Example:
        >>> total = count_lines('script.py')
        >>> code_only = count_lines('script.py', exclude_comments=True, exclude_blank=True)
        >>> print(f"Total: {total}, Code only: {code_only}")
        Total: 150, Code only: 120
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    if not exclude_comments and not exclude_blank:
        return len(lines)

    # Determine language from extension
    ext = os.path.splitext(file_path)[1]
    lang = _detect_language(ext)

    count = 0
    in_multi_line_comment = False

    for line in lines:
        stripped = line.strip()

        # Skip blank lines if requested
        if exclude_blank and not stripped:
            continue

        # Skip comments if requested
        if exclude_comments and lang:
            if _is_comment_line(stripped, lang, in_multi_line_comment):
                # Update multi-line comment state
                in_multi_line_comment = _update_comment_state(
                    stripped, lang, in_multi_line_comment
                )
                continue

        count += 1

    return count


def get_line_stats(file_path: str) -> Dict[str, int]:
    """
    Get detailed line statistics for a file.

    Args:
        file_path: Path to file

    Returns:
        Dict containing:
            - total: Total lines
            - code: Lines with code
            - comments: Comment-only lines
            - blank: Blank lines

    Example:
        >>> stats = get_line_stats('script.py')
        >>> print(f"Code: {stats['code']}, Comments: {stats['comments']}")
        Code: 120, Comments: 25
    """
    total = count_lines(file_path, exclude_comments=False, exclude_blank=False)
    code = count_lines(file_path, exclude_comments=True, exclude_blank=True)
    blank_count = count_lines(file_path, exclude_blank=False) - \
                  count_lines(file_path, exclude_blank=True)

    return {
        'total': total,
        'code': code,
        'comments': total - code - blank_count,
        'blank': blank_count
    }


def _detect_language(extension: str) -> str:
    """Detect language from file extension."""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
    }
    return ext_map.get(extension.lower(), '')


def _is_comment_line(line: str, lang: str, in_multi: bool) -> bool:
    """Check if line is a comment."""
    if in_multi:
        return True

    patterns = COMMENT_PATTERNS.get(lang, {})
    single_pattern = patterns.get('single_line')

    if single_pattern and re.match(single_pattern, line):
        return True

    return False


def _update_comment_state(line: str, lang: str, in_multi: bool) -> bool:
    """Update multi-line comment tracking state."""
    patterns = COMMENT_PATTERNS.get(lang, {})

    if patterns.get('multi_line_start') and re.match(patterns['multi_line_start'], line):
        return True
    if patterns.get('multi_line_end') and re.search(patterns['multi_line_end'], line):
        return False

    return in_multi
