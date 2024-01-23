#!/usr/bin/env python3

import unittest
import os

from llm_langchains import LLM

class TestLLM(unittest.TestCase):
    def test_llm(self):
        llm = LLM(os.getenv("OPENAI_KEY"))
        answer = llm.ask("who is Antonion Vivaldi?")
        assert("composer" in answer)

if __name__ == '__main__':
    unittest.main()