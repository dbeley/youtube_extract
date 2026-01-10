import pytest

from youtube_extract import __main__ as ydl


def test_is_youtube_channel():
    urls_correct = [
        "https://www.youtube.com/channel/UCbYMTn6xKV0IKshL4pRCV3g/videos",
        "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos",
        "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA",
    ]

    urls_incorrect = [
        "https://www.youtube.com",
        "https://www.youtubee.com",
        "https://www.youtubeee.com",
        "https://www.dbeley.ovh",
    ]

    for url in urls_correct:
        assert ydl.is_youtube_channel(url), f"Expected {url} to be recognized as YouTube channel"

    for url in urls_incorrect:
        assert not ydl.is_youtube_channel(
            url
        ), f"Expected {url} to NOT be recognized as YouTube channel"


def test_get_filename(entries):
    assert ydl.get_filename(entries) == "youtube_extract_Alex_Jimenez"


def test_check_args(
    args_simple,
    args_complex,
    args_complex_2,
    args_complex_3,
    args_complex_4,
    args_with_cookies,
    args_with_sleep,
    args_complex_with_cookies,
    args_complex_with_sleep,
    args_complex_with_all,
    args_incorrect,
    args_incorrect_2,
):
    ydl.check_args(args_simple)
    ydl.check_args(args_complex)
    ydl.check_args(args_complex_2)
    ydl.check_args(args_complex_3)
    ydl.check_args(args_complex_4)
    ydl.check_args(args_with_cookies)
    ydl.check_args(args_with_sleep)
    ydl.check_args(args_complex_with_cookies)
    ydl.check_args(args_complex_with_sleep)
    ydl.check_args(args_complex_with_all)
    with pytest.raises(ValueError):
        ydl.check_args(args_incorrect)
    with pytest.raises(ValueError):
        ydl.check_args(args_incorrect_2)


def test_extract_entries_for_url(url, entries, cookies_file, sleep_requests):
    extracted_entries = ydl.extract_entries_for_url(url, cookies_file, sleep_requests)
    print(entries)
    print(extracted_entries)

    print(len(entries))
    print(len(extracted_entries))
    assert len(extracted_entries) == 3, f"Expected 3 entries, got {len(extracted_entries)}"

    last_entry = extracted_entries[-1]
    assert last_entry["author"] == "Alex Jimenez"
    assert last_entry["title"] == "color red"
    assert last_entry["duration"] == 17
    assert last_entry["filesize_bytes"] == 207535


def test_extract_entries_with_cookies(url, cookies_file, sleep_requests):
    if cookies_file:  # Only run this test if a cookies file is provided
        entries_with_cookies = ydl.extract_entries_for_url(url, cookies_file, sleep_requests)
        # Add assertions specific to authenticated content if needed
        assert entries_with_cookies is not None


def test_extract_entries_with_sleep(url, cookies_file):
    # Test with a small sleep interval for verification
    test_sleep = 0.1
    entries_with_sleep = ydl.extract_entries_for_url(url, cookies_file, test_sleep)
    # No specific assertions needed - just verifying it runs without errors
    assert entries_with_sleep is not None
