"""Contains everything related to input processing"""

import sys
from enum import Enum, auto
from collections import defaultdict

from pokete.util import liner
from .event import _ev


class Action(Enum):
    """Keyboad action layer"""

    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    UP_LEFT = auto()
    UP_RIGHT = auto()
    DOWN_LEFT = auto()
    DOWN_RIGHT = auto()
    ACCEPT = auto()
    CANCEL = auto()

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
    STATS_INFO = auto()
    ABILITIES_INFO = auto()
    CHOOSE_ATTACK = auto()
    CHOOSE_ITEM = auto()
    CHOOSE_POKE = auto()
    REMOVE = auto()
    SCREEN_SWITCH = auto()

    ACT_1 = auto()
    ACT_2 = auto()
    ACT_3 = auto()
    ACT_4 = auto()
    ACT_5 = auto()
    ACT_6 = auto()
    ACT_7 = auto()
    ACT_8 = auto()
    ACT_9 = auto()

    QUICK_ATC_1 = auto()
    QUICK_ATC_2 = auto()
    QUICK_ATC_3 = auto()
    QUICK_ATC_4 = auto()

    INTERACT = auto()

    @property
    def mapping(self):
        """Returns the current mapped char"""
        return get_mapping(self, hotkey_mappings)


class ActionList(list):
    """List of actions triggered by a key"""

    def triggers(self, *actions):
        """Checks if the self triggers a set of actions"""
        for action in actions:
            if action in self:
                return True
        return False

    def get_number(self):
        """Returns 0-8 if ACT_1 through ACT_9 is in the list, else -1"""
        for action in self:
            if action.value in range(Action.ACT_1.value, Action.ACT_9.value):
                return action.value - Action.ACT_1.value
        return -1

    def get_y_strength(self) -> int:
        """Gets move in Y direction"""
        if self.triggers(Action.UP, Action.UP_LEFT, Action.UP_RIGHT):
            return -1
        if self.triggers(Action.DOWN, Action.DOWN_LEFT, Action.DOWN_RIGHT):
            return 1
        return 0

    def get_x_strength(self) -> int:
        """Gets move in X direction"""
        if self.triggers(Action.RIGHT, Action.UP_RIGHT, Action.DOWN_RIGHT):
            return 1
        if self.triggers(Action.LEFT, Action.UP_LEFT, Action.DOWN_LEFT):
            return -1
        return 0


ACTION_DIRECTIONS = (Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN, 
                    Action.UP_LEFT, Action.UP_RIGHT, Action.DOWN_LEFT, Action.DOWN_RIGHT)
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
            Action.ACT_3, Action.MAP, Action.FREE_POKETE, Action.STATS_INFO,
            Action.CHOOSE_ITEM
        ]
    ),
    '4': ActionList(
        [
            Action.ACT_4, Action.INVENTORY, Action.CHOOSE_POKE,
            Action.ABILITIES_INFO
        ]
    ),
    '5': ActionList([Action.ACT_5, Action.POKEDEX]),
    '6': ActionList([Action.ACT_6, Action.CLOCK]),
    '7': ActionList([Action.ACT_7]),
    '8': ActionList([Action.ACT_8]),
    '9': ActionList([Action.ACT_9]),

    'a': ActionList([Action.LEFT]),
    'Key.left': ActionList([Action.LEFT]),
    'd': ActionList([Action.RIGHT]),
    'Key.right': ActionList([Action.RIGHT]),
    'w': ActionList([Action.UP]),
    'Key.up': ActionList([Action.UP]),
    's': ActionList([Action.DOWN]),
    'Key.down': ActionList([Action.DOWN]),

    'Key.space': ActionList([Action.ACCEPT]),
    'Key.enter': ActionList([Action.ACCEPT]),
    'y': ActionList([Action.ACCEPT, Action.QUICK_ATC_1]),
    'o': ActionList([Action.ACCEPT]),
    'q': ActionList([Action.CANCEL]),
    'n': ActionList([Action.CANCEL]),
    'Key.esc': ActionList([Action.CANCEL]),
    'Key.backspace': ActionList([Action.CANCEL]),

    'r': ActionList([Action.REMOVE]),
    'i': ActionList([Action.INFO, Action.INVENTORY]),
    'p': ActionList([Action.POKEDEX]),
    'f': ActionList([Action.FREE_POKETE]),
    'm': ActionList([Action.MAP, Action.MOVE_POKETE]),
    'c': ActionList([Action.CLOCK, Action.QUICK_ATC_3]),
    '?': ActionList([Action.HELP, Action.INFO]),
    'e': ActionList([Action.MENU, Action.SCREEN_SWITCH]),
    ':': ActionList([Action.CONSOLE]),

    'z': ActionList([Action.QUICK_ATC_1]),
    'x': ActionList([Action.QUICK_ATC_2]),
    'v': ActionList([Action.QUICK_ATC_4]),

    '#': ActionList([Action.INTERACT]),

    'h': ActionList([Action.UP_LEFT]),
    'j': ActionList([Action.DOWN_LEFT]),
    'k': ActionList([Action.UP_RIGHT]),
    'l': ActionList([Action.DOWN_RIGHT]),
}


def get_mapping(action, keys):
    """Returns the current mapped char"""
    for key, actions_list in keys.items():
        if action in actions_list:
            return key
    return None


def hotkeys_save():
    """Returns a save dict"""
    return {key: [i.name for i in value] for key, value in
            hotkey_mappings.items()}


def hotkeys_from_save(ctx, save, version_change):
    """Sets hotkey_mappings from save"""
    from ..input_loops import ask_bool
    global hotkey_mappings

    if save == {}:
        return

    new_hotkey_mappings = defaultdict(
        ActionList,
        {
            key: ActionList(
                [
                    Action[i] for i in value if i in Action.__members__
                ]
            )
            for key, value in save.items()
        }
    )
    unset = [
        action for action in Action
        if get_mapping(action, new_hotkey_mappings) is None
    ]
    if unset:
        if version_change or ask_bool(ctx, f"""The folowing keys are not set:
{liner(", ".join([i.name for i in unset]), 60)}
Should defaults be loaded for those keys?"""):
            for action in unset:
                key = action.mapping
                new_hotkey_mappings[key].append(action)
        else:
            sys.exit()
    hotkey_mappings = new_hotkey_mappings


# Exists maybe for performance so references to new actionlists don't have
# to always be cleaned up when the following function returns nothing
# I don't trust python to be smart enough to do this itself
EMPTY_ACTIONLIST = ActionList()


# Returns an action, then clears input; all input is valid to read only once
def get_action() -> ActionList:
    """Returns the current actions list"""
    retval = EMPTY_ACTIONLIST
    raw_input = _ev.get()
    if raw_input == "exit":
        raise KeyboardInterrupt
    if raw_input in hotkey_mappings:
        retval = hotkey_mappings[raw_input]
    _ev.clear()
    return retval
