from io import BytesIO
import os
from languages import detect_language
import logging
import sys
from pydispatch import dispatcher
from RealtimeTTS import TextToAudioStream, OpenAIEngine
import httpx
import os
import hashlib
import pygame
import openai
from proxy import proxy

logger = logging.getLogger(__name__)

def md5hash(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

class TTS:
    def __init__(self):
        self.workdir = os.path.join(os.getcwd(), '.tts_cache')
        
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
    
        dispatcher.connect(self.stop, signal='stop', sender=dispatcher.Any)

        with proxy(os.environ.get("OPENAI_PROXY")):
            # voices https://github.com/KoljaB/RealtimeTTS/blob/master/RealtimeTTS/engines/openai_engine.py#L28
            # voices demo https://platform.openai.com/docs/guides/text-to-speech
            self.engine = OpenAIEngine(model='tts-1', voice='nova')
            self.stream = None


    def play(self, filename: str):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def stop(self):
        if self.stream:
             self.stream.stop()
             self.stream = None
        else:
            pygame.mixer.music.stop()

    def speak(self, text, block: bool=True):
        cache_key = md5hash(text)
        cache_file = os.path.join(self.workdir, f"{cache_key}.wav")
        # if os.path.exists(cache_file):
        #     self.play(cache_file)
        # else:
        # https://platform.openai.com/docs/guides/text-to-speech/quickstart
        self.stream = TextToAudioStream(self.engine)
        self.stream.feed(text)
        self.stream.play_async(language='ru', output_wavfile=cache_file)
        self.stream = None
