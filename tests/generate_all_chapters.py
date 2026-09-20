from src.ai_processing.write_chapter import (
    write_chapter,
)

chapters = [
    (
        1,
        "Pengakuan Tanpa Pengabdian",
        """
        Membedah perbedaan
        Rububiyah dan Uluhiyah,
        pengakuan kaum Quraisy
        terhadap Allah serta
        alasan mereka tetap
        dianggap musyrik.
        """
    ),
    (
        2,
        "Mitos Perantara dan Syafaat",
        """
        Membahas konsep
        perantara, syafaat,
        serta akar kesyirikan
        dalam sejarah manusia.
        """
    ),
    (
        3,
        "Spektrum Objek Sembahan",
        """
        Membahas berbagai
        objek kesyirikan,
        mulai dari patung,
        pohon, orang saleh,
        hingga malaikat.
        """
    ),
    (
        4,
        "Potret Ironi Kesyirikan Modern",
        """
        Membandingkan
        kesyirikan masa lalu
        dan kesyirikan yang
        muncul pada zaman modern.
        """
    ),
]

for nomor, judul, isi in chapters:
    write_chapter(
        chapter_title=judul,
        chapter_summary=isi,
        chapter_number=nomor,
    )