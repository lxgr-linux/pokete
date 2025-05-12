from typing import TypedDict

import pokete.bs_rpc as bs_rpc
from pokete.classes.model.position import Position

UPDATE_TYPE = "pokete.position.update"


class UpdateDict(TypedDict):
    name: str
    position: Position


class Update(bs_rpc.Body):
    def __init__(self, data: UpdateDict):
        super().__init__(UPDATE_TYPE, data)
