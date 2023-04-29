import os

# https://github.com/openai/openai-python
import openai
import azure.cognitiveservices.speech as speechsdk
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("plato")
logger.setLevel(logging.DEBUG)


activation_keyword_model_file = "HeyPlato.table"
activation_keyword = "Hey Plato"

speech_key = os.environ.get("AZURE_SPEECH_KEY")
service_region = os.environ.get("AZURE_REGION")

# Creates an instance of a speech config with specified subscription key and service region.
# https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig?view=azure-python
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
# Sets voice, there are many to choose from in Azure Speech Studio
speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_config
)


def speak(text) -> bool:
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    future = speech_synthesizer.speak_text_async(text).get()
    return future.reason == speechsdk.ResultReason.SynthesizingAudioCompleted


class AI(object):
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_KEY")
        self.context = []

    def ask(self, prompt):
        # ai_response = openai.Completion.create(
        #     engine="text-davinci-003",                  #Here's where you pick which model to use
        #     prompt=prompt,    #Here's where you can adjust your prompt
        #     max_tokens=100,                             #Max number of tokens used
        #     temperature=0.6,                            #Lower is more specific, higher is more creative responses
        #     frequency_penalty=0,                        #Adjusts how much the frequency of tokens in the source inmfluences outputs
        #     presence_penalty=0.6,                       #Lowers the probability of a word if it already appeared before
        # )
        # https://platform.openai.com/docs/models/model-endpoint-compatibility
        self.context.append({"role": "user", "content": prompt})

        messages = [
            {"role": "system", "content": "Don't say that you are an AI model"},
            {
                "role": "system",
                "content": "Act like you are human and philosopher Platon",
            },
        ]
        messages.extend(self.context)

        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # max_tokens: the maximum number of words or parts of words (tokens) the assistant is allowed to use in its response
            max_tokens=100,
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


def listen() -> str:
    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechrecognizer?view=azure-python
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.resultreason?view=azure-python#azure-cognitiveservices-speech-resultreason-recognizedspeech
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text

    return None


def communicate():
    text = "How can I help?"
    while speak(text):
        logger.info("Listening...")
        question = listen()
        if question:
            logger.info("Recognized %s, quering OpenAI", question)
            text = ai.ask(question)
            logger.info("AI response: %s", text)
        else:
            break

    speak(f"I am going to sleep. Feel free to wake up saying {activation_keyword}... Have a wonderful day")
    listen_for_activation_keyword()


def listen_for_activation_keyword():
    """runs keyword spotting locally, with direct access to the result audio"""

    # Creates an instance of a keyword recognition model. Update this to
    # point to the location of your keyword recognition model.
    model = speechsdk.KeywordRecognitionModel(activation_keyword_model_file)
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

    logger.info('Waiting for the activation keyword: "%s"', activation_keyword)
    # Start keyword recognition.
    result = keyword_recognizer.recognize_once_async(model).get()

    # Read result audio (incl. the keyword).
    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        logger.debug("recognezed an activation keyword")
        communicate()


if __name__ == "__main__":
    # listen_for_activation_keyword()
    communicate()
