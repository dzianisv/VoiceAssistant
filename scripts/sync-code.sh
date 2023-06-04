#!/bin/bash
HOST=root@orangepi4-lts

rsync -ra --progress . "$HOST:/opt/AssistantPlato/"
# ssh "$HOST" /opt/AssistantPlato/scripts/install.sh