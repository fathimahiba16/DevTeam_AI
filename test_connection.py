
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from config import (
    WATSONX_APIKEY,
    WATSONX_URL,
    WATSONX_PROJECT_ID,
    WATSONX_MODEL_ID,
)

# Check that the API key is available
if not WATSONX_APIKEY:
    print("ERROR: WATSONX_APIKEY is not available.")
    print("Check your Codespaces secret and restart the Codespace.")
    raise SystemExit(1)

print("API key detected. Connecting to IBM watsonx.ai...")

# Configure IBM credentials
credentials = Credentials(
    url=WATSONX_URL,
    api_key=WATSONX_APIKEY,
)

# Initialize the AI model
model = ModelInference(
    model_id=WATSONX_MODEL_ID,
    credentials=credentials,
    project_id=WATSONX_PROJECT_ID,
    params={
        "max_tokens": 100,
        "temperature": 0,
    },
)

# Send a simple test prompt
response = model.chat(
    messages=[
        {
            "role": "user",
            "content": "Say hello and introduce yourself in one sentence.",
        }
    ]
)

print("\nAI RESPONSE:")
print(response["choices"][0]["message"]["content"])
