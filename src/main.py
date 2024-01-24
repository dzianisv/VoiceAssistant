#!/usr/bin/env python3

import os

import logging
import string
from dataclasses import dataclass


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("assistant")
logger.setLevel(logging.DEBUG)

logger.info("loading llm...")
from llm_langchains import LLM
logger.info("loading wake word engine...")
import wakeword

greeting_message = "Как я могу помочь тебе?"

llm_type = "openai"
if llm_type == "google":
    llm = LLM(api_key=os.getenv("GOOGLE_API_KEY"))
elif llm_type == "openai":
    llm = LLM(api_key=os.getenv("OPENAI_KEY"))

from stt_speechrecognition import STT
stt = STT(language='ru-RU')

tts_type = 'rhvoice'
if tts_type == 'rhvoice':
    from tts_rhvoice import TTS
    tts = TTS(profile='tatiana')
elif tts_type == 'google':
    from tts_gtts import TTS
    tts = TTS('ru')

def speak(text, block=True) -> bool:
    return tts.speak(text, block)

def listen() -> str:
    return stt.listen()

def wait_for_activation_keyword():
    keyword = wakeword.wait()
    logger.debug("recognezed an activation keyword \"%s\"", keyword)
    communicate()
 

def communicate():
    text = greeting_message

    while speak(text):
        logger.info("Listening...")
        question = listen()
        if question:
            logger.info("Recognized %s", question)
            speak("Сейчас узнаю...", block=False)
            text = llm.ask(question)
            logger.info("AI response: %s", text)
        else:
            break

    wait_for_activation_keyword()



if __name__ == "__main__":
    communicate()
