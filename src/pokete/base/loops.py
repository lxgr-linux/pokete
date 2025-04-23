"""Standardized loops components"""

from threading import Event
import time

from pokete import release
from .context import Context
from .input import Action, get_action
from .tss import tss


def easy_exit(ctx: Context):
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


def std(ctx: Context):
    """Standard action executed in most loops"""
    if tss():
        ctx.overview.resize_view()
    ctx.pevm.event()
    ctx.map.full_show()
    time.sleep(release.FRAMETIME)
