import sys
import threading
import time
from typing import Optional

from pokete.base.exception_propagation.propagating_thread import (
    PropagatingThread,
)
from pokete.release import SPEED_OF_TIME

from .event import _ev


class Recogniser:
    ESCAPES: list[int] = [27, 0]
    ESCAPED_KEY_MAPPING: dict[str, str] = {
        "[A": "Key.up",
        "[B": "Key.down",
        "[C": "Key.right",
        "[D": "Key.left",
        "P": "Key.up",
        "M": "Key.down",
        "K": "Key.right",
        "H": "Key.left",
    }
    UNIX_KEY_MAPPING: dict[int, str] = {
        13: "Key.enter",
        127: "Key.backspace",
        32: "Key.space",
        27: "Key.esc",
        3: "exit",
    }
    WINDOWS_KEY_MAPPING: dict[int, str] = {
        13: "Key.enter",
        127: "Key.backspace",
        8: "Key.backspace",
        32: "Key.space",
        27: "Key.esc",
        3: "exit",
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
                    if msvcrt.kbhit():
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
                time.sleep(SPEED_OF_TIME * 0.1)

                while True:
                    char = sys.stdin.read(1)
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
                _ev.set("Key.esc")
                self.__escape_input = None

    def set_event(self, char: str, key_mapping: dict[int, str]):
        char_ord = ord(char)
        key_mapping.setdefault(char_ord, f"{char.rstrip()}")
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
