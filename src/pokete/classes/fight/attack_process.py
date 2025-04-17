import random
import time
import logging

from pokete.classes.attack import Attack
from pokete.release import SPEED_OF_TIME
from .providers import Provider
from .fightmap import FightMap
from ..attack_actions import AttackActions
from ..effects import effects
from ..poke import Poke


class AttackProcess:
    def __init__(self, fightmap: FightMap):
        self.fightmap: FightMap = fightmap

    @staticmethod
    def get_random_factor(attack, attacker) -> float:
        return random.choices(
            [0, 0.75, 1, 1.26],
            weights=[attack.miss_chance
                     + attacker.miss_chance,
                     1, 1, 1], k=1
        )[0]

    @staticmethod
    def get_base_effectivity(defender: Poke, attack: Attack) -> float:
        return (
            1.3 if defender.type.name in attack.type.effective else 0.5
            if defender.type.name in attack.type.ineffective else 1
        )

    @staticmethod
    def get_hp(attacker: Poke, defender: Poke, attack: Attack,
               random_factor: int, eff: int) -> int:
        return round((attacker.atc
                      * attack.factor
                      / (defender.defense if defender.defense >= 1 else 1))
                     * random_factor * eff)

    def __call__(self, attacker: Poke, defender: Poke, attack: Attack,
                 providers: list[Provider]):
        """Attack process
        ARGS:
            attack: Attack object
            defender: Enemy Poke"""
        weather = providers[0].map.weather
        if attack.ap > 0:
            for eff in attacker.effects:
                eff.remove()
            for eff in attacker.effects:
                if eff.effect() == 1:
                    return
            if any(isinstance(i, effects.confusion) for i in attacker.effects):
                attacker.enem = defender = attacker
            else:
                attacker.enem = defender
            w_eff = 1
            random_factor = self.get_random_factor(attack, attacker)
            if weather is not None:
                w_eff = weather.effect(attack.type)
                self.fightmap.show_weather(weather)

            eff = self.get_base_effectivity(defender, attack) * w_eff
            n_hp = self.get_hp(attacker, defender, attack, random_factor, eff)

            attacker.backup_hp()
            defender.backup_hp()
            defender.set_hp(n_hp)
            time.sleep(SPEED_OF_TIME * 0.4)
            for i in attack.move:
                getattr(attacker.moves, i)()
            if attack.action is not None and random_factor != 0:
                getattr(AttackActions, attack.action)(attacker, defender,
                                                      providers)
            attack.set_ap(attack.ap - 1)
            self.fightmap.show_effectivity(eff, n_hp, random_factor, attacker,
                                           attack)
            if defender == attacker:
                self.fightmap.show_hurt_it_self(attacker)
            if random_factor != 0:
                attack.give_effect(defender)
            for obj in [defender, attacker] if defender != attacker else [
                defender]:
                obj.hp_bar.update(obj.oldhp)
            logging.info("[Fight][%s] Used %s: %s", attacker.name, attack.name,
                         str({"eff": eff, "n_hp": n_hp}))
            self.fightmap.show()
