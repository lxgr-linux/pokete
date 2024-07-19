"""Standardized loops components"""

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
        ctx.map.full_show()


def std(ctx: Context | None = None):
    """Standard action executed in most loops"""
    if ctx is not None and tss():
        ctx.overview.resize_view()
    if ctx is not None:
        ctx.pevm.event()
    time.sleep(release.FRAMETIME)
