#!/bin/sh
apt install -yq --no-install-recommends python3 python3-pip python3-virtualenv pipenv rhvoice rhvoice-russian rhvoice-english flac
apt install -yq --no-install-recommends libxslt1-dev libxml2 libcurl4-openssl-dev 
apt install -yq --no-install-recommends vlc

cd /opt/VoiceAssistant
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

useradd -r -s /bin/false voice_assistant -m -G audio,puslse-access

cat << EOF > /etc/udev/rules.d/99-gpio.rules
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c 'chown -R root:voice_assistant /sys/class/gpio /sys/devices/platform/soc/1c20800.pinctrl/; chmod -R g+rw /sys/class/gpio /sys/devices/platform/soc/1c20800.pinctrl/'"
EOF

udevadm control --reload-rules && udevadm trigger

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
Restart=on-failure
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