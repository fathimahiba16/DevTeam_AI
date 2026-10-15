
class ReviewAgent:
    def __init__(self, llm):
        self.llm = llm

    def review(self, requirements, architecture, generated_code):
        """
        Review the generated project and provide
        actionable feedback without executing code.
        """

        prompt = f"""
You are the Review Agent in an AI software development team.

Your task is to review a generated software project.

USER REQUIREMENTS:
{requirements}

SYSTEM ARCHITECTURE:
{architecture}

GENERATED PROJECT CODE:
{generated_code}

Review the project for:

1. Requirement coverage
2. Code correctness and potential bugs
3. Code readability
4. Maintainability
5. Basic security concerns
6. Missing features or improvements

Respond using this format:

## Overall Assessment
Briefly summarize the code quality.

## Requirement Coverage
Explain whether the generated code appears to meet
the requirements.

## Potential Issues
List possible bugs, risks, or missing functionality.

## Suggested Improvements
Provide practical recommendations.

## Final Verdict
Choose one:
- APPROVED
- NEEDS IMPROVEMENT

IMPORTANT:
- Do not claim you executed the code.
- Do not claim tests passed unless test results were provided.
- Base your review only on the supplied information.
"""

        return self.llm.generate(prompt)
