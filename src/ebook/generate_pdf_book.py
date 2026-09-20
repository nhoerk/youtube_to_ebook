from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
)


def generate_pdf():

    manuscript = Path(
        "output/manuscript.md"
    )

    text = manuscript.read_text(
        encoding="utf-8"
    )

    output_file = (
        "output/Membentengi_Akidah_Memurnikan_Tauhid.pdf"
    )

    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
    )

    styles = getSampleStyleSheet()

    story = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("# "):
            story.append(
                Paragraph(
                    line.replace("# ", ""),
                    styles["Heading1"],
                )
            )

        elif line.startswith("## "):
            story.append(
                Paragraph(
                    line.replace("## ", ""),
                    styles["Heading2"],
                )
            )

        else:
            story.append(
                Paragraph(
                    line,
                    styles["BodyText"],
                )
            )

        story.append(
            Spacer(1, 6)
        )

    doc.build(story)

    print(
        f"PDF tersimpan: {output_file}"
    )

    return output_file