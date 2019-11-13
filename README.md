# youtube_extract

Extracts metadata for all videos from a youtube channel and exports it into a csv file.

Be sure to read the csv file using the tab character `\t` as field separator in your spreadsheet software of choice.

It's quite slow at the moment and unpredictable, expect ~400 seconds for extracting a channel containing 400 videos.

## Requirements

- youtube-dl

## Installation

```
pip install youtube_extract
```

If you are an Archlinux user, you can install the AUR package [youtube_extract-git](https://aur.archlinux.org/packages/youtube_extract-git).

### Installation of the virtualenv (with pipenv)

```
pipenv install
```

## Usage

If installed :

```
youtube_extract CHANNEL_URL
```

Otherwise, in the directory containing the source code :

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
