"""
Execution Tracer - Runtime Function Call Tracker

Tracks which Python files and functions are actually called during execution.
Uses sys.settrace() to monitor all function calls in real-time.
"""

import sys
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import json


class ExecutionTracer:
    """
    Tracks all function calls at runtime to identify which files are actually used.

    Example:
        >>> tracer = ExecutionTracer()
        >>> tracer.start()
        >>> # ... run your code ...
        >>> tracer.stop()
        >>> report = tracer.get_report()
    """

    def __init__(self, project_root=None):
        """
        Initialize the execution tracer.

        Args:
            project_root: Root directory of project (only track files under this)
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.files_called = set()
        self.functions_called = defaultdict(int)
        self.call_stack = []
        self.start_time = None
        self.stop_time = None
        self._original_trace = None

    def _should_track(self, filename):
        """Determine if we should track calls in this file."""
        try:
            filepath = Path(filename).resolve()

            # Only track files in our project
            if not str(filepath).startswith(str(self.project_root)):
                return False

            # Skip virtual environments
            if 'venv' in filepath.parts or 'env' in filepath.parts:
                return False

            # Skip test files (unless we want to track test execution)
            # if 'test' in filepath.parts:
            #     return False

            # Only track .py files in src/, skills/, and root scripts
            rel_path = filepath.relative_to(self.project_root)
            first_part = rel_path.parts[0] if rel_path.parts else ''

            return first_part in ['src', 'skills', 'legacy'] or filename.endswith(('.py',))

        except (ValueError, OSError):
            return False

    def _trace_calls(self, frame, event, arg):
        """Trace function that gets called on every function call."""
        if event != 'call':
            return

        code = frame.f_code
        filename = code.co_filename
        function_name = code.co_name

        if not self._should_track(filename):
            return

        # Track the file
        self.files_called.add(filename)

        # Track the function call
        relative_path = self._get_relative_path(filename)
        func_key = f"{relative_path}::{function_name}"
        self.functions_called[func_key] += 1

    def _get_relative_path(self, filename):
        """Get path relative to project root."""
        try:
            return str(Path(filename).relative_to(self.project_root))
        except ValueError:
            return filename

    def start(self):
        """Start tracing execution."""
        self.start_time = datetime.now()
        self._original_trace = sys.gettrace()
        sys.settrace(self._trace_calls)
        print(f"[TRACER] Started tracking at {self.start_time.strftime('%H:%M:%S')}")

    def stop(self):
        """Stop tracing execution."""
        sys.settrace(self._original_trace)
        self.stop_time = datetime.now()
        duration = (self.stop_time - self.start_time).total_seconds()
        print(f"[TRACER] Stopped tracking (duration: {duration:.2f}s)")

    def get_report(self):
        """
        Generate comprehensive usage report.

        Returns:
            dict: Report containing files called, functions called, statistics
        """
        # Organize files by directory
        files_by_dir = defaultdict(list)
        for filepath in sorted(self.files_called):
            rel_path = self._get_relative_path(filepath)
            directory = str(Path(rel_path).parent)
            files_by_dir[directory].append(rel_path)

        # Top functions by call count
        top_functions = sorted(
            self.functions_called.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]  # Top 20

        return {
            'summary': {
                'files_executed': len(self.files_called),
                'unique_functions_called': len(self.functions_called),
                'total_function_calls': sum(self.functions_called.values()),
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'stop_time': self.stop_time.isoformat() if self.stop_time else None,
                'duration_seconds': (self.stop_time - self.start_time).total_seconds() if self.start_time and self.stop_time else None
            },
            'files_called': sorted([self._get_relative_path(f) for f in self.files_called]),
            'files_by_directory': dict(files_by_dir),
            'top_functions': [
                {'function': func, 'call_count': count}
                for func, count in top_functions
            ],
            'all_function_calls': dict(self.functions_called)
        }

    def save_report(self, output_file='execution_trace.json'):
        """Save report to JSON file."""
        report = self.get_report()
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"[TRACER] Report saved to: {output_file}")
        return output_file

    def print_summary(self):
        """Print a human-readable summary."""
        report = self.get_report()

        print("\n" + "=" * 70)
        print("EXECUTION TRACE SUMMARY")
        print("=" * 70)

        summary = report['summary']
        print(f"\nFiles Executed:           {summary['files_executed']}")
        print(f"Unique Functions Called:  {summary['unique_functions_called']}")
        print(f"Total Function Calls:     {summary['total_function_calls']}")

        if summary['duration_seconds']:
            print(f"Execution Duration:       {summary['duration_seconds']:.2f}s")

        print("\n" + "-" * 70)
        print("FILES EXECUTED BY DIRECTORY")
        print("-" * 70)

        for directory, files in sorted(report['files_by_directory'].items()):
            print(f"\n{directory}/ ({len(files)} files):")
            for file in files:
                print(f"  + {file}")

        print("\n" + "-" * 70)
        print("TOP 10 MOST CALLED FUNCTIONS")
        print("-" * 70)

        for i, func_data in enumerate(report['top_functions'][:10], 1):
            print(f"{i:2}. {func_data['function']:<50} {func_data['call_count']:>6} calls")

        print("\n" + "=" * 70)


def trace_execution(func, *args, **kwargs):
    """
    Decorator/wrapper to trace a function's execution.

    Example:
        >>> result = trace_execution(my_function, arg1, arg2)
    """
    tracer = ExecutionTracer()
    tracer.start()

    try:
        result = func(*args, **kwargs)
    finally:
        tracer.stop()
        tracer.print_summary()
        tracer.save_report()

    return result, tracer
