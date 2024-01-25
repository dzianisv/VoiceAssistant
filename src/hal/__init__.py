

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
        from orangepipc import OrangePiPcHal
        return OrangePiPcHal()
    except ImportError:
        return DummyHal()