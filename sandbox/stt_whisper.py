import os
from io import BytesIO
import logging
import sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

import openai
import speech_recognition


class STT():
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.client = openai.OpenAI()
        
    def listen(self):
        with speech_recognition.Microphone() as source:
            logger.info("Listening...")

            audio = self.recognizer.listen(source)
            wav_data = BytesIO(audio.get_wav_data())
            wav_data.name = "SpeechRecognition_audio.wav"



        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=wav_data
        )

        return transcript["text"]
