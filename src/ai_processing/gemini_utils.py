# src/ai_processing/gemini_utils.py

import logging
import os
import random
import time

from src.ai_processing.gemini_client import (
    client,
    FALLBACK_MODELS,
    MODEL_NAME,
)

def _is_quota_error(error_text):
    normalized = error_text.lower()
    return any(
        marker in normalized
        for marker in (
            "429",
            "quota",
            "resource_exhausted",
            "rate limit",
            "too many requests",
        )
    )


def generate_with_fallback(prompt: str, retry: int = 2):
    models = (os.getenv("GEMINI_MODEL", MODEL_NAME), *FALLBACK_MODELS)
    last_error = None

    for model in models:
        for attempt in range(retry):
            try:
                logging.getLogger(__name__).info(
                    "Gemini request using model %s (attempt %d/%d)",
                    model,
                    attempt + 1,
                    retry,
                )
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                logging.getLogger(__name__).info(
                    "Gemini request succeeded using model %s",
                    model,
                )
                return response
            except Exception as error:
                last_error = error
                error_text = str(error)
                if _is_quota_error(error_text):
                    logging.getLogger(__name__).warning(
                        "Model %s reached a quota/rate limit; switching model",
                        model,
                    )
                    break
                if not any(
                    marker in error_text
                    for marker in ("500", "502", "503", "504", "UNAVAILABLE")
                ) or attempt >= retry - 1:
                    raise
                wait_time = min(60, (2 ** attempt) + random.random())
                time.sleep(wait_time)

    raise RuntimeError(
        "Semua model Gemini gagal atau mencapai limit."
    ) from last_error


def ask_gemini(
    prompt: str,
    retry: int = 5,
):

    return generate_with_fallback(prompt, retry=retry).text