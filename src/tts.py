import tts_rhvoice
import tts_gtts
import logging
import sys
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))


class FaultTollereantTTS():
    def __init__(self, tts, fallback_tts):
        self.tts = tts
        self.fallback_tts = fallback_tts
        self.fault_ts = 0

    def speak(self, text, block=True):
        while True:
            if time.time() - self.fault_ts < 3600:
                self.fallback_tts.speak(text, block)
            else:
                try:
                    return self.tts.speak(text, block)
                except Exception as e:
                    logger.exception(e)
                    self.fault_ts = time.time()
                    
def createFaultTollerantTTS():
    return FaultTollereantTTS(tts_gtts.TTS(), tts_rhvoice.TTS())
