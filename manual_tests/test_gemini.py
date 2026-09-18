import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

print("Testing Gemini 3.1 Flash Lite...")

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Write one short sentence about artificial intelligence."
)

print("SUCCESS")
print(response.text)