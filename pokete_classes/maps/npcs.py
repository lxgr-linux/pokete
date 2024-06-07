from typing import TypedDict, Self


class Chat(TypedDict):
    q: list[str]
    a: dict[str, Self]


class NPC(TypedDict):
    texts: list[str]
    fn: str | None
    map: str
    x: int
    y: int
    chat: Chat | None


NPCs = dict[str, NPC]
