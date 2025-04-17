import ctypes
import logging
import sys
from pathlib import Path


def playsound(file, volume):
    """Plays a mp3 file
    ARGS:
        file: path to file
        volume: the sound volume as an int 0-100"""
    logging.info("[Playsound] playing %s", file)
    _playsound.playsound(file.encode("utf-8"), volume)

_playsound = ctypes.cdll.LoadLibrary(
    str(
        Path(__file__).parent / (
            "libplaysound." +
            {
                sys.platform: "so",
                "win32": "dll",
                "darwin": "osx.so"
            }[sys.platform]
        )
    )
)
