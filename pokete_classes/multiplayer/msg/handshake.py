from typing import TypedDict

import bs_rpc
from pokete_classes.asset_service.resources.base import PokeDict
from pokete_classes.multiplayer.msg.player import player


class HandshakeData(TypedDict):
    user: player.User
    version: str


class Handshake(bs_rpc.Body):
    def __init__(self, data: HandshakeData):
        super().__init__("pokete.handshake", data)
