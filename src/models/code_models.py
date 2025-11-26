"""
Code Analysis Data Models

Dataclasses for code quality analysis results.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocstringViolation:
    """Represents a missing docstring."""
    file_path: str
    item_type: str  # 'module', 'function', 'class', 'method'
    item_name: str
    line_number: int

    def __str__(self) -> str:
        return f"{self.item_type} '{self.item_name}' at {self.file_path}:{self.line_number}"
