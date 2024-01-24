import subprocess
import os
import sys
import logging
import re
import tempfile

from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)
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
        url, v_id = extract_youtube_link_and_id(message)
        if url:
            workdir = tempfile.mkdtemp()
            try:
                logger.info("processing \"%s\"", url)

                output = subprocess.check_output(["yt-dlp", "--list-formats", url], cwd=workdir, encoding='utf8')
                for line in output.splitlines():
                    if 'audio only' in line:
                        y_format = line.split()[0]
                        logger.debug("Format string \"%s\", format %s", line, y_format)
                        p = subprocess.run(["yt-dlp", "-f", y_format, url], encoding='utf8', stdout=subprocess.PIPE)
                        if p.stdout.startswith("http://"):
                            url = p.stdout
                            break
                else:
                    raise Exception("Audio-only stream is not found")
        
                cmd = ["cvlc", url]
                logger.info("playing \"%s\"", cmd)
                p = subprocess.Popen(cmd, cwd=workdir)
                p.wait()
            finally:
                os.removedirs(workdir)
            return True
        else:
            return False