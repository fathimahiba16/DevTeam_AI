class LLMService:
    def __init__(self, provider="ibm"):
        self.provider = provider

    def generate(self, prompt):
        if self.provider == "ibm":
            return self._generate_ibm(prompt)

        elif self.provider == "gemini":
            return self._generate_gemini(prompt)

        else:
            raise ValueError("Unsupported AI provider")

    def _generate_ibm(self, prompt):
        raise NotImplementedError(
            "IBM connection will be added when watsonx.ai is ready."
        )

    def _generate_gemini(self, prompt):
        import os
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing.")

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        # print("GEMINI RESPONSE DETAILS:")
        # print(response.model_dump_json(indent=2, exclude_none=True))

        return response.text