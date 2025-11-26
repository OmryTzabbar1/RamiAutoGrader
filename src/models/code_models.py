"""
Code Analysis Data Models

Dataclasses for code quality analysis results.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DocstringViolation:
    """Represents a missing docstring."""
    file_path: str
    item_type: str  # 'module', 'function', 'class', 'method'
    item_name: str
    line_number: int

    def __str__(self) -> str:
        return f"{self.item_type} '{self.item_name}' at {self.file_path}:{self.line_number}"


@dataclass
class FunctionInfo:
    """Information about a function definition."""
    name: str
    line_number: int
    has_docstring: bool
    docstring: Optional[str]
    num_params: int
    is_method: bool = False


@dataclass
class ClassInfo:
    """Information about a class definition."""
    name: str
    line_number: int
    has_docstring: bool
    docstring: Optional[str]
    methods: List[FunctionInfo]
