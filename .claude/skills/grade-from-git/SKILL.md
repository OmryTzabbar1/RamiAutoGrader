---
name: grade-from-git
description: Clone a Git repository and grade it using the auto-grader
version: 1.0.0
---

# Grade From Git Skill

Clone a Git repository (from GitHub, GitLab, Bitbucket, etc.) and run the complete auto-grader on it.

**Use Case:** Grade student submissions directly from their Git repositories without manual cloning.

## Instructions

### 1. Validate Git URL

Check if the provided URL is a valid Git repository:

**Supported formats:**
- HTTPS: `https://github.com/user/repo.git`
- HTTPS (no .git): `https://github.com/user/repo`
- SSH: `git@github.com:user/repo.git`
- GitLab: `https://gitlab.com/user/repo.git`
- Bitbucket: `https://bitbucket.org/user/repo.git`

Use the Python helper to validate:
```bash
python -c "from src.utils.git_clone import is_git_url; print(is_git_url('$URL'))"
```

### 2. Clone the Repository

Use the Git clone helper utility:

```bash
python -c "
from src.utils.git_clone import clone_repository
import json

result = clone_repository(
    repo_url='$REPO_URL',
    branch='$BRANCH',  # Optional, use 'main' or 'master' if not specified
    depth=1  # Shallow clone for speed
)

print(json.dumps(result, indent=2))
"
```

**Parameters:**
- `repo_url`: Git repository URL (required)
- `branch`: Branch to clone (optional, defaults to default branch)
- `depth`: Clone depth (1 for shallow, None for full history)

**Return structure:**
```json
{
  "success": true,
  "path": "/tmp/autograder_xyz/project-name",
  "message": "Successfully cloned https://github.com/user/repo.git",
  "temp": true,
  "repo_name": "project-name"
}
```

### 3. Grade the Cloned Repository

Once cloned successfully, invoke the grade-project agent:

```bash
# Use the cloned path
CLONED_PATH="/tmp/autograder_xyz/project-name"

# Run the grader
python grade_project.py "$CLONED_PATH"
```

Or use the Python API directly:

```python
from src.core.skill_executor import run_all_skills
from src.core.grading_utils import format_results_summary

results = run_all_skills(cloned_path)
print(format_results_summary(results))
```

### 4. Save Results

Save grading results with repository information:

```bash
# Save to JSON with repo name
python grade_project.py "$CLONED_PATH" --output "results/${REPO_NAME}_grading_report.json"
```

### 5. Cleanup (Optional)

Clean up the cloned repository after grading:

```bash
python -c "
from src.utils.git_clone import cleanup_clone
cleanup_clone('$CLONED_PATH')
print('Cleanup complete')
"
```

**Note:** If using temporary directory (default), cleanup happens automatically on system reboot.

## Complete Workflow Example

```python
#!/usr/bin/env python
"""Complete grade-from-git workflow."""

from src.utils.git_clone import clone_repository, cleanup_clone, is_git_url
from src.core.skill_executor import run_all_skills
from src.core.grading_utils import format_results_summary
import json
import sys

def grade_from_git(repo_url, branch=None, output_file=None, cleanup=True):
    """
    Clone a Git repository and grade it.

    Args:
        repo_url: Git repository URL
        branch: Branch to clone (optional)
        output_file: Path to save results JSON (optional)
        cleanup: Whether to cleanup after grading (default: True)

    Returns:
        dict: Grading results
    """
    # Validate URL
    if not is_git_url(repo_url):
        print(f"Error: '{repo_url}' is not a valid Git URL")
        return None

    print(f"[*] Cloning repository: {repo_url}")
    if branch:
        print(f"    Branch: {branch}")

    # Clone repository
    clone_result = clone_repository(repo_url, branch=branch)

    if not clone_result['success']:
        print(f"[X] Clone failed: {clone_result['message']}")
        return None

    cloned_path = clone_result['path']
    repo_name = clone_result['repo_name']

    print(f"[+] Successfully cloned to: {cloned_path}")

    # Grade the repository
    print(f"\n[*] Grading {repo_name}...")
    results = run_all_skills(cloned_path)

    # Display summary
    print("\n" + format_results_summary(results))

    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n[+] Results saved to: {output_file}")

    # Cleanup if requested
    if cleanup:
        print(f"\n[*] Cleaning up cloned repository...")
        cleanup_clone(cloned_path)
        print("[+] Cleanup complete")

    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m grade_from_git <repo_url> [branch] [output_file]")
        print("\nExample:")
        print("  python -m grade_from_git https://github.com/user/project.git")
        print("  python -m grade_from_git https://github.com/user/project.git main")
        print("  python -m grade_from_git https://github.com/user/project.git main results.json")
        sys.exit(1)

    repo_url = sys.argv[1]
    branch = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    result = grade_from_git(repo_url, branch, output_file)

    sys.exit(0 if result and result['passed'] else 1)
```

