from typing import TypedDict


class Achievement(TypedDict):
    title: str
    desc: str


Achievements = dict[str, Achievement]
