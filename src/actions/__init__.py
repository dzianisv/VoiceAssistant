from .youtube import PlayYoutube
from dataclasses import dataclass
import queue

actions = [PlayYoutube]

@dataclass
class ActionsQueue:
    up: queue.Queue
    down: queue.Queue

def run(message: str, *args, **kwargs):
    for Action in actions:
        a = Action()
        if a.run(message, *args, **kwargs):
            return True
    return False