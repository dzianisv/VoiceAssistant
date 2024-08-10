#!/usr/bin/env python3

import unittest
from llm_langchains import LLM

class TestLLM(unittest.TestCase):
    def setUp(self) -> None:
        self.llm = LLM()
        return super().setUp()
    
    def test_weather(self):
        # Test the ask method
        response = self.llm.ask("What is the weather today in London, UK?")
        self.assertIn("°C", response)

    
    def test_wikipedia(self):
        # Test the ask method
        response = self.llm.ask("Who is Antonio Vivaldi?")
        self.assertIn("composer", response)


    def test_youtube(self):
        response = self.llm.ask("Find Antonio Vivaldo on youtube")
        print(response)

if __name__ == '__main__':
    unittest.main()