from langdetect import detect

class RuLanguagePack:
    llm_query = "Подождите, сейчас узнаю..."
    greeting_message = "Как я могу помочь тебе?"
    iam_on = "Я включился!"
    ok = "Окей"
    
    google_stt_lang = 'ru-RU'
    google_tts_lang = 'ru'
    
class EnLanguagePack:
    llm_query = "Wait a little bit..."
    greeting_message = "How I can help you?"
    iam_on = "I am available!"
    ok = "OK!"
    
    google_stt_lang = 'en-US'
    google_tts_lang = 'en'
    

lang_packs = {
    'ru': RuLanguagePack,
    'en': EnLanguagePack
}

stop_words = set(["забудь", "проехали", "отмена", "стоп", "stop", "cancel", "never mind"])

def detect_language(input_text):
    # Check if input_text is not a string or is empty
    if not isinstance(input_text, str) or not input_text.strip():
        raise ValueError("Input text must be a non-empty string.")

    try:
        # Detect the language of the input text
        language_code = detect(input_text)
    except:
        raise Exception("Language detection failed.")

    # Return 'ru' if Russian is detected, 'en' if English is detected, or None otherwise
    if language_code == 'ru':
        return 'ru'
    elif language_code == 'en':
        return 'en'
    else:
        return 'en'
    

