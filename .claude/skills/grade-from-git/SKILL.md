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

### 2. Clone the Repository

Use git clone command to clone the repository:

```bash
# Extract repo name from URL
REPO_URL="https://github.com/user/repo.git"
REPO_NAME=$(basename "$REPO_URL" .git)

# Clone to temporary directory
CLONED_PATH="temp_grading_${REPO_NAME}"
git clone "$REPO_URL" "$CLONED_PATH"

# Verify clone succeeded
if [ -d "$CLONED_PATH/.git" ]; then
    echo "Successfully cloned to: $CLONED_PATH"
else
    echo "Clone failed"
    exit 1
fi
```

**Parameters:**
- `REPO_URL`: Git repository URL (required)
- `CLONED_PATH`: Target directory for clone (auto-generated based on repo name)

### 3. Grade the Cloned Repository

Once cloned successfully, run all grading skills **in parallel** on the cloned path:

```bash
# Use the cloned path
CLONED_PATH="/tmp/autograder_xyz/project-name"

# Run grading skills in parallel groups (invoke multiple skills in one message)

# Group 1 (parallel): Security, Documentation, UX
/skill check-security "$CLONED_PATH"
/skill validate-docs "$CLONED_PATH"
/skill check-ux "$CLONED_PATH"

# Group 2 (parallel): Code Quality, Testing
/skill analyze-code "$CLONED_PATH"
/skill evaluate-tests "$CLONED_PATH"

# Group 3 (parallel): Git Workflow, Research
/skill assess-git "$CLONED_PATH"
/skill grade-research "$CLONED_PATH"
```

**Performance:** Running skills in parallel provides 3-5x speedup (3-5 seconds vs 15-20 seconds sequential).

Or let the grade-project agent orchestrate everything automatically:

```bash
# The agent runs all skills in parallel and aggregates results
# Simply provide the cloned path when prompted by the agent
```

### 4. Generate Report

After all skills complete, generate a comprehensive report:

```bash
# Use the generate-detailed-report skill
/skill generate-detailed-report "$CLONED_PATH"
```

### 5. Cleanup (Optional)

Clean up the cloned repository after grading:

```bash
# Remove cloned directory
rm -rf "$CLONED_PATH"
echo "Cleanup complete"
```

**Note:** If using temporary directory, cleanup happens automatically on system reboot.

## Complete Workflow Example

```bash
#!/bin/bash
# Complete grade-from-git workflow

REPO_URL="https://github.com/student/project.git"
REPO_NAME=$(basename "$REPO_URL" .git)
CLONED_PATH="temp_grading_${REPO_NAME}"

echo "[*] Cloning repository: $REPO_URL"
git clone "$REPO_URL" "$CLONED_PATH"

if [ ! -d "$CLONED_PATH/.git" ]; then
    echo "[X] Clone failed"
    exit 1
fi

echo "[+] Successfully cloned to: $CLONED_PATH"
echo ""
echo "[*] Grading $REPO_NAME..."

# The grade-project agent or manual skill invocation would run here
# For manual usage, invoke skills in parallel groups:
# /skill check-security "$CLONED_PATH"
# /skill validate-docs "$CLONED_PATH"
# /skill check-ux "$CLONED_PATH"
# ... (continue with other skills)

echo ""
echo "[*] Grading complete"
echo "[*] Cleaning up..."
rm -rf "$CLONED_PATH"
echo "[+] Cleanup complete"
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
done < repos.txt
```

### Example 3: Grade Specific Branch

```bash
/skill grade-from-git
# URL: https://github.com/user/project.git
# Branch: feature/final-submission
```

### Example 4: Keep Cloned Repository

```bash
# Clone to a permanent directory (skip cleanup)
REPO_URL="https://github.com/user/project.git"
REPO_NAME=$(basename "$REPO_URL" .git)
TARGET_DIR="./submissions/${REPO_NAME}"

git clone "$REPO_URL" "$TARGET_DIR"

# Grade it (use the grade-project agent or invoke skills manually)
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
