from src.ai_processing.gemini_utils import generate_with_fallback


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
    
    response = generate_with_fallback(prompt)
    print("Respons diterima...")

    return response.text
import os
