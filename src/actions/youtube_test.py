#!/usr/bin/env python3

import unittest
import os

from youtube import PlayYoutube
from utils import ActionsQueue
import time


class TestLLM(unittest.TestCase):
    def test_playing(self):
        message = "The link to 'Four Seasons' by Antonio Vivaldi on YouTube is [here](https://www.youtube.com/watch?v=GRxofEmo3HA&pp=ygUcQW50b25pbyBWaXZhbGRpIEZvdXIgU2Vhc29ucw%3D%3D)."
        message = """Here are some YouTube videos containing compositions by Antonio Vivaldi:
[Video 1](https://www.youtube.com/watch?v=pSo4wUPomfQ&pp=ygUf0JDQvdGC0L7QvdC40L4g0JLQuNCy0LDQu9GM0LTQuA%3D%3D)
Video 2](https://www.youtube.com/watch?v=QFFrkZOYojk&pp=ygUf0JDQvdGC0L7QvdC40L4g0JLQuNCy0LDQu9GM0LTQuA%3D%3D)
[Video 3](https://www.youtube.com/watch?v=D3qrt0EgVd8&pp=ygUf0JDQvdGC0L7QvdC40L4g0JLQuNCy0LDQu9GM0LTQuA%3D%3D)
[Video 4](https://www.youtube.com/watch?v=L2XGz5E0X2A&pp=ygUf0JDQvdGC0L7QvdC40L4g0JLQuNCy0LDQu9GM0LTQuA%3D%3D)
[Video 5](https://www.youtube.com/watch?v=0cnnOZb3394&pp=ygUf0JDQvdGC0L7QvdC40L4g0JLQuNCy0LDQu9GM0LTQuA%3D%3D)
"""
        a = PlayYoutube()
        q = ActionsQueue()
        assert(a.run(message, q))
        time.sleep(30)
        q.down.put("STOP")

if __name__ == '__main__':
    unittest.main()