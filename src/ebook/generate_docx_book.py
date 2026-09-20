from pathlib import Path
from src.core.paths import output_dir
from docx import Document


def generate_docx():

    manuscript = output_dir() / "manuscript.md"

    text = manuscript.read_text(
        encoding="utf-8"
    )

    doc = Document()

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("# "):
            doc.add_heading(
                line.replace("# ", ""),
                level=1,
            )

        elif line.startswith("## "):
            doc.add_heading(
                line.replace("## ", ""),
                level=2,
            )

        else:
            doc.add_paragraph(line)

    output_file = output_dir() / "Membentengi_Akidah_Memurnikan_Tauhid.docx"

    doc.save(output_file)

    print(
        f"DOCX tersimpan: {output_file}"
    )

    return output_file