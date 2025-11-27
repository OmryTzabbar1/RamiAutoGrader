---
name: grade-research
description: Evaluates research quality including parameter exploration, analysis depth, and documentation
version: 1.0.0
---

# Research Quality Evaluation Skill

Evaluates research rigor in academic software projects by checking:
- Parameter exploration and experimentation
- Statistical analysis and metrics
- Comparative analysis (comparing approaches)
- Research documentation quality
- Data visualization

**Scoring:** 10 points maximum (demonstrates academic rigor)

## Instructions

### 1. Find Research Documentation

Look for research-related files in the project:

```bash
# Common research document names
ls RESEARCH.md research.md ANALYSIS.md analysis.md EXPERIMENTS.md

# Check PLANNING.md for research sections
grep -i "research\|experiment\|analysis\|parameter" PLANNING.md

# Look for Jupyter notebooks (common for research)
find . -name "*.ipynb"

# Look for research/experiments directory
ls -R research/ experiments/ analysis/ data/
```

**Scoring:**
- No research documentation: 0/2 points
- Basic research documentation: 1/2 points
- Comprehensive research documentation: 2/2 points

### 2. Check for Parameter Exploration

Research projects should document parameter exploration:

**Look for evidence of:**
- Different parameter values tested
- Hyperparameter tuning
- Configuration experimentation
- Performance comparison across settings

```bash
# Search for parameter mentions in docs
grep -ri "parameter\|hyperparameter\|configuration\|experiment" *.md docs/

# Look for experiment results
grep -ri "result\|performance\|accuracy\|metric" PLANNING.md README.md

# Check for tables or comparisons
grep -E "\|.*\|.*\|" *.md | head -20
```

**Good indicators:**
- Tables comparing different parameter values
- Descriptions of what parameters were tested
- Rationale for parameter choices
- Multiple experiments documented

**Scoring:**
- No parameter exploration: 0/2 points
- Minimal exploration (1-2 parameters): 1/2 points
- Comprehensive exploration (3+ parameters, multiple values): 2/2 points

### 3. Check for Statistical Analysis

Look for quantitative analysis and metrics:

```bash
# Search for metrics and analysis
grep -ri "metric\|accuracy\|precision\|recall\|f1\|rmse\|mae\|r2\|correlation" *.md

# Look for statistical terms
grep -ri "mean\|median\|std\|variance\|distribution\|significant" *.md

# Check for numerical results
grep -E "[0-9]+\.[0-9]+%|[0-9]+\.[0-9]+ (seconds|ms)" *.md
```

**Expected elements:**
- Performance metrics reported
- Statistical measures (mean, std dev, confidence intervals)
- Baseline comparisons
- Quantitative results

**Scoring:**
- No quantitative analysis: 0/2 points
- Basic metrics reported: 1/2 points
- Comprehensive statistical analysis: 2/2 points

### 4. Check for Comparative Analysis

Research should compare different approaches:

```bash
# Look for comparison keywords
grep -ri "compare\|comparison\|versus\|vs\|alternative\|approach" *.md

# Look for pros/cons discussions
grep -ri "pros\|cons\|advantage\|disadvantage\|tradeoff\|trade-off" *.md

# Check for decision justification
grep -ri "chose\|selected\|decided\|because\|reason\|rationale" *.md
```

**Good indicators:**
- Multiple approaches considered
- Pros/cons of each approach listed
- Clear rationale for final choice
- Comparison tables

**Scoring:**
- No comparative analysis: 0/2 points
- Mentioned alternatives briefly: 1/2 points
- Detailed comparison with justification: 2/2 points

### 5. Check for Data Visualization

Visual representation of research findings:

```bash
# Look for images in docs
find . -name "*.png" -o -name "*.jpg" -o -name "*.svg" | grep -v node_modules | grep -v venv

# Check if images are referenced in docs
grep "!\[" *.md docs/*.md

# Look for plotting code (if notebooks exist)
grep -r "plt.plot\|plt.figure\|seaborn\|plotly" *.ipynb *.py
```

**Expected visualizations:**
- Performance graphs
- Parameter comparison charts
- Architecture diagrams
- Result visualizations

**Scoring:**
- No visualizations: 0/2 points
- Basic visualizations (1-2 images): 1/2 points
- Comprehensive visualizations (3+ charts/graphs): 2/2 points

### 6. Calculate Research Score

