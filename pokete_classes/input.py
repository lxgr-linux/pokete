import time
from pokete_general_use_fns import std_loop, hard_liner
from pokete_classes.ui_elements import InfoBox, InputBox


def text_input(obj, _map, name, ev, wrap_len, max_len=1000000):
    """Processes text input"""
    ev.clear()
    obj.rechar(hard_liner(wrap_len, name + "█"))
    bname = name
    _map.show()
    while True:
        if ev.get() in ["Key.enter", "Key.esc"]:
            ev.clear()
            obj.rechar(hard_liner(wrap_len, name))
            _map.show()
            return name
        elif ev.get() == "Key.backspace":
            if len(name) <= 0:
                ev.clear()
                obj.rechar(bname)
                _map.show()
                return bname
            name = name[:-1]
            obj.rechar(hard_liner(wrap_len, name + "█"))
            _map.show()
            ev.clear()
        elif ev.get() not in ["", "Key.enter", "exit", "Key.backspace", "Key.shift",
                        "Key.shift_r", "Key.esc"] and len(name) < max_len:
            if ev.get() == "Key.space":
                ev.set("' '")
            name += str(ev.get().strip("'"))
            obj.rechar(hard_liner(wrap_len, name + "█"))
            _map.show()
            ev.clear()
        std_loop(ev)
        time.sleep(0.05)


def ask_bool(_ev, _map, text):
    """Asks the player to aswer a yes/no question"""
    assert len(text) >= 12, "Text has to be longer then 12 characters!"
    text_len = sorted([len(i) for i in text.split('\n')])[-1]
    with InfoBox(f"{text}\n{round(text_len / 2 - 6) * ' '}[Y]es   [N]o", _map):
        while True:
            if _ev.get() == "'y'":
                ret = True
                break
            elif _ev.get() in ["'n'", "Key.esc", "'q'"]:
                ret = False
                break
            std_loop(_ev)
            time.sleep(0.05)
            _map.show()
        _ev.clear()
    return ret


def ask_text(_map, infotext, introtext, text, ev, max_len):
    """Asks the player to input a text"""
    with InputBox(infotext, introtext, text, max_len, _map) as inputbox:
        ret = text_input(inputbox.text, _map, text, ev, max_len + 1,
                         max_len=max_len)
    return ret


def ask_ok(_ev, _map, text):
    """Asks the player to an OK question"""
    assert len(text) >= 4, "Text has to be longer then 4 characters!"
    text_len = sorted([len(i) for i in text.split('\n')])[-1]
    with InfoBox(f"{text}\n{round(text_len / 2 - 2) * ' '}[O]k", _map):
        while True:
            if _ev.get() in ["'o'", "'O'", "Key.enter"]:
                break
            std_loop(_ev)
            time.sleep(0.05)
            _map.show()
        _ev.clear()
