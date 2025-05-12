from typing import TypedDict


class FightDecisionData(TypedDict):
    result: int
    attack: str | None
    item: str | None
    poke: int | None
