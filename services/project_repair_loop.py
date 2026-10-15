
from services.file_manager import FileManager
from agents.testing_agent import TestingAgent


class ProjectRepairLoop:
    def __init__(self, developer_agent, max_attempts=3):
        self.developer_agent = developer_agent
        self.max_attempts = max_attempts
        self.file_manager = FileManager()
        self.testing_agent = TestingAgent()

    def repair(self, generated_code, test_runner=None):
        """
        Repair a generated project using syntax checks and,
        optionally, simulated pytest results.

        IMPORTANT:
        - Syntax checks do not execute generated code.
        - test_runner must be a trusted simulation.
        - Do not pass a runner that executes AI-generated code.
        """
        attempts = 0

        while True:
            files = self.file_manager.extract_files(generated_code)

            if not files:
                return {
                    "status": "FAIL",
                    "attempts": attempts,
                    "message": "No project files could be extracted.",
                    "generated_code": generated_code
                }

            python_files = [
                filename
                for filename in files
                if filename.endswith(".py")
            ]

            if not python_files:
                return {
                    "status": "FAIL",
                    "attempts": attempts,
                    "message": "No Python files were extracted.",
                    "generated_code": generated_code
                }

            project_folder = self.file_manager.save_files(files)

            syntax_results = self.testing_agent.check_syntax(
                project_folder
            )

            syntax_errors = [
                result
                for result in syntax_results
                if result["status"] == "FAIL"
            ]

            # First, handle syntax errors.
            if syntax_errors:
                error_message = "\n".join(
                    f"{error['file']}: {error['message']}"
                    for error in syntax_errors
                )

                if attempts >= self.max_attempts:
                    return {
                        "status": "FAIL",
                        "stage": "syntax",
                        "attempts": attempts,
                        "project_folder": str(project_folder),
                        "syntax_results": syntax_results,
                        "generated_code": generated_code
                    }

                attempts += 1

                generated_code = self.developer_agent.fix_code(
                    generated_code,
                    error_message
                )

                continue

            # Syntax passed. If no simulated pytest runner
            # is supplied, stop here.
            if test_runner is None:
                return {
                    "status": "PASS",
                    "stage": "syntax_only",
                    "attempts": attempts,
                    "project_folder": str(project_folder),
                    "syntax_results": syntax_results,
                    "generated_code": generated_code,
                    "pytest_status": "NOT_RUN"
                }

            # Only use a trusted simulated test runner here.
            try:
                test_result = test_runner(generated_code)
            except Exception as error:
                return {
                    "status": "ERROR",
                    "stage": "pytest",
                    "attempts": attempts,
                    "project_folder": str(project_folder),
                    "syntax_results": syntax_results,
                    "generated_code": generated_code,
                    "pytest_status": "ERROR",
                    "message": str(error)
                }

            decision = self.evaluate_test_result(test_result)

            if decision["status"] == "PASS":
                return {
                    "status": "PASS",
                    "stage": "pytest",
                    "attempts": attempts,
                    "project_folder": str(project_folder),
                    "syntax_results": syntax_results,
                    "generated_code": generated_code,
                    "pytest_status": "PASS",
                    "test_result": test_result
                }

            if decision["status"] == "ERROR":
                return {
                    "status": "ERROR",
                    "stage": "pytest",
                    "attempts": attempts,
                    "project_folder": str(project_folder),
                    "syntax_results": syntax_results,
                    "generated_code": generated_code,
                    "pytest_status": "ERROR",
                    "test_result": test_result
                }

            # Simulated pytest reported a failure.
            if attempts >= self.max_attempts:
                return {
                    "status": "FAIL",
                    "stage": "pytest",
                    "attempts": attempts,
                    "project_folder": str(project_folder),
                    "syntax_results": syntax_results,
                    "generated_code": generated_code,
                    "pytest_status": "FAIL",
                    "test_result": test_result
                }

            attempts += 1

            generated_code = self.repair_test_failure(
                generated_code,
                test_result
            )

    def evaluate_test_result(self, test_result):
        """
        Decide whether a pytest result needs repair.
        Does not execute code.
        """
        status = test_result.get("status")

        if status == "PASS":
            return {
                "status": "PASS",
                "needs_repair": False,
                "message": "All pytest tests passed."
            }

        if status == "FAIL":
            return {
                "status": "FAIL",
                "needs_repair": True,
                "message": test_result.get(
                    "output",
                    "Pytest reported a failure."
                )
            }

        return {
            "status": "ERROR",
            "needs_repair": False,
            "message": test_result.get(
                "output",
                "Tests could not be completed."
            )
        }

    def repair_test_failure(self, generated_code, test_result):
        """
        Send simulated pytest failure details
        to the Developer Agent.
        """
        decision = self.evaluate_test_result(test_result)

        if not decision["needs_repair"]:
            return generated_code

        return self.developer_agent.fix_code(
            generated_code,
            decision["message"]
        )

    def repair_pytest_cycle(self, generated_code, test_runner):
        """
        Standalone simulated pytest repair cycle.

        Retained for compatibility with earlier tests.
        Do not pass a runner that executes untrusted code.
        """
        attempts = 0

        while True:
            test_result = test_runner(generated_code)
            decision = self.evaluate_test_result(test_result)

            if decision["status"] == "PASS":
                return {
                    "status": "PASS",
                    "attempts": attempts,
                    "generated_code": generated_code,
                    "test_result": test_result
                }

            if not decision["needs_repair"]:
                return {
                    "status": "ERROR",
                    "attempts": attempts,
                    "generated_code": generated_code,
                    "test_result": test_result
                }

            if attempts >= self.max_attempts:
                return {
                    "status": "FAIL",
                    "attempts": attempts,
                    "generated_code": generated_code,
                    "test_result": test_result
                }

            attempts += 1

            generated_code = self.repair_test_failure(
                generated_code,
                test_result
            )
