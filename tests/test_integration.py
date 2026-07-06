"""Integration tests — make real YouTube network calls.

These tests require live YouTube access.  They are **not** run by default in
CI (``-m "not integration"``).  Run them locally with::

    pytest -m integration
"""

import pytest

from youtube_extract import __main__ as ydl
from youtube_extract import ydl_utils

pytestmark = pytest.mark.integration


@pytest.fixture(scope="session")
def url():
    return "https://www.youtube.com/channel/UCbYMTn6xKV0IKshL4pRCV3g/videos"


@pytest.fixture(scope="session")
def cookies_file():
    return None


@pytest.fixture(scope="session")
def sleep_requests():
    return None


@pytest.fixture(scope="session")
def raw_entries(url, cookies_file, sleep_requests):
    entries = ydl_utils.ydl_get_entries(url, cookies_file, sleep_requests)
    if not entries:
        pytest.skip("YouTube extraction returned no entries (network blocked or missing cookies)")
    return entries


@pytest.fixture(scope="session")
def entries(url, cookies_file, sleep_requests):
    entries = ydl.extract_entries_for_url(url, cookies_file, sleep_requests)
    if not entries:
        pytest.skip("YouTube extraction returned no entries (network blocked or missing cookies)")
    return entries


class TestYdlGetEntriesIntegration:
    def test_ydl_get_entries(self, entries):
        assert entries, "Expected entries to be non-empty"
        assert len(entries) == 3, f"Expected 3 entries, got {len(entries)}"

    def test_ydl_get_entries_with_cookies(self, cookies_file, sleep_requests, raw_entries):
        assert raw_entries, "Expected raw_entries to be non-empty"

    def test_ydl_get_entries_with_sleep(self, url, cookies_file):
        test_sleep = 10
        entries = ydl_utils.ydl_get_entries(url, cookies_file, test_sleep)
        assert entries is not None


class TestMainIntegration:
    def test_get_filename(self, entries):
        assert ydl.get_filename(entries) == "youtube_extract_Alex_Jimenez"

    def test_extract_entries_for_url(self, url, entries, cookies_file, sleep_requests):
        extracted_entries = ydl.extract_entries_for_url(url, cookies_file, sleep_requests)
        assert len(extracted_entries) == 3, f"Expected 3 entries, got {len(extracted_entries)}"

        last_entry = extracted_entries[-1]
        assert last_entry["author"] == "Alex Jimenez"
        assert last_entry["title"] == "color red"
        assert last_entry["duration"] == 17
        assert last_entry["filesize_bytes"] == 207535

    def test_extract_entries_with_cookies(self, url, cookies_file, sleep_requests):
        if cookies_file:  # Only run if a cookies file is provided
            entries_with_cookies = ydl.extract_entries_for_url(url, cookies_file, sleep_requests)
            assert entries_with_cookies is not None

    def test_extract_entries_with_sleep(self, url, cookies_file):
        test_sleep = 0.1
        entries_with_sleep = ydl.extract_entries_for_url(url, cookies_file, test_sleep)
        assert entries_with_sleep is not None
