"""
Python AST Parser Module

Parses Python source code into Abstract Syntax Trees for analysis.
Extracts functions, classes, docstrings, and other structural elements.

Design Decision: Use built-in AST module for accuracy and no external dependencies.
"""

import ast
from typing import List, Dict, Optional
from dataclasses import dataclass


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


def parse_python_file(file_path: str) -> Optional[ast.AST]:
    """
    Parse a Python file into an AST.

    Args:
        file_path: Path to Python file

    Returns:
        ast.AST: Abstract Syntax Tree, or None if parsing fails

    Example:
        >>> tree = parse_python_file('script.py')
        >>> if tree:
        ...     print("Parsed successfully")
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()

        return ast.parse(source, filename=file_path)

    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def extract_functions(tree: ast.AST) -> List[FunctionInfo]:
    """
    Extract all function definitions from AST.

    Args:
        tree: Parsed AST

    Returns:
        List[FunctionInfo]: Information about each function

    Example:
        >>> tree = parse_python_file('script.py')
        >>> functions = extract_functions(tree)
        >>> print(f"Found {len(functions)} functions")
    """
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)

            func_info = FunctionInfo(
                name=node.name,
                line_number=node.lineno,
                has_docstring=docstring is not None,
                docstring=docstring,
                num_params=len(node.args.args)
            )
            functions.append(func_info)

    return functions


def extract_classes(tree: ast.AST) -> List[ClassInfo]:
    """
    Extract all class definitions from AST.

    Args:
        tree: Parsed AST

    Returns:
        List[ClassInfo]: Information about each class

    Example:
        >>> tree = parse_python_file('script.py')
        >>> classes = extract_classes(tree)
        >>> for cls in classes:
        ...     print(f"{cls.name}: {len(cls.methods)} methods")
    """
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)

            # Extract methods
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_docstring = ast.get_docstring(item)
                    method_info = FunctionInfo(
                        name=item.name,
                        line_number=item.lineno,
                        has_docstring=method_docstring is not None,
                        docstring=method_docstring,
                        num_params=len(item.args.args),
                        is_method=True
                    )
                    methods.append(method_info)

            class_info = ClassInfo(
                name=node.name,
                line_number=node.lineno,
                has_docstring=docstring is not None,
                docstring=docstring,
                methods=methods
            )
            classes.append(class_info)

    return classes


def get_module_docstring(tree: ast.AST) -> Optional[str]:
    """
    Get module-level docstring.

    Args:
        tree: Parsed AST

    Returns:
        Optional[str]: Module docstring or None

    Example:
        >>> tree = parse_python_file('module.py')
        >>> doc = get_module_docstring(tree)
        >>> if doc:
        ...     print("Module has docstring")
    """
    return ast.get_docstring(tree)
