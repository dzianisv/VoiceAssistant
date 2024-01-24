#!/bin/bash

HOST=root@orangepipc
rsync -ra --progress  --exclude ".venv" "./src/" "$HOST:/opt/VoiceAssistant/"
rsync -ra --progress  --exclude ".venv" "./scripts/install-dependencies.sh" "$HOST:/opt/VoiceAssistant/"
