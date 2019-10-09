import logging
from youtube_dl import YoutubeDL

logger = logging.getLogger(__name__)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def ydl_get_entries(search_term):
    try:
        ydl_opts = {"logger": MyLogger(), "ignoreerrors": True}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"{search_term}", download=False)
        return info_dict["entries"]
    except Exception as e:
        logger.error(
            "Error with getting the youtube url for %s : %s.", search_term, e
        )
        return None
