
import speech_recognition as sr
import logging 
import sys
import enum


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

class Engine(enum.Enum):
    Google = "google"
    OpenAIWhisper = "openai-whisper"

class STT():
    def __init__(self, engine = Engine.Google, **kws):
        self.recognizer = sr.Recognizer()

        if engine == Engine.Google:
            self.recognize_fn = self.recognizer.recognize_google
        elif engine == Engine.OpenAIWhisper:
             self.recognize_fn = self.recognizer.recognize_whisper_api

        self.kws = kws

    def listen(self):
        with sr.Microphone() as source:
            logger.info("Listening...")
            audio = self.recognizer.listen(source)
        try:
            text =  self.recognize_fn(audio, **self.kws)
            
            logger.debug("recognized %s", text)
            return text
        except sr.RequestError as e:
            logger.error(e)
