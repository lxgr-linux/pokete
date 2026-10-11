from typing import Protocol

from pokete.classes.asset_service.resources.base import Poke as ResourcePoke
from pokete.classes.types import PokeType


class IEffect(Protocol):
    name: str
    c_name: str
    rem_chance: int
    catch_chance: int
    text: str
    str_esccode: str
    exclude: list[str]


class IStats(Protocol):
    poke_name: str
    ownership_date: str
    caught_with: str | None
    evolved_date = str | None
    total_battles = int
    lost_battles = int
    win_battles = int
    earned_xp = int
    run_away = int


class IPoke(Protocol):
    xp: int
    hp: int
    full_hp: int
    name: str
    # Name to display i fights
    ext_name: str
    inf: ResourcePoke

    type: PokeType
    types: list[PokeType]

    atc: int
    defense: int
    initiative: int

    player: bool
    shiny: bool
    effects: list[IEffect]

    def lvl(self) -> int: ...
