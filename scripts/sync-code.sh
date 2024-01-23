#!/bin/bash

HOST=root@orangepipc.lan
rsync -ra --progress  --exclude ".venv" "./src/" "$HOST:/opt/VoiceAssistant/"