from typing import TypedDict


class Nature(TypedDict):
    esc: str
    atc: float
    _def: float


Natures = dict[str, Nature]
