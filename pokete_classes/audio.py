"""This manages audio playback"""

import multiprocessing
from pathlib import Path
from .settings import settings


MUSIC_PATH = Path(__file__).parents[1] / 'assets' / 'music'


def audio_fn(song, play_audio, volume):
    """plays a song in loop"""
    import playsound


    while play_audio:
        playsound.playsound(str(MUSIC_PATH / song), volume)


class Audio:
    """Audio controler class"""
    volume = 100

    def __init__(self):
        self.curr = None

    def start(self, song, volume):
        """Starts playing a song
        ARGS:
            song: The song played
            volume: The volume value in percentage from 0 to 100"""
        self.volume = volume
        self.curr = multiprocessing.Process(
            target=audio_fn,
            args=(song, settings("audio").val, self.volume)
        )
        self.curr.start()

    def switch(self, song):
        """Switched the played song
        ARGS:
            song: The song played"""
        self.kill()
        self.start(song, self.volume)

    def kill(self):
        """Kills the running music"""
        self.curr.terminate()

audio = Audio()
