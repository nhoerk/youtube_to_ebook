from urllib.parse import parse_qs, urlparse


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname == "youtu.be":
        return parsed.path[1:]

    if parsed.hostname in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
    ):
        return parse_qs(parsed.query)["v"][0]

    raise ValueError("URL YouTube tidak valid")