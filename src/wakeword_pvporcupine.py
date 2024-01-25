import os
import logging
import sys
import enum


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

# TODO: it can't mix keywords and keyword_paths
# keywords_en = ["bumblebee", "blueberry", "jarvis", "ok google", "hey siri", "alexa", "please stop"],
# porcupine_en = pvporcupine.create(
#     access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
#     keywords= keywords_en[:-1],
#     keyword_paths=[
#          os.path.join(os.path.dirname(__file__), "please-stop_en_arm.ppn"),
#     ]
# )

actions_ru = [KeywordSpottingActions.HEY, KeywordSpottingActions.STOP]
keywords_ru = ["товарищ", "отмена"]
porcupine_ru = pvporcupine.create(
    access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
    keyword_paths=[
        os.path.join(os.path.dirname(__file__), "Товарищ_ru_arm.ppn"),
        os.path.join(os.path.dirname(__file__), "отмена_ru_arm.ppn"),
    ],
    model_path=os.path.join(os.path.dirname(__file__), "porcupine_params_ru.pv"),
)


class Model:
    recognizer = porcupine_ru
    keywords = keywords_ru
    actions = actions_ru


model = Model


def wait():
    try:
        recorder = PvRecorder(
            device_index=-1, frame_length=model.recognizer.frame_length
        )
        recorder.start()
        while True:
            audio_frame = recorder.read()
            keyword_index = model.recognizer.process(audio_frame)
            if keyword_index > -1:
                logger.info('detected keyword "%s"', model.keywords[keyword_index])
                return model.actions[keyword_index]
    finally:
        recorder.stop()
        recorder.delete()
