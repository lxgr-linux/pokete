from typing import TypedDict


class Type(TypedDict):
    effective: list[str]
    ineffective: list[str]
    color: list[str]


Types = dict[str, Type]
