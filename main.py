import os
from pathlib import Path

from src.core.job_manager import (
    complete_stage,
    fail_stage,
    is_stage_complete,
    load_job,
    save_job,
    start_stage,
)

from src.youtube.download_transcript import (
    download_transcript,
)

from src.youtube.extract_video_id import (
    extract_video_id,
)

from src.transcript.clean_transcript import (
    clean_transcript,
)

from src.transcript.chunk_transcript import (
    chunk_transcript,
)

from src.ai_processing.save_summary import (
    process_chunk,
)

from src.ai_processing.create_book_outline import (
    create_book_outline,
)

from src.ebook.create_preface import (
    create_preface,
)

from src.ebook.create_toc import (
    create_toc,
)

from src.ai_processing.write_chapter import (
    write_chapter,
)

from src.ebook.build_manuscript import (
    build_manuscript,
)

from src.ebook.generate_docx_book import (
    generate_docx,
)

from src.ebook.generate_pdf_book import (
    generate_pdf,
)



def generate_all_summaries():

    chunk_dir = Path(
        os.getenv("YOUTUBE_TO_EBOOK_DATA_DIR", "data")
    ) / "transcript_chunks"

    for file in sorted(
        chunk_dir.glob("*.txt")
    ):

        print(
            f"Summary: {file.name}"
        )

        process_chunk(file)


def generate_chapters():

    chapters = [
        (
            1,
            "Pengakuan Tanpa Pengabdian",
            """
            Membahas perbedaan tauhid
            Rububiyah dan Uluhiyah,
            pengakuan kaum Quraisy
            terhadap Allah,
            dan sebab mereka tetap
            dianggap musyrik.
            """
        ),
        (
            2,
            "Mitos Perantara dan Syafaat",
            """
            Membahas konsep
            perantara, syafaat,
            dan akar kesyirikan
            dalam sejarah manusia.
            """
        ),
        (
            3,
            "Spektrum Objek Sembahan",
            """
            Membahas berbagai
            objek penyembahan
            selain Allah,
            baik patung, pohon,
            orang saleh maupun malaikat.
            """
        ),
        (
            4,
            "Potret Ironi Kesyirikan Modern",
            """
            Membahas perbandingan
            kesyirikan masa lalu
            dan penyimpangan yang
            muncul pada masa kini.
            """
        ),
    ]

    for nomor, judul, isi in chapters:

        write_chapter(
            chapter_title=judul,
            chapter_summary=isi,
            chapter_number=nomor,
        )


def run_stage(job, name, action):
    if is_stage_complete(job, name):
        print(f"{name.capitalize()} dilewati")
        return job["stages"].get(name, {}).get("result")

    start_stage(job, name)
    try:
        result = action()
    except Exception as error:
        fail_stage(job, name, error)
        print(f"{name.capitalize()} gagal: {error}")
        raise

    complete_stage(job, name, result)
    return result


def main():

    print("=" * 50)
    print("YOUTUBE TO EBOOK")
    print("=" * 50)

    url = input("Masukkan URL YouTube: ").strip()

    video_id = extract_video_id(url)

    job = load_job(video_id)
    job["youtube_url"] = url
    job["video_id"] = video_id
    save_job(job)
    os.environ["YOUTUBE_TO_EBOOK_DATA_DIR"] = str(
        Path("data") / video_id
    )
    os.environ["YOUTUBE_TO_EBOOK_OUTPUT_DIR"] = str(
        Path("output") / video_id
    )

    print("\n[1/11] Download transcript")
    raw_file = run_stage(
        job,
        "downloaded",
        lambda: download_transcript(url),
    )
    raw_file = Path(raw_file) if raw_file else Path(
        os.environ["YOUTUBE_TO_EBOOK_DATA_DIR"]
    ) / "transcript_raw" / f"{video_id}.txt"

    print("\n[2/11] Clean transcript")
    clean_file = run_stage(
        job,
        "cleaned",
        lambda: clean_transcript(raw_file),
    )
    clean_file = Path(clean_file) if clean_file else Path(
        os.environ["YOUTUBE_TO_EBOOK_DATA_DIR"]
    ) / "transcript_clean" / f"{raw_file.stem}_clean.txt"

    print("\n[3/11] Chunk transcript")
    run_stage(
        job,
        "chunked",
        lambda: chunk_transcript(clean_file),
    )

    print("\n[4/11] Generate summaries")
    run_stage(job, "summarized", generate_all_summaries)

    print("\n[5/11] Generate outline")
    run_stage(job, "outline", create_book_outline)

    print("\n[6/11] Generate preface")
    run_stage(job, "preface", create_preface)

    print("\n[7/11] Generate TOC")
    run_stage(job, "toc", create_toc)

    print("\n[8/11] Generate chapters")
    run_stage(job, "chapters", generate_chapters)

    print("\n[9/11] Build manuscript")
    run_stage(job, "manuscript", build_manuscript)

    print("\n[10/11] Generate DOCX")
    run_stage(job, "docx", generate_docx)

    print("\n[11/11] Generate PDF")
    run_stage(job, "pdf", generate_pdf)

    job["status"] = "completed"
    save_job(job)
    print("\nSELESAI")
    print("Cek folder output/")


if __name__ == "__main__":
    main()