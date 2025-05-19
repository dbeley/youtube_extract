def test_ydl_get_entries(entries):
    if not entries:
        raise AssertionError()

    if len(entries) != 3:
        raise AssertionError()


def test_ydl_get_entries_with_cookies(cookies_file, sleep_requests, raw_entries):
    if not raw_entries:
        raise AssertionError()


def test_ydl_get_entries_with_sleep(url, cookies_file):
    from youtube_extract import ydl_utils
    test_sleep = 10
    entries = ydl_utils.ydl_get_entries(url, cookies_file, test_sleep)
    assert entries is not None