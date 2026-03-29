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
) -> list | None:
    """
    Extract video entries from a YouTube channel using yt-dlp.

    Args:
        search_term: The YouTube channel URL to extract entries from
        cookies_file: Optional path to a cookies.txt file for authentication
        sleep_requests: Optional sleep interval between requests
        cookies_from_browser: Optional browser name to extract cookies from (e.g. chrome, firefox)

    Returns:
        List of video entry dictionaries, or None if an error occurred
    """
    try:
        ydl_opts = {"logger": MyLogger(), "ignoreerrors": True}

        # Add cookies file if provided
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file

        # Add cookies from browser if provided
        if cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)

        # Add sleep between requests if provided
        if sleep_requests is not None:
            ydl_opts["sleep_interval_requests"] = sleep_requests

        with YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
            info_dict = ydl.extract_info(search_term, download=False)
        return info_dict["entries"]  # type: ignore[index, typeddict-item, no-any-return]
    except Exception as e:
        logger.error("Error with getting the youtube url for %s : %s.", search_term, e)
        return None
