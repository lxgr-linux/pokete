from abc import ABC, abstractmethod
from enum import Enum, auto

from pokete.classes.fight.fightmap.fightmap import FightMap
from pokete.classes.fight.providers import Provider


class RoundContinuation(Enum):
    CONTINUE_ATTACK = auto()
    EXIT = auto()
    ENEMY_ATTACK = auto()


class FightItem(ABC):

    @abstractmethod
    def use(self, fightmap: FightMap, obj, enem:Provider) -> RoundContinuation:
        pass
