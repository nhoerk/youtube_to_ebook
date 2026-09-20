# src/ai_processing/gemini_utils.py

import logging
import os
import random
import time
import hashlib
import json
from pathlib import Path
from src.core.paths import data_dir
from src.core.context import current_context

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
    context = current_context()
    selected_model = (context.model if context and context.model else os.getenv("GEMINI_MODEL", MODEL_NAME))
    models = (selected_model, *FALLBACK_MODELS)
    cache_key = hashlib.sha256(
        json.dumps({"prompt": prompt, "models": models}, sort_keys=True).encode()
    ).hexdigest()
    cache_file = data_dir() / "cache" / f"{cache_key}.json"
    if os.getenv("YOUTUBE_TO_EBOOK_DISABLE_CACHE") != "1" and cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding="utf-8"))
        logging.getLogger(__name__).info("Gemini cache hit: %s", cache_key)
        return type("CachedResponse", (), {"text": cached["text"]})()
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
                if os.getenv("YOUTUBE_TO_EBOOK_DISABLE_CACHE") != "1":
                    cache_file.parent.mkdir(parents=True, exist_ok=True)
                    cache_file.write_text(
                        json.dumps({"text": response.text}, ensure_ascii=False),
                        encoding="utf-8",
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