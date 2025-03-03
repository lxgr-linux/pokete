from typing import TypedDict

import pokete.bs_rpc as bs_rpc
from pokete.classes.asset_service.resources.base import PokeDict
from pokete.classes.multiplayer.msg.player import player


class HandshakeData(TypedDict):
    user: player.User
    version: str


class Handshake(bs_rpc.Body):
    def __init__(self, data: HandshakeData):
        super().__init__("pokete.handshake", data)
