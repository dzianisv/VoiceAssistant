import subprocess


class TTS:
    def __init__(self, profile: str = "tatiana"):
        """
        @args:
            profile - you can list available profiles by `ls /usr/share/RHVoice/voices/`
        """
        # TODO: find RHVoice binary
        # install rhvoice rhvoice-english rhvoice-russian if required
        self.profile = profile

    def speak(self, text: str):
        p = subprocess.Popen(["RHVoice-test", "--profile", self.profile], stdin=subprocess.PIPE)
        p.communicate(input=text)
        p.wait()
        return p.returncode == 0
