from pathlib import Path

from src.core.job_manager import (
    load_job,
    save_job,
)

from src.youtube.download_transcript import (
    download_transcript,
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
        "data/transcript_chunks"
    )

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


def main():

    print("=" * 50)
    print("YOUTUBE TO EBOOK")
    print("=" * 50)

    url = input("Masukkan URL YouTube: ").strip()

    if "v=" not in url:
        raise ValueError("URL YouTube tidak valid.")

    video_id = url.split("v=")[1].split("&")[0]

    job = load_job(video_id)
    job["youtube_url"] = url
    job["video_id"] = video_id
    save_job(job)

    raw_file = None
    clean_file = None

    print("\n[1/11] Download transcript")
    if not job.get("downloaded"):
        raw_file = download_transcript(url)
        job["downloaded"] = True
        save_job(job)
    else:
        print("Download transcript dilewati")

    print("\n[2/11] Clean transcript")
    if not job.get("cleaned"):
        if raw_file is None:
            raw_file = download_transcript(url)
        clean_file = clean_transcript(raw_file)
        job["cleaned"] = True
        save_job(job)
    else:
        print("Clean transcript dilewati")

    print("\n[3/11] Chunk transcript")
    if not job.get("chunked"):
        if clean_file is None:
            if raw_file is None:
                raw_file = download_transcript(url)
            clean_file = clean_transcript(raw_file)
        chunk_transcript(clean_file)
        job["chunked"] = True
        save_job(job)
    else:
        print("Chunk dilewati")

    print("\n[4/11] Generate summaries")
    if not job.get("summarized"):
        generate_all_summaries()
        job["summarized"] = True
        save_job(job)
    else:
        print("Summary dilewati")

    print("\n[5/11] Generate outline")
    if not job.get("outline"):
        create_book_outline()
        job["outline"] = True
        save_job(job)
    else:
        print("Outline dilewati")

    print("\n[6/11] Generate preface")
    create_preface()

    print("\n[7/11] Generate TOC")
    create_toc()

    print("\n[8/11] Generate chapters")
    generate_chapters()

    print("\n[9/11] Build manuscript")
    build_manuscript()

    print("\n[10/11] Generate DOCX")
    generate_docx()

    print("\n[11/11] Generate PDF")
    generate_pdf()

    print("\nSELESAI")
    print("Cek folder output/")


if __name__ == "__main__":
    main()