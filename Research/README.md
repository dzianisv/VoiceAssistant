I recently decided to take on the task of building a voice assistant for my parents using a Raspberry Pi or Orangepi. Not only did I need a good text-to-speech (TTS) library, but I also needed something that would support Russian and Ukrainian, since that's what my parents speak. So, I set out on a journey to find the best TTS and speech-to-text (STT) libraries for Arm-enabled single board computers.

![Test device](./orangepi4-lts.webp)

# Text-to-Speech

## eSpeak

```bash
sudo apt install espeak
espeak  -vru "Привет, как дела?"
```
First, I tried eSpeak. 🙄 But let's just say that the quality was not up to my standards, so I moved on.

## Festival

Demo
```bash
sudo apt install festival festvox-ru
echo "Привет! Как дела?" | festival --tts --language russian
```


```bash
sudo apt install -yq pkg-config scons git

```

Next, I tried Festival 🎉. While the quality wasn't amazing, it was decent enough for me to understand.

## [RHVoice](https://github.com/RHVoice/RHVoice/blob/master/doc/ru/Compiling-on-Linux.md)

```bash
sudo apt install rhvoice rhvoice-russian
echo "Привет, как дела?" | RHVoice-client -s Elena | aplay
```

But then I found RHVoice.👌 This TTS library had better quality and sounded almost as good as TTS (my top pick).

## RHVoice + speech-dispatcher

Edit /etc/speech-dispatcher/speechd.conf
```conf
DefaultModule rhvoice
```

```bash
spd-say -o rhvoice -y aleksandr-hq "Привет, как дела?!"
```

With a linux `speech-dispatcher` interface it works even better, because you don't need to wait for a whole input "processing" and you hear shound immediately.


## [TTS](https://github.com/coqui-ai/TTS)

```bash
pip3 install TTS
tts "Hello, world"
paplay output.wav
```

The best quality, almost realtime on OrangePi4, but doesn't have good Russian models.

## Conclusion

I also tried Azure Speech Services, but it took a few weeks to make it work on latest Armbian/aarch64. Also, Microsoft library doesn't support arvm7 for python modules, so this is not an option. Therefore my choice is `rhvoice`.

# Speech Recognition

## Cloud Speech Recognition

Cloud Speech Services

|Service Name            | Free tier h/month|
|------------------------|------------------|
|Azure Speech Services   | 5h               |
|Google Cloud            | 1h               |
|IBM Cloud               |                  |



https://pypi.org/project/azure-cognitiveservices-speech/
https://github.com/Azure/azure-sdk-for-python/issues
# AI Speech-to-Text recognition libraries

| Name                      | Recognition time on RPi3 (speech duration/recogntion duration) |
|-----------                |--------------------------                                      |
|Mozilla Deep Speech Tflite | 2/10s|
|[Vosk-Api](https://github.com/alphacep/vosk-api)                  | 60/90s|
|Tensorflow ASR             |
|Whisper                    |

Finally, after testing a few different STT options, I settled on Vosk-Api. 🤘This library had a longer recognition time, but was still the best option for me since it had the best accuracy.
In conclusion, building a voice assistant takes a lot of research and testing, but finding the right TTS and STT libraries is key. Plus, making sure to support multiple languages is extremely important.


## Device Test

```bash

arecord -f S16_LE -r 44100 sample.wav
aplay sample.wav

```