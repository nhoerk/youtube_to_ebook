import re
from pathlib import Path
from src.core.paths import data_dir


def clean_transcript(input_file: Path) -> Path:

    text = input_file.read_text(
        encoding="utf-8"
    )

    patterns = [
        r"\[.*?\]",
        r"\(.*?\)",
        r"\bee+\b",
        r"\bemm+\b",
    ]

    for pattern in patterns:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)

    output_dir = data_dir() / "transcript_clean"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir /
        f"{input_file.stem}_clean.txt"
    )

    output_file.write_text(
        text,
        encoding="utf-8"
    )

    return output_file