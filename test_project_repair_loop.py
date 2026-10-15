
from services.project_repair_loop import ProjectRepairLoop


class FakeDeveloperAgent:
    def __init__(self):
        self.fix_calls = 0

    def fix_code(self, generated_code, test_errors):
        self.fix_calls += 1

        # Return the complete project with corrected Python code
        return """
### `app.py`
```python
print("Hello from DevTeam AI")
```

### `utils.py`
```python
def add(a, b):
    return a + b
```

### `requirements.txt`
```text
streamlit
```
"""


# The original project contains a syntax error in app.py
broken_project = """
### `app.py`
```python
print("Hello from DevTeam AI"
```

### `utils.py`
```python
def add(a, b):
    return a + b
```

### `requirements.txt`
```text
streamlit
```
"""

developer = FakeDeveloperAgent()
repair_loop = ProjectRepairLoop(developer, max_attempts=3)

result = repair_loop.repair(broken_project)

print("Status:", result["status"])
print("Repair attempts:", result["attempts"])
print("Developer fix calls:", developer.fix_calls)

assert result["status"] == "PASS"
assert result["attempts"] == 1
assert developer.fix_calls == 1

print("\nSUCCESS! Multi-file Project Repair Loop worked!")


class AlwaysFailDeveloper:
    def __init__(self):
        self.fix_calls = 0

    def fix_code(self, generated_code, test_errors):
        self.fix_calls += 1
        return generated_code


failing_developer = AlwaysFailDeveloper()

failing_loop = ProjectRepairLoop(
    failing_developer,
    max_attempts=3
)

failed_result = failing_loop.repair(broken_project)

print("\nFailure scenario:")
print("Status:", failed_result["status"])
print("Repair attempts:", failed_result["attempts"])

assert failed_result["status"] == "FAIL"
assert failed_result["attempts"] == 3
assert failing_developer.fix_calls == 3

print("\nSUCCESS! Project Repair Loop stopped after 3 failed attempts.")

