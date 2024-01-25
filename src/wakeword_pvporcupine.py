import os

import pvporcupine
from pvrecorder import PvRecorder

""">>> print(pvporcupine.KEYWORDS)
{'pico clock', 'hey google', 'grapefruit', 'picovoice', 'blueberry', 'ok google', 'jarvis', 'hey siri', 'bumblebee', 'alexa', 'hey barista', 'grasshopper', 'porcupine', 'americano', 'computer', 'terminator'}
>>> """

keywords_en = ["bumblebee", "blueberry", "jarvis", "please stop"],
porcupine_en = pvporcupine.create(
    access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
    keywords= keywords_en,
    keyword_paths=[
         os.path.join(os.path.dirname(__file__), "please-stop_en_arm.ppn"),
    ]
)

# ru_keywords = ["товарищ", "отмена"]
# porcupine_ru = pvporcupine.create(
#     access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
#     keyword_paths=[
#         os.path.join(os.path.dirname(__file__), "Товарищ_ru_arm.ppn"),
#         os.path.join(os.path.dirname(__file__), "отмена_ru_arm.ppn"),
#     ],
#     model_path=os.path.join(os.path.dirname(__file__), "porcupine_params_ru.pv"),
# )

class Model:
    recognizer = porcupine_en
    keywords = keywords_en

model = Model

def wait():
    try:
        recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
        recorder.start()
        while True:
            audio_frame = recorder.read()
            keyword_index = model.recognizer.process(audio_frame)
            if keyword_index > -1:
                return mode.keywords[keyword_index]
    finally:
        recorder.stop()
        recorder.delete()
