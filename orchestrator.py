from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from services.llm_service import LLMService


class Orchestrator:
    def __init__(self, provider="gemini"):
        self.llm = LLMService(provider=provider)

        self.requirement_agent = RequirementAgent(self.llm)
        self.architect_agent = ArchitectAgent(self.llm)

    def run(self, user_idea):
        print("Step 1: Requirement Agent is working...")

        requirements = self.requirement_agent.analyze(user_idea)

        print("Step 2: Architect Agent is working...")

        architecture = self.architect_agent.design(requirements)

        return {
            "requirements": requirements,
            "architecture": architecture
        }