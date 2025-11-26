---
name: assess-git
description: Assesses Git workflow quality including commit history, message format, and branching practices
version: 1.0.0
---

# Git Workflow Assessment Skill

Evaluates Git practices in academic software projects by checking:
- Commit count (minimum 15-25 commits showing progression)
- Commit message quality (conventional commit format)
- Commit frequency and distribution
- Task references in commits

**Scoring:** 10 points maximum (demonstrates development process)

## Instructions

### 1. Verify Git Repository

First, check if the project is a Git repository:

```bash
# Check for .git directory
ls -la .git/

# Or use git command
git rev-parse --git-dir
```

**If not a Git repo:** Score = 0 (auto-fail)

### 2. Count Total Commits

Count the number of commits in the repository:

```bash
# Count all commits (excluding merges)
git log --oneline --no-merges | wc -l

# Count commits on current branch
git rev-list --count HEAD

# Show commit history
git log --oneline --no-merges
```

**Requirements:**
- **Minimum:** 15 commits (demonstrates development progression)
- **Target:** 25+ commits (excellent progression)
- **Warning:** 1-5 commits = poor practice (single large commit)

**Scoring:**
- < 10 commits: 0/3 points
- 10-14 commits: 1/3 points
- 15-24 commits: 2/3 points
- ≥ 25 commits: 3/3 points

### 3. Analyze Commit Message Quality

Check commit messages for conventional commit format:

**Expected Format:**
```
<type>(<scope>): <description> [TASK-ID]

Example:
feat(skills): Add document validator skill [P2.2.1]
fix(parser): Handle empty file edge case [P2.2.2]
docs(readme): Update installation instructions
test(validators): Add unit tests for naming validator [P2.2.4]
```

**Types to look for:**
- `feat` - New features
- `fix` - Bug fixes
- `docs` - Documentation changes
- `test` - Adding tests
- `refactor` - Code restructuring
- `chore` - Build/tooling changes
- `style` - Formatting changes

```bash
# Extract all commit messages
git log --pretty=format:"%s" --no-merges

# Count conventional commits
git log --pretty=format:"%s" --no-merges | grep -E "^(feat|fix|docs|test|refactor|chore|style)" | wc -l

# Count commits with task references
git log --pretty=format:"%s" --no-merges | grep -E "\[.*\]" | wc -l
```

**Quality Metrics:**
- % of commits following conventional format
- % of commits with task references
- Average message length (should be >10 characters)
- Descriptive messages vs. vague ones ("update", "fix bug")

**Scoring:**
- < 50% conventional: 0/4 points
- 50-69% conventional: 2/4 points
- 70-89% conventional: 3/4 points
- ≥ 90% conventional: 4/4 points

### 4. Check Commit Distribution

Analyze commit frequency to detect:
- Single large commit (bad practice)
- Regular commits throughout development (good practice)

```bash
# Show commits by date
git log --pretty=format:"%ad - %s" --date=short --no-merges

# Count commits per day
git log --pretty=format:"%ad" --date=short --no-merges | uniq -c
```

**Good pattern:** Commits spread over multiple days/weeks
**Bad pattern:** All commits on one day (suggests bulk commit at end)

**Scoring:**
- All commits on 1 day: -2 points penalty
- Commits spread over 2-3 days: -1 point penalty
- Commits spread over 4+ days: 0 penalty (good)

### 5. Analyze Commit Content

Look for evidence of proper development workflow:

```bash
# Check for incremental development (small commits)
git log --stat --oneline --no-merges | head -20

# Look for test commits
git log --grep="test" --oneline --no-merges

# Look for documentation commits
git log --grep="docs\|documentation" --oneline --no-merges

# Look for refactor commits
git log --grep="refactor" --oneline --no-merges
```

**Good indicators:**
- Separate commits for features, tests, docs, refactoring
- Small, focused commits
- Clear progression from setup → implementation → testing → documentation

### 6. Use Python Helper for Complete Analysis

Run the Git analyzer for comprehensive assessment:

```bash
python src/analyzers/git_analyzer.py <project_path>
```

This will:
1. Check if directory is a Git repository
2. Count total commits
3. Analyze commit messages for conventional format
4. Check for task references
5. Analyze commit distribution over time
6. Identify commit quality issues
7. Calculate Git workflow score

