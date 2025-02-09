"""Mode setting"""

from enum import Enum, auto


class Mode(Enum):
    """The modes the game can have"""
    SINGLE = auto()
    MULTI = auto()


class ModeProvider:
    """Holds the games mode"""

    def __init__(self):
        self.mode: Mode = Mode.SINGLE


modeProvider = ModeProvider()
