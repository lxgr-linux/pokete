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

    # Returns 0-8 if ACT_1 through ACT_9 is in the list, else -1
    def get_number(self):
        for action in self:
            if action.value in range(Action.ACT_1.value, Action.ACT_9.value):
                return action.value - Action.ACT_1.value
        return -1

    def get_Y_strength(self) -> Number:
        if self.triggers(Action.UP):
                return -1
        elif self.triggers(Action.DOWN):
            return 1
        return 0

    def get_X_strength(self) -> Number:
        if self.triggers(Action.RIGHT):
            return 1
        elif self.triggers(Action.LEFT):
            return -1
        return 0

ACTION_DIRECTIONS = (Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN)
ACTION_UP_DOWN = (Action.UP, Action.DOWN)

hotkey_mappings = {
    'a':        ActionList([Action.LEFT]),
    'h':        ActionList([Action.LEFT]),
    'Key.left': ActionList([Action.LEFT]),
    'd':         ActionList([Action.RIGHT]),
    'l':         ActionList([Action.RIGHT]),
    'Key.right': ActionList([Action.RIGHT]),
    'w':      ActionList([Action.UP]),
    'k':      ActionList([Action.UP]),
    'Key.up': ActionList([Action.UP]),
    's':        ActionList([Action.DOWN]),
    'j':        ActionList([Action.DOWN]),
    'Key.down': ActionList([Action.DOWN]),

    'Key.space': ActionList([Action.ACCEPT]),
    'Key.enter': ActionList([Action.ACCEPT]),
    'y':         ActionList([Action.ACCEPT]),
    'o':         ActionList([Action.ACCEPT]),
    'n':             ActionList([Action.CANCEL]),
    'q':             ActionList([Action.CANCEL]),
    'Key.esc':       ActionList([Action.CANCEL]),
    'Key.backspace': ActionList([Action.CANCEL]),

    'r': ActionList([Action.RUN]),
    'e': ActionList([Action.DECK]),
    'i': ActionList([Action.INVENTORY]),
    'p': ActionList([Action.POKEDEX]),
    'm': ActionList([Action.MAP, Action.MOVE_POKETE]),
    'c': ActionList([Action.CLOCK]),
    '?': ActionList([Action.HELP, Action.INFO]),
    'u': ActionList([Action.MENU]),
    ':': ActionList([Action.CONSOLE]),

    '1': ActionList([Action.ACT_1]),
    '2': ActionList([Action.ACT_2]),
    '3': ActionList([Action.ACT_3]),
    '4': ActionList([Action.ACT_4]),
    '5': ActionList([Action.ACT_5]),
    '6': ActionList([Action.ACT_6]),
    '7': ActionList([Action.ACT_7]),
    '8': ActionList([Action.ACT_8]),
    '9': ActionList([Action.ACT_9]),
}

# Exists maybe for performance so references to new actionlists don't have to always be cleaned up when the following function returns nothing
# I don't trust python to be smart enough to do this itself
EMPTY_ACTIONLIST = ActionList()

# Returns an action, then clears input; all input is valid to read only once
def get_action() -> ActionList:
    retval = EMPTY_ACTIONLIST
    raw_input = _ev.get()
    if raw_input == "exit":
        raise KeyboardInterrupt
    if raw_input in hotkey_mappings:
        retval = hotkey_mappings[raw_input]
    _ev.clear()
    return retval
