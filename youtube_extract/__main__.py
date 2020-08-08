"""
Extract metadata for all videos from a youtube channel into a csv file.
"""
import logging
import time
import argparse
from youtube_extract import ydl_utils
import pandas as pd

logger = logging.getLogger()
temps_debut = time.time()

SUPPORTED_EXPORT_FORMAT = ["csv", "xlsx"]


def is_youtube_channel(channel_url):
    if "youtube" not in channel_url:
        return False
    if not any(x in channel_url for x in ["/c/", "channel", "user"]):
        return False
    return True


def return_entry(entry, field):
    try:
        return entry[field]
    except Exception as e:
        logger.error("%s", e)
        return None


def get_filename(list_dict):
    return f"youtube_extract_{list_dict[0]['author'].replace(' ', '_')}"


def check_args(args):
    if args.export_format not in SUPPORTED_EXPORT_FORMAT:
        raise Exception(
            f"{args.export_format} format not supported as export format. Exiting."
        )
    if not args.channel_url:
        # channel_url = str(input("Enter a youtube channel url : "))
        raise Exception(
            f"No url set. Use youtube_extract CHANNEL_URL as command to input an URL."
        )

    if not is_youtube_channel(args.channel_url):
        raise Exception(
            f"{args.channel_url} is not a valid youtube channel url. Exiting."
        )


def extract_entries_for_url(channel_url):
    list_dict = []
    logger.debug("Extracting videos infos for %s.", channel_url)
    entries = ydl_utils.ydl_get_entries(channel_url)
    for entry in entries:
        if entry:
            best_format = entry["formats"][-2]["format"]
            filesize = entry["formats"][-2]["filesize"]
            list_dict.append(
                {
                    "author": return_entry(entry, "uploader"),
                    "channel_url": return_entry(entry, "uploader_url"),
                    "title": return_entry(entry, "title"),
                    "webpage_url": return_entry(entry, "webpage_url"),
                    "view_count": return_entry(entry, "view_count"),
                    "like_count": return_entry(entry, "like_count"),
                    "dislike_count": return_entry(entry, "dislike_count"),
                    "average_rating": return_entry(entry, "average_rating"),
                    "duration": return_entry(entry, "duration"),
                    "upload_date": return_entry(entry, "upload_date"),
                    "tags": return_entry(entry, "tags"),
                    "categories": return_entry(entry, "categories"),
                    "description": return_entry(entry, "description"),
                    "thumbnail": return_entry(entry, "thumbnail"),
                    "best_format": best_format,
                    "filesize_bytes": filesize,
                }
            )
    return list_dict


def main():
    args = parse_args()
    logger.debug("youtube_extract : %s.", args)

    try:
        check_args(args)
    except Exception as e:
        logger.error(e)
        exit(1)

    entries = extract_entries_for_url(args.channel_url)
    export_filename = get_filename(entries)

    logger.debug("Exporting to %s.", export_filename)
    df = pd.DataFrame(entries)

    if args.export_format == "csv":
        df.to_csv(export_filename + ".csv", index=False, sep="\t")
    elif args.export_format in ["xls", "xlsx"]:
        df.to_excel(export_filename + ".xlsx", index=False)

    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))
    exit(0)


def parse_args():
    format = "%(levelname)s :: %(message)s"
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
        help="Export format (csv or xlsx). Default : csv.",
        default="csv",
    ),
    parser.add_argument("channel_url", nargs="?", type=str, help="Youtube channel url.")
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
