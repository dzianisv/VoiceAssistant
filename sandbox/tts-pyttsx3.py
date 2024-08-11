import pyttsx3

tts = pyttsx3.init()

voices = tts.getProperty('voices')

# Задать голос по умолчанию

tts.setProperty('voice', 'ru')

# Попробовать установить предпочтительный голос

for voice in voices:
    print(voice.name)
    if voice.name == 'Elena':
        tts.setProperty('voice', voice.id)
        break

tts.say('Командный голос вырабатываю, товарищ генерал-полковник!')

tts.runAndWait()