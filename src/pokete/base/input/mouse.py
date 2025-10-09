import re
from dataclasses import dataclass
from enum import Enum

from pokete import bs_rpc


class MouseEventType(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2
    ALT_LEFT = 8
    ALT_MIDDLE = 9
    ALT_RIGHT = 10
    DRAG_LEFT = 32
    DRAG_MIDDLE = 33
    DRAG_RIGHT = 34
    DRAG_ALT_LEFT = 40
    DRAG_ALT_MIDDLE = 41
    DRAG_ALT_RIGHT = 42
    MOVE = 35
    ALT_MOVE = 43
    SCROLL_UP = 64
    SCROLL_DOWN = 65
    SCROLL_RIGHT = 66
    SCROLL_LEFT = 67
    MISC_1 = 128
    MISC_2 = 129
    MISC_1_MOVE = 160
    MISC_2_MOVE = 161


@dataclass
class MouseEvent:
    type: MouseEventType
    x: int
    y: int
    pressed: bool


class MouseManager:
    def __init__(self) -> None:
        self.pattern = re.compile(r"\[<[0-9]*;[0-9]*;[0-9]*[m|M]")
        self.events: bs_rpc.Channel[MouseEvent] = bs_rpc.Channel()

    def is_mouse_event(self, inp: str) -> bool:
        return not not self.pattern.match(inp)

    def handle(self, inp: str):
        # logging.info("handle %s", inp)
        pressed = inp.endswith("m")

        num_vals: list[int] = [
            int(i) for i in inp.strip("[<").strip("m").strip("M").split(";")
        ]

        self.events.push(
            MouseEvent(
                MouseEventType(num_vals[0]),
                num_vals[1] - 1,
                num_vals[2] - 1,
                pressed,
            )
        )


mouse_manager = MouseManager()
