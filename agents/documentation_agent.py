
class DocumentationAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_report(
        self,
        requirements,
        architecture,
        generated_code,
        review,
        test_results
    ):
        """
        Generate content for a formal college project report.
        PDF formatting will be handled separately.
        """

        prompt = f"""
You are the Documentation Agent in DevTeam AI.

Write a formal academic mini-project report based on
the following software project information.

REQUIREMENTS:
{requirements}

SYSTEM ARCHITECTURE:
{architecture}

GENERATED SOURCE CODE:
{generated_code}

CODE REVIEW:
{review}

SYNTAX CHECK RESULTS:
{test_results}

Create the report with these sections:

# Project Title
# Abstract
# 1. Introduction
# 2. Problem Statement
# 3. Objectives
# 4. Requirement Analysis
# 5. System Architecture
# 6. Technologies Used
# 7. Implementation Details
# 8. Testing and Results
# 9. Limitations and Future Scope
# 10. Conclusion

INSTRUCTIONS:
- Use formal academic language.
- Explain the actual generated application.
- Do not invent features, dependencies, or results.
- Clearly distinguish syntax checking from executed tests.
- Do not claim the project was executed unless
  execution results are explicitly provided.
- Do not invent screenshots, references, or citations.
- Return only the report content in Markdown.
- Do not wrap the entire report in a code fence.
"""

        return self.llm.generate(prompt)
