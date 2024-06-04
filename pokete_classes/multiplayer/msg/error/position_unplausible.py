from typing import TypedDict

import bs_rpc
from ..position import Position


class PositionUnplausibleData(TypedDict):
    position: Position
    msg: str


class PositionUnplausible(bs_rpc.Body):
    def __init__(self, data: PositionUnplausibleData):
        super().__init__("pokete.error.position_unplausible", data)
