import json
from types import SimpleNamespace

from src.ai_processing import create_book_outline as outline_module


def test_create_book_outline_escapes_json_prompt(tmp_path, monkeypatch):
    monkeypatch.setenv("YOUTUBE_TO_EBOOK_DATA_DIR", str(tmp_path / "data"))
    summary_dir = tmp_path / "data" / "chapter_summary"
    summary_dir.mkdir(parents=True)
    (summary_dir / "part_1.md").write_text("Tema video", encoding="utf-8")

    captured = {}

    def fake_generate(prompt):
        captured["prompt"] = prompt
        return SimpleNamespace(
            text=json.dumps(
                {
                    "book_title": "Tema Baru",
                    "purpose": "Tujuan",
                    "chapters": [
                        {
                            "number": 1,
                            "title": "Bab Dinamis",
                            "summary": "Ringkasan",
                        }
                    ],
                }
            )
        )

    monkeypatch.setattr(outline_module, "generate_with_fallback", fake_generate)

    output = outline_module.create_book_outline()

    assert '"number": 1' in captured["prompt"]
    assert output.exists()
