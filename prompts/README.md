# Prompt Engineering Documentation

This directory contains all prompts used during the development of the Academic Software Auto-Grader System. Each prompt is documented with context, exact text, output received, and lessons learned.

## Purpose

- **Transparency**: Document all AI-assisted development decisions
- **Reproducibility**: Allow recreation of the development process
- **Learning**: Capture prompt engineering best practices
- **Academic Rigor**: Demonstrate depth of AI tool usage

## Organization

### `/architecture/`
Prompts related to system design, architectural decisions, and structural planning.

### `/code-generation/`
Prompts used to generate or refactor code components.

### `/testing/`
Prompts for test generation, test strategy, and quality assurance.

### `/documentation/`
Prompts for creating documentation, READMEs, and technical writing.

## Prompt Template

Each prompt file should follow this structure:

```markdown
# [Prompt Title]

## Context
Why this prompt was needed, what problem it was solving.

## Prompt Text
\```
[Exact prompt used]
\```

## Output Received
[Summary or excerpt of what Claude generated]

## Iteration Notes
- What worked well
- What needed refinement
- How the prompt was improved

## Lessons Learned
Best practices to apply to future prompts
```

## Naming Convention

Files are numbered sequentially: `001-description.md`, `002-description.md`, etc.

## Best Practices Learned

### 1. Be Specific
- ✅ "Create a Python function that validates GitHub URLs using regex"
- ❌ "Make a URL validator"

### 2. Provide Context
- Always explain the broader system context
- Reference related components
- Specify constraints (150-line limit, naming conventions)

### 3. Request Structured Output
- Ask for specific format (JSON, YAML, code with docstrings)
- Request examples when needed
- Specify error handling requirements

### 4. Iterate Based on Results
- Review output critically
- Refine prompts when output doesn't meet requirements
- Document what changes improved results

## Metrics

- **Total Prompts**: 0 (being populated)
- **Average Iterations per Prompt**: TBD
- **Success Rate**: TBD

---

**Last Updated**: 2025-01-26
