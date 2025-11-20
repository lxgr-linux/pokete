"""Standardized loops components"""

import time
from threading import Event

from pokete import release

from .context import Context
from .input import Action, get_action
from .tss import tss


def easy_exit(ctx: Context) -> bool:
    """Loops until Cancel or Accept is given"""
    while True:
        action = get_action()
        if action.triggers(Action.CANCEL):
            return False
        elif action.triggers(Action.ACCEPT):
            return True
        std(ctx)


def event_wait(ctx: Context, event: Event):
    """Loops until an event is set"""
    while True:
        if event.is_set():
            return
        std(ctx)


def std(ctx: Context):
    """Standard action executed in most loops"""
    if tss():
        ctx.overview.resize_view()
    ctx.pevm.event(ctx)
    ctx.map.full_show()
    time.sleep(release.FRAMETIME)
