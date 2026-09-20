from pathlib import Path

from src.ai_processing.gemini_utils import (
    ask_gemini,
)


def create_preface():

    outline_file = Path(
        "data/book_outline/book_outline.md"
    )

    outline = outline_file.read_text(
        encoding="utf-8"
    )

    prompt = f"""
Anda adalah editor buku Islam.

Buatkan Kata Pengantar berdasarkan outline buku berikut.

ATURAN:

1. Bahasa Indonesia formal.
2. Panjang 500-800 kata.
3. Jelaskan tujuan buku.
4. Jelaskan manfaat buku.
5. Jelaskan bahwa buku disusun dari kajian YouTube.
6. Tidak berlebihan memuji.
7. Tidak menambahkan materi akidah baru.
8. Gaya bahasa hangat dan profesional.
9. Sertakan harapan agar buku bermanfaat bagi pembaca.

Outline:

{outline}
"""

    print(
        "Membuat kata pengantar..."
    )

    response_text = ask_gemini(
        prompt
    )

    output_dir = Path(
        "data/book_assets"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir /
        "preface.md"
    )

    output_file.write_text(
        response_text,
        encoding="utf-8"
    )

    print(
        f"Tersimpan: {output_file}"
    )

    return output_file