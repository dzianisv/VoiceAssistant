## Running

1. Copy `env` to `.env`
2. Retrieve OPENAI_KEY= from https://platform.openai.com/account/api-keys
3. Retrieve AZURE_SPEECH_KEY= and AZURE_REGION= from https://portal.azure.com/?quickstart=true#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/SpeechServices
4. `pipenv run python src/main.py`
5. Have fun!


## Cloud Speech Recognition

Cloud Speech Services

|Service Name            | Free tier h/month|
|------------------------|------------------|
|Azure Speech Services   | 5h               |
|Google Cloud            | 1h               |
|IBM Cloud               |                  |


## Speech-to-Text recognition libraries

| Name                      | Recognition time on RPi3 (speech duration/recogntion duration) |
|-----------                |--------------------------                                      |
|Mozilla Deep Speech Tflite | 2/10s|
|[Vosk-Api](https://github.com/alphacep/vosk-api)                  | 60/90s|
|Tensorflow ASR             |
|Whisper                    |