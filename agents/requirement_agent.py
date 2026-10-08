class RequirementAgent:
    def __init__(self, llm_service):
        self.llm = llm_service

    def analyze(self, user_idea):
        prompt = f"""
You are a Requirement Analysis Agent in an AI software development team.

Analyze the following software idea:

{user_idea}

Provide:
1. Project Name
2. Project Description
3. Main Features
4. Functional Requirements
5. Non-Functional Requirements
6. Suggested Technology Stack

Keep the requirements simple and suitable for a small Python project.

The generated application must use:
- Python as the programming language.
- Streamlit for the web interface.
- SQLite for database storage when needed.

Do not suggest console-only applications or Tkinter.
Do not ask follow-up questions.
"""

        return self.llm.generate(prompt)