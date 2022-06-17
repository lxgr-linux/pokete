import multiprocessing
from playsound import playsound


def audio_fn(song):
    while True:
        playsound('./assets/music/' + song)


class Audio:
    def __init__(self):
        self.curr = None

    def start(self, song):
        self.curr = multiprocessing.Process(
            target=audio_fn,
            args=(song, )
        )
        self.curr.start()

    def switch(self, song):
        self.kill()
        self.start(song)

    def kill(self):
        self.curr.terminate()

audio = Audio()

