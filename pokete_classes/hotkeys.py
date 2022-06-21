from tokenize import Number
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
    MOVE_POKETE = auto()
    CLOCK = auto()
    HELP = auto()
    INFO = auto()
    MENU = auto()
    CONSOLE = auto()

    ACT_1 = auto()
    ACT_2 = auto()
    ACT_3 = auto()
    ACT_4 = auto()
    ACT_5 = auto()
    ACT_6 = auto()
    ACT_7 = auto()
    ACT_8 = auto()
    ACT_9 = auto()

class ActionList(list):
    def triggers(self, *actions):
        for action in actions:
            if action in self:
                return True
        return False

ACTION_DIRECTIONS = (Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN)
ACTION_UP_DOWN = (Action.UP, Action.DOWN)

hotkey_mappings = {
    'a':        [Action.LEFT],
    'h':        [Action.LEFT],
    'Key.left': [Action.LEFT],
    'd':         [Action.RIGHT],
    'l':         [Action.RIGHT],
    'Key.right': [Action.RIGHT],
    'w':      [Action.UP],
    'k':      [Action.UP],
    'Key.up': [Action.UP],
    's':        [Action.DOWN],
    'j':        [Action.DOWN],
    'Key.down': [Action.DOWN],

    'Key.space': [Action.ACCEPT],
    'Key.enter': [Action.ACCEPT],
    'y':         [Action.ACCEPT],
    'o':         [Action.ACCEPT],
    'n':             [Action.CANCEL],
    'q':             [Action.CANCEL],
    'Key.esc':       [Action.CANCEL],
    'Key.backspace': [Action.CANCEL],

    'r': [Action.RUN],
    'e': [Action.DECK],
    'i': [Action.INVENTORY],
    'p': [Action.POKEDEX],
    'm': [Action.MAP, Action.MOVE_POKETE],
    'c': [Action.CLOCK],
    '?': [Action.HELP, Action.INFO],
    'u': [Action.MENU],
    ':': [Action.CONSOLE],

    '1': [Action.ACT_1],
    '2': [Action.ACT_2],
    '3': [Action.ACT_3],
    '4': [Action.ACT_4],
    '5': [Action.ACT_5],
    '6': [Action.ACT_6],
    '7': [Action.ACT_7],
    '8': [Action.ACT_8],
    '9': [Action.ACT_9],
}

# Returns an action, then clears input; all input is valid to read only once
def get_action() -> ActionList:
    retval = None
    raw_input = _ev.get()
    if raw_input == "exit":
        raise KeyboardInterrupt
    if raw_input in hotkey_mappings:
        retval = hotkey_mappings[raw_input]
    _ev.clear()
    return retval

def get_Y_strength(action: Action) -> Number:
    if action == Action.UP:
            return -1
    elif action == Action.DOWN:
        return 1
    return 0

def get_X_strength(action: Action) -> Number:
    if action == Action.RIGHT:
        return 1
    elif action == Action.LEFT:
        return -1
    return 0
