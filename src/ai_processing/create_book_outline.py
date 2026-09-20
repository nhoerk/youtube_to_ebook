import json
from pathlib import Path
from src.core.paths import data_dir
from src.ai_processing.gemini_utils import generate_with_fallback


def create_book_outline():
    summary_dir = data_dir() / "chapter_summary"

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

Buat output JSON valid saja dengan struktur berikut:
{{
  "book_title": "judul buku",
  "purpose": "tujuan buku",
  "chapters": [
    {{
      "number": 1,
      "title": "judul bab",
      "summary": "ringkasan bab"
    }}
  ]
}}

Tentukan jumlah bab dan tema berdasarkan isi transcript. Jangan gunakan tema
atau jumlah bab tetap. Nomor bab harus berurutan mulai dari 1. Jangan menulis
markdown fence atau teks lain di luar JSON.

{combined}
"""

    print(
        "Membuat outline..."
    )

    response = generate_with_fallback(prompt)

    output_dir = data_dir() / "book_outline"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        outline = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError("Outline AI bukan JSON yang valid.") from error

    chapters = outline.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        raise ValueError("Outline AI tidak memiliki daftar chapter.")

    for expected_number, chapter in enumerate(chapters, start=1):
        if (
            chapter.get("number") != expected_number
            or not chapter.get("title")
            or not chapter.get("summary")
        ):
            raise ValueError("Format chapter pada outline AI tidak valid.")

    output_file = output_dir / "book_outline.json"

    output_file.write_text(
        json.dumps(outline, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(
        f"Outline tersimpan: {output_file}"
    )

    return output_file