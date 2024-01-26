import queue

class ActionsQueue:
    def __init__(self):
        self.up = queue.Queue()
        self.down = queue.Queue()