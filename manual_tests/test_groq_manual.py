import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

print("Groq API key detected:", bool(api_key))

if not api_key:
    raise RuntimeError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Groq connection successful",
        }
    ],
    max_tokens=50,
)

print(response.choices[0].message.content)