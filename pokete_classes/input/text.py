from util import hard_liner
from .event import _ev
from .. import loops


def text_input(obj, _map, name, wrap_len, max_len=1000000, box=None):
    """Processes text input
    ARGS:
        obj: The text label that will be rechared
        _map: The map this happens on
        name: The default value of the label
        wrap_len: The len at which the text wraps
        max_len: The len at which the text shall end
        box: The box this is called for"""
    _ev.clear()
    obj.rechar(hard_liner(wrap_len, name + "█"))
    bname = name
    _map.show()
    while True:
        # Use lower level ev.get() methods because we need
        # to handle typed text, not game actions
        if _ev.get() in ("Key.enter", "Key.esc"):
            _ev.clear()
            obj.rechar(hard_liner(wrap_len, name))
            _map.show()
            return name
        if _ev.get() == "Key.backspace":
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
            and len(name) < max_len or i == "Key.space"
        ):
            if _ev.get() == "Key.space":
                _ev.set(" ")
            name += str(_ev.get())
            obj.rechar(hard_liner(wrap_len, name + "█"))
            _map.show()
            _ev.clear()
        loops.std(_map.name == "movemap", box=box)
