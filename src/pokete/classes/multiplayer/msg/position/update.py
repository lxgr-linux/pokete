from typing import TypedDict

import pokete.bs_rpc as bs_rpc
from pokete.classes.asset_service.resources.base import PokeDict

UPDATE_TYPE = "pokete.position.update"


class Position(TypedDict):
    map: str
    x: int
    y: int


class UpdateDict(TypedDict):
    name: str
    position: Position


class Update(bs_rpc.Body):
    def __init__(self, data: UpdateDict):
        super().__init__(UPDATE_TYPE, data)
