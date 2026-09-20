from pathlib import Path


def build_manuscript():

    ebook_dir = Path(
        "data/ebook_content"
    )

    output_dir = Path(
        "output"
    )

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