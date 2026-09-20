from src.ebook.generate_pdf_book import generate_pdf


def test_generate_pdf_accepts_windows_output_path(tmp_path, monkeypatch):
    output = tmp_path / "output"
    output.mkdir()
    (output / "manuscript.md").write_text(
        "# Judul\n\nIsi buku.",
        encoding="utf-8",
    )
    monkeypatch.setenv("YOUTUBE_TO_EBOOK_OUTPUT_DIR", str(output))

    generated = generate_pdf()

    assert generated.exists()
    assert generated.stat().st_size > 0