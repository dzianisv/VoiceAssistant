
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))


class DummyHal:
    def __init__(self):
       pass

    def led_on(self):
        pass
    
    def led_off(self):
        pass
        
    def start_blink(self, interval):
        pass
    
    def stop_blink(self):
        pass
    

def detect():
    try:
        from .orangepipc import OrangePiPcHal
        return OrangePiPcHal()
    except ImportError as e:
        logger.warning("failed to load HAL package: %s", e)
        return DummyHal()