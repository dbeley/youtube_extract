from youtube_extract import ydl_utils
from youtube_extract import __main__ as ydl
import pytest
import sys


@pytest.fixture(scope="session")
def url():
    url = "https://www.youtube.com/channel/UCbYMTn6xKV0IKshL4pRCV3g/videos"
    return url


@pytest.fixture(scope="session")
def cookies_file():
    # Return None or a path to a test cookies file if you have one
    return None


@pytest.fixture(scope="session")
def sleep_requests():
    # Return None or a time interval for testing
    return None


@pytest.fixture(scope="session")
def raw_entries(url, cookies_file, sleep_requests):
    entries = ydl_utils.ydl_get_entries(url, cookies_file, sleep_requests)
    return entries


@pytest.fixture(scope="session")
def entries(url, cookies_file, sleep_requests):
    entries = ydl.extract_entries_for_url(url, cookies_file, sleep_requests)
    return entries


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
    sys.argv = ["youtube_extract", "--export_format", "xlsx", url, "--cookies", "cookies.txt", "--sleep-requests", "10"]
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
