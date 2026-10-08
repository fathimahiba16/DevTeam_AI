class ArchitectAgent:
    def __init__(self, llm_service):
        self.llm = llm_service

    def design(self, requirements):
        prompt = f"""
You are a Software Architect Agent in an AI development team.

Based on these requirements:

{requirements}

Create a simple software architecture.

Include:
1. System Overview
2. Technology Stack
3. Project Folder Structure
4. Main Python Files and Their Responsibilities
5. Database Design (if needed)
6. How the Components Work Together

Keep the design suitable for a small Python and Streamlit project.
"""

        return self.llm.generate(prompt)