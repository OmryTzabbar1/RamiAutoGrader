#!/usr/bin/env python
"""
Usage Tracker Skill

Tracks ACTUAL runtime execution - which files and functions are called
during a real grading session. Uses sys.settrace() to monitor execution.

Usage:
    /skill track-usage <project_path>
"""

import sys
import os
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.execution_tracer import ExecutionTracer


def run_all_skills_with_tracking(project_path):
    """
    Run all grading skills with execution tracking enabled.

    This simulates what the agent does: calls each skill individually.
    Skills are imported directly (not subprocess) so tracer can see everything.

    Args:
        project_path: Path to project being graded

    Returns:
        ExecutionTracer: Tracer with collected data
    """
    project_root = Path(__file__).parent.parent.parent
    tracer = ExecutionTracer(project_root=project_root)

    print("=" * 70)
    print("EXECUTION TRACKER - Runtime Function Call Monitor")
    print("=" * 70)
    print(f"\nTracking grading of: {project_path}")
    print("This will run all 7 grading skills and track what gets executed.\n")

    # Start tracing
    tracer.start()

    try:
        # Import all skill modules directly (so tracer can see them)
        print("[*] Importing check-security...")
        from src.analyzers.security_scanner import scan_for_secrets
        from src.validators.gitignore_validator import validate_gitignore
        from src.validators.env_validator import check_env_template

        print("[*] Importing validate-docs...")
        from src.analyzers.documentation_checker import check_project_documentation

        print("[*] Importing analyze-code...")
        from src.analyzers.file_size_analyzer import check_file_sizes
        from src.analyzers.docstring_analyzer import analyze_project_docstrings
        from src.validators.naming_validator import analyze_project_naming

        print("[*] Importing evaluate-tests...")
        from src.analyzers.test_analyzer import evaluate_tests

        print("[*] Importing assess-git...")
        from src.analyzers.git_analyzer import assess_git_workflow

        print("[*] Importing grade-research...")
        from src.analyzers.research_analyzer import evaluate_research_quality

        print("[*] Importing check-ux...")
        from src.analyzers.ux_analyzer import evaluate_ux_quality

        print("\n[*] All skills imported successfully!")
        print("[*] Now running skills on project...\n")

        # Run the functions to trigger actual execution
        print("[>] Running security checks...")
        try:
            scan_for_secrets(project_path)
            validate_gitignore(project_path)
            check_env_template(project_path)
        except Exception as e:
            print(f"    [WARN] Security check error: {e}")

        print("[>] Running documentation validation...")
        try:
            check_project_documentation(project_path)
        except Exception as e:
            print(f"    [WARN] Docs check error: {e}")

        print("[>] Running code analysis...")
        try:
            check_file_sizes(project_path)
            analyze_project_docstrings(project_path)
            analyze_project_naming(project_path)
        except Exception as e:
            print(f"    [WARN] Code analysis error: {e}")

        print("[>] Running test evaluation...")
        try:
            evaluate_tests(project_path)
        except Exception as e:
            print(f"    [WARN] Test evaluation error: {e}")

        print("[>] Running git assessment...")
        try:
            assess_git_workflow(project_path)
        except Exception as e:
            print(f"    [WARN] Git assessment error: {e}")

        print("[>] Running research evaluation...")
        try:
            evaluate_research_quality(project_path)
        except Exception as e:
            print(f"    [WARN] Research evaluation error: {e}")

        print("[>] Running UX evaluation...")
        try:
            evaluate_ux_quality(project_path)
        except Exception as e:
            print(f"    [WARN] UX evaluation error: {e}")

        print("\n[*] All skills executed!")

    finally:
        # Stop tracing
        tracer.stop()

    return tracer


def main():
    """Main entry point for usage tracker skill."""
    if len(sys.argv) < 2:
        print("Usage: /skill track-usage <project_path>")
        print("\nExample:")
        print("  /skill track-usage .")
        print("  /skill track-usage ./RamiAutoGrader")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Run grading with execution tracking
    tracer = run_all_skills_with_tracking(project_path)

    # Print summary
    tracer.print_summary()

    # Save detailed report
    output_file = "execution_trace.json"
    tracer.save_report(output_file)

    # Analysis: Compare with all existing files
    print("\n" + "=" * 70)
    print("USAGE ANALYSIS - Identifying Unused Files")
    print("=" * 70)

    project_root = Path(__file__).parent.parent.parent
    all_py_files = set()

    # Find all Python files in src/, skills/, and root
    for pattern in ['src/**/*.py', 'skills/**/*.py', '*.py']:
        for filepath in project_root.glob(pattern):
            if 'venv' not in str(filepath) and '__pycache__' not in str(filepath):
                rel_path = str(filepath.relative_to(project_root))
                all_py_files.add(rel_path)

    # Get files that were executed
    report = tracer.get_report()
    files_executed = set(report['files_called'])

    # Find unused files
    unused_files = all_py_files - files_executed

    print(f"\nTotal Python files:    {len(all_py_files)}")
    print(f"Files executed:        {len(files_executed)}")
    print(f"Files NOT executed:    {len(unused_files)}")

    if unused_files:
        print("\n" + "-" * 70)
        print("POTENTIALLY UNUSED FILES (not called during grading):")
        print("-" * 70)

        # Organize by directory
        unused_by_dir = {}
        for filepath in sorted(unused_files):
            directory = str(Path(filepath).parent)
            if directory not in unused_by_dir:
                unused_by_dir[directory] = []
            unused_by_dir[directory].append(filepath)

        for directory in sorted(unused_by_dir.keys()):
            files = unused_by_dir[directory]
            print(f"\n{directory}/ ({len(files)} files):")
            for file in files:
                print(f"  [!] {file}")

        print("\n" + "-" * 70)
        print("NOTE: These files were not executed during this grading run.")
        print("They may be:")
        print("  - Legacy code that can be archived")
        print("  - Helper utilities only used in specific scenarios")
        print("  - Test files (not called during normal grading)")
        print("-" * 70)

    print(f"\n[+] Complete report saved to: {output_file}")
    print(f"[+] Review the report to decide what to archive")
    print()


if __name__ == '__main__':
    main()
