from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

from src.core.paths import data_dir
from src.youtube.extract_video_id import extract_video_id


def download_transcript(youtube_url: str, languages=("id", "en")) -> Path:

    video_id = extract_video_id(youtube_url)

    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(
        video_id,
        languages=list(languages)
    )

    text = "\n".join(
        snippet.text
        for snippet in transcript
    )

    output_dir = data_dir() / "transcript_raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{video_id}.txt"

    output_file.write_text(
        text,
        encoding="utf-8"
    )

    return output_file