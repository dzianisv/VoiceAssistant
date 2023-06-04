## Installation
```sh
curl "https://raw.githubusercontent.com/dzianisv/AssistantPlato/main/scripts/install.sh" | bash -x
```

## Development

1. Copy `env` to `.env` and set the API keys in `.env`
4. `pipenv run python src/main.py`
5. Have fun!

# Research
## Cloud Speech Recognition

Cloud Speech Services

|Service Name            | Free tier h/month|
|------------------------|------------------|
|Azure Speech Services   | 5h               |
|Google Cloud            | 1h               |
|IBM Cloud               |                  |



https://pypi.org/project/azure-cognitiveservices-speech/
https://github.com/Azure/azure-sdk-for-python/issues
## Speech-to-Text recognition libraries

| Name                      | Recognition time on RPi3 (speech duration/recogntion duration) |
|-----------                |--------------------------                                      |
|Mozilla Deep Speech Tflite | 2/10s|
|[Vosk-Api](https://github.com/alphacep/vosk-api)                  | 60/90s|
|Tensorflow ASR             |
|Whisper                    |


## AI
[GPT explanation](https://www.datacamp.com/blog/what-we-know-gpt4)

> One objective benefit is that the GPT-4 API accepts a request with a context length of 8,192 tokens (12.5 pages of text) — this is 2x the context length of GPT-3.5.
> The GPT-4 API is 14x-29x more expensive than ChatGPT’s default model, gpt-3.5-turbo.
> The most difficult choice to make when deciding whether to use the GPT-4 API is pricing — as GPT-4 pricing works as follows:
prompt: $0.03 per 750 words (1k tokens)
completions: $0.06 per 750 words (1k tokens)
[Reference](https://medium.com/sopmac-ai/gpt-4-api-reference-guide-e4ba18bcbc5f)


### GPT system role

[Reference](https://community.openai.com/t/the-system-role-how-it-influences-the-chat-behavior/87353)


### Implementations
[Microsoft Converstational Speaker](https://github.com/microsoft/conversational-speaker)
[FrinedBot](https://www.hackster.io/484625/ai-conversation-speaker-aka-friend-bot-part-1-conversation-3adca1)
[Clippy](https://www.hackster.io/david-packman/clippygpt-6a683a#overview)
[Davinchi](https://www.hackster.io/devmiser/davinci-the-chatgpt-ai-virtual-assistant-you-can-talk-to-fd00fd)
[Azure OpenAI + Azure Speech Services](https://levelup.gitconnected.com/integrating-azure-openai-and-azure-speech-services-to-create-a-voice-enabled-chatbot-with-python-60a39f838367)
[Intune AI Voice Bot](https://jannikreinhard.com/2023/04/23/intune-ai-voice-bot/)


## Pulseaudio
pulsemixer
apt install systemd-container
machinectl shell user@ /bin/bash