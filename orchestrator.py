
from pathlib import Path

from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from agents.developer_agent import DeveloperAgent
from agents.testing_agent import TestingAgent
from agents.review_agent import ReviewAgent
from agents.documentation_agent import DocumentationAgent

from services.llm_service import LLMService
from services.file_manager import FileManager
from services.project_repair_loop import ProjectRepairLoop
from services.pdf_generator import PDFGenerator
from services.zip_manager import ZipManager


class Orchestrator:
    def __init__(self, provider="gemini"):
        self.llm = LLMService(provider=provider)

        self.requirement_agent = RequirementAgent(self.llm)
        self.architect_agent = ArchitectAgent(self.llm)
        self.developer_agent = DeveloperAgent(self.llm)
        self.review_agent = ReviewAgent(self.llm)
        self.documentation_agent = DocumentationAgent(self.llm)

        self.file_manager = FileManager()
        self.testing_agent = TestingAgent()
        self.pdf_generator = PDFGenerator()
        self.zip_manager = ZipManager()

        self.repair_loop = ProjectRepairLoop(
            developer_agent=self.developer_agent,
            max_attempts=3
        )

    def run(self, user_idea):
        print("Step 1: Requirement Agent is working...")
        requirements = self.requirement_agent.analyze(user_idea)

        print("Step 2: Architect Agent is working...")
        architecture = self.architect_agent.design(requirements)

        print("Step 3: Developer Agent is working...")
        generated_code = self.developer_agent.generate_code(
            architecture
        )

        print("Step 4: Project Repair Loop is checking syntax...")
        repair_result = self.repair_loop.repair(generated_code)

        generated_code = repair_result.get(
            "generated_code",
            generated_code
        )

        project_folder = repair_result.get("project_folder")

        if project_folder:
            test_results = repair_result.get(
                "syntax_results",
                []
            )

            test_availability = (
                self.testing_agent.check_test_availability(
                    project_folder
                )
            )

            files = self.file_manager.extract_files(
                generated_code
            )

            saved_files = list(files.keys())

        else:
            test_results = []

            test_availability = {
                "status": "NOT_CHECKED",
                "message": "No project folder was created."
            }

            saved_files = []

        review = None
        report_content = None
        pdf_path = None

        documentation_status = "SKIPPED"
        documentation_error = None

        # Review and document only if syntax checking passed.
        if repair_result["status"] == "PASS" and project_folder:

            print("Step 5: Review Agent is reviewing the project...")

            review = self.review_agent.review(
                requirements,
                architecture,
                generated_code
            )

            print("Step 6: Documentation Agent is writing the report...")

            try:
                report_content = (
                    self.documentation_agent.generate_report(
                        requirements=requirements,
                        architecture=architecture,
                        generated_code=generated_code,
                        review=review,
                        test_results=test_results
                    )
                )

                if not isinstance(report_content, str):
                    raise ValueError(
                        "Documentation Agent returned invalid report content."
                    )

                if not report_content.strip():
                    raise ValueError(
                        "Documentation Agent returned an empty report."
                    )

                print("Step 7: Generating college project PDF...")

                output_path = (
                    Path(project_folder) / "Project_Report.pdf"
                )

                pdf_path = self.pdf_generator.generate_pdf(
                    report_content=report_content,
                    output_path=output_path,
                    project_title="Software Project Report"
                )

                documentation_status = "SUCCESS"

                if "Project_Report.pdf" not in saved_files:
                    saved_files.append("Project_Report.pdf")

            except Exception as error:
                documentation_status = "ERROR"
                documentation_error = str(error)

                print(
                    "Documentation generation failed:",
                    documentation_error
                )

        else:
            print(
                "Review and documentation skipped because "
                "the project did not pass syntax checking."
            )

            review = (
                "Review skipped because the generated project "
                "did not pass Python syntax checking."
            )

        # Package the generated project into a ZIP file.
        print("Step 8: Packaging project into ZIP...")

        zip_path = None
        zip_error = None

        if project_folder:
            try:
                zip_path = self.zip_manager.create_zip(
                    project_folder
                )

                print("ZIP created:", zip_path)

            except Exception as error:
                zip_error = str(error)

                print(
                    "ZIP packaging failed:",
                    zip_error
                )

        else:
            print("ZIP skipped: no project folder.")

        print("Repair status:", repair_result["status"])
        print("Repair attempts:", repair_result["attempts"])
        print("Documentation status:", documentation_status)

        return {
            "requirements": requirements,
            "architecture": architecture,
            "generated_code": generated_code,

            "project_folder": (
                str(project_folder)
                if project_folder
                else None
            ),

            "saved_files": saved_files,
            "test_results": test_results,
            "test_availability": test_availability,

            "repair_status": repair_result["status"],
            "repair_attempts": repair_result["attempts"],
            "repair_stage": repair_result.get("stage"),
            "repair_message": repair_result.get(
                "message",
                ""
            ),

            "pytest_status": repair_result.get(
                "pytest_status",
                "NOT_RUN"
            ),

            "review": review,

            "report_content": report_content,
            "pdf_path": pdf_path,
            "documentation_status": documentation_status,
            "documentation_error": documentation_error,

            "zip_path": zip_path,
            "zip_error": zip_error
        }
