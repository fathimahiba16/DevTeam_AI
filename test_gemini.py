
import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY is not available.")
    raise SystemExit(1)

print("Gemini API key detected. Connecting...")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Say hello in one short sentence."
)

print("\nAI RESPONSE:")
print(response.text)
