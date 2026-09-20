import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    book_title: str = ""
    author: str = ""
    languages: tuple[str, ...] = ("id", "en")
    chunk_size: int = 3000
    gemini_model: str = ""
    generate_references: bool = True
    max_chapters: int = 12
    max_retries: int = 3
    allow_model_fallback: bool = True

    def fingerprint(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_config(path: Path | None = None) -> AppConfig:
    if path is None or not path.exists():
        return AppConfig()

    values = json.loads(path.read_text(encoding="utf-8"))
    defaults = asdict(AppConfig())
    defaults.update(values)
    defaults["languages"] = tuple(defaults["languages"])
    defaults["chunk_size"] = int(defaults["chunk_size"])
    return AppConfig(**defaults)
