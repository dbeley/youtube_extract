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
| dislike_count  | Dislike Count                  |
| average_rating | Rating                         |
| duration       | Duration in seconds            |
| upload_date    | Upload Date in YYYYMMDD Format |
| tags           | Tags                           |
| categories     | Categories                     |
| description    | Description                    |
| thumbnail      | Thumbnail URL                  |
| best_format    | Highest Format Available       |
| filesize_bytes | Filesize in bytes              |

## Requirements

- youtube-dl
- pandas
- openpyxl

## Installation

### Preferred install method

```
pip install youtube_extract
```

If you are an Archlinux user, you can install the AUR package [youtube_extract-git](https://aur.archlinux.org/packages/youtube_extract-git).

### Run from source

#### First method (installing the youtube_extract package)

```
git clone https://github.com/dbeley/youtube_extract
cd youtube_extract
python setup.py install
youtube_extract -h
```

#### Second method (installing only the dependencies)

```
git clone https://github.com/dbeley/youtube_extract
cd youtube_extract
pip install -r requirements.txt
python -m youtube_extract -h
```

#### Third method (installing the youtube_extract package with pipenv)

```
git clone https://github.com/dbeley/youtube_extract
cd youtube_extract
pipenv install '-e .'
pipenv run youtube_extract -h
```

## Usage

If installed :

```
youtube_extract CHANNEL_URL
# or xlsx format
youtube_extract CHANNEL_URL -e xlsx
```

Otherwise, in the directory containing the source code :

```
python -m youtube_extract CHANNEL_URL
# or xlsx format
python -m youtube_extract CHANNEL_URL -e xlsx
```

## Help

```
youtube_extract -h
```

```
usage: youtube_extract [-h] [--debug] [-e EXPORT_FORMAT] [channel_url]

Extract metadata for all videos from a youtube channel into a csv or xlsx
file.

positional arguments:
  channel_url           Youtube channel url.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -e EXPORT_FORMAT, --export_format EXPORT_FORMAT
                        Export format (csv or xlsx). Default : csv.
```
