
import ast
from pathlib import Path
import subprocess
import sys

class TestingAgent:
    def check_syntax(self, project_folder):
        """
        Check generated Python files for syntax errors
        without executing the code.
        """

        project_folder = Path(project_folder)
        results = []

        for file_path in project_folder.rglob("*.py"):
            try:
                code = file_path.read_text(encoding="utf-8")
                ast.parse(code, filename=str(file_path))

                results.append({
                    "file": str(file_path.relative_to(project_folder)),
                    "status": "PASS",
                    "message": "No syntax errors"
                })

            except SyntaxError as error:
                results.append({
                    "file": str(file_path.relative_to(project_folder)),
                    "status": "FAIL",
                    "message": str(error)
                })

        return results

    def find_test_files(self, project_folder):
        """
        Find pytest test files in a generated project.
        Does not execute any code.
        """

        project_folder = Path(project_folder)
        test_files = []

        for file_path in project_folder.rglob("*.py"):
            if (
                file_path.name.startswith("test_")
                or file_path.name.endswith("_test.py")
            ):
                test_files.append(
                    str(file_path.relative_to(project_folder))
                )

        return sorted(test_files)

    def check_test_availability(self, project_folder):
        """
        Check whether a generated project contains pytest files.
        """
        test_files = self.find_test_files(project_folder)

        if not test_files:
            return {
                "status": "NO_TESTS",
                "message": "No pytest test files were generated.",
                "test_files": []
            }

        return {
            "status": "READY",
            "message": f"Found {len(test_files)} pytest test file(s).",
            "test_files": test_files
        }



    def run_pytest(self, project_folder):
        """
        Run pytest and capture its output.

        Only use this with trusted test projects.
        """

        project_folder = Path(project_folder).resolve()

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q"
                ],
                cwd=project_folder,
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "status": "PASS" if result.returncode == 0 else "FAIL",
                "output": result.stdout + result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "ERROR",
                "output": "Testing timed out after 30 seconds."
            }

