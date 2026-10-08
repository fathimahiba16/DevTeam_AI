from agents.requirement_agent import RequirementAgent


class FakeLLM:
    def generate(self, prompt):
        assert "Student Management System" in prompt
        assert "Functional Requirements" in prompt

        return "Sample requirements generated successfully!"


llm = FakeLLM()
agent = RequirementAgent(llm)

result = agent.analyze("Build a Student Management System")

print("RESULT:")
print(result)