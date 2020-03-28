"""
Extract metadata for all videos from a youtube channel into a csv file.
"""
import logging
import time
import argparse
from . import ydl_utils
import csv
import pandas as pd

logger = logging.getLogger()
temps_debut = time.time()


def is_youtube_channel(channel_url):
    if "youtube" not in channel_url:
        return False
    if not any(x in channel_url for x in ["channel", "user"]):
        return False
    return True


def return_entry(entry, field):
    try:
        return entry[field]
    except Exception as e:
        logger.error("%s", e)
        return None


def get_username_from_entries(list_dict):
    return list_dict[0]["author"].replace(" ", "_")


def main():
    args = parse_args()
    if args.export_format not in ["csv", "xlsx", "xls"]:
        logger.error(
            "%s format not supported as export format. Exiting.",
            args.export_format,
        )
        exit()
    if not args.channel_url:
        channel_url = str(input("Enter a youtube channel url : "))
    else:
        channel_url = args.channel_url

    if not is_youtube_channel(channel_url):
        logger.error(
            "%s is not a valid youtube channel url. Exiting.", channel_url
        )
        exit()

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

    export_file_name = (
        f"youtube_extract_{get_username_from_entries(list_dict)}"
    )
    logger.debug("Exporting to %s.", export_file_name)
    df = pd.DataFrame(list_dict)

    if args.export_format == "csv":
        df.to_csv(export_file_name + ".csv", index=False, sep="\t")
    elif args.export_format in ["xls", "xlsx"]:
        df.to_excel(export_file_name + ".xlsx", index=False)

    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


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
    parser.add_argument(
        "channel_url", nargs="?", type=str, help="Youtube channel url."
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
