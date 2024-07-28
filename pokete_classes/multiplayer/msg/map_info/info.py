from typing import TypedDict

import bs_rpc
from pokete_classes.maps import Obmaps, Maps, NPCs, Trainers, Stations, \
    Decorations
from pokete_classes.multiplayer.msg.position import Position
from pokete_classes.multiplayer.msg.position.update import User

INFO_TYPE = "pokete.map.info"


class InfoData(TypedDict):
    obmaps: Obmaps
    maps: Maps
    npcs: NPCs
    trainers: Trainers
    map_stations: Stations
    map_decorations: Decorations
    position: Position
    users: list[User]
    greeting_text: str


class Info(bs_rpc.Body):
    def __init__(self, data: InfoData):
        super().__init__(INFO_TYPE, data)
