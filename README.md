# youtube_extract

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/131858400ee84232a50c03f4b06c9344)](https://app.codacy.com/manual/dbeley/youtube_extract?utm_source=github.com&utm_medium=referral&utm_content=dbeley/youtube_extract&utm_campaign=Badge_Grade_Dashboard)
![Build Status](https://github.com/dbeley/youtube_extract/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/dbeley/youtube_extract/branch/master/graph/badge.svg)](https://codecov.io/gh/dbeley/youtube_extract)

Extract metadata for all videos from a youtube channel and exports it into a csv or xlsx file.

Be sure to read the csv file using the tab character `\t` as field separator in your spreadsheet software of choice.

As of now it's quite slow and unpredictable when extracting full metadata (~400 seconds for 400 videos).
Use the `--extract-flat` flag for a ~10-100x speedup (at the cost of missing format details).

## Fields extracted

| Field          | Description                    |
|----------------|--------------------------------|
| author         | Channel Name                   |
| channel_url    | Channel URL                    |
| title          | Video Title                    |
| webpage_url    | Video URL                      |
| view_count     | View Count                     |
| like_count     | Like Count                     |
| duration       | Duration in seconds            |
| upload_date    | Upload Date in YYYYMMDD Format |
| tags           | Tags                           |
| categories     | Categories                     |
| description    | Description                    |
| thumbnail      | Thumbnail URL                  |
| best_format    | Highest Format Available       |
| filesize_bytes | Filesize in bytes              |

> **Note:** When using `--extract-flat`, `best_format` and `filesize_bytes` will be empty since format details are not resolved.

## Requirements

- Python >=3.10
- yt-dlp
- pandas
- openpyxl

## Installation

### From PyPI

```bash
pip install youtube_extract
```

### From GitHub (Latest Development Version)

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/dbeley/youtube_extract.git
```

### From Source

Clone the repository and install:

```bash
git clone https://github.com/dbeley/youtube_extract
cd youtube_extract
pip install -e .
```

## Usage

If installed :

```bash
youtube_extract CHANNEL_URL
# or xlsx format
youtube_extract CHANNEL_URL -e xlsx
```

Otherwise, in the directory containing the source code :

```bash
python -m youtube_extract CHANNEL_URL
# or xlsx format
python -m youtube_extract CHANNEL_URL -e xlsx
```

### Using Cookies

The `--cookies` option allows you to provide a Netscape-formatted cookies file which can be used to access age-restricted content, private videos, or content that requires authentication.
You can obtain a cookies file using browser extensions like:

- [cookies.txt](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc?pli=1) for Chrome
- [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) for Firefox

The cookies file should be in the standard Netscape format:

#### Netscape HTTP Cookie File

```
.domain.com TRUE / FALSE 1234567890 name value
```

### Extracting Cookies from a Browser

You can also extract cookies directly from a browser using `--cookies-from-browser`:

```bash
youtube_extract CHANNEL_URL --cookies-from-browser firefox
```

### Fast Extraction (Flat Mode)

For a ~10-100x speedup when you don't need format details (`best_format`, `filesize_bytes`), use the `--extract-flat` flag:

```bash
youtube_extract CHANNEL_URL --extract-flat
```

This skips format resolution entirely and only extracts basic metadata.

### Limiting the Number of Entries

Use `--max-entries` to limit how many videos are extracted (useful for testing or when you only need recent videos):

```bash
youtube_extract CHANNEL_URL --max-entries 10
```

### Rate Limiting

YouTube may rate-limit your requests if you extract data from channels with many videos. To avoid this, you can use the --sleep-requests option to add a delay between requests:

```bash
youtube_extract CHANNEL_URL --sleep-requests 10
```

This will pause for 10 seconds between requests, which can help avoid rate limiting at the cost of longer extraction time.
See: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#this-content-isnt-available-try-again-later

## Help

```bash
youtube_extract -h
```

```
usage: youtube_extract [-h] [--debug] [-e EXPORT_FORMAT] [--cookies COOKIE_FILE]
                       [--cookies-from-browser BROWSER] [--sleep-requests SECONDS]
                       [--extract-flat] [--max-entries MAX_ENTRIES]
                       [channel_url]

Extract metadata for all videos from a youtube channel into a csv or xlsx file.

positional arguments:
  channel_url           Youtube channel url.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -e EXPORT_FORMAT, --export_format EXPORT_FORMAT
                        Export format (csv or xlsx). Default : csv.
  --cookies COOKIE_FILE Path to cookies.txt file.
                        Use for age-restricted content.
  --cookies-from-browser BROWSER
                        Browser to extract cookies from (e.g. chrome, firefox, safari, edge)
  --sleep-requests SECONDS
                        Number of seconds to sleep between requests during data extraction.
  --extract-flat        Extract only flat metadata (no format details).
                        ~10-100x faster but best_format and filesize_bytes will be empty.
  --max-entries MAX_ENTRIES
                        Maximum number of videos to extract (useful for testing or limiting scope).
```
