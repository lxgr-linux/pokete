"""This manages audio playback"""

import multiprocessing
from pathlib import Path
from .settings import settings


MUSIC_PATH = Path(__file__).parents[1] / 'assets' / 'music'


def audio_fn(song, play_audio):
    """plays a song in loop"""
    import playsound
    while play_audio:
        playsound.playsound(str(MUSIC_PATH / song))


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
            args=(song, settings("audio").val)
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

