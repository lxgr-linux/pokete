"""Standardized loops components"""

import time

import release
from .context import Context
from .ui import notifier
from .input import Action, get_action
from .tss import tss


def easy_exit(on_mvmp=True, ctx: Context | None = None):
    """Loops until Cancel or Accept is given
    ARGS:
        on_mvmp: Indicates if the loop is executed on movemap"""
    while True:
        if get_action().triggers(*(Action.CANCEL, Action.ACCEPT)):
            return
        std(on_mvmp, ctx)
        ctx.map.full_show()


def std(on_mvmp=True, ctx: Context | None = None):
    """Standard action executed in most loops
    ARGS:
        on_mvmp: Indicates if the loop is executed on movemap"""
    if ctx is not None and tss():
        ctx.overview.resize_view()
    if on_mvmp:
        notifier.next()
    if ctx is not None:
        ctx.pevm.event()
    time.sleep(release.FRAMETIME)
