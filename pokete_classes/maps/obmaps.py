from typing import TypedDict

from .coords import Coords


class DorArgs(TypedDict):
    x: int
    y: int
    map: str


class Dor(TypedDict):
    x: int
    y: int
    args: DorArgs


class SpecialDors(TypedDict):
    dor: Coords
    shopdor: Coords


class Ob(TypedDict):
    x: int
    y: int
    txt: str


class Obmap(TypedDict):
    hard_obs: dict[str, Ob]
    soft_obs: dict[str, Ob]
    dors: dict[str, Dor]
    special_dors: SpecialDors | None
    balls: dict[str, Coords]


Obmaps = dict[str, Obmap]
