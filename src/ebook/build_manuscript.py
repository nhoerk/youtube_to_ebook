from pathlib import Path
from src.core.paths import data_dir, output_dir as get_output_dir
from src.core.context import current_context
from datetime import datetime, timezone
import os


def build_manuscript():

    ebook_dir = data_dir() / "ebook_content"

    output_dir = get_output_dir()

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manuscript = []
    context = current_context()

    title = (
        context.book_title
        if context and context.book_title
        else os.getenv("YOUTUBE_TO_EBOOK_BOOK_TITLE", "Ebook Kajian YouTube")
    )
    manuscript.append(f"# {title}\n")
    if context:
        manuscript.append(
            "\n".join(
                [
                    "## Sumber",
                    f"- Judul ebook: {title}",
                    f"- URL: {context.youtube_url}",
                    f"- Video ID: {context.video_id}",
                    f"- Tanggal pemrosesan: {datetime.now(timezone.utc).date().isoformat()}",
                    f"- Model AI: {context.model or 'default'}",
                    "",
                ]
            )
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