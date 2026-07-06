"""Tests for ydl_utils — all network calls to yt-dlp are mocked."""

from unittest import mock

import pytest

from youtube_extract import ydl_utils


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_ydl(info_dict):
    """Return a patcher for ``yt_dlp.YoutubeDL`` that yields *info_dict*."""
    patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
    mock_ydl_cls = patcher.start()
    mock_instance = mock_ydl_cls.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = info_dict
    return patcher


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestYdlGetEntries:
    """ydl_get_entries is a thin wrapper around yt-dlp."""

    def test_returns_entries(self):
        """Happy path: yt-dlp returns entries, we pass them through."""
        info = {"entries": [{"id": "v1"}, {"id": "v2"}]}
        patcher = _mock_ydl(info)
        try:
            result = ydl_utils.ydl_get_entries("https://youtube.com/...")
            assert result == [{"id": "v1"}, {"id": "v2"}]
        finally:
            patcher.stop()

    def test_filters_none_entries(self):
        """Entries that are None (yt-dlp error per video) are removed."""
        info = {"entries": [{"id": "v1"}, None, {"id": "v2"}, None]}
        patcher = _mock_ydl(info)
        try:
            result = ydl_utils.ydl_get_entries("https://youtube.com/...")
            assert result == [{"id": "v1"}, {"id": "v2"}]
        finally:
            patcher.stop()

    def test_returns_none_on_exception(self):
        """Network error → exception caught → returns None."""
        patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
        mock_ydl_cls = patcher.start()
        mock_instance = mock_ydl_cls.return_value.__enter__.return_value
        mock_instance.extract_info.side_effect = Exception("Connection error")
        try:
            result = ydl_utils.ydl_get_entries("https://youtube.com/...")
            assert result is None
        finally:
            patcher.stop()

    def test_forwards_cookies_file(self):
        """cookies_file → cookiefile in ydl_opts."""
        patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
        mock_ydl_cls = patcher.start()
        mock_instance = mock_ydl_cls.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"entries": [{"id": "v1"}]}
        try:
            ydl_utils.ydl_get_entries("url", cookies_file="/tmp/cookies.txt")
            _opts = mock_ydl_cls.call_args[0][0]
            assert _opts.get("cookiefile") == "/tmp/cookies.txt"
        finally:
            patcher.stop()

    def test_forwards_cookies_from_browser(self):
        """cookies_from_browser → cookiesfrombrowser in ydl_opts."""
        patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
        mock_ydl_cls = patcher.start()
        mock_instance = mock_ydl_cls.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"entries": [{"id": "v1"}]}
        try:
            ydl_utils.ydl_get_entries("url", cookies_from_browser="firefox")
            _opts = mock_ydl_cls.call_args[0][0]
            assert _opts.get("cookiesfrombrowser") == ("firefox",)
        finally:
            patcher.stop()

    def test_forwards_sleep_requests(self):
        """sleep_requests → sleep_interval_requests in ydl_opts."""
        patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
        mock_ydl_cls = patcher.start()
        mock_instance = mock_ydl_cls.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"entries": [{"id": "v1"}]}
        try:
            ydl_utils.ydl_get_entries("url", sleep_requests=2.5)
            _opts = mock_ydl_cls.call_args[0][0]
            assert _opts.get("sleep_interval_requests") == 2.5
        finally:
            patcher.stop()

    def test_forwards_extract_flat(self):
        """extract_flat=True → extract_flat in ydl_opts."""
        patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
        mock_ydl_cls = patcher.start()
        mock_instance = mock_ydl_cls.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"entries": [{"id": "v1"}]}
        try:
            ydl_utils.ydl_get_entries("url", extract_flat=True)
            _opts = mock_ydl_cls.call_args[0][0]
            assert _opts.get("extract_flat") is True
        finally:
            patcher.stop()

    def test_forwards_max_entries(self):
        """max_entries → playlistend in ydl_opts."""
        patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
        mock_ydl_cls = patcher.start()
        mock_instance = mock_ydl_cls.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"entries": [{"id": "v1"}]}
        try:
            ydl_utils.ydl_get_entries("url", max_entries=5)
            _opts = mock_ydl_cls.call_args[0][0]
            assert _opts.get("playlistend") == 5
        finally:
            patcher.stop()

    def test_default_opts(self):
        """Always sets logger and ignoreerrors."""
        patcher = mock.patch.object(ydl_utils, "YoutubeDL", autospec=True)
        mock_ydl_cls = patcher.start()
        mock_instance = mock_ydl_cls.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"entries": [{"id": "v1"}]}
        try:
            ydl_utils.ydl_get_entries("url")
            _opts = mock_ydl_cls.call_args[0][0]
            assert _opts.get("ignoreerrors") is True
            assert "logger" in _opts
        finally:
            patcher.stop()
