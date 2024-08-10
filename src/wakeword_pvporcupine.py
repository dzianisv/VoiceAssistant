import os
import logging
import sys
import enum
import dataclasses
import platform

class KeywordSpottingActions(enum.Enum):
    HEY = "hey"
    STOP = "stop"

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

import pvporcupine
from pvrecorder import PvRecorder

@dataclasses.dataclass
class Model:
    recognizer: None
    keywords: list
    actions: list

class WakeWord:
    def __init__(self, lang="en"):
        arch = platform.machine()
        system = platform.system()
        model_dir = os.path.join(os.path.dirname(__file__), "wakeword_models")

        if lang == "en":
            keywords = ["bumblebee", "blueberry", "jarvis", "ok google", "hey siri", "alexa"]
            actions = [KeywordSpottingActions.HEY for _ in range(len(keywords))]
            recognizer = pvporcupine.create(
                access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
                keywords=keywords,
            )
        elif lang == "ru":
            keywords = ["товарищ"]
            actions = [KeywordSpottingActions.HEY]

            if system == "Darwin":  # macOS
                keyword_paths = [
                    os.path.join(model_dir, "товарищ_ru_mac_v3_0_0.ppn"),
                ]
            elif arch in ["arm", "armv7l"]:
                keywords.append("отмена")
                actions.append(KeywordSpottingActions.STOP)
                keyword_paths = [
                    os.path.join(model_dir, "Товарищ_ru_arm.ppn"),
                    os.path.join(model_dir, "отмена_ru_arm.ppn"),
                ]
            else:
                raise Exception(f"Unsupported architecture: {arch}")

            recognizer = pvporcupine.create(
                access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
                keyword_paths=keyword_paths,
                model_path=os.path.join(model_dir, "porcupine_params_ru.pv"),
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