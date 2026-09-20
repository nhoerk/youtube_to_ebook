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

FALLBACK_MODELS = tuple(
    model.strip()
    for model in os.getenv(
        "GEMINI_FALLBACK_MODELS",
        "gemini-2.5-flash,gemini-2.5-pro",
    ).split(",")
    if model.strip() and model.strip() != MODEL_NAME
)

api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key or api_key == "your_gemini_api_key_here":
    raise RuntimeError(
        "GEMINI_API_KEY belum dikonfigurasi. Isi file .env sebelum menjalankan AI pipeline."
    )

print(
    f"MODEL = {MODEL_NAME}"
)

client = genai.Client(
    api_key=api_key
)