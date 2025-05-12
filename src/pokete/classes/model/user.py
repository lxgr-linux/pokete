from typing_extensions import TypedDict

from pokete.classes.model.poke import PokeDict
from pokete.classes.model.position import Position


class User(TypedDict):
    name: str
    position: Position
    client: None
    pokes: list[PokeDict]
    items: dict[str, int]
