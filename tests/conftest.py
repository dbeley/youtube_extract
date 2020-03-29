from youtube_extract import ydl_utils
from youtube_extract import __main__ as ydl
import pytest
import sys


@pytest.fixture(scope="session")
def url():
    url = "https://www.youtube.com/channel/UCbYMTn6xKV0IKshL4pRCV3g/videos"
    return url


@pytest.fixture(scope="session")
def raw_entries(url):
    entries = ydl_utils.ydl_get_entries(url)
    return entries


@pytest.fixture(scope="session")
def entries(url):
    entries = ydl.extract_entries_for_url(url)
    return entries


@pytest.fixture(scope="session")
def args_simple():
    url = "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos"
    sys.argv = ["youtube_extract", url]
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
