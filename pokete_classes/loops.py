"""Standardized loops components"""

import time
import release
from .event import _ev
from .notify import notifier


def easy_exit_loop():
    """Loops until q or Esc are pressed"""
    while True:
        if _ev.get() in ["'q'", "Key.esc"]:
            _ev.clear()
            return
        std_loop()


def std_loop(on_mvmp=True, pevm=None):
    """Standart action executed in most loops
    ARGS:
        on_mvmp: Indicates if the loop is executed on movemap"""
    if _ev.get() == "exit":
        raise KeyboardInterrupt
    if on_mvmp:
        notifier.next()
    if pevm is not None:
        pevm.event()
    time.sleep(release.FRAMETIME)
