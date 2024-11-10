from enum import Enum, auto
import logging

from pokete_classes.multiplayer.msg.fight.fight_decision import FightDecisionData
from pokete_classes.multiplayer.msg.player import player
from pokete_classes.multiplayer.msg.poke import PokeDict
from pokete_classes.inv.items import invitems
from pokete_classes.poke.poke import Poke
from ..attack import Attack
from ..inv import InvItem


class Result(Enum):
    ATTACK = auto()
    RUN_AWAY = auto()
    ITEM = auto()
    CHOOSE_POKE = auto()



class FightDecision:
    def __init__(
        self, result: Result, attack: Attack | None = None,
        item: InvItem | None = None
    ):
        self.result: Result = result
        self.attack_value: Attack | None = attack
        self.item_value: InvItem | None = item

    def to_dict(self) -> FightDecisionData:
        result: FightDecisionData = {
            "result": self.result.value,
            "attack": None if self.attack_value is None else self.attack_value.index,
            "item": None if self.item_value is None else self.item_value.name,
        }
        return result

    @classmethod
    def from_dict(
        cls, _d: FightDecisionData, _poke: Poke, _player: player.User
    ):
        match _d["result"]:
            case Result.ATTACK.value:
                logging.info("%s, %s", _d["attack"], _poke.attacks)
                assert _d["attack"] in _poke.attacks
                attack = _poke.attack_obs[_poke.attacks.index(_d["attack"])]
                return cls.attack(attack)
            case Result.ITEM.value:
                assert _d["item"] in _player["items"].keys()
                item = getattr(invitems, _d["item"])
                return cls.item(item)
            case Result.RUN_AWAY.value:
                return cls.run_away()
            case Result.CHOOSE_POKE.value:
                return cls.run_away()
            case _:
                assert False


    @classmethod
    def attack(cls, attack: Attack) -> "FightDecision":
        return cls(Result.ATTACK, attack=attack)

    @classmethod
    def run_away(cls) -> "FightDecision":
        return cls(Result.RUN_AWAY)

    @classmethod
    def item(cls, item: InvItem) -> "FightDecision":
        return cls(Result.ITEM, item=item)

    @classmethod
    def choose_poke(cls) -> "FightDecision":
        return cls(Result.CHOOSE_POKE)
