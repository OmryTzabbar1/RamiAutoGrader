"""
Comment Pattern Definitions

Regular expression patterns for identifying comments in different languages.
Used by line counter to exclude comments from code metrics.
"""

# Comment patterns for different programming languages
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


# Extension to language mapping
EXTENSION_LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
}
