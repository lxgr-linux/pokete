"""Standardized loops components"""

import time
from pokete_classes.hotkeys import Action, get_action
import release
from .notify import notifier
from .tss import tss


def easy_exit_loop(on_mvmp=True, box=None):
    """Loops until Cancel or Accept is given
    ARGS:
        on_mvmp: Indicates if the loop is executed on movemap"""
    while True:
        if get_action().triggers(*(Action.CANCEL, Action.ACCEPT)):
            return
        std_loop(on_mvmp, box=box)


def std_loop(on_mvmp=True, pevm=None, box=None):
    """Standard action executed in most loops
    ARGS:
        on_mvmp: Indicates if the loop is executed on movemap
        pevm: The PeriodicEventManager object, that may be needed to trigger
              periodic events in the overlaing loop"""
    if box is not None and tss():
        box.resize_view()
    if on_mvmp:
        notifier.next()
    if pevm is not None:
        pevm.event()
    time.sleep(release.FRAMETIME)
