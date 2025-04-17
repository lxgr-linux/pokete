from abc import ABC
import logging
import random
import time

from pokete.classes.achievements import achievements
from pokete.classes.fight.fightmap.fightmap import FightMap
from pokete.classes.fight.providers import Provider
from pokete.classes.audio import audio
from ... import ob_maps as obmp
from pokete.classes.fight.providers import NatureProvider
from .item import FightItem, RoundContinuation
from ...asset_service.service import asset_service
from pokete.release import SPEED_OF_TIME


class GenericPokeBall(FightItem, ABC):
    def __init__(self, chance:int, name: str):
        self.chance = chance
        self.name = name

    def use(self, fightmap: FightMap, obj:Provider, enem:Provider) -> RoundContinuation:
        """Throws a ball
        ARGS:
            obj: The players Poke object
            enem: The enemys Poke object
            chance: The balls catch chance
            name: The balls name
        RETURNS:
            1: The continue the attack round
            2: The win the game
            None: To let the enemy attack"""
        if not isinstance(enem, NatureProvider):
            fightmap.outp.outp("You can't do that in a duel!")
            return RoundContinuation.CONTINUE_ATTACK
        fightmap.outp.rechar(f"You threw a {self.name.capitalize()}!")
        fightmap.fast_change(
            [enem.curr.ico, fightmap.deadico1, fightmap.deadico2,
             fightmap.pball], enem.curr.ico)
        time.sleep(SPEED_OF_TIME * random.choice([1, 2, 3, 4]))
        obj.remove_item(self.name)
        catch_chance = 20 if obj.map == obmp.ob_maps.get("playmap_1", None) else 0
        for effect in enem.curr.effects:
            catch_chance += effect.catch_chance
        if random.choices([True, False],
                          weights=[(enem.curr.full_hp / enem.curr.hp)
                                   * self.chance + catch_chance,
                                   enem.curr.full_hp], k=1)[0]:
            audio.switch("xDeviruchi - Decisive Battle (End).mp3")
            obj.add_poke(enem.curr, caught_with=self.name)
            fightmap.outp.outp(f"You caught {enem.curr.name}!")
            time.sleep(SPEED_OF_TIME * 2)
            fightmap.pball.remove()
            fightmap.clean_up(obj, enem)
            obj.balls_label_rechar()
            logging.info("[Fighitem][%s] Caught %s", self.name, enem.curr.name)
            achievements.achieve("first_poke")
            if all(poke in obj.caught_pokes for poke in
                   asset_service.get_base_assets().pokes):
                achievements.achieve("catch_em_all")
            return RoundContinuation.EXIT
        fightmap.outp.outp("You missed!")
        fightmap.show()
        fightmap.pball.remove()
        enem.curr.ico.add(fightmap, enem.curr.ico.x, enem.curr.ico.y)
        fightmap.show()
        logging.info("[Fighitem][%s] Missed", self.name)
        return RoundContinuation.ENEMY_ATTACK

class PoketeBall(GenericPokeBall):
    def __init__(self):
        super().__init__(1, "poketeball")


class SuperBall(GenericPokeBall):
    def __init__(self):
        super().__init__(6, "superball")

class HyperBall(GenericPokeBall):
    def __init__(self):
        super().__init__(1000, "hyperball")
