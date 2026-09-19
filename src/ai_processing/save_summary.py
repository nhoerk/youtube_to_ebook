from pathlib import Path

from src.ai_processing.summarize_chunk import summarize_chunk


def process_chunk(chunk_file):

    text = Path(chunk_file).read_text(
        encoding="utf-8"
    )

    summary = summarize_chunk(text)

    output_dir = Path(
        "data/chapter_summary"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir /
        f"{Path(chunk_file).stem}.md"
    )

    output_file.write_text(
        summary,
        encoding="utf-8"
    )

    return output_file