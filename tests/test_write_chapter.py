from src.ai_processing.write_chapter import (
    write_chapter,
)

file = write_chapter(
    chapter_title=
    "Pengakuan Tanpa Pengabdian",

    chapter_summary=
    """
    Membahas perbedaan
    Rububiyah dan Uluhiyah,
    pengakuan kaum Quraisy
    terhadap Allah,
    serta mengapa mereka
    tetap dianggap musyrik.
    """,

    chapter_number=1,
)

print(file)