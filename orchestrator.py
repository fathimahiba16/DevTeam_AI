
from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from agents.developer_agent import DeveloperAgent
from services.llm_service import LLMService
from services.file_manager import FileManager


class Orchestrator:
    def __init__(self, provider="gemini"):
        self.llm = LLMService(provider=provider)

        self.requirement_agent = RequirementAgent(self.llm)
        self.architect_agent = ArchitectAgent(self.llm)
        self.developer_agent = DeveloperAgent(self.llm)

    def run(self, user_idea):
        print("Step 1: Requirement Agent is working...")
        requirements = self.requirement_agent.analyze(user_idea)

        print("Step 2: Architect Agent is working...")
        architecture = self.architect_agent.design(requirements)

        print("Step 3: Developer Agent is working...")
        generated_code = self.developer_agent.generate_code(architecture)

        print("\n===== DEVELOPER AGENT RAW OUTPUT =====")
        print(generated_code)
        print("===== END OF OUTPUT =====\n")

        print("Step 4: File Manager is saving generated files...")
        file_manager = FileManager()
        files = file_manager.extract_files(generated_code)

        if not files:
            raise ValueError("No files could be extracted from the generated code.")

        project_folder = file_manager.save_files(files)

        return {
            "requirements": requirements,
            "architecture": architecture,
            "generated_code": generated_code,
            "project_folder": str(project_folder),
            "saved_files": list(files.keys())
        }
