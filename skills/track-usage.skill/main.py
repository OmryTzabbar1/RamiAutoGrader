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


def run_full_agent_workflow_with_tracking(project_path, is_github_url=False):
    """
    Simulate the COMPLETE agent workflow with execution tracking.

    This tracks everything the agent does:
    1. Clone repository (if GitHub URL)
    2. Run all grading skills
    3. Generate detailed report

    Args:
        project_path: Path to project or GitHub URL
        is_github_url: Whether project_path is a GitHub URL

    Returns:
        ExecutionTracer: Tracer with collected data
    """
    project_root = Path(__file__).parent.parent.parent
    tracer = ExecutionTracer(project_root=project_root)

    print("=" * 70)
    print("EXECUTION TRACKER - Complete Agent Workflow Monitor")
    print("=" * 70)
    print(f"\nTracking: {project_path}")
    print("This simulates the full agent workflow:\n")
    print("  1. Clone repository (if GitHub URL)")
    print("  2. Run all 7 grading skills")
    print("  3. Generate detailed report\n")

    # Start tracing
    tracer.start()

    actual_project_path = project_path
    temp_dir = None

    try:
        # PHASE 1: Clone repository (if GitHub URL)
        if is_github_url:
            print("[PHASE 1] Cloning repository...")
            from src.utils.git_clone import clone_repository
            try:
                result = clone_repository(project_path, depth=None)
                actual_project_path = result['path']
                temp_dir = result.get('temp_dir')
                print(f"    [OK] Cloned to: {actual_project_path}\n")
            except Exception as e:
                print(f"    [FAIL] Clone error: {e}\n")
                return tracer
        else:
            print("[PHASE 1] Using local project path (no clone needed)\n")

        # PHASE 2: Run all grading skills
        print("[PHASE 2] Running all grading skills...\n")

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

        print("\n[*] All skills imported! Running on project...\n")

        # Collect results for report generation
        results = {}

        print("[>] Running security checks...")
        try:
            results['security'] = {
                'secrets': scan_for_secrets(actual_project_path),
                'gitignore': validate_gitignore(actual_project_path),
                'env': check_env_template(actual_project_path)
            }
        except Exception as e:
            print(f"    [WARN] Security check error: {e}")
            results['security'] = None

        print("[>] Running documentation validation...")
        try:
            results['documentation'] = check_project_documentation(actual_project_path)
        except Exception as e:
            print(f"    [WARN] Docs check error: {e}")
            results['documentation'] = None

        print("[>] Running code analysis...")
        try:
            results['code_quality'] = {
                'file_sizes': check_file_sizes(actual_project_path),
                'docstrings': analyze_project_docstrings(actual_project_path),
                'naming': analyze_project_naming(actual_project_path)
            }
        except Exception as e:
            print(f"    [WARN] Code analysis error: {e}")
            results['code_quality'] = None

        print("[>] Running test evaluation...")
        try:
            results['testing'] = evaluate_tests(actual_project_path)
        except Exception as e:
            print(f"    [WARN] Test evaluation error: {e}")
            results['testing'] = None

        print("[>] Running git assessment...")
        try:
            results['git'] = assess_git_workflow(actual_project_path)
        except Exception as e:
            print(f"    [WARN] Git assessment error: {e}")
            results['git'] = None

        print("[>] Running research evaluation...")
        try:
            results['research'] = evaluate_research_quality(actual_project_path)
        except Exception as e:
            print(f"    [WARN] Research evaluation error: {e}")
            results['research'] = None

        print("[>] Running UX evaluation...")
        try:
            results['ux'] = evaluate_ux_quality(actual_project_path)
        except Exception as e:
            print(f"    [WARN] UX evaluation error: {e}")
            results['ux'] = None

        print("\n[*] All skills executed!")

        # PHASE 3: Generate detailed report
        print("\n[PHASE 3] Generating detailed report...")
        try:
            from src.reporters.detailed_reporter import generate_detailed_report
            report_path = generate_detailed_report(actual_project_path, results)
            print(f"    [OK] Report generated: {report_path}\n")
        except Exception as e:
            print(f"    [WARN] Report generation error: {e}\n")

    finally:
        # Stop tracing
        tracer.stop()

        # Cleanup temp directory if created
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            try:
                shutil.rmtree(temp_dir)
                print(f"[*] Cleaned up temp directory: {temp_dir}")
            except Exception as e:
                print(f"[WARN] Cleanup error: {e}")

    return tracer


def main():
    """Main entry point for usage tracker skill."""
    if len(sys.argv) < 2:
        print("Usage: /skill track-usage <project_path_or_github_url>")
        print("\nExamples:")
        print("  /skill track-usage .")
        print("  /skill track-usage ./RamiAutoGrader")
        print("  /skill track-usage https://github.com/user/repo.git")
        sys.exit(1)

    project_path = sys.argv[1]

    # Check if it's a GitHub URL
    is_github_url = project_path.startswith(('http://', 'https://')) and 'github.com' in project_path

    # Validate local path (if not GitHub URL)
    if not is_github_url and not os.path.exists(project_path):
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Run full agent workflow with execution tracking
    tracer = run_full_agent_workflow_with_tracking(project_path, is_github_url)

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
