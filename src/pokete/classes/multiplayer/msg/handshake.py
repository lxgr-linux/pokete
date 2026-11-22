from typing import TypedDict

from pokete import bs_rpc
from pokete.classes.multiplayer.msg.player import player


class HandshakeData(TypedDict):
    user: player.User
    version: str


class Handshake(bs_rpc.Body):
    def __init__(self, data: HandshakeData) -> None:
        super().__init__("pokete.handshake", data)
