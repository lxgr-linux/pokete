from typing import TypedDict

import bs_rpc


class HandshakeData(TypedDict):
    user_name: str
    version: str


class Handshake(bs_rpc.Body):
    def __init__(self, data: HandshakeData):
        super().__init__("pokete.handshake", data)
