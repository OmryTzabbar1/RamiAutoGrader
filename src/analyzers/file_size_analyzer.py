"""
File Size Analyzer Module

Enforces the CRITICAL 150-line file size limit requirement.
This is a strict academic requirement with NO EXCEPTIONS.

Design Decision: Simple line counting approach for clarity and reliability.
Does not exclude comments/blanks - total file size matters for maintainability.
"""

import os
from typing import List, Dict
from dataclasses import dataclass

from ..utils.file_finder import find_code_files
from ..utils.line_counter import count_lines


@dataclass
class FileSizeViolation:
    """
    Represents a file that exceeds the size limit.

    Attributes:
        file_path: Absolute path to the violating file
        line_count: Actual number of lines in the file
        limit: Maximum allowed lines
        excess: How many lines over the limit
        severity: 'critical' (always, since this is strict requirement)
    """
    file_path: str
    line_count: int
    limit: int
    excess: int
    severity: str = 'critical'

    def __str__(self) -> str:
        return (
            f"{self.file_path}: {self.line_count} lines "
            f"(exceeds limit by {self.excess} lines)"
        )


def check_file_sizes(
    project_path: str,
    limit: int = 150,
    extensions: List[str] = None
) -> List[FileSizeViolation]:
    """
    Check all code files for size limit violations.

    This is a CRITICAL check - the 150-line limit is strictly enforced
    in the academic grading criteria. Files exceeding this limit result
    in significant penalties.

    Args:
        project_path: Root directory of project to analyze
        limit: Maximum allowed lines per file (default: 150)
        extensions: File extensions to check (default: ['.py', '.js', '.ts'])

    Returns:
        List[FileSizeViolation]: All files exceeding the limit

    Raises:
        NotADirectoryError: If project_path is not a valid directory

    Example:
        >>> violations = check_file_sizes('/path/to/project')
        >>> if violations:
        ...     print(f"Found {len(violations)} oversized files")
        ...     for v in violations:
        ...         print(f"  {v}")
        Found 2 oversized files
          src/main.py: 215 lines (exceeds limit by 65 lines)
          src/utils.py: 180 lines (exceeds limit by 30 lines)
    """
    if not os.path.isdir(project_path):
        raise NotADirectoryError(f"Not a directory: {project_path}")

    if extensions is None:
        extensions = ['.py', '.js', '.ts']

    # Find all code files
    code_files = find_code_files(project_path, extensions=extensions)

    violations = []

    for file_path in code_files:
        try:
            line_count = count_lines(file_path)

            if line_count > limit:
                violation = FileSizeViolation(
                    file_path=file_path,
                    line_count=line_count,
                    limit=limit,
                    excess=line_count - limit
                )
                violations.append(violation)

        except Exception as e:
            # Log but continue - don't let one bad file stop analysis
            print(f"Warning: Could not analyze {file_path}: {e}")
            continue

    return violations


def generate_size_report(violations: List[FileSizeViolation]) -> Dict:
    """
    Generate a structured report of file size violations.

    Args:
        violations: List of file size violations

    Returns:
        Dict containing:
            - total_violations: Number of files exceeding limit
            - files: List of violation details
            - total_excess_lines: Sum of all excess lines
            - passed: Boolean (True if no violations)

    Example:
        >>> violations = check_file_sizes('/path/to/project')
        >>> report = generate_size_report(violations)
        >>> print(f"Passed: {report['passed']}")
        Passed: False
    """
    return {
        'total_violations': len(violations),
        'files': [
            {
                'path': v.file_path,
                'lines': v.line_count,
                'excess': v.excess,
                'severity': v.severity
            }
            for v in violations
        ],
        'total_excess_lines': sum(v.excess for v in violations),
        'passed': len(violations) == 0
    }
