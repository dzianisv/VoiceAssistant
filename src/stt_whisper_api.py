
import speech_recognition as sr
import logging 
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

class STT():
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            return recognizer.recognize_whisper_api(audio)
        except sr.UnknownValueError as e:
            logger.error(e)
        except sr.RequestError as e:
            logger.error(e)
