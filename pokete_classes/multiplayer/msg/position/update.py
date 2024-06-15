from typing import TypedDict

import bs_rpc

UPDATE_TYPE = "pokete.position.update"


class Position(TypedDict):
    map: str
    x: int
    y: int


class User(TypedDict):
    name: str
    position: Position
    client: None  # TODO: Remove later


class Update(bs_rpc.Body):
    def __init__(self, data: User):
        super().__init__(UPDATE_TYPE, data)
