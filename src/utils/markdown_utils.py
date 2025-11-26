"""
Markdown Utility Functions

Helper functions for parsing and analyzing markdown documents.
Used by document validator to extract sections and count content.
"""

import re
from typing import List


def count_words(text: str) -> int:
    """
    Count words in text, excluding code blocks.

    Args:
        text: Markdown text content

    Returns:
        int: Word count

    Example:
        >>> text = "# Header\n\nSome text here\n\n```\ncode\n```\n\nMore text"
        >>> count_words(text)
        6
    """
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Count words
    words = text.split()
    return len(words)


def extract_sections(content: str) -> List[str]:
    """
    Extract markdown section headers.

    Args:
        content: Markdown text content

    Returns:
        List[str]: List of section header texts

    Example:
        >>> content = "# Main\n\n## Sub\n\n### Details"
        >>> extract_sections(content)
        ['Main', 'Sub', 'Details']
    """
    # Match # Header, ## Header, ### Header
    headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    return [h.strip() for h in headers]
