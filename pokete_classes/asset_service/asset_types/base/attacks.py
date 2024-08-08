from typing import TypedDict


class Attack(TypedDict):
    name: str
    factor: float
    action: str | None
    world_action: str
    move: list[str]
    miss_chance: float
    min_lvl: int
    desc: str
    types: list[str]
    effect: str | None
    is_generic: bool
    ap: int


Attacks = dict[str, Attack]
