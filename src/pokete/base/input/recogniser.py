import sys
import threading
import time
from typing import Optional

from pokete.base.exception_propagation.propagating_thread import (
    PropagatingThread,
)
from pokete.base.input import key

from .event import _ev
from .mouse import mouse_manager


class Recogniser:
    ESCAPES: list[int] = [27, 0]
    ESCAPED_KEY_MAPPING: dict[str, key.Key] = {
        "[A": key.UP,
        "[B": key.DOWN,
        "[C": key.RIGHT,
        "[D": key.LEFT,
        "H": key.UP,
        "P": key.DOWN,
        "M": key.RIGHT,
        "K": key.LEFT,
    }
    UNIX_KEY_MAPPING: dict[int, key.Key] = {
        13: key.ENTER,
        127: key.BACKSPACE,
        32: key.SPACE,
        27: key.ESC,
        3: key.EXIT,
    }
    WINDOWS_KEY_MAPPING: dict[int, key.Key] = {
        13: key.ENTER,
        127: key.BACKSPACE,
        8: key.BACKSPACE,
        32: key.SPACE,
        27: key.ESC,
        3: key.EXIT,
    }

    def __init__(self):
        self.__escape_event = threading.Event()
        self.__escape_input: Optional[str] = None
        self.__fd = None
        self.__old_settings = None
        if sys.platform == "win32":
            import msvcrt

            def recogniser():
                """Gets keyboard input from msvcrt, the Microsoft Visual C++ Runtime"""
                while True:
                    char = msvcrt.getwch()
                    self.set_event(
                        char,
                        self.WINDOWS_KEY_MAPPING,
                    )

        else:
            import termios
            import tty

            def recogniser():
                """Use another (not on xserver relying) way to read keyboard input,
                to make this shit work in tty or via ssh,
                where no xserver is available"""

                self.__fd = sys.stdin.fileno()
                self.__old_settings = termios.tcgetattr(self.__fd)
                tty.setraw(self.__fd)

                while True:
                    char = sys.stdin.read(1)
                    # logging.info("input %s -- %d", char, ord(char))
                    self.set_event(
                        char,
                        self.UNIX_KEY_MAPPING,
                    )
                    if ord(char) == 3:
                        self.reset()

        PropagatingThread(target=self.check_escape, daemon=True).start()
        self.recogniser = recogniser

    def check_escape(self):
        while True:
            self.__escape_event.wait()
            self.__escape_event.clear()
            time.sleep(0.01)
            if self.__escape_input == "":
                _ev.set(key.ESC)
                self.__escape_input = None

    def set_event(self, char: str, key_mapping: dict[int, key.Key]):
        char_ord = ord(char)
        key_mapping.setdefault(char_ord, key.Key(f"{char.rstrip()}"))
        if char_ord in self.ESCAPES:
            self.__escape_input = ""
            self.__escape_event.set()
        elif self.__escape_input is not None:
            self.__escape_input += char
            if (
                event := self.ESCAPED_KEY_MAPPING.get(self.__escape_input, None)
            ) is not None:
                _ev.set(event)
                self.__escape_input = None
            elif mouse_manager.is_mouse_event(self.__escape_input):
                mouse_manager.handle(self.__escape_input)
                self.__escape_input = None
        else:
            _ev.set(key_mapping[char_ord])

    def __call__(self):
        self.recogniser()

    def reset(self):
        """Resets the terminals state"""
        if sys.platform == "linux":
            import termios

            assert self.__fd is not None
            assert self.__old_settings is not None

            termios.tcsetattr(self.__fd, termios.TCSADRAIN, self.__old_settings)


recogniser = Recogniser()
