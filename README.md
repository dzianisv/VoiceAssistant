## Intro

This is ChatGPT powered Voice Assistant. You probably found a lot projects like this. What do you think I created one more?

1. I needed an assistant that could work on armv7. A lot of projects was designed for arm64. For instance Microsoft Speech Services python library is not available for armv7. 
2. I needed an assistant that can play music from youtube and tell me the weather.
3. I need an assistant that supports English, Russian and Ukranian.
4. I tried to install OpenVoiceOS and Mycroft on armv7 orangepipc, but a lot of components are not available out of the box.

## How first prototype looks like
![](Research/orangepipc1.webp)

## Components

- rhvoice.org - Text-to-Speech
- SpeechRecognition - Speech-to-Text (google)
- langchains + langchains_openai
- yt-dlp for streaming from youtube
- openweathermap API


## Run & Debug
Disclaimer: This is erly stages sofware and tested only on OrangePiPc

- Install Armbian on the Single Board Computer and ssh to it
- Copy rsync the installation scripts and `src/` to /opt/VoiceAssistant/ (you can use script scripts/sync-code.sh)
- Set api keys in .env file /opt/VoiceAssistant/.env
- `/opt/VoiceAssistant/install-dependencies.sh` - this script will install all the dependencies, create a user and then start a voice-assistent.service

As an option, you can stop service `systemctl stop voice-assistant` and run `./start.sh` by youself.

## Installation on Armbian
`scripts/install-dependencies.sh` installs all the required dependencies on Armbian

