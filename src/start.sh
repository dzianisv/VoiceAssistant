#!/bin/bash
. .venv/bin/activate
export $( < .env )
./main.py