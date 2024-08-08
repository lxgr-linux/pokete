from typing import TypedDict


class BaseIco(TypedDict):
    txt: str
    esc: str | None


class Poke(TypedDict):
    name: str
    hp: int
    atc: int
    defense: int
    attacks: list[str]
    pool: list[str]
    miss_chance: int
    desc: str
    lose_xp: int
    rarity: int
    types: list[str]
    evolve_poke: str
    evolve_lvl: int
    initiative: int
    ico: list[BaseIco]


Pokes = dict[str, Poke]
