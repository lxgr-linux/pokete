from typing import TypedDict

import bs_rpc
from pokete_classes.asset_service.resources.base import PokeDict


class HandshakeData(TypedDict):
    user_name: str
    version: str
    pokes: list[PokeDict]


class Handshake(bs_rpc.Body):
    def __init__(self, data: HandshakeData):
        super().__init__("pokete.handshake", data)
