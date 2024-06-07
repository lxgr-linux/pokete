from typing import TypedDict

from .coords import Coords


class StationGen(TypedDict):
    additionals: list[str]
    width: int
    height: int
    desc: str
    a_next: str | None
    w_next: str | None
    s_next: str | None
    d_next: str | None


class Station(TypedDict):
    gen: StationGen
    add: Coords


Stations = dict[str, Station]
