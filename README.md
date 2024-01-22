## Installation
```sh
curl "https://raw.githubusercontent.com/dzianisv/AssistantPlato/main/scripts/install.sh" | bash -x
```

## Development

1. Copy `env` to `.env` and set the API keys in `.env`
4. `pipenv run python src/main.py`
5. Have fun!


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


## Troubleshooting

1. You have hit your assigned rate limit.
> openai.error.RateLimitError: You exceeded your current quota, please check your plan and billing details.
RateLimitError	Cause: You have hit your assigned rate limit.
Solution: Pace your requests. Read more in our rate limit guide.

2.  [`synthesizer_create_speech_synthesizer_from_config+0x10c` crash](https://github.com/Azure-Samples/cognitive-services-speech-sdk/issues/1969)
> cognitiveservices/speech/libMicrosoft.CognitiveServices.Speech.core.so(synthesizer_create_speech_synthesizer_from_config+0x10c) [0xffff7df6f9f8]
/lib/aarch64-linux-gnu/libffi.so.8(+0x6e10) [0xffff7e3d6e10]
/lib/aarch64-linux-gnu/libffi.so.8(+0x3a94) [0xffff7e3d3a94]
/usr/lib/python3.10/lib-dynload/_ctypes.cpython-310-aarch64-linux-gnu.so(+0x12b10) [0xffff7e402b10]
[CALL STACK END]

```bash
wget "http://ports.ubuntu.com/ubuntu-ports/pool/main/o/openssl/libssl1.1_1.1.1-1ubuntu2.1~18.04.23_arm64.deb"
dpkg -i ./libssl1.1_1.1.1-1ubuntu2.1~18.04.23_arm64.deb
```


2. Pulseaudio

```bash
pactl list sources | grep "Name:"
# Name: alsa_output.platform-es8316c-card.stereo-fallback.monitor
# Name: alsa_input.platform-es8316c-card.stereo-fallback
# Name: alsa_output.platform-hdmi-sound.stereo-fallback.monitor
device=alsa_input.platform-es8316c-card.stereo-fallback
parec --device ${device} --format=s16le --channels=2 --rate=44100 --file-format=wav output.wav
paplay output.wav

paplay /usr/share/sounds/alsa/Front_Right.wav
paplay /usr/share/sounds/alsa/Front_Left.wav
```

# Sandbox

## wakeword

```shell
apt-get install libspeexdsp-dev portaudio
```
