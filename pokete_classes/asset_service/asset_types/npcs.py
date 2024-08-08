from typing import TypedDict


class Chat(TypedDict):
    q: list[str]
    a: dict[str, "Chat"]


class NPC(TypedDict):
    texts: list[str]
    fn: str | None
    map: str
    x: int
    y: int
    chat: Chat | None


NPCs = dict[str, NPC]
