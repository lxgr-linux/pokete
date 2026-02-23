class Key:
    def __init__(self, char="", rep=""):
        self.char = char
        self.__rep = rep

    def marshall(self) -> str:
        if self.__rep:
            return f"Key.{self.__rep}"
        return self.char

    def has_char(self) -> bool:
        return not not self.char


UP = Key(rep="up")
DOWN = Key(rep="down")
LEFT = Key(rep="left")
RIGHT = Key(rep="right")
ENTER = Key(rep="enter")
BACKSPACE = Key(rep="backspace")
SPACE = Key(" ", rep="space")
ESC = Key(rep="esc")
EXIT = Key()
