import json
from pathlib import Path
from src.core.paths import data_dir


def create_toc():
    outline_file = data_dir() / "book_outline" / "book_outline.json"
    outline = json.loads(outline_file.read_text(encoding="utf-8"))

    lines = ["# DAFTAR ISI", "", "Kata Pengantar", ""]
    lines.extend(
        f"Bab {chapter['number']} - {chapter['title']}"
        for chapter in outline["chapters"]
    )
    lines.extend(["", "Penutup", ""])
    toc = "\n".join(lines)

    output_dir = data_dir() / "book_assets"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir /
        "toc.md"
    )

    output_file.write_text(
        toc,
        encoding="utf-8"
    )

    print(
        f"Tersimpan: {output_file}"
    )

    return output_file