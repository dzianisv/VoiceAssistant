import os
import openai
import azure.cognitiveservices.speech as speechsdk
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

keyword = "Hey Plato"

def keyword_from_microphone():

    """runs keyword spotting locally, with direct access to the result audio"""
    # Creates an instance of a keyword recognition model. Update this to
    # point to the location of your keyword recognition model.
    model = speechsdk.KeywordRecognitionModel("dd238e75-10d4-4c44-a691-9098aeac7e28.table")
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
            logger.info("RECOGNIZED KEYWORD: {}".format(result.text))
        nonlocal done
        done = True

    def canceled_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.Canceled:
            logger.info('CANCELED: {}'.format(result.cancellation_details.reason))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the keyword recognizer.
    keyword_recognizer.recognized.connect(recognized_cb)
    keyword_recognizer.canceled.connect(canceled_cb)

    # Start keyword recognition.
    result_future = keyword_recognizer.recognize_once_async(model)
    print('Clippy is ready to help...'.format(keyword))
    result = result_future.get()

    # Read result audio (incl. the keyword).
    if result.reason == speechsdk.ResultReason.RecognizedKeyword:
        logger.debug('recognezed keyword')


def Responding_To_KW():
   #Creates an instance of a speech config with specified subscription key and service region.
   speech_key = os.environ.get("AZURE_SPEECH_KEY")
   service_region = os.environ.get("AZURE_REGION")
   speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
   # Note: the voice setting will not overwrite the voice element in input SSML.
   # Sets voice, there are many to choose from in Azure Speech Studio
   speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"
    #Responds
   text = "How can I help?"

   # use the default speaker as audio output.
   speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

   result = speech_synthesizer.speak_text_async(text).get()
   # Check result
   if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        # Get from mic
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            logger.info("Recognized: {}".format(speech_recognition_result.text))

            #Send question as prompt to ChatGPT
            openai.api_key = os.environ.get("OPENAI_KEY")
            completion_request = openai.Completion.create(
                engine="text-davinci-003",                  #Here's where you pick which model to use
                prompt=(speech_recognition_result.text),    #Here's where you can adjust your prompt
                max_tokens=100,                             #Max number of tokens used
                temperature=0.6,                            #Lower is more specific, higher is more creative responses
                frequency_penalty=0,                        #Adjusts how much the frequency of tokens in the source inmfluences outputs
                presence_penalty=0.6,                       #Lowers the probability of a word if it already appeared before
            )

            #Get response
            response_text = completion_request["choices"][0]["text"]
            print(response_text)

            #Say response
            speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"
            text = response_text
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            result = speech_synthesizer.speak_text_async(text).get()
            #Go back
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                keyword_from_microphone()

keyword_from_microphone()