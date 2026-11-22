from typing import TypedDict

from pokete import bs_rpc
from pokete.classes.model.user import User

PLAYER_TYPE = "pokete.player.player"


class PlayerData(TypedDict):
    user: User


class Player(bs_rpc.Body):
    def __init__(self, data: PlayerData) -> None:
        super().__init__(PLAYER_TYPE, data)
