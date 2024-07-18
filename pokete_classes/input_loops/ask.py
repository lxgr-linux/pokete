"""This file contains input wrappers for ui elements"""
from ..context import Context
from ..ui.elements import InfoBox, InputBox
from ..input import Action, get_action, _ev
from .. import loops
from .text_input import text_input


def ask_bool(_map, text, overview=None):
    """Asks the player to aswer a yes/no question
    ARGS:
        _map: The map the question should be asked on
        text: The actual question
        overview: The overview this is called on"""
    assert len(text) >= 12, "Text has to be longer then 12 characters!"
    text_len = sorted([len(i) for i in text.split('\n')])[-1]
    with InfoBox(f"{text}\n{round(text_len / 2 - 6) * ' '}[Y]es   [N]o",
                 info="", _map=_map, overview=overview) as box:
        while True:
            action = get_action()
            if action.triggers(Action.ACCEPT):
                ret = True
                break
            if action.triggers(Action.CANCEL):
                ret = False
                break
            loops.std(_map.name == "movemap", box=box)
    return ret


def ask_text(ctx: Context, infotext, introtext, text, name, max_len):
    """Asks the player to input a text
    ARGS:
        ctx: Context
        infotext: The information text about the input
        introtext: The text that introduces the text field
        text: The default text in the text field
        name: The boxes displayed name
        max_len: Max length of the text"""
    with InputBox(
        infotext, introtext, text, max_len, name, ctx.map, ctx.overview
    ) as inputbox:
        ret = text_input(
            ctx.with_overview(inputbox), inputbox.text, text,
            max_len + 1,
            max_len=max_len
        )
    return ret


def ask_ok(ctx: Context, text):
    """Shows the player some information
    ARGS:
        ctx:Context
        text: The question it self"""
    assert len(text) >= 4, "Text has to be longer then 4 characters!"
    text_len = sorted([len(i) for i in text.split('\n')])[-1]
    with InfoBox(f"{text}\n{round(text_len / 2 - 2) * ' '} [O]k ", name="Info",
                 info="", _map=ctx.map, overview=ctx.overview) as box:
        while True:
            action = get_action()
            if action.triggers(Action.ACCEPT or action == Action.CANCEL):
                break
            loops.std(ctx.map.name == "movemap", ctx.with_overview(box))
        _ev.clear()
