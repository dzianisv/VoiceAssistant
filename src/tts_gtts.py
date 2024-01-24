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
        # subprocess.run(["cvlc", "--play-and-exit", filename])
        subprocess.run(["play", filename])
    else:
        import pygame
        pygame.init()
        pygame.mixer.init()

        sound = pygame.mixer.Sound(filename)
        channel = sound.play()
        while channel.get_busy():
            pygame.time.wait(1000)
        pygame.quit()

class TTS:
    def __init__(self, lang='en', block=True):
        self.lang = lang
        self.workdir = os.path.join(os.getcwd(), 'gtts')
        
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

    def speak(self, text, block):
        should_be_cached = False
        
        if len (text) < 80:
            should_be_cached = True
            name = text
        else:
            name = text[:61] + "..."
            
        self.workfile = os.path.join(self.workdir, f"{name}.mp3")
        
        if os.path.exists(self.workfile):
            play(self.workfile)
            return True
        
        tts = gTTS(text, lang=self.lang)
        tts.save(self.workfile)
        play(self.workfile)
    
        if not should_be_cached:
            os.unlink(self.workfile)
    
        return True