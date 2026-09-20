from pathlib import Path

from src.ai_processing.save_summary import (
    process_chunk,
)

chunk_dir = Path(
    "data/transcript_chunks"
)

for file in chunk_dir.glob("*.txt"):
    print(
        f"Memproses {file.name}..."
    )

    output = process_chunk(file)

    print(
        f"Tersimpan: {output}"
    )