from typing import TypedDict

import pokete.bs_rpc as bs_rpc

RESPONSE_TYPE = "pokete.fight.response"


class ResponseData(TypedDict):
    accept: bool


class Response(bs_rpc.Body):
    def __init__(self, data: ResponseData):
        super().__init__(RESPONSE_TYPE, data)
