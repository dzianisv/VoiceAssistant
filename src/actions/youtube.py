import subprocess
import os
import sys
import logging
import re
import threading
import dataclasses

from urllib.parse import urlparse, parse_qs

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
        pass

    def run(self, message: str, queue):
        urls = extract_youtube_link_and_id(message)

        if len(urls) > 0:
            @dataclasses.dataclass
            class SharedData:
                player: subprocess.Popen
                canceled: False    
            
            shared_object = SharedData(player=None, canceled=False)

            def event_listener(shared_object: SharedData):
                while True:
                    command = queue.down.get()  # Get a command from the queue
                    logger.debug("received command: %s", command)
                    if command == "STOP":
                        shared_object.cancled = True
                        shared_object.player.kill()
                        break
                    if command == "NEXT":
                        shared_object.player.kill()
                        continue

            def play(shared_object: SharedData):                
                for video_url, video_id in urls:
                    if shared_object.canceled:
                        break

                    logger.info('loading "%s"', video_url)
                    try:
                        audio_stream_url = get_audio_stream_url(video_url)
                        logger.info('playing "%s"', audio_stream_url)
                        player_process = subprocess.Popen(
                            ["cvlc", "--play-and-exit", audio_stream_url]
                        )
                        shared_object.player = player_process
                        player_process.wait()
                    except NoAudioStream:
                        logger.debug(
                            "No audio stream found for youtube video %s", video_url
                        )
                        continue

                queue.up.put("FINISHED")

            threading.Thread(target=play, args=[shared_object]).start()
            threading.Thread(target=event_listener, args=[shared_object]).start()
            return True
        else:
            return False
