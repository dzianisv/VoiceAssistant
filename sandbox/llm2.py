#!/usr/bin/env python3

import os
import sys
import logging
import json

from langchain_openai import ChatOpenAI
from contextlib import contextmanager

logger = logging.getLogger(__name__)


def init_llm(memory_window=3):
    proxy_url = os.environ.get("OPENAI_PROXY")

    return  ChatOpenAI(
        openai_api_base=os.environ.get("OPENAI_API_BASE"), 
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        openai_proxy=proxy_url,
        temperature=0.7, 
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
    )


if __name__ == "__main__":
    llm = init_llm()
    print(llm.invoke(sys.argv[1]))