import sys

import pytest

from youtube_extract import __main__ as ydl


# ---------------------------------------------------------------------------
# Shared mock data
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_video():
    """A single sample video dict as yt-dlp would return it (with formats)."""
    return {
        "uploader": "Alex Jimenez",
        "uploader_url": "https://www.youtube.com/@alexjimenez",
        "title": "color red",
        "webpage_url": "https://www.youtube.com/watch?v=xyz789",
        "view_count": 5000,
        "like_count": 200,
        "duration": 17,
        "upload_date": "20230115",
        "tags": ["art", "color"],
        "categories": ["Education"],
        "description": "A video about the color red",
        "thumbnail": "https://i.ytimg.com/vi/xyz789/default.jpg",
        "formats": [
            {"format": "audio only", "filesize": 50000},
            {"format": "mp4 720p", "filesize": 207535},
            {"format": "mp4 1080p", "filesize": 500000},
        ],
    }


@pytest.fixture
def sample_video_flat():
    """A sample video dict *without* formats (flat‑extraction mode)."""
    return {
        "uploader": "Alex Jimenez",
        "uploader_url": "https://www.youtube.com/@alexjimenez",
        "title": "blue sky",
        "webpage_url": "https://www.youtube.com/watch?v=abc123",
        "view_count": 3000,
        "like_count": 150,
        "duration": 42,
        "upload_date": "20230201",
        "tags": ["sky", "blue"],
        "categories": ["Science"],
        "description": "About the blue sky",
        "thumbnail": "https://i.ytimg.com/vi/abc123/default.jpg",
    }


@pytest.fixture
def sample_entries(sample_video, sample_video_flat):
    """List of entries returned by a successful extraction."""
    return [sample_video, sample_video_flat, dict(sample_video, title="video 3")]


# ---------------------------------------------------------------------------
# CLI-argument fixtures (purely local, no network)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def args_simple():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", url]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_with_cookies():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", url, "--cookies", "cookies.txt"]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_with_sleep():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", url, "--sleep-requests", "0.5"]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_complex():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", url, "-e", "xlsx"]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_complex_2():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", url, "-e", "csv"]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_complex_3():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", "--export_format", "xlsx", url]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_complex_4():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", "--export_format", "csv", url]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_complex_with_cookies():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", "--export_format", "xlsx", url, "--cookies", "cookies.txt"]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_complex_with_sleep():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", "--export_format", "xlsx", url, "--sleep-requests", "0.5"]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_complex_with_all():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = [
        "youtube_extract",
        "--export_format",
        "xlsx",
        url,
        "--cookies",
        "cookies.txt",
        "--sleep-requests",
        "10",
    ]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_incorrect():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", "--export_format", "mp4", url]
    args = ydl.parse_args()
    return args


@pytest.fixture(scope="session")
def args_incorrect_2():
    sys.argv = ["youtube_extract", "--export_format", "xlsx"]
    args = ydl.parse_args()
    return args
