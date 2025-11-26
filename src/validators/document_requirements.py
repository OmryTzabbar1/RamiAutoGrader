"""
Document Requirements Configuration

Default requirements for academic project documentation.
Defines required documents, sections, and minimum word counts.
"""

# Default documentation requirements
DEFAULT_DOC_REQUIREMENTS = {
    'required_documents': [
        {
            'name': 'README.md',
            'required_sections': ['Installation', 'Usage'],
            'min_words': 200
        },
        {
            'name': 'PRD.md',
            'required_sections': ['Project Overview', 'Objectives', 'Functional Requirements'],
            'min_words': 1000
        },
        {
            'name': 'PLANNING.md',
            'required_sections': ['Architecture', 'Technical Decisions'],
            'min_words': 800
        },
        {
            'name': 'TASKS.md',
            'required_sections': ['Task Breakdown'],
            'min_words': 300
        },
        {
            'name': 'CLAUDE.md',
            'required_sections': ['AI Tool Usage', 'Prompt Documentation'],
            'min_words': 500
        }
    ]
}
