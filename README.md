# Youtube To Ebook

Pipeline otomatis untuk mengubah kajian YouTube menjadi ebook.

## Alur

1. Ambil transcript YouTube
2. Simpan transcript mentah
3. Bersihkan transcript
4. Ringkas menggunakan AI
5. Susun bab buku
6. Perbaiki tata bahasa
7. Generate DOCX
8. Generate PDF

## Struktur

YouTube → Transcript → Summary → Chapter → Ebook

## Setup

1. Buat environment virtual dan aktifkan.
2. Install dependency:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Salin file `.env.example` menjadi `.env` dan isi nilai API key Gemini.
4. Jalankan:
   ```bash
   python main.py
   ```

## Environment variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Catatan

- Proyek masih menggunakan pipeline berbasis file dan hardcode pada tahap tertentu.
- Status setiap tahap disimpan di `data/jobs/<video_id>.json`. Tahap yang sudah sukses
  akan dilewati saat pipeline dijalankan kembali, sedangkan tahap yang gagal dapat
  dicoba ulang.
- Setiap video memakai workspace terpisah di `data/<video_id>/` dan output terpisah
  di `output/<video_id>/`, sehingga URL baru menghasilkan ebook baru tanpa menimpa
  hasil URL lain.
- Untuk penggunaan yang lebih umum, perlu dibuat konfigurasi buku dan CLI argument agar judul, bab, dan output tidak tertanam di kode.