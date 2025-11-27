"""
Display Formatter for Code Analysis Results

Formats and displays code quality analysis results in terminal.
Separated from main analysis logic for modularity.
"""


def display_header(project_path: str):
    """Display analysis header."""
    print(f"[*] Code Quality Analysis: {project_path}")
    print("=" * 60)


def display_file_size_results(size_violations):
    """Display file size check results."""
    print("\n[*] Checking file size limits (150 lines max)...")

    if size_violations:
        print(f"\n[X] CRITICAL: {len(size_violations)} file(s) exceed 150-line limit!")
        for v in size_violations[:5]:  # Show first 5
            print(f"   {v}")
        if len(size_violations) > 5:
            print(f"   ... and {len(size_violations) - 5} more")
    else:
        print("[+] All files within 150-line limit")


def display_docstring_results(docstring_result):
    """Display docstring coverage results."""
    print("\n[*] Analyzing docstring coverage (90% target)...")

    coverage_pct = docstring_result['coverage'] * 100
    if docstring_result['passed']:
        print(f"[+] Docstring coverage: {coverage_pct:.1f}% (PASSED)")
    else:
        print(f"[!] Docstring coverage: {coverage_pct:.1f}% (target: 90%)")
        print(f"   Missing {docstring_result['missing']} docstrings")

        # Show some examples
        for v in docstring_result['violations'][:3]:
            print(f"   - {v.item_type} '{v.item_name}' in {v.file_path}:{v.line_number}")


def display_naming_results(naming_result):
    """Display naming convention validation results."""
    print("\n[*] Validating naming conventions...")

    if naming_result['passed']:
        print("[+] All naming conventions followed")
    else:
        print(f"[!] Found {len(naming_result['violations'])} naming violations")

        # Show examples
        for v in naming_result['violations'][:3]:
            print(f"   - {v.item_type} '{v.item_name}' should use {v.expected_pattern}")


def display_summary(score: float, max_score: int):
    """Display final score summary."""
    print("\n" + "=" * 60)
    print(f"Code Quality Score: {score:.1f}/{max_score}")

    if score >= 27:  # 90%
        print("[+] EXCELLENT - High quality code")
    elif score >= 21:  # 70%
        print("[+] PASSED - Acceptable code quality")
    else:
        print("[X] FAILED - Significant quality issues")
