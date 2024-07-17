from enum import Enum, auto

from ..attack import Attack
from ..inv import InvItem


class Result(Enum):
    ATTACK = auto()
    RUN_AWAY = auto()
    ITEM = auto()
    CHOOSE_POKE = auto()


class AttackResult:
    def __init__(
        self, result: Result, attack: Attack | None = None,
        item: InvItem | None = None
    ):
        self.result: Result = result
        self.attack: Attack | None = attack
        self.item: InvItem | None = item

    @classmethod
    def attack(cls, attack: Attack) -> "AttackResult":
        return cls(Result.ATTACK, attack=attack)

    @classmethod
    def run_away(cls) -> "AttackResult":
        return cls(Result.RUN_AWAY)

    @classmethod
    def item(cls, item: InvItem) -> "AttackResult":
        return cls(Result.ITEM, item=item)

    @classmethod
    def choose_poke(cls) -> "AttackResult":
        return cls(Result.CHOOSE_POKE)
