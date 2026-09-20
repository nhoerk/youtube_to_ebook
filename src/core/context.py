from dataclasses import dataclass
from pathlib import Path
from contextvars import ContextVar


@dataclass(frozen=True)
class JobContext:
    video_id: str
    youtube_url: str
    data_path: Path
    output_path: Path
    book_title: str = ""
    author: str = ""
    model: str = ""


_current: ContextVar[JobContext | None] = ContextVar("job_context", default=None)


def set_context(context: JobContext):
    _current.set(context)


def current_context() -> JobContext | None:
    return _current.get()
