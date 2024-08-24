from typing import TypedDict

from .base import Items, Pokes, Natures, Weathers, Types, Achievements, Attacks
from .maps import Maps
from .npcs import NPCs
from .stations import Stations, Decorations
from .trainers import Trainers
from .obmaps import Obmaps


class BaseAssets(TypedDict):
    items: Items
    pokes: Pokes
    attacks: Attacks
    natures: Natures
    weathers: Weathers
    types: Types
    sub_types: list[str]
    achievements: Achievements


class Assets(TypedDict):
    trainers: Trainers
    npcs: NPCs
    obmaps: Obmaps
    stations: Stations
    decorations: Decorations
    maps: Maps
