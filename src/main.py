#!/usr/bin/env python3

import os

import logging
import string
from dataclasses import dataclass
from llm_langchains import LLM
from stt_whisper_api import STT
from tts_rhvoice import TTS
import wakeword

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("assistant")
logger.setLevel(logging.DEBUG)

greeting_message = "Привет, я твой голосовой помощник. Как я могу помочь тебе?"

openai_key = os.environ.get("OPENAI_KEY")
if len(openai_key) == 0:
    raise KeyError("OPENAI_KEY is not set")

llm = LLM(openai_key)
stt = STT()
tts = TTS()

def speak(text) -> bool:
    return tts.speak(text)

def listen() -> str:
    return stt.listen()

def communicate():
    text = greeting_message
    while speak(text):
        logger.info("Listening...")
        question = listen()
        if question:
            logger.info("Recognized %s, quering OpenAI", question)
            text = llm.ask(question)
            if not text:
                text = "Sorry, I can't answer your question"

            logger.info("AI response: %s", text)
        else:
            break

    speak(text)
    listen_for_activation_keyword()


def listen_for_activation_keyword():
    """runs keyword spotting locally, with direct access to the result audio"""
    wakeword.wait()
    logger.debug("recognezed an activation keyword")
    communicate()


if __name__ == "__main__":
    communicate()
