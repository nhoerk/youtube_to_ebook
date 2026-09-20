import json

from src.ebook.create_toc import create_toc


def test_toc_uses_dynamic_outline(tmp_path, monkeypatch):
    monkeypatch.setenv("YOUTUBE_TO_EBOOK_DATA_DIR", str(tmp_path / "data"))
    outline_dir = tmp_path / "data" / "book_outline"
    outline_dir.mkdir(parents=True)
    (outline_dir / "book_outline.json").write_text(
        json.dumps(
            {
                "book_title": "Tema Baru",
                "chapters": [
                    {"number": 1, "title": "Bab Dinamis", "summary": "Ringkasan"},
                    {"number": 2, "title": "Bab Kedua", "summary": "Ringkasan"},
                ],
            }
        ),
        encoding="utf-8",
    )

    output = create_toc()

    text = output.read_text(encoding="utf-8")
    assert "Bab 1 - Bab Dinamis" in text
    assert "Bab 2 - Bab Kedua" in text
    assert "Pengakuan Tanpa Pengabdian" not in text
