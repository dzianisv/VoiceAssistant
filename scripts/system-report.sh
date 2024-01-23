#!/bin/sh

lsb_release -d
uname -a
arecord -l
python3 --version
pip3 list | grep azure
