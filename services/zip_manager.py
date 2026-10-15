
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


class ZipManager:
    def create_zip(self, project_folder):
        """
        Package a generated project into a ZIP file.

        Includes source files and Project_Report.pdf
        if the PDF exists in the project folder.
        """

        project_path = Path(project_folder).resolve()

        if not project_path.is_dir():
            raise ValueError(
                "Project folder does not exist."
            )

        zip_path = project_path.parent / (
            project_path.name + ".zip"
        )

        with ZipFile(
            zip_path,
            "w",
            compression=ZIP_DEFLATED
        ) as zip_file:

            for file_path in project_path.rglob("*"):
                if not file_path.is_file():
                    continue

                # Do not follow symbolic links.
                if file_path.is_symlink():
                    continue

                # Avoid packaging files that resolve
                # outside the project directory.
                resolved_file = file_path.resolve()

                if not resolved_file.is_relative_to(project_path):
                    continue

                relative_path = file_path.relative_to(
                    project_path
                )

                zip_file.write(
                    file_path,
                    arcname=str(relative_path)
                )

        return str(zip_path)
