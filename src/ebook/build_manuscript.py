from pathlib import Path
from src.core.paths import data_dir, output_dir as get_output_dir


def build_manuscript():

    ebook_dir = data_dir() / "ebook_content"

    output_dir = get_output_dir()

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manuscript = []

    manuscript.append(
        "# MEMBENTENGI AKIDAH, MEMURNIKAN TAUHID\n"
    )

    for file in sorted(
        ebook_dir.glob("bab_*.md")
    ):
        manuscript.append(
            file.read_text(
                encoding="utf-8"
            )
        )

    output_file = (
        output_dir /
        "manuscript.md"
    )

    output_file.write_text(
        "\n\n".join(manuscript),
        encoding="utf-8",
    )

    print(
        f"Tersimpan: {output_file}"
    )

    return output_file