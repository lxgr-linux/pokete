import logging
from pokete.classes.fight.fightmap.fightmap import FightMap
from pokete.classes.fight.items.item import FightItem, RoundContinuation
from pokete.classes.fight.providers import Provider


class ApPotion(FightItem):
    def use(self, fightmap: FightMap, obj, enem: Provider) -> RoundContinuation:
        obj.remove_item("ap_potion")
        for atc in obj.curr.attack_obs:
            atc.set_ap(atc.max_ap)
        logging.info("[Fighitem][ap_potion] Used")
        return RoundContinuation.ENEMY_ATTACK
