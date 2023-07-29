#!/bin/bash
HOST=root@orangepi4-lts

rsync -ra --progress --exclude ".*"  --exclude "bin" --include ".env" . "$HOST:/opt/AssistantPlato/"
# ssh "$HOST" /opt/AssistantPlato/scripts/install.sh