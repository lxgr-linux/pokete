from typing import TypedDict


class StatsDict(TypedDict):
    ownership_date: str | None
    evolved_date: str | None
    total_battles: int
    lost_battles: int
    win_battles: int
    earned_xp: int
    caught_with: str
    run_away: int


class NatureDict(TypedDict):
    nature: str
    grade: int


class PokeDict(TypedDict):
    name: str
    xp: int
    hp: int
    ap: list[int]
    effects: list[str]
    attacks: list[str]
    shiny: bool
    nature: NatureDict
    stats: StatsDict
