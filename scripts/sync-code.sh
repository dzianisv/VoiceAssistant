#!/bin/bash
HOST=root@orangepi4.lan

rsync -ra --progress . "$HOST:/opt/AssistantPlato/"