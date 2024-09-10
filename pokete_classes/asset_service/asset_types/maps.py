from typing import TypedDict


class PokeArgs(TypedDict):
    pokes: list[str]
    minlvl: int
    maxlvl: int


class Map(TypedDict):
    height: int
    width: int
    song: str
    pretty_name: str
    extra_actions: str | None
    poke_args: PokeArgs | None
    w_poke_args: PokeArgs | None
    weather: str | None


Maps = dict[str, Map]
