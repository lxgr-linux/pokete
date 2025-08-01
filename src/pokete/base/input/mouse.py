import logging
import re
from dataclasses import dataclass
from enum import Enum

from pokete import bs_rpc


class MouseEventType(Enum):
    MOVE = 35
    LEFT = 0
    RIGHT = 2


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
        logging.info("handle %s", inp)
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
