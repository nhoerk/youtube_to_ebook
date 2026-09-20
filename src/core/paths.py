import os
from pathlib import Path


def data_dir() -> Path:
    return Path(os.getenv("YOUTUBE_TO_EBOOK_DATA_DIR", "data"))


def output_dir() -> Path:
    return Path(os.getenv("YOUTUBE_TO_EBOOK_OUTPUT_DIR", "output"))
