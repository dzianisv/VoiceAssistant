#!/usr/bin/env python3

import os
import sys
import logging
import string
import time
from dataclasses import dataclass

import actions
from pydispatch import dispatcher

logger = logging.getLogger("assistant")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

from hal import detect
import languages
from llm_langchains import LLM
from wakeword_pvporcupine import WakeWord, KeywordSpottingActions
from stt_speechrecognition import STT
import tts


class VoiceAssistant:
    def __init__(self, llm_type="openai"):
        self.hal = detect()
        self.hal.start_blink((1, 2))

        self.lang_pack = languages.lang_packs[os.getenv("LANGUAGE", "ru")]
        self.tts = tts.createFaultTolerantTTS()
        self.stt = STT(language=self.lang_pack.google_stt_lang)
        logger.info("loading wake word engine...")
        self.wakeword = WakeWord(lang=os.getenv("LANGUAGE", "ru"))
        logger.info("loading llm...")
        if llm_type == "google":
            self.llm = LLM(api_key=os.getenv("GOOGLE_API_KEY"))
        elif llm_type == "openai":
            self.llm = LLM(api_key=os.getenv("OPENAI_KEY"))
        else:
            raise ValueError("invalid llm_type")

    def speak(self, text, *args, **kwargs) -> bool:
        logger.info("Speaking...: %s", text)
        self.hal.start_blink((0.5, 2))
        try:
            return self.tts.speak(text, *args, **kwargs)
        finally:
            self.hal.stop_blink()

    def listen(self) -> str:
        logger.info("Listening...")
        self.hal.led_on()
        try:
            return self.stt.listen()
        finally:
            self.hal.led_off()

    def start(self):
        self.wait_for_activation_keyword()

    def wait_for_activation_keyword(self):
        logger.info("Waiting for the wake word...")
        keyword = self.wakeword.wait()
        dispatcher.send(signal="stop", sender=dispatcher.Any)
        logger.debug('recognezed an activation keyword "%s"', keyword)
        try:
            self.communicate()
        except Exception as e:
            logger.exception(e)
            self.tts.speak(self.lang_pack.error_message)

    def communicate(self):
        self.speak(self.lang_pack.greeting_message, block=True)
        question = self.listen()
        logger.info("recognized: %s", question)
        if question:
            if question.strip().lower() in languages.stop_words:
                self.speak(self.lang_pack.ok, block=True)
                return

            self.speak(self.lang_pack.llm_query)
            self.hal.start_blink((0.5, 1))
            text = self.llm.ask(question)
            logger.info("LLM response: %s", text)

            if actions.run(text):
                return

        self.wait_for_activation_keyword()


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.start()
