#!/bin/sh
apt install -yq python3 python3-pip python3-virtualenv pipenv rhvoice rhvoice-russian rhvoice-english flac
apt install -yq sox libsox-fmt-all # required to play mp3

cd /opt/VoiceAssistant
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

useradd -r -s /bin/false voice_assistant -G audio

cat << EOF > /usr/lib/systemd/system/voice-assistant.service
[Unit]
Description=Voice Assistant Service
After=network.target sound.target


[Service]
Type=simple
User=voice_assistant
StateDirectory=voice_assistant
EnvironmentFile=/opt/VoiceAssistant/.env
ExecStart=/bin/bash -c 'source /opt/VoiceAssistant/.venv/bin/activate && exec python /opt/VoiceAssistant/main.py'
WorkingDirectory=/var/lib/voice_assistant
# ProtectHome=yes
# PrivateTmp=yes
# NoNewPrivileges=yes
# PrivateDevices=no
# DeviceAllow=/dev/snd rw
# ProtectKernelTunables=yes
# ProtectKernelModules=yes
# ProtectControlGroups=yes

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl restart voice-assistant