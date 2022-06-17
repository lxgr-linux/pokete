"""This manages audio playback"""

import multiprocessing
try:
    from playsound import playsound
except ModuleNotFoundError:
    from .dummy_playsound import playsound
from .settings import settings


def audio_fn(song):
    """plays a song in loop"""
    while settings("audio").val:
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

