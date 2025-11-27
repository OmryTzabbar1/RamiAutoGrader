---
name: check-ux
description: Evaluates user experience quality including README usability, CLI help, and documentation clarity
version: 1.0.0
---

# User Experience Evaluation Skill

Evaluates user experience (UX) quality in academic software projects by checking:
- README usability and clarity
- CLI help availability (argparse, --help flags)
- Documentation user-friendliness
- Installation ease
- Usage examples

**Scoring:** 10 points maximum (bonus category - demonstrates professional polish)

## Instructions

### 1. Evaluate README Usability

The README is the primary UX touchpoint. Check for user-friendly elements:

**Essential Sections:**
```bash
# Check for key sections in README
grep -i "## installation\|## usage\|## getting started\|## quick start" README.md

# Check for examples
grep -i "## example\|## usage example" README.md

# Check for troubleshooting
grep -i "## troubleshooting\|## common issues\|## faq" README.md
```

**User-Friendly Elements:**
- Clear project description (first paragraph)
- Installation steps (numbered list)
- Usage examples with code blocks
- Screenshots or demo (visual aids)
- Troubleshooting section
- Contact/support information

**Score Breakdown (4 points total):**
- Has all essential sections: 2 points
- Has code examples: 1 point
- Has troubleshooting/FAQ: 1 point

### 2. Check CLI Help Availability

If the project has a command-line interface, check for help:

```bash
# Check for argparse in Python files
grep -r "argparse.ArgumentParser\|import argparse" *.py src/

# Check for help strings in argparse
grep -r "help=" *.py src/ | wc -l

# Check for --help flag documentation
grep -r "parser.add_argument.*--help" *.py src/
```

**For JavaScript/Node.js:**
```bash
# Check for commander or yargs (CLI libraries)
grep -r "require('commander')\|require('yargs')" *.js src/

# Check for .help() or .usage()
grep -r "\.help()\|\.usage()" *.js src/
```

**Test help availability:**
```bash
# Try running with --help
```

**Score Breakdown (3 points total):**
- Has argparse/CLI framework: 1 point
- Has --help flag: 1 point
- Help text is comprehensive: 1 point

### 3. Check Installation Clarity

Evaluate how easy it is to install and set up:

```bash
# Check for requirements file
ls requirements.txt package.json pyproject.toml

# Check for setup instructions in README
grep -A 10 -i "## installation" README.md

# Check for virtual environment instructions
grep -i "venv\|virtualenv\|conda" README.md

# Check for example .env file
ls .env.example
```

**Good installation documentation includes:**
- Prerequisites listed (Python version, Node version, etc.)
- Step-by-step installation commands
- Virtual environment setup
- Configuration template (.env.example)
- Verification step ("run this to test")

**Score Breakdown (2 points total):**
- Clear installation steps: 1 point
- Configuration template provided: 1 point

### 4. Check Usage Examples

Documentation should show how to use the software:

```bash
# Count code blocks in README (usage examples)
grep -c '```' README.md

# Check for specific example section
grep -A 20 -i "## usage\|## example" README.md

# Check for screenshots
find . -name "*.png" -o -name "*.jpg" -o -name "*.gif" | grep -i "screenshot\|demo\|example"
```

**Good usage documentation includes:**
- Basic usage example
- Advanced usage examples
- Command-line flags explained
- Configuration options shown
- Expected output demonstrated

**Score Breakdown (1 point):**
- Has comprehensive usage examples: 1 point

### 5. Calculate UX Score

**Scoring Formula:**
```
Base Score: 10 points

Components:
- README quality: 4 points
  - Essential sections (Installation, Usage, Examples): 2 points
  - Code examples present: 1 point
  - Troubleshooting/FAQ: 1 point

- CLI help: 3 points
  - Has CLI framework (argparse): 1 point
  - --help flag works: 1 point
  - Help text comprehensive: 1 point

- Installation clarity: 2 points
  - Clear steps: 1 point
  - Config template: 1 point

- Usage examples: 1 point
  - Comprehensive examples: 1 point

