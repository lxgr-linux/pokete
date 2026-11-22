import ctypes
import logging
import platform
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def playsound(file: str, volume: int) -> None:
    """Plays a mp3 file
    ARGS:
        file: path to file
        volume: the sound volume as an int 0-100"""
    logger.info("[Playsound] playing %s", file)
    _playsound.playsound(file.encode("utf-8"), volume)


_playsound = ctypes.cdll.LoadLibrary(
    str(
        Path(__file__).parent
        / (
            f"libplaysound.{platform.machine()}."
            + {sys.platform: "so", "win32": "dll", "darwin": "osx.so"}[sys.platform]
        )
    )
)
