def test_ydl_get_entries(entries):
    assert entries, "Expected entries to be non-empty"
    assert len(entries) == 3, f"Expected 3 entries, got {len(entries)}"


def test_ydl_get_entries_with_cookies(cookies_file, sleep_requests, raw_entries):
    assert raw_entries, "Expected raw_entries to be non-empty"


def test_ydl_get_entries_with_sleep(url, cookies_file):
    from youtube_extract import ydl_utils

    test_sleep = 10
    entries = ydl_utils.ydl_get_entries(url, cookies_file, test_sleep)
    assert entries is not None
