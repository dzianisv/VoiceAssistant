#!/usr/bin/env python3


# https://github.com/Jeremie-C/OrangePi.GPIO/blob/1ee758716799c57ec6179ab93d0bbfa8f25ac18d/source/common.h#L29C9-L29C17
import orangepi.pc
from OPi import GPIO
import threading
import time

# """GND 25 26 PA21 PA21 21"""
LED_PIN = 26
    
class OrangePiPcHal:
    def __init__(self):
        GPIO.setmode(orangepi.pc.BOARD)
        GPIO.setup(LED_PIN, GPIO.OUT) 
        self.blink_event = None

    def led_on(self):
        GPIO.output(LED_PIN, 1)
    def led_off(self):
        GPIO.output(LED_PIN, 0)
        
    def start_blink(self, interval):
        self.stop_blink()
        self.blink_event  = threading.Event()
        self.blink_thread = threading.Thread(target=self.blink, args=(interval, self.blink_event))
        self.blink_thread.start()
    
    def stop_blink(self):
        if self.blink_event:
            self.blink_event.set()
            self.blink_event = None

    def blink(self, interval, event):
        while not event.is_set():
            self.led_on()
            time.sleep(interval)
            self.led_off()
            time.sleep(interval)
    
if __name__ == "__main__":
    hal = OrangePiPcHal()
    hal.start_blink(3)
    hal.blink_thread.join()
        
