from typing import TypedDict

from .coords import Coords


class StationGen(TypedDict):
    additionals: list[str]
    desc: str
    text: str
    color: str
    a_next: str | None
    w_next: str | None
    s_next: str | None
    d_next: str | None


class Station(TypedDict):
    gen: StationGen
    add: Coords


class DecorationGen(TypedDict):
    text: str
    color: str


class Decoration(TypedDict):
    gen: DecorationGen
    add: Coords


Decorations = dict[str, Decoration]
Stations = dict[str, Station]
