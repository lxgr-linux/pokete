from typing import TypedDict

import bs_rpc
from pokete_classes.multiplayer.msg.poke import PokeDict
from pokete_classes.multiplayer.msg.position.update import Position

PLAYER_TYPE = "pokete.player.player"


class User(TypedDict):
    name: str
    position: Position
    client: None
    pokes: list[PokeDict]
    items: dict[str, int]

class PlayerData(TypedDict):
    user: User


class Player(bs_rpc.Body):
    def __init__(self, data: PlayerData):
        super().__init__(PLAYER_TYPE, data)
