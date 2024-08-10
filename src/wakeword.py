#!/usr/bin/env python3

import pyaudio
import numpy as np
from openwakeword.model import Model
import argparse


# Get microphone stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = args.chunk_size
audio = pyaudio.PyAudio()
mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)



class Wakeword:
    def __init__(self, inference_framework = 'tflite', model_path = ''):
        # Load pre-trained openwakeword models
        if len(model_path) > 0:
            self.owwModel = Model(wakeword_models=[model_path], inference_framework=inference_framework)
        else:
            self.owwModel = Model(inference_framework=inference_framework)

        self.n_models = len(self.owwModel.models.keys())


    def wait(self):
        while True:
            # Get audio
            audio = np.frombuffer(self.mic_stream.read(CHUNK), dtype=np.int16)
            # Feed to openWakeWord model
            prediction = self.owwModel.predict(audio)
            for mdl in self.owwModel.prediction_buffer.keys():
                # Add scores in formatted table
                scores = list(self.owwModel.prediction_buffer[mdl])
                print(scores)


def main():
    # Parse input arguments
    parser=argparse.ArgumentParser()
    parser.add_argument(
        "--model_path",
        help="The path of a specific model to load",
        type=str,
        default="",
        required=False
    )
    parser.add_argument(
        "--inference_framework",
        help="The inference framework to use (either 'onnx' or 'tflite'",
        type=str,
        default='tflite',
        required=False
    )

    args=parser.parse_args()
    predictor = Wakeword(args.inference_framework, args.model_path)
    predictor.wait()

# Run capture loop continuosly, checking for wakewords
if __name__ == "__main__":
    main()