import os

# https://github.com/openai/openai-python
import openai
import azure.cognitiveservices.speech as speechsdk
import logging
import string
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("plato")
logger.setLevel(logging.DEBUG)


@dataclass
class SpeechConfiguration:
    speech_recognition_language: str
    activation_keyword: str
    activation_keyword_model_file: str
    voice_name: str
    greeting_message: str
    suspend_message: str
    actor: str

# https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=stt#text-to-speech
# ru-RU-SvetlanaNeural
# ru-RU-DariyaNeural
# ru-RU-DmitryNeural
# en-US-GuyNeural
plato_speech_configuration = SpeechConfiguration("en-US", "Hey Plato", "HeyPlato.table", "en-US-GuyNeural", "How can I help?!", "I am going to sleep, feel free to wake up me when you need my assistance", "Act like you are stoic philosopher and your are Plato philosoper")
ru_speech_configuration_2 = SpeechConfiguration("ru-RU", "Hey Claudia", "HeyClaudia.table", "ru-RU-SvetlanaNeural", "Приветик, как я могу помочь?", "Я пойду вздремну, разбуди меня когда тебе станет скучно, котик", "Act like you are Sarah Connor")
ru_speech_configuration = SpeechConfiguration("ru-RU", "Hey Claudia", "HeyClaudia.table", "ru-RU-DmitryNeural", "Приветик, как я могу помочь?", "Я пойду вздремну, разбуди меня когда тебе станет скучно, котик", "Act like you Сергей Есенин")


speech_configuration = ru_speech_configuration


speech_key = os.environ.get("AZURE_SPEECH_KEY")
service_region = os.environ.get("AZURE_REGION")

# Creates an instance of a speech config with specified subscription key and service region.
# https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig?view=azure-python
speech_config = speechsdk.SpeechConfig(
    speech_recognition_language=speech_configuration.speech_recognition_language,
    subscription=speech_key,
    region=service_region
)
# Note: the voice setting will not overwrite the voice element in input SSML.
# Sets voice, there are many to choose from in Azure Speech Studio
speech_config.speech_synthesis_voice_name = speech_configuration.voice_name
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_config
)

def speak(text) -> bool:
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    future = speech_synthesizer.speak_text_async(text).get()
    return future.reason == speechsdk.ResultReason.SynthesizingAudioCompleted


def listen() -> str:
    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechrecognizer?view=azure-python
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.resultreason?view=azure-python#azure-cognitiveservices-speech-resultreason-recognizedspeech
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text

    return None


class AI(object):
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_KEY")
        self.context = []
        self.system_context = [
            {"role": "system", "content": "Don't say that you are an AI model"},
            {
                "role": "system",
                "content": speech_configuration.actor,
            },
        ]
        self.model = "gpt-3.5-turbo"
        self.tokens_limit = 4096
        self.tokens = 0
        for msg in self.system_context:
            self.tokens += self.estimate_tokens(msg["content"])

    @staticmethod
    def estimate_tokens(text):
        words = 0
        spaces = 0
        punctuation_marks = 0

        # Count words and spaces
        for index, char in enumerate(text):
            if char == " ":
                spaces += 1
                if index > 0 and text[index - 1] != " ":
                    words += 1
            elif char in string.punctuation:
                punctuation_marks += 1

        # Count the last word if the text does not end with a space
        if len(text) > 0 and text[-1] != " ":
            words += 1

        # https://gptforwork.com/guides/openai-gpt3-tokens
        # In English: 1 word ≈ 1.3 tokens
        # In Spanish: 1 word ≈ 2 tokens
        # In French: 1 word ≈ 2 tokens
        # Punctuation marks (,:;?!) = 1 token
        # Special characters (∝√∅°¬) = 1 to 3 tokens
        # Emojis (😁🙂🤩) = 2 to 3 tokens
        return words * 2 + spaces + punctuation_marks


    def ask(self, prompt):
        # remove conetxt when tokens limit is reached
        estimated_tokens = self.estimate_tokens(prompt)
        if estimated_tokens > self.tokens_limit:
            # TODO: truncate question?
            logger.error("Message is too long")
            return None

        self.tokens += estimated_tokens
        while self.tokens_limit < self.tokens:
            self.tokens -= self.estimate_tokens(self.context.pop(0)["message"])

        self.context.append({"role": "user", "content": prompt})

        messages = []
        messages.extend(self.system_context)
        messages.extend(self.context)


        ai_response = openai.ChatCompletion.create(
            model=self.model,
            # max_tokens: the maximum number of words or parts of words (tokens) the assistant is allowed to use in its response
            max_tokens=500,
            # temperature: controls how creative or random the digital assistant’s responses will be. A lower number (like 0.05) means the assistant will be more focused and consistent, while a higher number would make the assistant more creative and unpredictable
            temperature=0.7,
            messages=messages,
        )
        # Get response
        # {
        #     "id": "chatcmpl-6viHI5cWjA8QWbeeRtZFBnYMl1EKV",
        #     "object": "chat.completion",
        #     "created": 1679212920,
        #     "model": "gpt-4-0314",
        #     "usage": {
        #         "prompt_tokens": 21,
        #         "completion_tokens": 5,
        #         "total_tokens": 26
        #     },
        #     "choices": [
        #         {
        #             "message": {
        #                 "role": "assistant",
        #                 "content": "GPT-4 response returned here"
        #             },
        #             "finish_reason": "stop",
        #             "index": 0
        #         }
        #     ]
        # }

        # Self response for context
        self.context.append(ai_response["choices"][0]["message"])

        response_text = ai_response["choices"][0]["message"]["content"].strip()
        logger.debug("Got the OpenAI response: %s", ai_response)
        return response_text


ai = AI()


def communicate():
    text = speech_configuration.greeting_message
    while speak(text):
        logger.info("Listening...")
        question = listen()
        if question:
            logger.info("Recognized %s, quering OpenAI", question)
            text = ai.ask(question)
            if not text:
                text = "Sorry, I can't answer your question"

            logger.info("AI response: %s", text)
        else:
            break

    speak(
        speech_configuration.suspend_message
    )
    listen_for_activation_keyword()


def listen_for_activation_keyword():
    """runs keyword spotting locally, with direct access to the result audio"""

    # Creates an instance of a keyword recognition model. Update this to
    # point to the location of your keyword recognition model.
    model = speechsdk.KeywordRecognitionModel(speech_configuration.activation_keyword_model_file)
    # The phrase your keyword recognition model triggers on, matching the keyword used to train the above table.

    # Create a local keyword recognizer with the default microphone device for input.
    keyword_recognizer = speechsdk.KeywordRecognizer()
    done = False

    def recognized_cb(evt):
        # Only a keyword phrase is recognized. The result cannot be 'NoMatch'
        # and there is no timeout. The recognizer runs until a keyword phrase
        # is detected or recognition is canceled (by stop_recognition_async()
        # or due to the end of an input file or stream).
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            logger.info("Recognized the activation keyword: %s".format(result.text))
        nonlocal done
        done = True

    def canceled_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.Canceled:
            logger.info("Canceled: {}".format(result.cancellation_details.reason))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the keyword recognizer.
    keyword_recognizer.recognized.connect(recognized_cb)
    keyword_recognizer.canceled.connect(canceled_cb)

    logger.info('Waiting for the activation keyword: "%s"', speech_configuration.activation_keyword)
    # Start keyword recognition.
    result = keyword_recognizer.recognize_once_async(model).get()

    # Read result audio (incl. the keyword).
    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        logger.debug("recognezed an activation keyword")
        communicate()


if __name__ == "__main__":
    # listen_for_activation_keyword()
    communicate()
