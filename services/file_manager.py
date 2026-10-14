from pathlib import Path
import re


class FileManager:
    def extract_files(self, generated_text):
        """
        Extract filenames and code blocks from AI-generated text.
        Returns a dictionary: {filename: content}
        """

        pattern = r"###\s+`([^`]+)`\s*\n```[^\n]*\n(.*?)\n```"

        matches = re.findall(
            pattern,
            generated_text,
            re.DOTALL
        )

        files = {}

        for filename, content in matches:
            filename = filename.strip()

            # Reject unsafe file paths
            path = Path(filename)

            if (
                path.is_absolute()
                or ".." in path.parts
                or not filename
            ):
                continue

            files[filename] = content

        return files

    def save_files(self, files, project_name="generated_project"):
        """
        Save extracted files inside the workspace folder.
        """

        workspace = Path("workspace").resolve()
        from uuid import uuid4

        project_folder = workspace / f"{project_name}_{uuid4().hex[:8]}"
        project_folder.mkdir(parents=True, exist_ok=True)

        for filename, content in files.items():
            file_path = (project_folder / filename).resolve()

            # Prevent files from being saved outside this project
            if not file_path.is_relative_to(project_folder.resolve()):
                raise ValueError(f"Unsafe filename: {filename}")

            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")

        return project_folder