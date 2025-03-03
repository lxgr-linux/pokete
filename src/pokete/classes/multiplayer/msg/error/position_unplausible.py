from typing import TypedDict

import pokete.bs_rpc as bs_rpc
from ..position import Position

POSITION_UNPLAUSIBLE_TYPE = "pokete.error.position_unplausible"


class PositionUnplausibleData(TypedDict):
    position: Position
    msg: str


class PositionUnplausible(bs_rpc.Body):
    def __init__(self, data: PositionUnplausibleData):
        super().__init__(POSITION_UNPLAUSIBLE_TYPE, data)
