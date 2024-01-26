#!/usr/bin/env python3

import os
import sys
import logging
import string
import time
import threading
from dataclasses import dataclass
from pydispatch import dispatcher

logger = logging.getLogger("assistant")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

import skills
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

        self.event = threading.Event()
        self.thinking_thread = threading.Thread(target=self.thinking_process)
        self.question = None

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

    def run(self):
        self.thinking_thread.start()

        while True:
            self.wait_for_activation_keyword()
            try:
                self.communicate()
            except Exception as e:
                logger.exception(e)
                self.tts.speak(self.lang_pack.error_message)

    def wait_for_activation_keyword(self):
        self.hal.start_blink((0.3, 10))
        logger.info("Waiting for the wake word...")
        keyword = self.wakeword.wait()
        logger.debug('recognezed an activation keyword "%s"', keyword)
        dispatcher.send(signal="stop", sender=dispatcher.Any)

    def communicate(self):
        # todo: mutex
        self.question = (
            None  # reset question, this var is used in self.thinking_process()
        )
        self.event.clear()

        self.speak(self.lang_pack.greeting_message, block=True)
        question = self.listen()
        logger.info("recognized: %s", question)
        if question:
            if question.strip().lower() in languages.stop_words:
                self.speak(self.lang_pack.ok, block=True)
                return

            # todo: mutex
            self.question = question
            self.event.set()

    def thinking_process(self):
        while True:
            self.event.wait()
            question = self.question
            self.event.clear()

            self.speak(self.lang_pack.llm_query)
            self.hal.start_blink((0.5, 1))
            text = self.llm.ask(question)

            if (
                self.question != question
            ):  # event is not set, looks like a new question is there
                continue

            logger.info("LLM response: %s", text)

            if skills.run(text):
                return

            self.speak(text)


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
