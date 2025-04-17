import sys
import time

from pokete.release import SPEED_OF_TIME
from .event import _ev


class Recogniser:
    def __init__(self):
        self.fd = None
        self.old_settings = None
        if sys.platform == "win32":
            import msvcrt

            def recogniser():
                """Gets keyboard input from msvcrt, the Microsoft Visual C++ Runtime"""
                while True:
                    if msvcrt.kbhit():
                        char = msvcrt.getwch()
                        _ev.set(
                            {
                                ord(char): f"{char.rstrip()}",
                                13: "Key.enter",
                                127: "Key.backspace",
                                8: "Key.backspace",
                                32: "Key.space",
                                27: "Key.esc",
                                3: "exit",
                            }[ord(char)]
                        )

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
                    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if rlist:
                        char = sys.stdin.read(1)
                        _ev.set(
                            {
                                ord(char): f"{char.rstrip()}",
                                13: "Key.enter",
                                127: "Key.backspace",
                                32: "Key.space",
                                27: "Key.esc",
                                3: "exit",
                            }[ord(char)]
                        )
                        if ord(char) == 3:
                            self.reset()

        self.recogniser = recogniser

    def __call__(self):
        self.recogniser()

    def reset(self):
        """Resets the terminals state"""
        if sys.platform == "linux":
            import termios
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


recogniser = Recogniser()
