from agents.requirement_agent import RequirementAgent
from services.llm_service import LLMService


llm = LLMService(provider="gemini")

agent = RequirementAgent(llm)

idea = "Build a Student Management System where teachers can add, view, update, and delete student records."

print("Sending software idea to Gemini...\n")

requirements = agent.analyze(idea)

print("GENERATED REQUIREMENTS:\n")
print(requirements)