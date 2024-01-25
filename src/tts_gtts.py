from gtts import gTTS
from io import BytesIO
import os
import subprocess
import tempfile
from languages import detect_language

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

def play(filename: str):
    if find_in_path("play"):
        subprocess.run(["play", filename])
    else:
        import pygame
        pygame.init()
        pygame.mixer.init()

        sound = pygame.mixer.Sound(filename)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.wait(1000)
        pygame.quit()

class TTS:
    def __init__(self, block=True):
        self.workdir = os.path.join(os.getcwd(), 'gtts')
        
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

    def speak(self, text, block):
        should_be_cached = len (text) < 80
        name = hex(hash(text))
        workfile = os.path.join(self.workdir, f"{name}.mp3")
    
        if os.path.exists(workfile):
            play(workfile)
            return True
        
        lang_code = detect_language(tetx)
        tts = gTTS(text, lang=lang_code)
        tts.save(workfile)
        play(workfile)
    
        if not should_be_cached:
            os.unlink(workfile)
    
        return True