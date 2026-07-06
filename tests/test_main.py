"""Tests for __main__ — all calls to ydl_utils are mocked."""

from unittest import mock

import pytest

from youtube_extract import __main__ as ydl
from youtube_extract import ydl_utils


# =======================================================================
# Pure unit tests (no mocking needed)
# =======================================================================


class TestIsYoutubeChannel:
    def test_recognises_channel_urls(self):
        urls = [
            "https://www.youtube.com/channel/UCbYMTn6xKV0IKshL4pRCV3g/videos",
            "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA/videos",
            "https://www.youtube.com/channel/UCz4wfOcIw_OezAZTQ0SjiYA",
            "https://www.youtube.com/c/SomeChannel",
            "https://www.youtube.com/user/SomeUser",
            "https://www.youtube.com/@SomeHandle",
        ]
        for url in urls:
            assert ydl.is_youtube_channel(url), f"Expected {url} to be recognised"

    def test_rejects_non_channel_urls(self):
        urls = [
            "https://www.youtube.com",
            "https://www.youtubee.com",
            "https://www.youtubeee.com",
            "https://www.dbeley.ovh",
        ]
        for url in urls:
            assert not ydl.is_youtube_channel(url), f"Expected {url} to be rejected"


class TestGetFilename:
    def test_generates_filename_from_author(self):
        entries = [{"author": " Alex  Jimenez "}]
        # Only the first entry matters; spaces are replaced
        entries[0]["author"] = "Alex Jimenez"
        assert ydl.get_filename(entries) == "youtube_extract_Alex_Jimenez"

    def test_generates_filename_with_underscores(self):
        entries = [{"author": "Music Channel"}]
        assert ydl.get_filename(entries) == "youtube_extract_Music_Channel"

    def test_raises_on_empty_list(self):
        with pytest.raises(ValueError, match="list_dict cannot be empty"):
            ydl.get_filename([])


class TestCheckArgs:
    """Argument validation — purely local logic."""

    def test_valid_args(
        self,
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
    ):
        for args in [
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
        ]:
            ydl.check_args(args)

    def test_raises_on_unsupported_format(self, args_incorrect):
        with pytest.raises(ValueError, match="not supported as export format"):
            ydl.check_args(args_incorrect)

    def test_raises_on_missing_url(self, args_incorrect_2):
        with pytest.raises(ValueError, match="No url set"):
            ydl.check_args(args_incorrect_2)


# =======================================================================
# extract_entries_for_url — ydl_utils.ydl_get_entries is mocked
# =======================================================================


@pytest.fixture
def mock_ydl_get_entries():
    """Mock *ydl_utils.ydl_get_entries* to return empty by default.

    Individual tests override ``.return_value`` on the mock.
    """
    with mock.patch.object(ydl_utils, "ydl_get_entries") as m:
        m.return_value = []
        yield m


