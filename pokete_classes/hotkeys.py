from pokete_classes.event import _ev
from enum import Enum, auto

class Action(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    ACCEPT = auto()
    CANCEL = auto()

    RUN = auto()
    DECK = auto()
    INVENTORY = auto()
    POKEDEX = auto()
    MAP = auto()
    CLOCK = auto()
    HELP = auto()

    ACT_1 = auto()
    ACT_2 = auto()
    ACT_3 = auto()
    ACT_4 = auto()

hotkey_mappings = {
    'a':        Action.LEFT,
    'h':        Action.LEFT,
    'Key.left': Action.LEFT,
    'd':         Action.RIGHT,
    'l':         Action.RIGHT,
    'Key.right': Action.RIGHT,
    'w':      Action.UP,
    'k':      Action.UP,
    'Key.up': Action.UP,
    's':        Action.DOWN,
    'j':        Action.DOWN,
    'Key.down': Action.DOWN,

    'Key.space': Action.ACCEPT,
    'Key.enter': Action.ACCEPT,
    'y':         Action.ACCEPT,
    'n':             Action.CANCEL,
    'q':             Action.CANCEL,
    'Key.esc':       Action.CANCEL,
    'Key.backspace': Action.CANCEL,

    'r': Action.RUN,
    'e': Action.DECK,
    'i': Action.INVENTORY,
    'p': Action.POKEDEX,
    'm': Action.MAP,
    'c': Action.CLOCK,
    '?': Action.HELP,

    '1': Action.ACT_1,
    '2': Action.ACT_2,
    '3': Action.ACT_3,
    '4': Action.ACT_4,
}

# Returns an action, then clears input; all input is valid to read only once
def get_action() -> Action:
    retval = None
    raw_input = _ev.get()
    if raw_input == "exit":
        raise KeyboardInterrupt
    if raw_input in hotkey_mappings:
        retval = hotkey_mappings[raw_input]
    _ev.clear()
    return retval
