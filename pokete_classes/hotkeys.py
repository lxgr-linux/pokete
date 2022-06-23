from enum import Enum, auto
from .event import _ev

class Action(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    ACCEPT = auto()
    CANCEL = auto()
    NO = auto()

    RUN = auto()
    DECK = auto()
    INVENTORY = auto()
    POKEDEX = auto()
    MAP = auto()
    MOVE_POKETE = auto()
    FREE_POKETE = auto()
    CLOCK = auto()
    HELP = auto()
    INFO = auto()
    MENU = auto()
    CONSOLE = auto()
    EXIT_GAME = auto()

    NATURE_INFO = auto()
    ABILITIES = auto()
    CHOOSE_ATTACK = auto()
    CHOOSE_ITEM = auto()
    CHOOSE_POKE = auto()
    REMOVE = auto()

    ACT_1 = auto()
    ACT_2 = auto()
    ACT_3 = auto()
    ACT_4 = auto()
    ACT_5 = auto()
    ACT_6 = auto()
    ACT_7 = auto()
    ACT_8 = auto()
    ACT_9 = auto()

    @property
    def mapping(self):
        return get_mapping(self)

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

    def get_Y_strength(self) -> int:
        if self.triggers(Action.UP):
                return -1
        elif self.triggers(Action.DOWN):
            return 1
        return 0

    def get_X_strength(self) -> int:
        if self.triggers(Action.RIGHT):
            return 1
        elif self.triggers(Action.LEFT):
            return -1
        return 0

ACTION_DIRECTIONS = (Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN)
ACTION_UP_DOWN = (Action.UP, Action.DOWN)

hotkey_mappings = {
    '1': ActionList([Action.ACT_1, Action.DECK, Action.CHOOSE_ATTACK]),
    '2': ActionList(
        [
            Action.ACT_2, Action.EXIT_GAME, Action.MOVE_POKETE,
            Action.NATURE_INFO, Action.RUN
        ]
    ),
    '3': ActionList(
        [
            Action.ACT_3, Action.MAP, Action.FREE_POKETE, Action.ABILITIES,
            Action.CHOOSE_ITEM
        ]
    ),
    '4': ActionList([Action.ACT_4, Action.INVENTORY, Action.CHOOSE_POKE]),
    '5': ActionList([Action.ACT_5, Action.POKEDEX]),
    '6': ActionList([Action.ACT_6, Action.CLOCK]),
    '7': ActionList([Action.ACT_7]),
    '8': ActionList([Action.ACT_8]),
    '9': ActionList([Action.ACT_9]),

    'a':        ActionList([Action.LEFT]),
    'Key.left': ActionList([Action.LEFT]),
    'd':         ActionList([Action.RIGHT]),
    'Key.right': ActionList([Action.RIGHT]),
    'w':      ActionList([Action.UP]),
    'Key.up': ActionList([Action.UP]),
    's':        ActionList([Action.DOWN]),
    'Key.down': ActionList([Action.DOWN]),

    'Key.space': ActionList([Action.ACCEPT]),
    'Key.enter': ActionList([Action.ACCEPT]),
    'y':         ActionList([Action.ACCEPT]),
    'o':         ActionList([Action.ACCEPT]),
    'q':             ActionList([Action.CANCEL]),
    'n':             ActionList([Action.CANCEL]),
    'Key.esc':       ActionList([Action.CANCEL]),
    'Key.backspace': ActionList([Action.CANCEL]),

    'r': ActionList([Action.REMOVE]),
    'i': ActionList([Action.INFO, Action.INVENTORY]),
    'p': ActionList([Action.POKEDEX]),
    'f': ActionList([Action.FREE_POKETE]),
    'm': ActionList([Action.MAP, Action.MOVE_POKETE]),
    'c': ActionList([Action.CLOCK]),
    '?': ActionList([Action.HELP, Action.INFO]),
    'e': ActionList([Action.MENU]),
    ':': ActionList([Action.CONSOLE]),
}

def get_mapping(action):
    for key, actions_list in hotkey_mappings.items():
        if action in actions_list:
            return key
    return None

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
