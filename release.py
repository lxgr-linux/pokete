"""Contains general constants"""
import os
from pathlib import Path


VERSION = "0.7.2"
CODENAME = "Grey Edition"
SAVEPATH = Path(
    os.environ.get(
        "XDG_DATA_HOME",
        str(Path.home())+"/.local/share"
    )
) / "pokete"
FRAMETIME = 0.05

# Speeds up all parts of the game by this factor (smaller is faster)
SPEED_OF_TIME = 1
