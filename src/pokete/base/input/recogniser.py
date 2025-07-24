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
    ESCAPES: list[int] = [27]
    ESCAPED_KEY_MAPPING: dict[str, str] = {
        "[A": "Key.up",
        "[B": "Key.down",
        "[C": "Key.right",
        "[D": "Key.left",
    }

    def __init__(self):
        self.escape_event = threading.Event()
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
                        self.set_event(
                            char,
                            {
                                ord(char): f"{char.rstrip()}",
                                13: "Key.enter",
                                127: "Key.backspace",
                                8: "Key.backspace",
                                32: "Key.space",
                                27: "Key.esc",
                                3: "exit",
                            },
                        )

        else:
            import termios
            import tty

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
                    self.set_event(
                        char,
                        {
                            ord(char): f"{char.rstrip()}",
                            13: "Key.enter",
                            127: "Key.backspace",
                            32: "Key.space",
                            27: "Key.esc",
                            3: "exit",
                        },
                    )
                    if ord(char) == 3:
                        self.reset()

        self.recogniser = recogniser
        PropagatingThread(target=self.check_escape, daemon=True).start()

    def check_escape(self):
        while True:
            self.escape_event.wait()
            self.escape_event.clear()
            time.sleep(0.01)
            if self.escape_input == "":
                _ev.set("Key.esc")
                self.escape_input = None

    def set_event(self, char: str, key_mapping: dict[int, str]):
        char_ord = ord(char)
        if char_ord in self.ESCAPES:
            self.escape_input = ""
            self.escape_event.set()
        elif self.escape_input is not None:
            self.escape_input += char
            if (
                event := self.ESCAPED_KEY_MAPPING.get(self.escape_input, None)
            ) is not None:
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

            assert self.fd is not None
            assert self.old_settings is not None

            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


recogniser = Recogniser()
