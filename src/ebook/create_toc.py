from pathlib import Path
from src.core.paths import data_dir


def create_toc():

    toc = """
# DAFTAR ISI

Kata Pengantar

Bab 1 - Pengakuan Tanpa Pengabdian

Bab 2 - Mitos Perantara dan Syafaat

Bab 3 - Spektrum Objek Sembahan

Bab 4 - Potret Ironi Kesyirikan Modern

Penutup
"""

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