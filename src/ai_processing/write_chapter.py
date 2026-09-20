from pathlib import Path
from src.core.paths import data_dir

from src.ai_processing.gemini_client import (
    client,
    MODEL_NAME,
)


def write_chapter(
    chapter_title: str,
    chapter_summary: str,
    chapter_number: int,
):
    prompt = f"""
Anda adalah editor buku Islam profesional.

Tugas Anda adalah mengubah materi kajian menjadi format buku.

Judul Bab:
{chapter_title}

Materi:
{chapter_summary}

ATURAN PENULISAN:

1. Prioritaskan isi kajian yang diberikan.
2. Jangan menambahkan konsep baru yang tidak terdapat dalam materi.
3. Jangan menambahkan dalil, cerita, atau pendapat ulama baru.
4. Boleh memperjelas istilah yang sudah disebutkan.
5. Boleh memperluas penjelasan yang sudah ada.
6. Boleh menyusun ulang urutan pembahasan agar lebih sistematis.
7. Boleh membuat subbab agar nyaman dibaca.
8. Jika memberikan elaborasi tambahan dari AI, tandai dengan:

### Penjelasan Tambahan

9. Target komposisi:
   - 80% materi kajian
   - 20% elaborasi AI

10. Gunakan gaya bahasa buku yang formal dan mudah dipahami.
11. Kembangkan setiap poin menjadi uraian yang lebih mendalam.
12. Setiap subbab minimal 500 kata.
13. Jangan menambahkan tema baru di luar materi.
14. Tambahkan bagian "Refleksi Pembaca" di akhir bab.
15. Tambahkan bagian "Pelajaran Penting" sebelum kesimpulan.
16. Jika informasi tidak terdapat pada outline atau summary kajian,jangan ditulis.
17. Lebih baik singkat daripada menambahkan materi baru.

Hasilkan dalam format Markdown.
"""

    print(
        f"Menulis Bab {chapter_number}..."
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    output_dir = data_dir() / "ebook_content"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir /
        f"bab_{chapter_number:02d}.md"
    )

    output_file.write_text(
        response.text,
        encoding="utf-8",
    )

    print(
        f"Tersimpan: {output_file}"
    )

    return output_file