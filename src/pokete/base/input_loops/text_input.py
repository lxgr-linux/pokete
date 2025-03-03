from pokete.util import hard_liner
from ..context import Context
from ..input import _ev
from .. import loops


def text_input(ctx: Context, obj, name, wrap_len, max_len=1000000):
    """Processes text input
    ARGS:
        obj: The text label that will be rechared
        ctx: Context
        name: The default value of the label
        wrap_len: The len at which the text wraps
        max_len: The len at which the text shall end"""
    _ev.clear()
    obj.rechar(hard_liner(wrap_len, name + "█"))
    bname = name
    ctx.map.show()
    while True:
        # Use lower level ev.get() methods because we need
        # to handle typed text, not game actions
        if _ev.get() in ("Key.enter", "Key.esc"):
            _ev.clear()
            obj.rechar(hard_liner(wrap_len, name))
            ctx.map.show()
            return name
        if _ev.get() == "Key.backspace":
            if len(name) <= 0:
                _ev.clear()
                obj.rechar(bname)
                ctx.map.show()
                return bname
            name = name[:-1]
            obj.rechar(hard_liner(wrap_len, name + "█"))
            ctx.map.show()
            _ev.clear()
        elif (
            ((i := _ev.get()) not in ["", "exit"] and "Key." not in i)
            and len(name) < max_len or i == "Key.space"
        ):
            if _ev.get() == "Key.space":
                _ev.set(" ")
            name += str(_ev.get())
            obj.rechar(hard_liner(wrap_len, name + "█"))
            ctx.map.show()
            _ev.clear()
        loops.std(ctx)
        ctx.map.full_show()
