from typing import TypedDict

import bs_rpc
from pokete_classes.asset_service.asset_types import Assets
from pokete_classes.multiplayer.msg.position import Position
from pokete_classes.multiplayer.msg.position.update import User

INFO_TYPE = "pokete.map.info"


class InfoData(TypedDict):
    assets: Assets
    position: Position
    users: list[User]
    greeting_text: str


class Info(bs_rpc.Body):
    def __init__(self, data: InfoData):
        super().__init__(INFO_TYPE, data)
