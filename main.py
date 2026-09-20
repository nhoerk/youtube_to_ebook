import os
import argparse
import json
import logging
from pathlib import Path

from src.core.config import load_config
from src.core.paths import log_dir
from src.core.job_manager import (
    complete_stage,
    fail_stage,
    is_stage_complete,
    invalidate_stages,
    load_job,
    reset_job,
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


def generate_chapters(outline_file=None):
    outline_path = Path(outline_file) if outline_file else (
        Path(os.getenv("YOUTUBE_TO_EBOOK_DATA_DIR", "data"))
        / "book_outline"
        / "book_outline.json"
    )
    outline = json.loads(outline_path.read_text(encoding="utf-8"))
    for chapter in outline["chapters"]:
        write_chapter(
            chapter_title=chapter["title"],
            chapter_summary=chapter["summary"],
            chapter_number=chapter["number"],
        )


def run_stage(job, name, action):
    if is_stage_complete(job, name):
        print(f"{name.capitalize()} dilewati")
        return job["stages"].get(name, {}).get("result")

    logging.info("Starting stage: %s", name)
    start_stage(job, name)
    try:
        result = action()
    except Exception as error:
        fail_stage(job, name, error)
        logging.exception("Stage failed: %s", name)
        print(f"{name.capitalize()} gagal: {error}")
        raise

    complete_stage(job, name, result)
    logging.info("Completed stage: %s", name)
    return result


def parse_args():
    parser = argparse.ArgumentParser(description="Generate an ebook from a YouTube video.")
    parser.add_argument("--url", help="YouTube URL. If omitted, prompt interactively.")
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--resume", action="store_true", help="Resume the existing job.")
    parser.add_argument("--restart", action="store_true", help="Restart this video's job.")
    parser.add_argument("--status", action="store_true", help="Show job status and exit.")
    return parser.parse_args()


def configure_logging(video_id):
    directory = log_dir()
    directory.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=directory / f"{video_id}.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def validate_outputs():
    output = Path(os.environ["YOUTUBE_TO_EBOOK_OUTPUT_DIR"])
    expected = [output / "manuscript.md", *output.glob("*.docx"), *output.glob("*.pdf")]
    missing = [path for path in expected[:1] if not path.exists() or path.stat().st_size == 0]
    if not list(output.glob("*.docx")) or not list(output.glob("*.pdf")):
        missing.append(output)
    if missing:
        raise RuntimeError(f"Output ebook tidak lengkap: {', '.join(map(str, missing))}")


def main():
    args = parse_args()

    print("=" * 50)
    print("YOUTUBE TO EBOOK")
    print("=" * 50)

    url = (args.url or input("Masukkan URL YouTube: ")).strip()

    video_id = extract_video_id(url)
    configure_logging(video_id)
    config = load_config(args.config)
    os.environ["YOUTUBE_TO_EBOOK_DATA_DIR"] = str(args.data / video_id)
    os.environ["YOUTUBE_TO_EBOOK_OUTPUT_DIR"] = str(args.output / video_id)
    os.environ["YOUTUBE_TO_EBOOK_BOOK_TITLE"] = config.book_title
    if config.gemini_model:
        os.environ["GEMINI_MODEL"] = config.gemini_model

    job = load_job(video_id)
    if args.restart:
        reset_job(video_id)
        job = load_job(video_id)
    elif job.get("config_fingerprint") != config.fingerprint():
        invalidate_stages(job)
    job["config_fingerprint"] = config.fingerprint()
    job["youtube_url"] = url
    job["video_id"] = video_id
    save_job(job)

    if args.status:
        print(f"Job: {video_id}")
        print(f"Status: {job['status']}")
        for name, state in job.get("stages", {}).items():
            print(f"- {name}: {state.get('status')}")
        return

    print("\n[1/11] Download transcript")
    raw_file = run_stage(
        job,
        "downloaded",
        lambda: download_transcript(url, config.languages),
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
        lambda: chunk_transcript(clean_file, config.chunk_size),
    )

    print("\n[4/11] Generate summaries")
    run_stage(job, "summarized", generate_all_summaries)

    print("\n[5/11] Generate outline")
    outline_file = run_stage(job, "outline", create_book_outline)
    outline_file = Path(outline_file) if outline_file else (
        Path(os.environ["YOUTUBE_TO_EBOOK_DATA_DIR"])
        / "book_outline"
        / "book_outline.json"
    )

    print("\n[6/11] Generate preface")
    run_stage(job, "preface", create_preface)

    print("\n[7/11] Generate TOC")
    run_stage(job, "toc", create_toc)

    print("\n[8/11] Generate chapters")
    run_stage(job, "chapters", lambda: generate_chapters(outline_file))

    print("\n[9/11] Build manuscript")
    run_stage(job, "manuscript", build_manuscript)

    print("\n[10/11] Generate DOCX")
    run_stage(job, "docx", generate_docx)

    print("\n[11/11] Generate PDF")
    run_stage(job, "pdf", generate_pdf)
    validate_outputs()

    job["status"] = "completed"
    save_job(job)
    print("\nSELESAI")
    print("Cek folder output/")


if __name__ == "__main__":
    main()