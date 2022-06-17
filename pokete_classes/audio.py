"""This manages audio playback"""

import multiprocessing
from playsound import playsound


def audio_fn(song):
    """plays a song in loop"""
    while True:
        playsound('./assets/music/' + song)


class Audio:
    """Audio controler class"""

    def __init__(self):
        self.curr = None

    def start(self, song):
        """Starts playing a song
        ARGS:
            song: The song played"""
        self.curr = multiprocessing.Process(
            target=audio_fn,
            args=(song, )
        )
        self.curr.start()

    def switch(self, song):
        """Switched the played song
        ARGS:
            song: The song played"""
        self.kill()
        self.start(song)

    def kill(self):
        """Kills the running music"""
        self.curr.terminate()

audio = Audio()

