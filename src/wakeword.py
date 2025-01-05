import logging
import dataclasses

from microwakeword import inference
import logging
import logging
import pyaudio
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)

SAMPLE_RATE=16000
sliding_window_average_size = 10
probability_cutoff = 0.5
# Buffer to store the previous 3 samples of audio
read_buffer_size = int(SAMPLE_RATE * 0.5)
rolling_buffer_size = 3 * read_buffer_size
rolling_buffer = np.zeros(rolling_buffer_size, dtype=np.int16)


# Initialize logger
logger = logging.getLogger(__name__)

@dataclasses.dataclass
class Model:
    recognizer: None
    keywords: list
    actions: list

class WakeWord:
    def __init__(self, lang="en"):
        self.model = inference.Model(tflite_model_path='wakeword_models/alexa.tflite')
        self.p = pyaudio.PyAudio()
        
    
    def wait(self):
        stream = self.p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=SAMPLE_RATE,
                            input=True,
                            frames_per_buffer=SAMPLE_RATE)

 
        try:
            while True:
                # Read audio data from the stream
                
                audio_data = stream.read(read_buffer_size)
                # Convert audio data to numpy array
                current_data = np.frombuffer(audio_data, dtype=np.int16)

                # Update the rolling buffer with the current data
                rolling_buffer = np.roll(rolling_buffer, -read_buffer_size)
                rolling_buffer[-read_buffer_size:] = current_data

                # Predict using the rolling buffer
                probabilities = self.model.predict_clip(rolling_buffer)
                if any(map(lambda p: p > probability_cutoff, probabilities)):
                    rolling_buffer.fill(0)
                    return True
        
        except KeyboardInterrupt:
            logging.info("Stopping audio capture.")
        finally:
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            # Terminate PyAudio
            # self.p.terminate()
        