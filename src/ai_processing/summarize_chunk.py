from src.ai_processing.gemini_client import (
    client,
    MODEL_NAME,
)


def summarize_chunk(text: str):

    prompt = f"""
    Anda adalah editor buku profesional.

    Ringkas isi kajian berikut.

    Buat:
    1. Tema utama
    2. Poin penting
    3. Ringkasan

    {text}
    """
    print("Mengirim ke Gemini...")
    
    response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
    )
    print("Respons diterima...")

    return response.text