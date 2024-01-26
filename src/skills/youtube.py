import subprocess
import os
import sys
import logging
import re
import threading
import dataclasses

from urllib.parse import urlparse, parse_qs

from pydispatch import dispatcher

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

def extract_youtube_link_and_id(message):
    r = []
    # Regular expression pattern to find YouTube URLs
    youtube_url_pattern = (
        r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w\-]+)"
    )
    # Search for the pattern in the message
    urls = re.findall(youtube_url_pattern, message)
    for url in urls:
        # Parsing the URL to extract the 'v' parameter
        parsed_url = urlparse(url)
        # For 'youtube.com' links, the video ID is stored in query parameters
        if "youtube.com" in parsed_url.netloc:
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]
        # For 'youtu.be' links, the video ID is stored in the path
        else:
            video_id = parsed_url.path[1:]

        r.append((url, video_id))

    return r


class NoAudioStream(Exception):
    pass


def get_audio_stream_url(url: str):
    formats = subprocess.check_output(
        ["yt-dlp", "--list-formats", url], encoding="utf8"
    )

    for line in formats.splitlines():
        if "audio only" in line:
            y_format = line.split()[0]
            logger.debug('Format string "%s", format %s', line, y_format)
            p = subprocess.run(
                ["yt-dlp", "-f", y_format, "-g", url],
                encoding="utf8",
                stdout=subprocess.PIPE,
            )
            if p.stdout.startswith("https://"):
                return p.stdout.strip()
            else:
                logger.warning("failed to get the url of the stream: %s", p.stdout)
    else:
        raise NoAudioStream()


class PlayYoutube:
    def __init__(self):
        dispatcher.connect(self.stop, signal='stop', sender=dispatcher.Any)
        # TODO: mutex
        self.proc = None
        self.stopped = False
    
    def stop(self):
        self.stopped = True
        self.proc.kill()

    def run(self, message):
        urls = extract_youtube_link_and_id(message)

        if len(urls) > 0:
            self.stopped = False
            
            def play():                
                for video_url, video_id in urls:
                    if self.stopped:
                        break

                    logger.info('loading "%s"', video_url)
                    try:
                        audio_stream_url = get_audio_stream_url(video_url)
                        logger.info('playing "%s"', audio_stream_url)
                        
                        if self.stopped:
                            break
                        
                        self.proc = subprocess.Popen(
                            ["cvlc", "--play-and-exit", audio_stream_url]
                        )
                        self.proc.wait()
                        self.proc = None
                    except NoAudioStream:
                        logger.debug(
                            "No audio stream found for youtube video %s", video_url
                        )
                        continue

            threading.Thread(target=play).start()
            return True
        else:
            return False
