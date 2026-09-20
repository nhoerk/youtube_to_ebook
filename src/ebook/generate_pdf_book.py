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
from src.core.paths import output_dir
import os
import re


def _output_name(extension):
    title = os.getenv(
        "YOUTUBE_TO_EBOOK_BOOK_TITLE",
        "Membentengi Akidah, Memurnikan Tauhid",
    )
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return f"{slug}.{extension}"


def generate_pdf():

    manuscript = output_dir() / "manuscript.md"

    text = manuscript.read_text(
        encoding="utf-8"
    )

    output_file = output_dir() / _output_name("pdf")

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