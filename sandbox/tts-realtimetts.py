#!/usr/bin/env python3
from RealtimeTTS import TextToAudioStream, OpenAIEngine
import httpx
import os

# https://platform.openai.com/docs/guides/text-to-speech/quickstart
# alloy, echo, fable, onyx, nova, and shimmer
proxy_url = os.environ.get("OPENAI_PROXY")
http_client=httpx.Client(proxy=proxy_url)
engine = OpenAIEngine(model='tts-1', voice='echo', openai_args={"http_client": http_client})
stream = TextToAudioStream(engine)
# text="""“В уездном городе N было так много парикмахерских заведений и бюро похоронных процессий, что, казалось, жители города рождаются лишь затем, чтобы побриться, остричься, освежить голову вежеталем и сразу же умереть"""
text = "Слушаю тебя!"
stream.feed(text)
stream.play_async()