# youtube_extract

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/131858400ee84232a50c03f4b06c9344)](https://app.codacy.com/manual/dbeley/youtube_extract?utm_source=github.com&utm_medium=referral&utm_content=dbeley/youtube_extract&utm_campaign=Badge_Grade_Dashboard)
![Build Status](https://github.com/dbeley/youtube_extract/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/dbeley/youtube_extract/branch/master/graph/badge.svg)](https://codecov.io/gh/dbeley/youtube_extract)

Extract metadata for all videos from a youtube channel and exports it into a csv or xlsx file.

Be sure to read the csv file using the tab character `\t` as field separator in your spreadsheet software of choice.

As of now it's quite slow and unpredictable, expect ~400 seconds for extracting all videos metadata from a channel containing 400 videos.

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

## Requirements

- python >=3.8
- yt-dlp
- pandas
- openpyxl

## Installation

### Preferred install method

```bash
pip install youtube_extract
```

If you are an Archlinux user, you can install the AUR package [youtube_extract-git](https://aur.archlinux.org/packages/youtube_extract-git).

### Run from source

```bash
git clone https://github.com/dbeley/youtube_extract
cd youtube_extract
pip install yt-dlp pandas openpyxl
python setup.py install
youtube_extract -h
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
usage: youtube_extract [-h] [--debug] [-e EXPORT_FORMAT] [--cookies COOKIE_FILE] [channel_url]

Extract metadata for all videos from a youtube channel into a csv or xlsx
file.

positional arguments:
  channel_url           Youtube channel url.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -e EXPORT_FORMAT, --export_format EXPORT_FORMAT
                        Export format (csv or xlsx). Default : csv.
  --cookies COOKIE_FILE Path to cookies.txt file. 
                        Use for age-restricted content.
  --sleep-requests SLEEP_REQUESTS
                        Number of seconds to sleep between requests during data extraction.
```