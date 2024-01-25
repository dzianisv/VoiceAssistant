#!/usr/bin/env python3

import unittest
import os

from youtube import PlayYoutube
from utils import ActionsQueue
import time


class TestLLM(unittest.TestCase):
    def test_playing(self):
        message = "answer The link to 'Four Seasons' by Antonio Vivaldi on YouTube is [here](https://www.youtube.com/watch?v=GRxofEmo3HA&pp=ygUcQW50b25pbyBWaXZhbGRpIEZvdXIgU2Vhc29ucw%3D%3D)."
        a = PlayYoutube()
        q = ActionsQueue()
        assert(a.run(message, q))
        time.sleep(30)
        q.down.put("STOP")

if __name__ == '__main__':
    unittest.main()