import logging
from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def ydl_get_entries(search_term, cookies_file=None, sleep_requests=None):
    try:
        ydl_opts = {"logger": MyLogger(), "ignoreerrors": True}
        
        # Add cookies file if provided
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file
            
        # Add sleep between requests if provided
        if sleep_requests is not None:
            ydl_opts["sleep_interval_requests"] = sleep_requests
            
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(search_term, download=False)
        return info_dict["entries"]
    except Exception as e:
        logger.error("Error with getting the youtube url for %s : %s.", search_term, e)
        return None
