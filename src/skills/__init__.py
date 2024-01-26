from .youtube import PlayYoutube
from enum import Enum
from .utils import ActionsQueue

class Commands(Enum):
    STOP = "STOP"
    FINISHED = "FINISHED"

actions = [PlayYoutube]

def run(message: str, *args, **kwargs):
    for Action in actions:
        a = Action()
        if a.run(message, *args, **kwargs):
            return True
    return False