"""Extract metadata for all videos from a youtube channel into a csv file."""

import argparse
import logging
import time

import pandas as pd

from youtube_extract import ydl_utils

logger = logging.getLogger()
START_TIME = time.time()

SUPPORTED_EXPORT_FORMATS = ["csv", "xlsx"]


def is_youtube_channel(channel_url: str) -> bool:
    """Check if the URL is a valid YouTube channel URL."""
    if "youtube" not in channel_url:
        return False
    if not any(x in channel_url for x in ["/c/", "channel", "user", "@"]):
        return False
    return True


def get_filename(list_dict: list) -> str:
    """Generate filename from channel author name."""
    if not list_dict:
        raise ValueError("list_dict cannot be empty")
    return f"youtube_extract_{list_dict[0]['author'].replace(' ', '_')}"


def check_args(args: argparse.Namespace) -> None:
    """Validate command line arguments."""
    if args.export_format not in SUPPORTED_EXPORT_FORMATS:
        raise ValueError(
            f"{args.export_format} format not supported as export format. "
            f"Supported formats: {', '.join(SUPPORTED_EXPORT_FORMATS)}"
        )
    if not args.channel_url:
        raise ValueError("No url set. Use youtube_extract CHANNEL_URL as command to input an URL.")

    if not is_youtube_channel(args.channel_url):
        raise ValueError(f"{args.channel_url} is not a valid youtube channel url.")


def extract_entries_for_url(
    channel_url: str,
    cookies_file: str | None = None,
    sleep_requests: float | None = None,
    cookies_from_browser: str | None = None,
    extract_flat: bool = False,
    max_entries: int | None = None,
) -> list:
    """Extract video entries from a YouTube channel URL."""
    list_dict: list[dict] = []
    logger.debug("Extracting videos infos for %s.", channel_url)
    entries = ydl_utils.ydl_get_entries(
        channel_url,
        cookies_file,
        sleep_requests,
        cookies_from_browser,
        extract_flat,
        max_entries,
    )

    if not entries:
        logger.warning("No entries found for %s", channel_url)
        return list_dict

    # Filter out None entries (yt-dlp returns None for errored videos
    # when ignoreerrors=True, e.g. when YouTube blocks the request)
    entries = [e for e in entries if e is not None]

    if not entries:
        logger.warning("No entries found for %s", channel_url)
        return list_dict

    # workaround if channel videos are seen as a playlist
    if "_type" in entries[0] and entries[0]["_type"] == "playlist":
        entries = entries[0]["entries"]

    for entry in entries:
        if not entry:
            continue

        # In flat mode, formats are not available
        if not extract_flat and entry.get("formats"):
            best_format = entry["formats"][-2].get("format", "")
            filesize = entry["formats"][-2].get("filesize", "")
        else:
            best_format = ""
            filesize = ""

        list_dict.append(
            {
                "author": entry.get("uploader", ""),
                "channel_url": entry.get("uploader_url", ""),
                "title": entry.get("title", ""),
                "webpage_url": entry.get("webpage_url", ""),
                "view_count": entry.get("view_count", ""),
                "like_count": entry.get("like_count", ""),
                "duration": entry.get("duration", ""),
                "upload_date": entry.get("upload_date", ""),
                "tags": entry.get("tags", ""),
                "categories": entry.get("categories", ""),
                "description": entry.get("description", ""),
                "thumbnail": entry.get("thumbnail", ""),
                "best_format": best_format,
                "filesize_bytes": filesize,
            }
        )
    return list_dict


def main() -> None:
    """Main entry point."""
    args = parse_args()
    logger.debug("youtube_extract : %s.", args)

    check_args(args)

    entries = extract_entries_for_url(
        args.channel_url,
        args.cookies,
        args.sleep_requests,
        args.cookies_from_browser,
        args.extract_flat,
        args.max_entries,
    )

    if not entries:
        logger.error("No entries extracted. Exiting.")
        return

    export_filename = get_filename(entries)

    logger.debug("Exporting to %s.", export_filename)
    df = pd.DataFrame(entries)

    if args.export_format == "csv":
        df.to_csv(export_filename + ".csv", index=False, sep="\t")
    elif args.export_format in ["xls", "xlsx"]:
        df.to_excel(export_filename + ".xlsx", index=False)

    logger.info("Runtime : %.2f seconds.", time.time() - START_TIME)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract metadata for all videos from a youtube channel into a csv or xlsx file."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-e",
        "--export_format",
        type=str,
        help="Export format (csv or xlsx). Default: csv.",
        default="csv",
    )
    parser.add_argument("channel_url", nargs="?", type=str, help="Youtube channel url.")

    parser.add_argument(
        "--cookies",
        type=str,
        help="Path to cookies.txt file",
        default=None,
    )

    parser.add_argument(
        "--cookies-from-browser",
        type=str,
        help="Browser to extract cookies from (e.g. chrome, firefox, safari, edge)",
        default=None,
        dest="cookies_from_browser",
    )

    parser.add_argument(
        "--sleep-requests",
        type=float,
        help="Number of seconds to sleep between requests during data extraction",
        default=None,
    )

    parser.add_argument(
        "--extract-flat",
        action="store_true",
        dest="extract_flat",
        default=False,
        help=(
            "Extract only flat metadata (no format details). "
            "~10-100x faster but best_format and filesize_bytes will be empty."
        ),
    )

    parser.add_argument(
        "--max-entries",
        type=int,
        dest="max_entries",
        default=None,
        help="Maximum number of videos to extract (useful for testing or limiting scope).",
    )

    args = parser.parse_args()

    log_format = "%(levelname)s :: %(message)s"
    logging.basicConfig(level=args.loglevel, format=log_format)
    return args


if __name__ == "__main__":
    main()
