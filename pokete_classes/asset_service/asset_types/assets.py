from typing import TypedDict

from .base import Items, Pokes, Natures, Weathers, Types, Achievements
from .maps import Maps
from .npcs import NPCs
from .stations import Stations, Decorations
from .trainers import Trainers
from .obmaps import Obmaps


class BaseAssets(TypedDict):
    items: Items
    pokes: Pokes
    natures: Natures
    weathers: Weathers
    types: Types
    achievements: Achievements


class Assets(TypedDict):
    trainers: Trainers
    npcs: NPCs
    obmaps: Obmaps
    stations: Stations
    decorations: Decorations
    maps: Maps
