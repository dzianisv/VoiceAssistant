from gtts import gTTS
from io import BytesIO
import os
import subprocess
import tempfile


"""https://gtts.readthedocs.io/en/latest/"""

def find_in_path(name: str):
    for d in os.getenv("PATH").split(":"):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p

    return None

def find_player():
    for player in ["play"]:
        if find_in_path(player):
            return player

    return None

def play(filename: str):
    external_player = find_player()
    if external_player:
        subprocess.call([external_player, filename])
    else:
        import pygame
        pygame.init()
        pygame.mixer.init()

        sound = pygame.mixer.Sound("speech.mp3")
        channel = sound.play()
        while channel.get_busy():
            pygame.time.wait(1000)
        pygame.quit()

class TTS:
    def __init__(self, lang='en'):
        self.lang = lang
        self.workdir = tempfile.mkdtemp()
        self.workfile = os.path.join(self.workdir, "speech.mp3")

    def speak(self, text):
        stream = BytesIO()
        tts = gTTS(text, lang=self.lang)
        # tts.write_to_fp(stream)
        tts.save(self.workfile)
        play(self.workfile)
        os.unlink(self.workfile)
        return True