### 7. Calculate Git Workflow Score

**Scoring Formula:**
```
Base Score: 10 points

Components:
- Commit count: 3 points
  - <10: 0 points
  - 10-14: 1 point
  - 15-24: 2 points
  - ≥25: 3 points

- Message quality: 4 points
  - Conventional format adherence
  - Task references present
  - Descriptive messages

- Commit distribution: 3 points
  - Spread over multiple days
  - Regular commit pattern
  - Not all on one day

Penalties:
- Not a Git repo: 0 total
- All commits on one day: -2 points
- Vague commit messages: -1 point

Final Score: max(0, min(Total, 10))
```

**Passing Threshold:** 7/10 (70%)

### 8. Generate Report

Output a detailed Git workflow assessment:

```json
{
  "score": 8.0,
  "max_score": 10,
  "passed": true,
  "is_git_repo": true,
  "commit_count": 23,
  "conventional_commits": 19,
  "conventional_percentage": 0.826,
  "has_task_references": 18,
  "commit_days": 7,
  "details": {
    "commit_types": {
      "feat": 9,
      "fix": 3,
      "docs": 4,
      "test": 5,
      "refactor": 2
    },
    "good_commit_examples": [
      "feat(skills): Add document validator skill [P2.2.1]",
      "test(validators): Add unit tests for naming conventions [P2.2.4]",
      "docs(readme): Update installation and usage instructions"
    ],
    "poor_commit_examples": [
      "update",
      "fix stuff",
      "changes"
    ],
    "commit_timeline": [
      "2025-01-20: 3 commits",
      "2025-01-21: 5 commits",
      "2025-01-22: 7 commits",
      "2025-01-23: 4 commits",
      "2025-01-24: 2 commits",
      "2025-01-25: 2 commits"
    ]
  }
}
```

## Example Usage

```bash
# Run the Git workflow assessment skill
/skill assess-git

# When prompted, provide project path
/path/to/student/project
```

## Python Helpers Available

1. **git_analyzer.py** - Complete Git workflow analysis
   ```bash
   python src/analyzers/git_analyzer.py <path>
   ```

2. **git_commands.py** - Git command utilities
   ```bash
   python src/utils/git_commands.py <path>
   ```

## Success Criteria

- ✅ Project is a Git repository
- ✅ Minimum 15 commits (target: 25+)
- ✅ ≥70% commits follow conventional format
- ✅ Commits include task references
- ✅ Commits spread over multiple days
- ✅ Score ≥ 7/10 to pass

## Common Issues

1. **Single large commit** - All work committed at once (very bad)
2. **Vague commit messages** - "update", "fix", "changes"
3. **No task references** - Can't track commits to requirements
4. **All commits on one day** - Suggests poor planning
5. **Not using conventional commits** - Inconsistent format

## Recommendations Format

Provide actionable feedback:
```
[+] Git Workflow Assessment:

    Repository Status: ✓ Valid Git repository
    Total Commits: 23 ✓ (Target: 25+)
    Conventional Commits: 19/23 (82.6%) ✓
    Task References: 18/23 (78.3%) ✓
    Commit Timeline: 7 days ✓

    Commit Type Breakdown:
    - feat: 9 commits (features)
    - test: 5 commits (testing)
    - docs: 4 commits (documentation)
    - fix: 3 commits (bug fixes)
    - refactor: 2 commits (code improvement)

    Good Examples:
    ✓ "feat(skills): Add document validator skill [P2.2.1]"
    ✓ "test(validators): Add unit tests for naming conventions [P2.2.4]"
    ✓ "docs(readme): Update installation and usage instructions"

    Issues Found:
    ⚠ 4 commits with poor messages:
       - "update" (commit 8a3f2)
       - "fix stuff" (commit 9b4e1)
       - "changes" (commit 7c2d5)

    ⚠ 5 commits missing task references

    Recommendations:
    1. Use conventional commit format for all commits:
       <type>(<scope>): <description> [TASK-ID]

    2. Always reference task IDs from TASKS.md:
       Example: feat(parser): Add AST parser [P2.2.2]

    3. Make commits more descriptive:
       Instead of: "update"
       Write: "docs(readme): Add troubleshooting section"

    4. Continue making small, focused commits
       Your current commit pattern is excellent!

    Final Score: 8/10 (80%) - PASSED
```
