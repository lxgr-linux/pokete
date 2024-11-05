from typing import TypedDict

import bs_rpc
from pokete_classes.asset_service.resources import AssetsDict
from pokete_classes.multiplayer.msg.position import Position
from pokete_classes.multiplayer.msg.position.update import UpdateDict

INFO_TYPE = "pokete.map.info"


class InfoData(TypedDict):
    assets: AssetsDict
    position: Position
    users: list[UpdateDict]
    greeting_text: str


class Info(bs_rpc.Body):
    def __init__(self, data: InfoData):
        super().__init__(INFO_TYPE, data)
