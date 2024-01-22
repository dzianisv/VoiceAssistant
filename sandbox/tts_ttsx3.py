import pyttsx3


class TTS:
    def __init__(self):
        engine = pyttsx3.init("espeak")
        """ RATE"""
        rate = engine.getProperty("rate")  # getting details of current speaking rate
        print(rate)  # printing current voice rate
        engine.setProperty("rate", 125)  # setting up new voice rate

        """VOLUME"""
        volume = engine.getProperty(
            "volume"
        )  # getting to know current volume level (min=0 and max=1)
        print(volume)  # printing current volume level
        engine.setProperty("volume", 1.0)  # setting up volume level  between 0 and 1

        voices = engine.getProperty("voices")  # getting details of current voice
        # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
        engine.setProperty(
            "voice", voices[1].id
        )  # changing index, changes voices. 1 for female

        self.engine = engine

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
        return True
