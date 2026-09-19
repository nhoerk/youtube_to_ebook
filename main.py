from src.youtube.download_transcript import (
    download_transcript,
)

from src.transcript.clean_transcript import (
    clean_transcript,
)

from src.transcript.chunk_transcript import (
    chunk_transcript,
)

def main():

    url = input(
        "Masukkan URL YouTube: "
    )

    raw_file = download_transcript(url)

    clean_file = clean_transcript(raw_file)

    chunk_files = chunk_transcript(clean_file)

    print(chunk_files)

if __name__ == "__main__":
    main()