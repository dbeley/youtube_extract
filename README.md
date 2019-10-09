# youtube_extract

Extracts metadata for all videos from a youtube channel and exports it to a csv file.

Be sure to read the file using the tab character ('\t') as field separator in your spreadsheet software of choice.

## Requirements

- youtube-dl

## Installation of the virtualenv (with pipenv)

```
pipenv install
```

## Usage

```
python youtube_extract.py CHANNEL_URL
```

## Help

```
python youtube_extract.py -h
```

```
usage: youtube_extract.py [-h] [--debug] [channel_url]

Extract metadata for all videos from a youtube channel into a csv file.

positional arguments:
  channel_url  Youtube channel url.

optional arguments:
  -h, --help   show this help message and exit
  --debug      Display debugging information.
```
