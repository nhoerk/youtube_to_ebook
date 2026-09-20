from pathlib import Path
import time

from src.ai_processing.gemini_client import (
    client,
    MODEL_NAME,
)


def create_book_outline():
    summary_dir = Path(
        "data/chapter_summary"
    )

    all_summary = []

    for file in sorted(
        summary_dir.glob("*.md")
    ):
        all_summary.append(
            file.read_text(
                encoding="utf-8"
            )
        )

    combined = "\n\n".join(
        all_summary
    )

    prompt = f"""
Anda adalah editor buku profesional.

Berikut adalah kumpulan ringkasan dari beberapa bagian
kajian YouTube.

Buat:

1. Judul buku
2. Tujuan buku
3. Daftar isi
4. Struktur bab yang logis
5. Ringkasan setiap bab

Format markdown.

{combined}
"""

    print(
        "Membuat outline..."
    )

    response = None

    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            break
        except Exception as e:
            print(
                f"Percobaan {attempt+1} gagal:"
            )
            print(e)

            if attempt < 4:
                print(
                    "Menunggu 30 detik..."
                )
                time.sleep(30)
            else:
                raise

    if response is None:
        raise RuntimeError(
            "Gagal membuat outline setelah beberapa percobaan."
        )

    output_dir = Path(
        "data/book_outline"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir /
        "book_outline.md"
    )

    output_file.write_text(
        response.text,
        encoding="utf-8",
    )

    print(
        f"Outline tersimpan: {output_file}"
    )

    return output_file