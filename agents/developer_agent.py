class DeveloperAgent:
    def __init__(self, llm_service):
        self.llm = llm_service

    def generate_code(self, architecture):
        prompt = f"""
You are the Developer Agent in DevTeam AI.

Your job is to generate a complete, small Python web application
based on the software architecture provided below.

SOFTWARE ARCHITECTURE:
{architecture}

Follow these rules:
1. Use Python and Streamlit for the user interface.
2. Use SQLite for database storage when required.
3. Keep the application simple and beginner-friendly.
4. Generate all necessary source files.
5. Include a requirements.txt file.
6. Include basic pytest tests.
7. Clearly label each file with its filename.
8. Put each file's code inside a Python code block.
9. Do not include explanations outside the generated files.
10. Do not execute any generated code.

Generate the application files now.
"""
        return self.llm.generate(prompt)