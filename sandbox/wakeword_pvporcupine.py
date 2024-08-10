import os
import logging
import sys
import enum
import dataclasses


class KeywordSpottingActions(enum.Enum):
    HEY = "hey"
    STOP = "stop"


# initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))


import pvporcupine
from pvrecorder import PvRecorder

""">>> print(pvporcupine.KEYWORDS)
{'pico clock', 'hey google', 'grapefruit', 'picovoice', 'blueberry', 'ok google', 'jarvis', 'hey siri', 'bumblebee', 'alexa', 'hey barista', 'grasshopper', 'porcupine', 'americano', 'computer', 'terminator'}
>>> """


@dataclasses.dataclass
class Model:
    recognizer: None
    keywords: list
    actions: list


class WakeWord:
    def __init__(self, lang="en"):
        if lang == "en":
            keywords = ["bumblebee", "blueberry", "jarvis", "ok google", "hey siri", "alexa"]
            actions = [KeywordSpottingActions.HEY for _ in range(len(keywords))]
            recognizer = pvporcupine.create(
                access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
                keywords=keywords,
            )
        elif lang == "ru":
            actions = [KeywordSpottingActions.HEY, KeywordSpottingActions.STOP]
            keywords = ["товарищ", "отмена"]
            recognizer = pvporcupine.create(
                access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
                keyword_paths=[
                    os.path.join(os.path.dirname(__file__), "Товарищ_ru_arm.ppn"),
                    os.path.join(os.path.dirname(__file__), "отмена_ru_arm.ppn"),
                ],
                model_path=os.path.join(
                    os.path.dirname(__file__), "porcupine_params_ru.pv"
                ),
            )
        else:
            raise Exception("Not supported language")

        self.model = Model(keywords=keywords, actions=actions, recognizer=recognizer)

    def wait(self):
        try:
            recorder = PvRecorder(
                device_index=-1, frame_length=self.model.recognizer.frame_length
            )
            recorder.start()
            while True:
                audio_frame = recorder.read()
                keyword_index = self.model.recognizer.process(audio_frame)
                if keyword_index > -1:
                    logger.info(
                        'detected keyword "%s"', self.model.keywords[keyword_index]
                    )
                    return self.model.actions[keyword_index]
        finally:
            recorder.stop()
            recorder.delete()