Final Score: sum of all components (max 10)
```

**Passing Threshold:** 7/10 (70%)

**Note:** This is a bonus category - projects can pass overall with lower UX score, but high UX demonstrates professional polish.

### 7. Generate Report

Output a detailed UX evaluation:

```json
{
  "score": 8.0,
  "max_score": 10,
  "passed": true,
  "readme_result": {
    "has_readme": true,
    "score": 3,
    "sections": ["Installation", "Usage", "Examples", "Configuration"],
    "has_code_examples": true,
    "has_troubleshooting": false,
    "word_count": 542,
    "issues": ["Missing troubleshooting section"]
  },
  "cli_result": {
    "score": 3,
    "has_argparse": true,
    "has_help_flag": true,
    "help_comprehensive": true,
    "example_help_output": "usage: main.py [-h] [--config CONFIG] project_path\\n\\nGrade academic projects..."
  },
  "installation_result": {
    "score": 2,
    "has_clear_steps": true,
    "has_config_template": true,
    "has_requirements": true
  },
  "usage_examples_result": {
    "score": 0,
    "code_block_count": 3,
    "has_examples_section": true,
    "issues": ["Examples could be more comprehensive"]
  },
  "details": {
    "strengths": [
      "Comprehensive README with all key sections",
      "CLI help is well-documented",
      "Clear installation instructions",
      ".env.example template provided"
    ],
    "weaknesses": [
      "Missing troubleshooting section",
      "Could benefit from more usage examples"
    ],
    "recommendations": [
      "Add troubleshooting section to README",
      "Include advanced usage examples",
      "Add screenshots or demo GIF"
    ]
  }
}
```

## Example Usage

```bash
# Run the UX quality evaluation skill
/skill check-ux

# When prompted, provide project path
/path/to/student/project
```

## Success Criteria

- ✅ README has all essential sections
- ✅ README includes code examples
- ✅ CLI help available via --help flag
- ✅ Clear installation instructions
- ✅ Configuration template provided
- ✅ Score ≥ 7/10 to pass

## Common Issues

1. **README too technical** - Assumes too much knowledge
2. **No usage examples** - Documentation without examples is incomplete
3. **Missing --help flag** - CLI tools should always have help
4. **Complex installation** - Too many manual steps
5. **No troubleshooting** - Users get stuck on common issues

## Recommendations Format

Provide actionable feedback:
```
[+] User Experience Evaluation:

    README Quality: 3/4 ⚠
    ✓ Has Installation section
    ✓ Has Usage section
    ✓ Has Examples section
    ✓ Has code examples
    ⚠ Missing Troubleshooting section

    CLI Help: 3/3 ✓
    ✓ Uses argparse framework
    ✓ --help flag implemented
    ✓ Comprehensive help text

    Installation Clarity: 2/2 ✓
    ✓ Clear step-by-step instructions
    ✓ .env.example template provided
    ✓ requirements.txt present

    Usage Examples: 0/1 ⚠
    ⚠ Only 3 code examples (could be more comprehensive)

    Recommendations:
    1. Add Troubleshooting section to README:
       ```markdown
       ## Troubleshooting

       ### "ModuleNotFoundError: No module named 'anthropic'"
       **Solution:** Install dependencies:
       ```bash
       pip install -r requirements.txt
       ```

       ### "Permission denied" when running script
       **Solution:** Make script executable:
       ```bash
       chmod +x main.py
       ```
       ```

    2. Add more usage examples:
       - Basic usage example
       - Advanced usage with all flags
       - Batch processing example
       - Custom configuration example

    3. Consider adding visual aids:
       - Screenshot of output
       - Demo GIF showing usage
       - Architecture diagram

    4. Add "Quick Start" section:
       Show minimal steps to get running immediately:
       ```markdown
       ## Quick Start

       ```bash
       # Clone and install
       git clone https://github.com/user/project.git
       cd project
       pip install -r requirements.txt

       # Run on sample project
       ```
       ```

    Final Score: 8/10 (80%) - PASSED

    Excellent CLI help and installation clarity!
    Adding troubleshooting and more examples would perfect the UX.
```

## UX Best Practices

**README Structure:**
1. Title and one-line description
2. Badges (optional: build status, coverage, version)
3. Quick Start (3-5 commands to get running)
4. Installation (detailed steps)
5. Usage (with examples)
6. Configuration (all options explained)
7. Troubleshooting (common issues)
8. Contributing (optional)
9. License

**CLI Design:**
- Always provide --help flag
- Use --verbose for detailed output
- Provide progress indicators for long operations
- Use clear error messages
- Support both --flag and -f short forms

**Documentation Writing:**
- Write for beginners (don't assume knowledge)
- Provide examples for every feature
- Use code blocks liberally
- Include expected output
- Link to additional resources
