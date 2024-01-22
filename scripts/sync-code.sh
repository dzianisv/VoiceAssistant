#!/bin/bash
HOST=root@orangepipc.lan

rsync -ra --progress --exclude ".*"  --exclude "bin" --include ".env" . "$HOST:/opt/AssistantPlato/"
# ssh "$HOST" /opt/AssistantPlato/scripts/install.sh