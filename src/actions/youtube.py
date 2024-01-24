import subprocess
import os
import sys
import logging
import re
import tempfile

from urllib.parse import urlparse, parse_qs

logger = logging.getLogger("assistant")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

def extract_youtube_link_and_id(message):
    # Regular expression pattern to find YouTube URLs
    youtube_url_pattern = r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w\-]+)'
    # Search for the pattern in the message
    match = re.search(youtube_url_pattern, message)
    # If a match is found, extract the URL and the 'v' parameter
    if match:
        url = match.group()
        # Parsing the URL to extract the 'v' parameter
        parsed_url = urlparse(url)
        # For 'youtube.com' links, the video ID is stored in query parameters
        if 'youtube.com' in parsed_url.netloc:
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        # For 'youtu.be' links, the video ID is stored in the path
        else:
            video_id = parsed_url.path[1:]
        return url, video_id
    else:
        return None, None

class PlayYoutube():
    def __init__(self):
        pass    
    
    def run(self, message: str):
        workdir = tempfile.mkdtemp()

        url, v_id = extract_youtube_link_and_id(message)
        if url:
            cmd = ["yt-dlp", "-x", "--audio-format", "opus", "--output", "%(id)s.%(ext)s", url]
            logger.info("run \"%s\"", cmd)

            p = subprocess.Popen(cmd, cwd=workdir)
            p.wait()
            if p.returncode != 0:
                # TODO: raise exception?
                return True
    
            cmd = ["play", os.path.join(workdir, f"{v_id}.opus")]
            logger.info("playing \"%s\"", cmd)
            p = subprocess.Popen(cmd, cwd=workdir)
            p.wait()
            return True
        else:
            return False