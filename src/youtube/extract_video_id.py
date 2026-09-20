from urllib.parse import parse_qs, urlparse


def extract_video_id(url: str) -> str:
    if not isinstance(url, str):
        raise ValueError("URL YouTube tidak valid")

    candidate = url.strip()
    if not candidate:
        raise ValueError("URL YouTube tidak valid")

    parsed = urlparse(candidate)
    hostname = (parsed.hostname or "").lower()

    if hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
        if video_id:
            return video_id
        raise ValueError("URL YouTube tidak valid")

    if hostname in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "www.music.youtube.com",
        "youtube-nocookie.com",
        "www.youtube-nocookie.com",
    }:
        path = parsed.path.strip("/")
        if path.startswith("shorts/"):
            video_id = path.split("shorts/")[1].split("/")[0]
            if video_id:
                return video_id
        elif path.startswith("embed/"):
            video_id = path.split("embed/")[1].split("/")[0]
            if video_id:
                return video_id
        elif path.startswith("live/"):
            video_id = path.split("live/")[1].split("/")[0]
            if video_id:
                return video_id
        elif path.startswith("v/"):
            video_id = path.split("v/")[1].split("/")[0]
            if video_id:
                return video_id

        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            return video_id

    if parsed.scheme == "":
        maybe_url = "https://" + candidate
        return extract_video_id(maybe_url)

    raise ValueError("URL YouTube tidak valid")