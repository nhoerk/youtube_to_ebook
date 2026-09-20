import json
from src.core.paths import data_dir
from src.ai_processing.gemini_utils import generate_with_fallback


def run_editorial_review():
    summary_dir = data_dir() / "chapter_summary"
    source = "\n\n".join(
        file.read_text(encoding="utf-8")
        for file in sorted(summary_dir.glob("*.md"))
    )
    prompt = f"""Tinjau ringkasan materi berikut untuk kebutuhan buku.
Kembalikan JSON valid saja:
{{"items":[{{"original":"teks","revised":"perbaikan bahasa","notes":"catatan"}}]}}
Jangan mengubah makna dan jangan menambahkan fakta baru.

{source}"""
    response = generate_with_fallback(prompt)
    try:
        result = json.loads(response.text.strip().strip("`"))
    except json.JSONDecodeError as error:
        raise ValueError("Hasil editorial review bukan JSON valid.") from error
    if not isinstance(result.get("items"), list):
        raise ValueError("Hasil editorial review tidak memiliki items.")
    output = data_dir() / "editorial" / "review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return output
