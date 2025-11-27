---
name: check-security
description: Scans for hardcoded secrets, validates .gitignore and .env configuration
version: 1.1.0
---

# Security Check Skill

Evaluates security practices in academic software projects by checking for:
- Hardcoded secrets (API keys, passwords, tokens)
- Proper .gitignore configuration
- Environment variable management

**Scoring:** 10 points maximum (critical security category)

---

## Strictness Parameter (Optional)

This skill supports **adaptive grading strictness** based on student self-assessment.

**Default**: `strictness = 1.0` (standard grading)
**Range**: `1.0 to 1.3` (higher = more critical evaluation)

**How strictness affects grading:**
- **Critical violations** (hardcoded secrets) always result in 0 points (not affected by strictness)
- **Non-critical penalties** (gitignore, env config) are multiplied by strictness value
- **Security best practices** are scrutinized more carefully at higher strictness

**Usage**: If strictness is specified in the grading request, apply it to non-critical penalty calculations.

## Instructions

### 1. Scan for Hardcoded Secrets

Use Grep to search for common secret patterns in source files:

**API Keys and Tokens:**
```bash
# Search for API key patterns
grep -r "api[_-]?key\s*=\s*['\"][^'\"]+['\"]" --include="*.py" --include="*.js" --include="*.ts"
grep -r "API_KEY\s*=\s*['\"][^'\"]+['\"]" --include="*.py" --include="*.js" --include="*.ts"
grep -r "secret[_-]?key\s*=\s*['\"][^'\"]+['\"]" -i --include="*.py" --include="*.js" --include="*.ts"
```

**AWS Credentials:**
```bash
grep -r "aws_access_key_id\s*=\s*['\"][^'\"]+['\"]" -i
grep -r "aws_secret_access_key\s*=\s*['\"][^'\"]+['\"]" -i
```

**Database Passwords:**
```bash
grep -r "password\s*=\s*['\"][^'\"]+['\"]" -i --include="*.py" --include="*.js" --include="*.ts"
```

**Tokens:**
```bash
grep -r "token\s*=\s*['\"][^'\"]+['\"]" -i --include="*.py" --include="*.js" --include="*.ts"
```

If any secrets are found, **CRITICAL FAILURE** - score = 0.

### 2. Validate .gitignore

Read the `.gitignore` file and verify it contains these security patterns:

**Required patterns:**
- `.env` (environment files)
- `*.key` (key files)
- `*.pem` (certificate files)
- `credentials.json` (credential files)
- `secrets.yaml` or `secrets.yml` (secret files)
- `config/secrets.*` (secret configuration)

**Penalty:** `-3 × strictness` points if .gitignore is missing required patterns
  - strictness=1.0: -3 points
  - strictness=1.3: -3.9 points

### 3. Check Environment Configuration

Verify proper environment variable management:

1. **Check .env.example exists:**
   ```bash
   ls .env.example
   ```

2. **Verify .env is in .gitignore:**
   ```bash
   grep "^\.env$" .gitignore || grep "^\.env" .gitignore
   ```

3. **Verify .env (if it exists) is NOT tracked in git:**
   ```bash
   git ls-files | grep "^\.env$"
   ```
   (Should return empty - if .env appears, it's tracked and this is a violation)

**Penalty:** `-2 × strictness` points if environment config is improper
  - strictness=1.0: -2 points
  - strictness=1.3: -2.6 points

### 4. Calculate Score

**Scoring Logic (with strictness):**
- Start with 10 points
- Strictness: 1.0 to 1.3 (default: 1.0)
- **Hardcoded secrets found:** 0 points (critical failure, not affected by strictness)
- **Missing .gitignore patterns:** `-3 × strictness` points
- **Improper environment config:** `-2 × strictness` points
- Minimum score: 0
- Passing threshold: 7/10

**Examples:**
- strictness=1.0, missing .gitignore patterns, improper env config:
  - Deductions: -3 -2 = -5
  - Score: 10 - 5 = 5/10 (FAIL)

- strictness=1.3, missing .gitignore patterns, improper env config:
  - Deductions: -3.9 -2.6 = -6.5
  - Score: 10 - 6.5 = 3.5/10 (FAIL, worse than standard)

### 5. Generate Report

Output a JSON report with:

```json
{
  "score": 10,
  "max_score": 10,
  "passed": true,
  "secrets_found": 0,
  "gitignore_valid": true,
  "env_valid": true,
  "details": {
    "secret_locations": [],
    "missing_gitignore_patterns": [],
    "env_issues": []
  }
}
```

## Example Usage

```bash
# Run the security check skill
/skill check-security

# When prompted, provide project path
/path/to/student/project
```

## Success Criteria

- ✅ No hardcoded secrets in source code
- ✅ .gitignore contains all security patterns
- ✅ .env.example exists as template
- ✅ .env (if exists) is not tracked by git
- ✅ Score >= 7/10 to pass

## Common Violations

1. **API keys in config files** - Often found in `config.py` or `settings.py`
2. **Database passwords in connection strings** - Check database initialization code
3. **Missing .env pattern in .gitignore** - Most common oversight
4. **Committing .env file** - Check git history with `git log --all --full-history -- .env`
