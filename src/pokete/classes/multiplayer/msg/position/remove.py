from typing import TypedDict

import pokete.bs_rpc as bs_rpc

REMOVE_TYPE = "pokete.position.remove"


class RemoveData(TypedDict):
    user_name: str


class Remove(bs_rpc.Body):
    def __init__(self, data: RemoveData):
        super().__init__(REMOVE_TYPE, data)
