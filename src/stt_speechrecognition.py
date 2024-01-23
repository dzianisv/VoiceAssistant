
import speech_recognition as sr
import logging 
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

class STT():
    def __init__(self, api_key: str):
        self.recognizer = sr.Recognizer()
        self.api_key = api_key

    def listen(self):
        with sr.Microphone() as source:
            logger.info("Listening...")
            audio = self.recognizer.listen(source)
        try:
            # text =  self.recognizer.recognize_whisper_api(audio, api_key=self.api_key)
            text = self.recognizer.recognize_google(audio, language='ru-RU')
            logger.debug("recognized %s", text)
            return text
        except sr.RequestError as e:
            logger.error(e)
