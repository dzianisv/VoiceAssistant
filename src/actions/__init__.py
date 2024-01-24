from .youtube import PlayYoutube

actions = [PlayYoutube]

def run(message: str):
    for Action in actions:
        a = Action()
        if a.run(message):
            return True
    return False