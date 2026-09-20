import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

MODELS = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
).strip()

print(
    f"MODEL = {MODEL_NAME}"
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)