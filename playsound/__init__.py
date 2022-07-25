import ctypes
import time
import logging
import sys
from pathlib import Path


def playsound(file):
    logging.info("[Playsound] playing %s", file)
    _playsound.playsound(file.encode("utf-8"))


_playsound = ctypes.cdll.LoadLibrary(
    str(
        Path(__file__).parent / (
            "libplaysound." +
            {
                sys.platform: "so",
                "win32": "dll"
            }[sys.platform]
        )
    )
)
