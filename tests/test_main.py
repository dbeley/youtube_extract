from youtube_extract import __main__ as ydl
import pytest


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
        if not ydl.is_youtube_channel(url):
            raise AssertionError()

    for url in urls_incorrect:
        if ydl.is_youtube_channel(url):
            raise AssertionError()


def test_get_filename(entries):
    if not ydl.get_filename(entries) == "youtube_extract_Alex_Jimenez":
        raise AssertionError()


def test_check_args(
    args_simple,
    args_complex,
    args_complex_2,
    args_complex_3,
    args_complex_4,
    args_incorrect,
    args_incorrect_2,
):
    ydl.check_args(args_simple)
    ydl.check_args(args_complex)
    ydl.check_args(args_complex_2)
    ydl.check_args(args_complex_3)
    ydl.check_args(args_complex_4)
    with pytest.raises(Exception):
        ydl.check_args(args_incorrect)
    with pytest.raises(Exception):
        ydl.check_args(args_incorrect_2)


def test_extract_entries_for_url(url, entries):
    extracted_entries = ydl.extract_entries_for_url(url)
    print(entries)
    print(extracted_entries)
    if not extracted_entries == entries:
        raise AssertionError()

    print(len(extracted_entries))
    if len(extracted_entries) != 2:
        raise AssertionError()

    if extracted_entries[-1]["author"] != "Alex Jimenez":
        raise AssertionError()
    if extracted_entries[-1]["title"] != "color red":
        raise AssertionError()
    if extracted_entries[-1]["duration"] != 17:
        raise AssertionError()
    if extracted_entries[-1]["filesize_bytes"] != 150217:
        raise AssertionError()
