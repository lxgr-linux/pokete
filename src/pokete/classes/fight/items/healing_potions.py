from abc import ABC
import logging

from pokete.classes.fight.fightmap.fightmap import FightMap
from pokete.classes.fight.items.item import FightItem, RoundContinuation
from pokete.classes.fight.providers import Provider


class GenericeHealingPotion(FightItem, ABC):
    def __init__(self, hp: int, name: str):
        self.hp = hp
        self.name = name

    def use(self, fightmap: FightMap, obj, enem: Provider) -> RoundContinuation:
        obj.remove_item(self.name)
        obj.curr.oldhp = obj.curr.hp
        obj.curr.hp = min(obj.curr.full_hp, obj.curr.hp + self.hp)
        obj.curr.hp_bar.update(obj.curr.oldhp)
        logging.info("[Fighitem][%s] Used", self.name)
        return RoundContinuation.ENEMY_ATTACK

class HealingPotion(GenericeHealingPotion):
    def __init__(self):
        super().__init__(5, "healing_potion")

class SuperPotion(GenericeHealingPotion):
    def __init__(self):
        super().__init__(15, "super_potion")
