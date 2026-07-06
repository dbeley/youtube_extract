"""Utilities for interacting with yt-dlp."""

import logging

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


class MyLogger:
    """Custom logger for yt-dlp to suppress debug/warning output."""

    def debug(self, msg: str) -> None:
        """Suppress debug messages."""
        pass

    def warning(self, msg: str) -> None:
        """Suppress warning messages."""
        pass

    def error(self, msg: str) -> None:
        """Print error messages."""
        print(msg)


def ydl_get_entries(
    search_term: str,
    cookies_file: str | None = None,
    sleep_requests: float | None = None,
    cookies_from_browser: str | None = None,
    extract_flat: bool = False,
    max_entries: int | None = None,
) -> list | None:
    """
    Extract video entries from a YouTube channel using yt-dlp.

    Args:
        search_term: The YouTube channel URL to extract entries from
        cookies_file: Optional path to a cookies.txt file for authentication
        sleep_requests: Optional sleep interval between requests
        cookies_from_browser: Optional browser name to extract cookies from (e.g. chrome, firefox)
        extract_flat: If True, only extract flat metadata (no format details).
                       Much faster but best_format/filesize_bytes won't be available.
        max_entries: Optional maximum number of entries to extract

    Returns:
        List of video entry dictionaries, or None if an error occurred
    """
    try:
        ydl_opts: dict = {"logger": MyLogger(), "ignoreerrors": True}

        # Add cookies file if provided
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file

        # Add cookies from browser if provided
        if cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)

        # Add sleep between requests if provided
        if sleep_requests is not None:
            ydl_opts["sleep_interval_requests"] = sleep_requests

        # Flat extraction: skip format resolution for massive speedup
        if extract_flat:
            ydl_opts["extract_flat"] = True

        # Limit entries
        if max_entries is not None:
            ydl_opts["playlistend"] = max_entries

        with YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
            info_dict = ydl.extract_info(search_term, download=False)
        entries = info_dict["entries"]  # type: ignore[index, typeddict-item]
        # yt-dlp may return None for errored entries when ignoreerrors=True
        return [e for e in entries if e is not None] if entries else entries  # type: ignore[no-any-return]
    except Exception as e:
        logger.error("Error with getting the youtube url for %s : %s.", search_term, e)
        return None
