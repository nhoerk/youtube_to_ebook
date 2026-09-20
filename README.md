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
   Atau gunakan CLI:
   ```bash
   python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
   python main.py --url "..." --config config.json
   python main.py --url "..." --status
   python main.py --url "..." --restart
   ```

   Salin `config.example.json` menjadi `config.json` untuk mengatur judul,
   penulis, bahasa transcript, ukuran chunk, dan model Gemini.

## Environment variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODELS=gemini-2.5-pro,gemini-2.5-flash-lite
```

Jika model utama terkena quota atau rate limit, pipeline otomatis mencoba model
di `GEMINI_FALLBACK_MODELS` secara berurutan. Model fallback harus tersedia pada
akun/API key yang digunakan.

## Catatan

- Proyek masih menggunakan pipeline berbasis file dan hardcode pada tahap tertentu.
- Status setiap tahap disimpan di `data/jobs/<video_id>.json`. Tahap yang sudah sukses
  akan dilewati saat pipeline dijalankan kembali, sedangkan tahap yang gagal dapat
  dicoba ulang.
- Setiap video memakai workspace terpisah di `data/<video_id>/` dan output terpisah
  di `output/<video_id>/`, sehingga URL baru menghasilkan ebook baru tanpa menimpa
  hasil URL lain.
- Log pipeline disimpan di `logs/<video_id>.log`. Perubahan konfigurasi akan
  menginvalidasi tahap lama agar hasil tidak tercampur dengan konfigurasi baru.
- Outline disimpan sebagai `data/<video_id>/book_outline/book_outline.json`.
  Jumlah, judul, dan ringkasan chapter dibuat dari transcript video, lalu
  digunakan oleh generator chapter dan daftar isi.
- Kandidat perbaikan bahasa disimpan di `data/<video_id>/editorial/review.json`,
  sedangkan kandidat dalil disimpan di `data/<video_id>/references/candidates.json`.
  Kandidat dalil selalu berstatus `needs_verification` dan bukan verifikasi final.
- `--dry-run`, `--clean`, dan `--status-json` tersedia untuk pemeriksaan,
  pembersihan, dan integrasi dengan UI/otomasi.
- Untuk penggunaan yang lebih umum, perlu dibuat konfigurasi buku dan CLI argument agar judul, bab, dan output tidak tertanam di kode.