from collections.abc import Buffer
from io import BufferedReader
from json.encoder import ESCAPE
import logging
import sys
import time
from typing import Optional

from pokete.release import SPEED_OF_TIME
from .event import _ev


class Recogniser:
    ESCAPES: list[int] = [27]
    ESCAPED_KEY_MAPPING: dict[str, str] = {
        "[A": "Key.up", "[B": "Key.down", "[C": "Key.right", "[D": "Key.left"
    }

    def __init__(self):
        self.escape_input: Optional[str] = None
        self.fd = None
        self.old_settings = None
        if sys.platform == "win32":
            import msvcrt

            def recogniser():
                """Gets keyboard input from msvcrt, the Microsoft Visual C++ Runtime"""
                while True:
                    if msvcrt.kbhit():
                        char = msvcrt.getwch()
                        self.set_event(char, {
                            ord(char): f"{char.rstrip()}",
                            13: "Key.enter",
                            127: "Key.backspace",
                            8: "Key.backspace",
                            32: "Key.space",
                            27: "Key.esc",
                            3: "exit",
                        })

        else:
            import tty
            import termios
            import select

            def recogniser():
                """Use another (not on xserver relying) way to read keyboard input,
                    to make this shit work in tty or via ssh,
                    where no xserver is available"""

                self.fd = sys.stdin.fileno()
                self.old_settings = termios.tcgetattr(self.fd)
                tty.setraw(self.fd)
                time.sleep(SPEED_OF_TIME * 0.1)

                while True:
                    char = sys.stdin.read(1)

                    logging.info("input %s %d", char, ord(char))
                    self.set_event(char, {
                            ord(char): f"{char.rstrip()}",
                            13: "Key.enter",
                            127: "Key.backspace",
                            32: "Key.space",
                            27: "Key.esc",
                            3: "exit",
                    })
                    if ord(char) == 3:
                        self.reset()

        self.recogniser = recogniser

    def set_event(self, char:str, key_mapping:dict[int, str]):
        char_ord = ord(char)
        if char_ord in self.ESCAPES:
            self.escape_input = ""
        elif self.escape_input is not None:
            self.escape_input += char
            if (event := self.ESCAPED_KEY_MAPPING.get(self.escape_input, None)) is not None:
                _ev.set(event)
                self.escape_input = None
        else:
            _ev.set(key_mapping[char_ord])

    def __call__(self):
        self.recogniser()

    def reset(self):
        """Resets the terminals state"""
        if sys.platform == "linux":
            import termios
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


recogniser = Recogniser()
