from agents.architect_agent import ArchitectAgent


class FakeLLM:
    def generate(self, prompt):
        assert "Student Management System" in prompt
        assert "Database Design" in prompt

        return "Sample software architecture generated successfully!"


llm = FakeLLM()
agent = ArchitectAgent(llm)

requirements = "Build a Student Management System"

result = agent.design(requirements)

print("RESULT:")
print(result)