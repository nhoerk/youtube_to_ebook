import os
from pathlib import Path
from src.core.context import current_context


def data_dir() -> Path:
    context = current_context()
    if context:
        return context.data_path
    return Path(os.getenv("YOUTUBE_TO_EBOOK_DATA_DIR", "data"))


def output_dir() -> Path:
    context = current_context()
    if context:
        return context.output_path
    return Path(os.getenv("YOUTUBE_TO_EBOOK_OUTPUT_DIR", "output"))


def log_dir() -> Path:
    return Path(os.getenv("YOUTUBE_TO_EBOOK_LOG_DIR", "logs"))
