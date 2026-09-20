import json
from src.core.paths import data_dir
from src.ai_processing.gemini_utils import generate_with_fallback


def find_candidate_references():
    outline_file = data_dir() / "book_outline" / "book_outline.json"
    outline = outline_file.read_text(encoding="utf-8")
    prompt = f"""Identifikasi kandidat dalil yang relevan dari outline berikut.
Kembalikan JSON valid saja:
{{"references":[{{"claim":"klaim","type":"quran atau hadith","reference":"rujukan",
"status":"needs_verification","notes":"alasan relevansi"}}]}}
Jangan mengarang nomor hadis. Semua hasil wajib berstatus needs_verification.

{outline}"""
    response = generate_with_fallback(prompt)
    try:
        result = json.loads(response.text.strip().strip("`"))
    except json.JSONDecodeError as error:
        raise ValueError("Hasil kandidat dalil bukan JSON valid.") from error
    for reference in result.get("references", []):
        reference["status"] = "needs_verification"
    output = data_dir() / "references" / "candidates.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return output
