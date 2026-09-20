import pytest

from src.youtube.extract_video_id import extract_video_id


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ?feature=share", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ?start=10", "dQw4w9WgXcQ"),
    ],
)
def test_extract_video_id_valid_urls(url, expected):
    assert extract_video_id(url) == expected


@pytest.mark.parametrize(
    "url",
    [
        "",
        "https://example.com",
        "https://www.youtube.com/watch",
    ],
)
def test_extract_video_id_invalid_urls(url):
    with pytest.raises(ValueError):
        extract_video_id(url)
