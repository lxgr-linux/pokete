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


def std_loop():
    """Standart action executed in most loops"""
    if _ev.get() == "exit":
        raise KeyboardInterrupt
    notifier.next()
