
from pathlib import Path
from tempfile import TemporaryDirectory

from agents.testing_agent import TestingAgent


with TemporaryDirectory() as folder:
    project = Path(folder)

    # Create a Python file with correct syntax
    (project / "good.py").write_text(
        'print("Hello World")\n',
        encoding="utf-8"
    )

    # Create a Python file with a syntax error
    (project / "bad.py").write_text(
        'print("Hello World"\n',
        encoding="utf-8"
    )

    agent = TestingAgent()
    results = agent.check_syntax(project)

    for result in results:
        print(
            result["file"],
            "->",
            result["status"],
            "->",
            result["message"]
        )

    assert len(results) == 2
    assert any(r["status"] == "PASS" for r in results)
    assert any(r["status"] == "FAIL" for r in results)

    print("\nSUCCESS! Testing Agent detected the syntax error.")
