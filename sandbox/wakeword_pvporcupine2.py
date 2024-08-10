#!/usr/bin/env python3

import pvporcupine
import pyaudio
import struct

def detect_wake_word():
    # Initialize Porcupine engine
    try:
        porcupine = pvporcupine.create(keywords=["jarvis"])
    except pvporcupine.PorcupineInvalidArgumentError as e:
        print("Failed to initialize Porcupine with 'hey jarvis':", e)
        return False
    except pvporcupine.PorcupineActivationError as e:
        print("Failed to activate Porcupine with 'hey jarvis':", e)
        return False

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for 'hey jarvis'...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm_unpacked)
            if keyword_index >= 0:
                print("'hey jarvis' detected")
                return True

    except KeyboardInterrupt:
        print("Stopping wake word detection")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()

# Example usage
if detect_wake_word():
    print("Wake word detected, proceeding with tasks...")
else:
    print("Wake word not detected.")