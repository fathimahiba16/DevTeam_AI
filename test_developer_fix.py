
from agents.developer_agent import DeveloperAgent


class FakeLLM:
    def __init__(self):
        self.last_prompt = ""

    def generate(self, prompt):
        self.last_prompt = prompt
        return "Corrected application code"


fake_llm = FakeLLM()
developer = DeveloperAgent(fake_llm)

original_code = 'print("Hello World"'
test_errors = "SyntaxError: '(' was never closed"

result = developer.fix_code(original_code, test_errors)

assert result == "Corrected application code"
assert original_code in fake_llm.last_prompt
assert test_errors in fake_llm.last_prompt
assert "COMPLETE corrected application" in fake_llm.last_prompt

print("SUCCESS! Developer Agent received the code and test errors.")
print("SUCCESS! Developer Agent returned the simulated fix.")
