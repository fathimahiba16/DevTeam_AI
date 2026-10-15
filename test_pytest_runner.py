
from pathlib import Path
from tempfile import TemporaryDirectory

from agents.testing_agent import TestingAgent


with TemporaryDirectory() as folder:
    project = Path(folder)

    # Create a trusted sample test
    (project / "test_sample.py").write_text(
        "def test_addition():\n"
        "    assert 2 + 2 == 4\n\n"
        "def test_subtraction():\n"
        "    assert 10 - 3 == 8\n",
        encoding="utf-8"
    )

    agent = TestingAgent()
    result = agent.run_pytest(project)

    print("Status:", result["status"])
    print("Pytest output:")
    print(result["output"])

    assert result["status"] == "FAIL"

    print("\nSUCCESS! Testing Agent ran pytest automatically.")
