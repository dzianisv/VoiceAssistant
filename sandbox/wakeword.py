#!/usr/bin/env python3

import openwakeword

import sounddevice as sd
import os
import numpy as np
import time
from openwakeword.model import Model
import pyaudio
import wave

MAX_FRAME=500


def wait_for_wakeup_word():
    oww_model = Model(enable_speex_noise_suppression=True)
    mic_stream = audio_device.open(format=FORMAT, channels=CHANNELS, input_device_index=pyaudio_device_index, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while True:
        audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
        oww_model.predict(audio)
        print(oww_model.prediction_buffer)
        if oww_model.prediction_buffer['alexa'][-1] > 0.5:
            return True

    mic_stream.stop_stream()
    mic_stream.close()

if __name__ == "__main__":
    wait_for_wakeup_word()