## Usage Examples

### Example 1: Grade a GitHub Repository

```bash
# Using the skill
/skill grade-from-git

# When prompted:
# Repository URL: https://github.com/student123/final-project.git
# Branch (optional): main
# Save results? yes
```

### Example 2: Grade Multiple Repositories (Batch)

```bash
# Create a file with repository URLs
cat > repos.txt <<EOF
https://github.com/student1/project.git
https://github.com/student2/project.git
https://github.com/student3/project.git
EOF

# Grade each one
while read repo; do
    python -m grade_from_git "$repo" main "results/$(basename $repo .git).json"
done < repos.txt
```

### Example 3: Grade Specific Branch

```bash
/skill grade-from-git
# URL: https://github.com/user/project.git
# Branch: feature/final-submission
```

### Example 4: Keep Cloned Repository

```python
from src.utils.git_clone import clone_repository
from src.core.skill_executor import run_all_skills

# Clone but don't cleanup
result = clone_repository(
    "https://github.com/user/project.git",
    target_dir="./submissions"  # Keeps in ./submissions/project/
)

if result['success']:
    # Grade it
    grades = run_all_skills(result['path'])
    print(f"Score: {grades['total_score']}/100")

    # Repository remains in ./submissions/project/ for manual review
```

## Error Handling

**Common Errors:**

1. **Invalid URL:**
   ```
   Error: 'not-a-url' is not a valid Git URL
   ```
   **Solution:** Provide full Git URL (https://github.com/user/repo.git)

2. **Clone Timeout:**
   ```
   Git clone timed out (>5 minutes)
   ```
   **Solution:** Large repository or slow connection. Try shallow clone (depth=1).

3. **Authentication Required:**
   ```
   Git clone failed: remote: Repository not found
   ```
   **Solution:** For private repos, use SSH with configured keys or HTTPS with credentials.

4. **Git Not Installed:**
   ```
   Git command not found. Please install Git.
   ```
   **Solution:** Install Git: `sudo apt install git` or download from git-scm.com

## Success Criteria

- ✅ Valid Git URL provided
- ✅ Repository cloned successfully
- ✅ Auto-grader runs on cloned code
- ✅ Results generated and saved
- ✅ Optional cleanup completes

## Integration with Orchestrator

The grade-project agent should automatically detect Git URLs and invoke this skill:

```
User: "Grade https://github.com/student/project.git"

Agent detects Git URL →
  1. Invokes grade-from-git skill
  2. Clones repository to temp directory
  3. Runs all 7 grading skills on cloned code
  4. Generates comprehensive report
  5. Cleans up temporary files
  6. Returns results to user
```

## Security Considerations

- **Shallow clones** (depth=1) recommended to save bandwidth and time
- **Temporary directories** cleaned up automatically
- **No code execution** - static analysis only (safe)
- **Private repositories** require authentication (SSH keys or tokens)
- **Timeout protection** - clones timeout after 5 minutes

## Performance

- **Shallow clone:** ~5-10 seconds for typical project
- **Full clone:** Variable (depends on repository size)
- **Grading:** ~2-5 seconds for analysis
- **Total:** ~10-20 seconds end-to-end

## Future Enhancements

- Support for pull request grading (specific commit)
- Parallel batch grading of multiple repositories
- Caching of previously graded repositories
- Webhook integration for automatic grading on push
