import time
from pokete_classes.event import _ev
from pokete_classes.notify import notifier


def easy_exit_loop():
    """Loops until q or Esc are pressed"""
    while True:
        if _ev.get() in ["'q'", "Key.esc"]:
            _ev.clear()
            return
        std_loop()
        time.sleep(0.05)


def std_loop(on_mvmp=True):
    """Standart action executed in most loops
    ARGS:
        on_mvmp: Indicates if the loop is executed on movemap"""
    if _ev.get() == "exit":
        raise KeyboardInterrupt
    if on_mvmp:
        notifier.next()
