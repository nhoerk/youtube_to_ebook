import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)