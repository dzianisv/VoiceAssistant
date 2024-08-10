#!/usr/bin/env python3

import unittest
import os

from llm_langchains import LLM

class TestLLM(unittest.TestCase):
    def test_question(self):
        llm = LLM()
        answer = llm.ask("who is Antonion Vivaldi?")
        print(answer)
        assert("composer" in answer)

    def test_weather(self):
        llm = LLM(o)
        answer = llm.ask("What is whether in Venice?")
        print("asnwer", answer)

    def test_youtube_search(self):
        llm = LLM()
        answer = llm.ask("Find 'Four Seasons' by Antonio Vivaldi on youtube")
        print("asnwer", answer)

if __name__ == '__main__':
    unittest.main()