"""This file contains input wrappers for ui elements"""

from pokete_general_use_fns import hard_liner

from .event import _ev
from .loops import std_loop
from .ui_elements import InfoBox, InputBox


def text_input(obj, _map, name, wrap_len, max_len=1000000):
    """Processes text input
    ARGS:
        obj: The text label that will be rechared
        _map: The map this happens on
        name: The default value of the label
        wrap_len: The len at which the text wraps
        max_len: The len at which the text shall end"""
    _ev.clear()
    obj.rechar(hard_liner(wrap_len, name + "█"))
    bname = name
    _map.show()
    while True:
        if _ev.get() in ["Key.enter", "Key.esc"]:
            _ev.clear()
            obj.rechar(hard_liner(wrap_len, name))
            _map.show()
            return name
        elif _ev.get() == "Key.backspace":
            if len(name) <= 0:
                _ev.clear()
                obj.rechar(bname)
                _map.show()
                return bname
            name = name[:-1]
            obj.rechar(hard_liner(wrap_len, name + "█"))
            _map.show()
            _ev.clear()
        elif (
            ((i := _ev.get()) not in ["", "exit"] and "Key." not in i)
            and len(name) < max_len
            or i == "Key.space"
        ):
            if _ev.get() == "Key.space":
                _ev.set("' '")
            name += str(_ev.get().strip("'"))
            obj.rechar(hard_liner(wrap_len, name + "█"))
            _map.show()
            _ev.clear()
        std_loop(_map.name == "movemap")


def ask_bool(_map, text):
    """Asks the player to aswer a yes/no question
    ARGS:
        _map: The map the question should be asked on
        text: The actual question"""
    assert len(text) >= 12, "Text has to be longer then 12 characters!"
    text_len = sorted(len(i) for i in text.split("\n"))[-1]
    with InfoBox(
        f"{text}\n{round(text_len / 2 - 6) * ' '}[Y]es   [N]o", info="", _map=_map
    ):
        while True:
            if _ev.get() == "'y'":
                ret = True
                break
            elif _ev.get() in ["'n'", "Key.esc", "'q'"]:
                ret = False
                break
            std_loop(_map.name == "movemap")
        _ev.clear()
    return ret


def ask_text(_map, infotext, introtext, text, name, max_len):
    """Asks the player to input a text
    ARGS:
        _map: The map the input box should be shown on
        infotext: The information text about the input
        introtext: The text that introduces the text field
        text: The default text in the text field
        name: The boxes displayed name
        max_len: Max length of the text"""
    with InputBox(infotext, introtext, text, max_len, name, _map) as inputbox:
        ret = text_input(inputbox.text, _map, text, max_len + 1, max_len=max_len)
    return ret


def ask_ok(_map, text):
    """Asks the player to an OK question
    ARGS:
        _map: The map the question is asked on
        text: The question it self"""
    assert len(text) >= 4, "Text has to be longer then 4 characters!"
    text_len = sorted(len(i) for i in text.split("\n"))[-1]
    with InfoBox(
        f"{text}\n{round(text_len / 2 - 2) * ' '}[O]k", name="Info", info="", _map=_map
    ):
        while True:
            if _ev.get() in ["'o'", "'O'", "Key.enter"]:
                break
            std_loop(_map.name == "movemap")
        _ev.clear()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
