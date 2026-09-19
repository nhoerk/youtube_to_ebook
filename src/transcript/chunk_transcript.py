from pathlib import Path


def chunk_transcript(
    input_file: Path,
    chunk_size: int = 3000,
):
    text = input_file.read_text(
        encoding="utf-8"
    )

    words = text.split()

    chunks = [
        words[i:i + chunk_size]
        for i in range(
            0,
            len(words),
            chunk_size
        )
    ]

    output_dir = Path(
        "data/transcript_chunks"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    files = []

    for idx, chunk in enumerate(chunks, start=1):

        output_file = (
            output_dir /
            f"{input_file.stem}_part_{idx}.txt"
        )

        output_file.write_text(
            " ".join(chunk),
            encoding="utf-8"
        )

        files.append(output_file)

    return files