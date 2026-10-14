
from services.file_manager import FileManager

sample_response = """
### `app.py`
```python
print("Hello from generated app")
```

### `database.py`
```python
import sqlite3
print("Database connected")
```

### `requirements.txt`
```text
streamlit
pytest
```
"""

manager = FileManager()
files = manager.extract_files(sample_response)

print("Extracted filenames:")
for filename in files:
    print(filename)

assert len(files) == 3

print("\nSUCCESS! All 3 files extracted correctly.")

project_folder = manager.save_files(
    files,
    project_name="test_project"
)

print("\nFiles saved successfully!")
print("Location:", project_folder)

for filename in files:
    assert (project_folder / filename).is_file()

print("SUCCESS! All files exist in the workspace.")