**Scoring Formula:**
```
Base Score: 10 points

Components:
- Research documentation presence: 2 points
  - No docs: 0 points
  - Basic docs: 1 point
  - Comprehensive: 2 points

- Parameter exploration: 2 points
  - None: 0 points
  - Minimal (1-2 params): 1 point
  - Comprehensive (3+ params): 2 points

- Statistical analysis: 2 points
  - None: 0 points
  - Basic metrics: 1 point
  - Comprehensive stats: 2 points

- Comparative analysis: 2 points
  - None: 0 points
  - Mentioned alternatives: 1 point
  - Detailed comparison: 2 points

- Visualizations: 2 points
  - None: 0 points
  - Basic (1-2): 1 point
  - Comprehensive (3+): 2 points

Final Score: sum of all components (max 10)
```

**Passing Threshold:** 7/10 (70%)

### 8. Generate Report

Output a detailed research evaluation:

```json
{
  "score": 8.0,
  "max_score": 10,
  "passed": true,
  "research_docs_found": ["PLANNING.md", "research/analysis.md"],
  "parameter_exploration": {
    "score": 2,
    "parameters_tested": ["learning_rate", "batch_size", "hidden_units", "dropout_rate"],
    "experiments_documented": 5
  },
  "statistical_analysis": {
    "score": 2,
    "metrics_reported": ["accuracy", "f1_score", "training_time"],
    "has_baseline": true,
    "has_statistical_measures": true
  },
  "comparative_analysis": {
    "score": 1,
    "approaches_compared": ["Random Forest", "Neural Network"],
    "has_detailed_comparison": false,
    "has_rationale": true
  },
  "visualizations": {
    "score": 1,
    "count": 2,
    "types": ["performance graph", "parameter comparison"]
  },
  "details": {
    "strengths": [
      "Comprehensive parameter exploration (4 parameters)",
      "Clear statistical metrics reported",
      "Baseline comparison included"
    ],
    "weaknesses": [
      "Limited visualizations (only 2 charts)",
      "Comparative analysis could be more detailed"
    ],
    "recommendations": [
      "Add more visualizations showing parameter effects",
      "Expand comparative analysis with pros/cons table",
      "Include confidence intervals in results"
    ]
  }
}
```

## Example Usage

```bash
# Run the research quality evaluation skill
/skill grade-research

# When prompted, provide project path
/path/to/student/project
```

## Success Criteria

- ✅ Research documentation present and comprehensive
- ✅ Parameter exploration documented (3+ parameters)
- ✅ Statistical analysis with metrics
- ✅ Comparative analysis of approaches
- ✅ Visualizations of findings
- ✅ Score ≥ 7/10 to pass

## Common Issues

1. **No research documentation** - Most serious issue
2. **No parameter exploration** - Just used default values
3. **Missing baselines** - No comparison to existing solutions
4. **No visualizations** - Text-only results
5. **Superficial comparison** - Mentioned alternatives but didn't analyze

## Recommendations Format

Provide actionable feedback:
```
[+] Research Quality Evaluation:

    Documentation: 2/2 ✓
    - Found: PLANNING.md, research/analysis.md
    - Comprehensive research sections

    Parameter Exploration: 2/2 ✓
    - Tested 4 parameters: learning_rate, batch_size, hidden_units, dropout_rate
    - 5 experiments documented
    - Clear rationale for choices

    Statistical Analysis: 2/2 ✓
    - Metrics: accuracy (0.89), f1_score (0.87), training_time (42s)
    - Baseline comparison: ✓ (accuracy: 0.75)
    - Statistical measures: mean, std dev included

    Comparative Analysis: 1/2 ⚠
    - Compared Random Forest vs Neural Network
    - Has rationale for choice
    ⚠ Missing: Detailed pros/cons table

    Visualizations: 1/2 ⚠
    - 2 visualizations found:
      - Performance graph over epochs
      - Parameter comparison chart
    ⚠ Recommendation: Add more visualizations

    Recommendations:
    1. Expand comparative analysis:
       Create a pros/cons table:
       | Approach | Pros | Cons | Performance |
       |----------|------|------|-------------|
       | Random Forest | Fast, interpretable | Limited accuracy | 0.75 |
       | Neural Network | High accuracy | Slow training | 0.89 |

    2. Add more visualizations:
       - Learning curve showing training vs validation
       - Parameter sensitivity analysis plot
       - Confusion matrix for final model
       - Feature importance chart

    3. Include confidence intervals:
       Report results as: accuracy = 0.89 ± 0.03 (95% CI)

    Final Score: 8/10 (80%) - PASSED

    Excellent parameter exploration and statistical analysis!
    Adding more visualizations would strengthen the research presentation.
```
