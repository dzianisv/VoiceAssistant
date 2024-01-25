import os

import pvporcupine
from pvrecorder import PvRecorder

""">>> print(pvporcupine.KEYWORDS)
{'pico clock', 'hey google', 'grapefruit', 'picovoice', 'blueberry', 'ok google', 'jarvis', 'hey siri', 'bumblebee', 'alexa', 'hey barista', 'grasshopper', 'porcupine', 'americano', 'computer', 'terminator'}
>>> """


porcupine = pvporcupine.create(
  access_key=os.getenv("PVPORCUPINE_ACCESS_KEY"),
  keywords=["bumblebee", "blueberry", "jarvis"]
#   keyword_paths=[os.path.join(os.path.dirname(__file__), 'Товарищ_ru.ppn')],
#   model_path=os.path.join(os.path.dirname(__file__), 'porcupine_params_ru.pv'),
)

def wait():
    try:
        recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
        recorder.start()
        while True:
            audio_frame = recorder.read()
            keyword_index = porcupine.process(audio_frame)
            if keyword_index > 0:
                return True
    finally:
        recorder.stop()
        recorder.delete()
        