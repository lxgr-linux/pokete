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
    'Key.LEFT': Action.LEFT,
    'd':         Action.RIGHT,
    'l':         Action.RIGHT,
    'Key.RIGHT': Action.RIGHT,
    'w':      Action.UP,
    'k':      Action.UP,
    'Key.UP': Action.UP,
    's':        Action.DOWN,
    'j':        Action.DOWN,
    'Key.DOWN': Action.DOWN,

    ' ':         Action.ACCEPT,
    'Key.ENTER': Action.ACCEPT,
    'y':         Action.ACCEPT,
    'q':       Action.CANCEL,
    'Key.ESC': Action.CANCEL,
    'n':       Action.CANCEL,

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

def get_input() -> Action:
    event = _ev()
    return hotkey_mappings[event]
