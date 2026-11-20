import logging
from abc import ABC

from pokete.classes.fight.fightmap.fightmap import FightMap
from pokete.classes.fight.items.item import FightItem, RoundContinuation
from pokete.classes.fight.providers import Provider



class GenericeHealingPotion(FightItem, ABC):
    logger = logging.getLogger("GenericeHealingPotion")
    def __init__(self, hp: int, name: str) -> None:
        self.hp = hp
        self.name = name

    def use(self, fightmap: FightMap, obj, enem: Provider) -> RoundContinuation:
        obj.remove_item(self.name)
        obj.curr.oldhp = obj.curr.hp
        obj.curr.hp = min(obj.curr.full_hp, obj.curr.hp + self.hp)
        obj.curr.hp_bar.update(obj.curr.oldhp, obj.curr.hp)
        self.logger.info("[Fighitem][%s] Used", self.name)
        return RoundContinuation.ENEMY_ATTACK


class HealingPotion(GenericeHealingPotion):
    logger = logging.getLogger("HealingPotion")
    def __init__(self) -> None:
        super().__init__(5, "healing_potion")


class SuperPotion(GenericeHealingPotion):
    logger = logging.getLogger("SuperPotion")
    def __init__(self) -> None:
        super().__init__(15, "super_potion")
