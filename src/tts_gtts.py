from io import BytesIO
import os
import tempfile
from languages import detect_language
import logging
import sys
import threading
from pydispatch import dispatcher
import pygame
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

logger.debug("loading gtts")
from gtts import gTTS

logger.debug("loading pygame")
pygame.mixer.init()
logger.debug("all modules are loaded")

class TTS:
    def __init__(self):
        self.workdir = os.path.join(os.getcwd(), 'gtts')
        
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
            
        dispatcher.connect(self.stop, signal='stop', sender=dispatcher.Any)
            
    def play(self, filename: str):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def stop(self):
        pygame.mixer.music.stop()

    def speak(self, text, block=True):
        logger.info("speaking: %s", text)
        should_be_cached = len(text) < 80
        name = hex(hash(text))
        
        if should_be_cached:
            workfile = os.path.join(self.workdir, f"{name}.mp3")
        else:
            workfile = os.path.join(tempfile.gettempdir(), f"{name}.mp3")

        def _task():
            if os.path.exists(workfile):
                self.play(workfile)
                return
        
            lang_code = detect_language(text)
            tts = gTTS(text, lang=lang_code)
            tts.save(workfile)
            self.play(workfile)
    
            if not should_be_cached:
                os.unlink(workfile)
    
        if block:
            _task()
        else:
            threading.Thread(target=_task).start()
    
        return True