class TestExtractEntriesForUrl:
    """extract_entries_for_url orchestrates ydl_get_entries + field mapping."""

    # ------------------------------------------------------------------ #
    # Success cases
    # ------------------------------------------------------------------ #

    def test_maps_all_fields(self, mock_ydl_get_entries, sample_video):
        """Every field from a yt-dlp entry is mapped to the correct output key."""
        mock_ydl_get_entries.return_value = [sample_video]
        result = ydl.extract_entries_for_url("https://youtube.com/...")

        assert len(result) == 1
        entry = result[0]
        assert entry["author"] == "Alex Jimenez"
        assert entry["channel_url"] == "https://www.youtube.com/@alexjimenez"
        assert entry["title"] == "color red"
        assert entry["webpage_url"] == "https://www.youtube.com/watch?v=xyz789"
        assert entry["view_count"] == 5000
        assert entry["like_count"] == 200
        assert entry["duration"] == 17
        assert entry["upload_date"] == "20230115"
        assert entry["tags"] == ["art", "color"]
        assert entry["categories"] == ["Education"]
        assert entry["description"] == "A video about the color red"
        assert entry["thumbnail"] == "https://i.ytimg.com/vi/xyz789/default.jpg"

    def test_best_format_from_second_to_last(self, mock_ydl_get_entries, sample_video):
        """best_format / filesize_bytes come from formats[-2]."""
        mock_ydl_get_entries.return_value = [sample_video]
        result = ydl.extract_entries_for_url("https://youtube.com/...")

        entry = result[0]
        assert entry["best_format"] == "mp4 720p"
        assert entry["filesize_bytes"] == 207535

    def test_flat_mode_has_no_formats(self, mock_ydl_get_entries, sample_video_flat):
        """When extract_flat=True, best_format/filesize are empty strings."""
        mock_ydl_get_entries.return_value = [sample_video_flat]
        result = ydl.extract_entries_for_url(
            "https://youtube.com/...", extract_flat=True
        )

        entry = result[0]
        assert entry["best_format"] == ""
        assert entry["filesize_bytes"] == ""
        assert entry["title"] == "blue sky"

    def test_multiple_entries(self, mock_ydl_get_entries, sample_entries):
        """All entries are returned, preserving order."""
        mock_ydl_get_entries.return_value = sample_entries
        result = ydl.extract_entries_for_url("https://youtube.com/...")

        assert len(result) == 3
        assert result[0]["title"] == "color red"
        assert result[1]["title"] == "blue sky"
        assert result[2]["title"] == "video 3"

    def test_get_filename_integration(self, mock_ydl_get_entries, sample_entries):
        """get_filename works on the output of extract_entries_for_url."""
        mock_ydl_get_entries.return_value = sample_entries
        entries = ydl.extract_entries_for_url("https://youtube.com/...")
        assert ydl.get_filename(entries) == "youtube_extract_Alex_Jimenez"

    # ------------------------------------------------------------------ #
    # None / empty handling
    # ------------------------------------------------------------------ #

    def test_empty_when_ydl_returns_none(self, mock_ydl_get_entries):
        """ydl_get_entries returns None → empty list."""
        mock_ydl_get_entries.return_value = None
        result = ydl.extract_entries_for_url("https://youtube.com/...")
        assert result == []

    def test_empty_when_ydl_returns_empty_list(self, mock_ydl_get_entries):
        """ydl_get_entries returns [] → empty list."""
        mock_ydl_get_entries.return_value = []
        result = ydl.extract_entries_for_url("https://youtube.com/...")
        assert result == []

    def test_filters_none_entries(self, mock_ydl_get_entries, sample_video):
        """None entries from yt-dlp are filtered out."""
        mock_ydl_get_entries.return_value = [None, sample_video, None]
        result = ydl.extract_entries_for_url("https://youtube.com/...")
        assert len(result) == 1

    def test_empty_when_all_none(self, mock_ydl_get_entries):
        """All entries are None → empty list."""
        mock_ydl_get_entries.return_value = [None, None]
        result = ydl.extract_entries_for_url("https://youtube.com/...")
        assert result == []

    # ------------------------------------------------------------------ #
    # Playlist workaround
    # ------------------------------------------------------------------ #

    def test_playlist_workaround(self, mock_ydl_get_entries, sample_video):
        """When entries[0] has _type='playlist', the nested entries are used."""
        playlist_payload = [
            {
                "_type": "playlist",
                "entries": [
                    sample_video,
                    dict(sample_video, title="playlist video"),
                ],
            }
        ]
        mock_ydl_get_entries.return_value = playlist_payload
        result = ydl.extract_entries_for_url("https://youtube.com/...")
        assert len(result) == 2
        assert result[0]["title"] == "color red"
        assert result[1]["title"] == "playlist video"

    # ------------------------------------------------------------------ #
    # Missing / partial fields
    # ------------------------------------------------------------------ #

    def test_missing_fields_default_to_empty_string(
        self, mock_ydl_get_entries
    ):
        """Entries with missing optional fields get empty strings."""
        minimal_entry = {"uploader": "Test"}
        mock_ydl_get_entries.return_value = [minimal_entry]
        result = ydl.extract_entries_for_url("https://youtube.com/...")

        assert result[0]["author"] == "Test"
        assert result[0]["channel_url"] == ""
        assert result[0]["title"] == ""
        assert result[0]["view_count"] == ""
        assert result[0]["filesize_bytes"] == ""

    # ------------------------------------------------------------------ #
    # Parameter forwarding
    # ------------------------------------------------------------------ #

    def test_forwards_all_params(self, mock_ydl_get_entries):
        """All keyword arguments are forwarded to ydl_get_entries."""
        mock_ydl_get_entries.return_value = [{"uploader": "Test"}]

        ydl.extract_entries_for_url(
            "https://youtube.com/...",
            cookies_file="/cookies.txt",
            sleep_requests=1.5,
            cookies_from_browser="chrome",
            extract_flat=True,
            max_entries=10,
        )

        mock_ydl_get_entries.assert_called_once_with(
            "https://youtube.com/...",
            "/cookies.txt",
            1.5,
            "chrome",
            True,
            10,
        )
