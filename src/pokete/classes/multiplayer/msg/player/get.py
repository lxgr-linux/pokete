from typing import TypedDict

import pokete.bs_rpc as bs_rpc

GET_TYPE = "pokete.player.get"


class GetData(TypedDict):
    name: str


class Get(bs_rpc.Body):
    def __init__(self, data: GetData):
        super().__init__(GET_TYPE, data)
