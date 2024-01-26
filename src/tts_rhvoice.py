import subprocess
import os
import threading
from languages import detect_language

class TTS:
    def __init__(self):
        """
        @args:
            profile - you can list available profiles by `ls /usr/share/RHVoice/voices/`
            alan  aleksandr  aleksandr-hq  anna  arina  artemiy  bdl  clb  elena  evgeniy-eng  evgeniy-rus  irina  lyubov  mikhail  pavel  slt  tatiana  victoria  vitaliy  yuriy
        """

    def speak(self, text: str, block=True):
        lang_code = detect_language(text)
        if lang_code == 'ru':
            profile = 'tatiana'
        else:
            profile = 'evgeniy-eng'
    
        # for some reason it drops a few first words
        with open(os.devnull, "wb") as devnull:
            p = subprocess.Popen(["RHVoice-test", "--profile", profile], stdin=subprocess.PIPE, stdout=devnull, stderr=devnull)
        p.communicate(input=text.encode('utf8'))
        if block:
            p.wait()
            return p.returncode == 0
        else:
            threading.Thread(target=p.wait).start()
            return True
