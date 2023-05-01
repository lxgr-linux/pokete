from enum import Enum, auto


class Mode(Enum):
    SINGLE = auto
    MULTI = auto
    

class ModeProvider:
    def __init__(self):
        self.mode: Mode = Mode.SINGLE
        

modeProvider = ModeProvider()
