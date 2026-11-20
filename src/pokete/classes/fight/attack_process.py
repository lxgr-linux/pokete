import logging
import random
import time

from pokete.base.context import Context
from pokete.classes.attack import Attack
from pokete.classes.attack_actions import AttackActions
from pokete.classes.effects import effects
from pokete.classes.poke.poke import Poke
from pokete.classes.weather import Weather
from pokete.release import SPEED_OF_TIME

from .fightmap import FightMap
from .providers import Provider


class AttackProcess:
    def __init__(self, fightmap: FightMap) -> None:
        self.fightmap: FightMap = fightmap

    @staticmethod
    def get_random_factor(attack, attacker) -> float:
        return random.choices(
            [0, 0.75, 1, 1.26],
            weights=[attack.miss_chance + attacker.miss_chance, 1, 1, 1],
            k=1,
        )[0]

    @staticmethod
    def get_base_effectivity(defender: Poke, attack: Attack) -> float:
        return (
            1.3
            if defender.type.name in attack.type.effective
            else 0.5
            if defender.type.name in attack.type.ineffective
            else 1
        )

    @staticmethod
    def get_hp(
        attacker: Poke, defender: Poke, attack: Attack, random_factor: float, eff: int
    ) -> int:
        return (
            0
            if random_factor == 0
            else max(
                3,
                round(
                    (attacker.atc * attack.factor / max(defender.defense, 1))
                    * random_factor
                    * eff
                ),
            )
        )

    def __call__(
        self,
        ctx: Context,
        attacker: Poke,
        defender: Poke,
        attack: Attack,
        providers: list[Provider],
    ) -> None:
        """Attack process
        ARGS:
            attack: Attack object
            defender: Enemy Poke"""
        weather: Weather = ctx.figure.map.weather
        if attack.ap > 0:
            for e in attacker.effects:
                self.fightmap.remove_effect(e, attacker, providers[0])
            for e in attacker.effects:
                if e.effect(
                    attacker, self.fightmap, self.fightmap.provider_labels(providers[0])
                ):
                    return
            if any(isinstance(i, effects["confusion"]) for i in attacker.effects):
                attacker.enem = defender = attacker
            else:
                attacker.enem = defender
            w_eff: float = 1
            random_factor = self.get_random_factor(attack, attacker)
            if weather is not None:
                w_eff = weather.effect(attack.type)
                self.fightmap.show_weather(weather)

            eff: float = self.get_base_effectivity(defender, attack) * w_eff
            n_hp = self.get_hp(attacker, defender, attack, random_factor, eff)

            attacker.backup_hp()
            defender.backup_hp()
            defender.set_hp(n_hp)
            time.sleep(SPEED_OF_TIME * 0.4)
            for i in attack.move:
                self.fightmap.show_attack_move(i, bool(attacker.player))
            if attack.action is not None and random_factor != 0:
                getattr(AttackActions, attack.action)(attacker, defender, providers)
            attack.set_ap(attack.ap - 1)
            self.fightmap.show_effectivity(eff, n_hp, random_factor, attacker, attack)
            if defender == attacker:
                self.fightmap.show_hurt_it_self(attacker)
            if random_factor != 0:
                self.give_effect(defender, attack, providers[1])
            for prov in providers if providers[0] != providers[1] else [providers[1]]:
                self.fightmap.provider_labels(prov).hp_bar.update(
                    prov.curr.oldhp, prov.curr.hp
                )
            logging.info(
                "[Fight][%s] Used %s: %s",
                attacker.name,
                attack.name,
                str({"eff": eff, "n_hp": n_hp}),
            )
            self.fightmap.show()

    def give_effect(self, enem: Poke, attack: Attack, provider: Provider) -> None:
        """Gives the associated effect to a Pokete
        ARGS:
            enem: Enemy object"""
        if attack.effect is not None:
            time.sleep(SPEED_OF_TIME * 1.5)
            self.fightmap.add_effect(effects[attack.effect](), enem, provider)
