"""
Research Quality Analyzer Module

Evaluates research quality in academic software projects.
Checks for parameter exploration, statistical analysis, and research documentation.

Target: Evidence of systematic experimentation and analysis.
"""

import os
from typing import Dict, List

from ..utils.file_finder import find_code_files, find_markdown_files


# Research-related file patterns
RESEARCH_INDICATORS = {
    'documentation': ['RESEARCH.md', 'EXPERIMENTS.md', 'ANALYSIS.md', 'METHODOLOGY.md'],
    'config_files': ['experiments.yaml', 'parameters.yaml', 'config.yaml'],
    'data_files': ['.csv', '.json', '.xlsx'],
    'result_files': ['results/', 'output/', 'experiments/'],
    'analysis_scripts': ['analyze', 'experiment', 'eval'],
}


def find_research_documents(project_path: str) -> List[str]:
    """
    Find research-related documentation files.

    Args:
        project_path: Root directory to search

    Returns:
        List[str]: Paths to research documents

    Example:
        >>> docs = find_research_documents('/path/to/project')
        >>> print(f"Found {len(docs)} research documents")
    """
    md_files = find_markdown_files(project_path)
    research_docs = []

    for doc_name in RESEARCH_INDICATORS['documentation']:
        for md_file in md_files:
            if doc_name.lower() in os.path.basename(md_file).lower():
                research_docs.append(md_file)

    return research_docs


def find_parameter_files(project_path: str) -> List[str]:
    """Find configuration/parameter files."""
    all_files = []
    for root, dirs, files in os.walk(project_path):
        # Skip common ignore directories
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '__pycache__'}]

        for file in files:
            for pattern in RESEARCH_INDICATORS['config_files']:
                if pattern in file.lower():
                    all_files.append(os.path.join(root, file))

    return all_files


def find_analysis_scripts(project_path: str) -> List[str]:
    """Find analysis or experiment scripts."""
    py_files = find_code_files(project_path, extensions=['.py'])
    analysis_scripts = []

    for script in py_files:
        basename = os.path.basename(script).lower()
        for pattern in RESEARCH_INDICATORS['analysis_scripts']:
            if pattern in basename:
                analysis_scripts.append(script)
                break

    return analysis_scripts


def evaluate_research_quality(project_path: str) -> Dict:
    """
    Evaluate research quality in a project.

    Args:
        project_path: Root directory of project

    Returns:
        Dict with research evaluation results and score (out of 10)

    Example:
        >>> result = evaluate_research_quality('/path/to/project')
        >>> print(f"Research Score: {result['score']}/10")
    """
    # Find research artifacts
    research_docs = find_research_documents(project_path)
    param_files = find_parameter_files(project_path)
    analysis_scripts = find_analysis_scripts(project_path)

    # Calculate score (out of 10)
    max_score = 10
    score = 0

    # Points for research documentation (4 points)
    if research_docs:
        score += 4

    # Points for parameter files (3 points)
    if param_files:
        score += 3

    # Points for analysis scripts (3 points)
    if analysis_scripts:
        score += 3

    # Build message
    components = []
    if research_docs:
        components.append(f"{len(research_docs)} research doc(s)")
    if param_files:
        components.append(f"{len(param_files)} parameter file(s)")
    if analysis_scripts:
        components.append(f"{len(analysis_scripts)} analysis script(s)")

    if components:
        message = f"Found: {', '.join(components)}"
    else:
        message = "No research artifacts found"

    return {
        'score': score,
        'max_score': max_score,
        'passed': score >= 7,  # 70% threshold
        'has_research': score > 0,
        'research_docs': research_docs,
        'param_files': param_files,
        'analysis_scripts': analysis_scripts,
        'message': message
    }
