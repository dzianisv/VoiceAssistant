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

logger = logging.getLogger(__name__)

def md5hash(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

class TTS:
    def __init__(self):
        self.workdir = os.path.join(os.getcwd(), '.tts_cache')
        
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
            
        dispatcher.connect(self.stop, signal='stop', sender=dispatcher.Any)

         # alloy, echo, fable, onyx, nova, and shimmer
        proxy_url = os.environ.get("OPENAI_PROXY")
        http_client=httpx.Client(proxy=proxy_url)
        self.engine = OpenAIEngine(model='tts-1', voice='echo')

        # self.voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        # self.model = model
        # self.voice = voice
        # self.client = OpenAI()

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
        if os.path.exists(cache_file):
            self.play(cache_file)
        else:
            # https://platform.openai.com/docs/guides/text-to-speech/quickstart
            self.stream = TextToAudioStream(self.engine)
            self.stream.feed(text)
            self.stream.play_async(language='ru', output_wavfile=cache_file)
            self.stream = None
