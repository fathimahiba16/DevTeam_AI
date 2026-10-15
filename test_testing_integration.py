
from pathlib import Path
from tempfile import TemporaryDirectory

from agents.testing_agent import TestingAgent


with TemporaryDirectory() as folder:
    project = Path(folder)

    # Create a valid application file
    (project / "app.py").write_text(
        'print("Hello from DevTeam AI")\n',
        encoding="utf-8"
    )

    # Create a pytest test file
    (project / "test_app.py").write_text(
        "def test_example():\n    assert 2 + 2 == 4\n",
        encoding="utf-8"
    )

    agent = TestingAgent()

    syntax_results = agent.check_syntax(project)
    availability = agent.check_test_availability(project)

    print("Syntax results:", syntax_results)
    print("Test availability:", availability)

    assert len(syntax_results) == 2
    assert all(item["status"] == "PASS" for item in syntax_results)
    assert availability["status"] == "READY"
    assert availability["test_files"] == ["test_app.py"]

    print("\nSUCCESS! Testing Agent integration checks passed.")
