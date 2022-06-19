"""Contains general constants"""
import os
from pathlib import Path


VERSION = "0.7.2"
CODENAME = "Grey Edition"
SAVEPATH = os.environ.get(
    "XDG_DATA_HOME",
    str(Path.home())+"/.local/share"
) + "/pokete"
FRAMETIME = 0.05
