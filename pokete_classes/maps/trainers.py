from typing import TypedDict


class TrainerPokeArgs(TypedDict):
    name: str
    xp: int


class TrainerArgs(TypedDict):
    name: str
    gender: str
    texts: list[str]
    lose_texts: list[str]
    win_texts: list[str]
    x: int
    y: int


class Trainer(TypedDict):
    pokes: list[TrainerPokeArgs]
    args: TrainerArgs


Trainers = dict[str, list[Trainer]]
