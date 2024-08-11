#!/usr/bin/env python3

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
♪ Где же моя темноглазая где
В Вологде-где-где-где, в Вологде где
В доме, где резной палисад ♪
"""

# https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c
# v2/ru_speaker_5
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("output.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
Audio(audio_array, rate=SAMPLE_RATE)
