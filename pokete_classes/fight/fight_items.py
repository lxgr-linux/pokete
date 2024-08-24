import logging
import random
import time

from pokete_classes import ob_maps as obmp
from pokete_classes.achievements import achievements
from pokete_classes.audio import audio
from pokete_classes.fight import FightMap
from pokete_classes.fight.providers import NatureProvider, Provider
from release import SPEED_OF_TIME
from .. import movemap as mvp
from ..asset_service.service import asset_service


class FightItems:
    """Contains all fns callable by an item in fight
    The methods that can actually be called in fight follow
    the following pattern:
        ARGS:
            obj: The players Provider
            enem: The enemys Provider
        RETURNS:
            1: To continue the attack round
            2: To win the game
            None: To let the enemy attack"""

    @staticmethod
    def __throw(fightmap: FightMap, obj, enem: Provider, chance, name):
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
            return 1
        fightmap.outp.rechar(f"You threw a {name.capitalize()}!")
        fightmap.fast_change(
            [enem.curr.ico, fightmap.deadico1, fightmap.deadico2,
             fightmap.pball], enem.curr.ico)
        time.sleep(SPEED_OF_TIME * random.choice([1, 2, 3, 4]))
        obj.remove_item(name)
        catch_chance = 20 if obj.map == obmp.ob_maps["playmap_1"] else 0
        for effect in enem.curr.effects:
            catch_chance += effect.catch_chance
        if random.choices([True, False],
                          weights=[(enem.curr.full_hp / enem.curr.hp)
                                   * chance + catch_chance,
                                   enem.curr.full_hp], k=1)[0]:
            audio.switch("xDeviruchi - Decisive Battle (End).mp3")
            obj.add_poke(enem.curr, caught_with=name)
            fightmap.outp.outp(f"You caught {enem.curr.name}!")
            time.sleep(SPEED_OF_TIME * 2)
            fightmap.pball.remove()
            fightmap.clean_up(obj, enem)
            mvp.movemap.balls_label_rechar(obj.pokes)
            logging.info("[Fighitem][%s] Caught %s", name, enem.curr.name)
            achievements.achieve("first_poke")
            if all(poke in obj.caught_pokes for poke in
                   asset_service.get_base_assets()["pokes"]):
                achievements.achieve("catch_em_all")
            return 2
        fightmap.outp.outp("You missed!")
        fightmap.show()
        fightmap.pball.remove()
        enem.curr.ico.add(fightmap, enem.curr.ico.x, enem.curr.ico.y)
        fightmap.show()
        logging.info("[Fighitem][%s] Missed", name)
        return None

    @staticmethod
    def __potion(obj, hp, name):
        """Potion function
        ARGS:
            obj: The players Poke object
            hp: The hp that will be given to the Poke
            name: The potions name"""

        obj.remove_item(name)
        obj.curr.oldhp = obj.curr.hp
        obj.curr.hp = min(obj.curr.full_hp, obj.curr.hp + hp)
        obj.curr.hp_bar.update(obj.curr.oldhp)
        logging.info("[Fighitem][%s] Used", name)

    def heal_potion(self, fightmap: FightMap, obj, _):
        """Healing potion function"""
        return self.__potion(obj, 5, "healing_potion")

    def super_potion(self, fightmap: FightMap, obj, _):
        """Super potion function"""
        return self.__potion(obj, 15, "super_potion")

    def poketeball(self, fightmap: FightMap, obj, enem):
        """Poketeball function"""
        return self.__throw(fightmap, obj, enem, 1, "poketeball")

    def superball(self, fightmap: FightMap, obj, enem):
        """Superball function"""
        return self.__throw(fightmap, obj, enem, 6, "superball")

    def hyperball(self, fightmap: FightMap, obj, enem):
        """Hyperball function"""
        return self.__throw(fightmap, obj, enem, 1000, "hyperball")

    @staticmethod
    def ap_potion(obj, _):
        """AP potion function"""
        obj.remove_item("ap_potion")
        for atc in obj.curr.attack_obs:
            atc.set_ap(atc.max_ap)
        logging.info("[Fighitem][ap_potion] Used")


fightitems = FightItems()
