# Git Clone Skill

Clone a Git repository to a temporary or specified directory for grading purposes.

**Usage:** `/skill git-clone <repository_url> [target_directory]`

## Purpose

This skill clones Git repositories (from GitHub, GitLab, Bitbucket, etc.) with full history for comprehensive Git workflow assessment. It's used by the grade-project agent to fetch student submissions before grading.

## Instructions

### 1. Validate Git URL

Check if the provided URL is a valid Git repository URL:

**Supported formats:**
- HTTPS: `https://github.com/user/repo.git`
- HTTPS (no .git): `https://github.com/user/repo`
- SSH: `git@github.com:user/repo.git`
- GitLab: `https://gitlab.com/user/repo.git`
- Bitbucket: `https://bitbucket.org/user/repo.git`

### 2. Determine Clone Location

**If target_directory provided:**
```bash
git clone <repository_url> <target_directory>
```

**If no target specified:**
Clone to a temporary directory in the project:
```bash
# Generate unique directory name
REPO_NAME=$(basename <repository_url> .git)
TARGET_DIR="temp_grading_${REPO_NAME}"

# Clone repository
git clone <repository_url> ${TARGET_DIR}
```

### 3. Clone with Full History

**CRITICAL:** Always clone with **full Git history** (no shallow clone) to enable Git workflow assessment:

```bash
# Clone with full history
git clone <repository_url> <target_directory>

# DO NOT use --depth flag for grading purposes
# Shallow clones break git log analysis
```

### 4. Verify Clone Success

After cloning, verify the repository:

```bash
# Check .git directory exists
test -d <target_directory>/.git && echo "SUCCESS" || echo "FAILED"

# Get absolute path
cd <target_directory> && pwd
```

### 5. Return Clone Path

Output the cloned repository path in a machine-readable format:

```
Repository cloned successfully!

Path: /absolute/path/to/cloned/repo
Repository: user/repo
URL: https://github.com/user/repo.git

You can now grade this repository using:
/skill validate-docs <path>
/skill analyze-code <path>
```

## Example Usage

### Example 1: Clone to Auto-Generated Directory

```bash
/skill git-clone https://github.com/student/final-project.git

# Output:
# Cloning into 'temp_grading_final-project'...
# Repository cloned successfully!
# Path: /home/user/grader/temp_grading_final-project
```

### Example 2: Clone to Specific Directory

```bash
/skill git-clone https://github.com/student/project.git ./submissions/student-123

# Output:
# Cloning into './submissions/student-123'...
# Repository cloned successfully!
# Path: /home/user/grader/submissions/student-123
```

## Error Handling

### Common Errors

**Invalid URL:**
```
Error: Invalid Git URL format
Expected: https://github.com/user/repo.git
Received: not-a-valid-url
```

**Repository Not Found:**
```
Error: Repository not found or access denied
URL: https://github.com/user/nonexistent.git
Check: 1) Repository exists, 2) You have access (for private repos)
```

**Directory Already Exists:**
```
Error: Target directory already exists
Path: ./temp_grading_project
Action: Remove existing directory or specify different target
```

**Git Not Installed:**
```
Error: Git command not found
Install Git: https://git-scm.com/downloads
```

## Integration with Grading Workflow

This skill is typically used as the first step in grading GitHub submissions:

```bash
# Step 1: Clone repository
/skill git-clone https://github.com/student/project.git

# Step 2: Grade the cloned repository
# (Agent automatically runs all grading skills on cloned path)
```

## Security Considerations

- **Read-only operation:** Cloning only reads remote repositories
- **No code execution:** Skill only clones, never runs student code
- **Temporary storage:** Use `temp_grading_*` directories for easy cleanup
- **Private repositories:** Requires SSH keys or credentials configured in Git

## Success Criteria

- ✅ Valid Git URL provided
- ✅ Repository cloned with full history
- ✅ .git directory present in cloned repo
- ✅ Absolute path returned for subsequent grading

## Notes

- **Full history required:** Git workflow assessment needs complete commit history
- **Cleanup:** Temporary directories can be removed after grading
- **Timeout:** Large repositories may take several minutes to clone
- **Network:** Requires internet connection to access remote repositories
