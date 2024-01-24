
#!/usr/bin/env python3

import os
from pocketsphinx import LiveSpeech, get_model_path
import logging
import sys

# initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

# Set up the paths for the models
model_path = get_model_path()

def wait(keyword='hey wallee', threshold=1e-20):
    # Configuration for PocketSphinx
    config = {
        'verbose': False,
        'hmm': os.path.join(model_path, 'en-us', 'en-us'),
        'lm': False,
        'keyphrase': keyword,  # Your activation word here
        # You need to optimize it on desktop with a prerecorded audio file, see details from the tutorial
        # Threshold must be specified for every keyphrase. For shorter keyphrase you can use smaller thresholds like 1e-1, for longer threshold must be bigger, up to 1e-50. If your keyphrase is very long, larger than 10 syllables, it is recommended to split it and spot for parts separately. For the best accuracy it is better to have keyphrase with 3-4 syllables. Too short phrases are easily confused.
        # https://stackoverflow.com/questions/40138509/how-to-optimize-threshold-in-pocketsphinx-js
        'kws_threshold': threshold,
        'dic': os.path.join(os.path.dirname(__file__), "dict.txt")
    }
    # Create a live speech recognition object
    speech = LiveSpeech(**config)

    logger.info("waiting for activation keyword %s", config['keyphrase'])

    # Process audio chunk by chunk
    for phrase in speech:
        logger.debug("recognized \"%s\"", phrase)
        if config['keyphrase'] == str(phrase):
            return phrase

if __name__ == "__main__":
    while True:
        wait()