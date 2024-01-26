
from io import BytesIO
import os
import subprocess
import tempfile
from languages import detect_language
import logging
import sys
import threading

from pydispatch import dispatcher

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

logger.debug("laoding gtts")
from gtts import gTTS
logger.debug("loading audioplayer")
from audioplayer import AudioPlayer
logger.debug("all modules are loaded")

"""https://gtts.readthedocs.io/en/latest/"""

def find_in_path(name: str):
    for d in os.getenv("PATH").split(":"):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p

    return None

import re
import string

def clean_filename(filename):
    """
    Cleans the filename by removing not-allowed symbols and trimming spaces.
    
    :param filename: The original file name
    :return: A clean, file-system safe file name
    """
    # Define the set of not-allowed characters for file names
    # Windows does not allow <>:"/\|?* and filenames cannot end with a dot or space
    # Unix/Linux does not allow /
    not_allowed_chars = set('<>:"/\\|?*') | set(chr(0))

    # Replace not-allowed characters with an underscore
    cleaned_filename = ''.join('_' if c in not_allowed_chars else c for c in filename)

    # Additionally, remove leading and trailing whitespaces and replace sequences of whitespace with a single underscore
    cleaned_filename = re.sub(r'\s+', '_', cleaned_filename.strip())
    return cleaned_filename


    
class TTS:
    def __init__(self):
        self.workdir = os.path.join(os.getcwd(), 'gtts')
        self.proc = None
        
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
            
        dispatcher.connect(self.stop, signal='stop', sender=dispatcher.Any)
            
    def play(self, filename: str):
        if self.proc is not None:
            self.proc.kill()
            self.proc.wait()

        self.proc = subprocess.Popen(["play", filename])
        self.proc.wait()
        self.proc = None
    
    def stop(self):
        if self.proc is not None:
            self.proc.kill()

    def speak(self, text):
        logger.info("speaking: %s", text)
        should_be_cached = len (text) < 80
        name = hex(hash(text))
        
        if should_be_cached:
            workfile = os.path.join(self.workdir, f"{name}.mp3")
        else:
            workfile = os.path.join(tempfile.gettempdir(), f"{name}.mp3")

        def _task():
            if os.path.exists(workfile):
                self.play(workfile)
        
            lang_code = detect_language(text)
            tts = gTTS(text, lang=lang_code)
            tts.save(workfile)
            self.play(workfile)
    
            if not should_be_cached:
                os.unlink(workfile)
    
        threading.Thread(target=_task).start()
        return True