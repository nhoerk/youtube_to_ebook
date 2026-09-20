# src/ai_processing/gemini_utils.py

import time

from src.ai_processing.gemini_client import (
    client,
    MODEL_NAME,
)


def ask_gemini(
    prompt: str,
    retry: int = 5,
):

    for attempt in range(retry):

        try:

            print(
                f"Gemini Request ({attempt + 1}/{retry})"
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            return response.text

        except Exception as e:

            error_text = str(e)

            print(
                f"Request gagal ({attempt + 1}/{retry})"
            )

            print(error_text)

            # Quota habis
            if "429" in error_text:

                wait_time = 60

                print(
                    f"Quota habis. Tunggu {wait_time} detik..."
                )

                if attempt < retry - 1:

                    time.sleep(wait_time)
                    continue

            # Gemini overload
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                wait_time = 30

                print(
                    f"Server sibuk. Retry {wait_time} detik..."
                )

                if attempt < retry - 1:

                    time.sleep(wait_time)
                    continue

            # Error lainnya
            if attempt < retry - 1:

                print(
                    "Retry 10 detik..."
                )

                time.sleep(10)

            else:

                raise

    raise RuntimeError(
        "Semua percobaan Gemini gagal."
    )