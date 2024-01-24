from .youtube import PlayYoutube
from enum import Enum
import queue

class Commands(Enum):
    STOP = "STOP"
    FINISHED = "FINISHED"

actions = [PlayYoutube]


class ActionsQueue:
    def __init__(self):
        self.up = queue.Queue()
        self.down = queue.Queue()

def run(message: str, *args, **kwargs):
    for Action in actions:
        a = Action()
        if a.run(message, *args, **kwargs):
            return True
    return False