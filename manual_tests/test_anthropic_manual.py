import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")

print("API key detected:", bool(api_key))

if not api_key:
    raise RuntimeError("API key not found")

client = Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Anthropic connection successful",
        }
    ],
)

print(response.content[0].text)