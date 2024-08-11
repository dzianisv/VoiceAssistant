import tts_rhvoice
import tts_gtts
import tts_realtimetts
import logging
import sys
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))


class FaultTolerantTTS:
    def __init__(self, engines):
        self.engines = engines
        self.fault_ts = 0
        self.idx = 0

    def speak(self, text, *args, **kwargs):
        if time.time() - self.fault_ts > 3600:
            self.idx = 0

        while True:    
            try:
                return self.engines[self.idx].speak(text, *args, **kwargs)
            except Exception as e:
                self.idx += 1
                if self.idx > len(self.engines):
                    self.idx = 0
                    raise Exception('All TTS engines failed...')
                logger.exception(e)
                self.fault_ts = time.time()
          

def createFaultTolerantTTS():
    return FaultTolerantTTS([tts_realtimetts.TTS(), tts_gtts.TTS(), tts_rhvoice.TTS()])
