# test_gemini.py

from src.ai_processing.gemini_client import (
    client,
    MODEL_NAME,
)

response = client.models.generate_content(
    model=MODEL_NAME,
    contents="Halo, jawab singkat saja."
)

print(response.text)