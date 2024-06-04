from typing import TypedDict

import bs_rpc


class Position(TypedDict):
    map: str
    x: int
    y: int


class UpdateData(TypedDict):
    name: str
    position: Position
    client: str  # TODO: Remove later


class Update(bs_rpc.Body):
    def __init__(self, data: UpdateData):
        super().__init__("pokete.position.update", data)
