"""This file contains input wrappers for ui elements"""

from threading import Event

from pokete.base.change import change_ctx

from ... import loops
from ...context import Context
from ...ui.elements import InfoBox, InputBox
from ..text_input import text_input
from .bool import ask_bool
from .ok import ask_ok


def wait_event(ctx: Context, text: str, event: Event):
    """Shows box until event is set"""
    with InfoBox(text, info="", ctx=ctx):
        loops.event_wait(ctx, event)


def ask_text(ctx: Context, infotext, introtext, text, name, max_len):
    """Asks the player to input a text
    ARGS:
        ctx: Context
        infotext: The information text about the input
        introtext: The text that introduces the text field
        text: The default text in the text field
        name: The boxes displayed name
        max_len: Max length of the text"""
    with InputBox(infotext, introtext, text, max_len, name, ctx) as inputbox:
        ctx = change_ctx(ctx, inputbox)
        ret = text_input(
            ctx,
            inputbox.text,
            text,
            max_len + 1,
            max_len=max_len,
        )
    return ret
