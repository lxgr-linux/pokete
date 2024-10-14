"""Standardized loops components"""

from threading import Event
import time

import release
from .context import Context
from .input import Action, get_action
from .tss import tss


def easy_exit(ctx: Context | None = None):
    """Loops until Cancel or Accept is given"""
    while True:
        if get_action().triggers(*(Action.CANCEL, Action.ACCEPT)):
            return
        std(ctx)

def event_wait(ctx: Context, event:Event):
    """Loops until an event is set"""
    while True:
        if event.is_set():
            return
        std(ctx)


def std(ctx: Context | None = None):
    """Standard action executed in most loops"""
    if ctx is not None and tss():
        ctx.overview.resize_view()
    if ctx is not None:
        ctx.pevm.event()
    ctx.map.full_show()
    time.sleep(release.FRAMETIME)
