"""Contains the Poke class"""

import math
import time
import logging
import random
from datetime import datetime
import scrap_engine as se
import pokete_data as p_data
from pokete_general_use_fns import liner
from release import SPEED_OF_TIME
from .attack_actions import AttackActions
from .attack import Attack
from .health_bar import HealthBar
from .pokestats import PokeStats
from .evomap import EvoMap
from .color import Color
from .moves import Moves
from .types import types
from .effects import effects
from .learnattack import LearnAttack
from .nature import PokeNature
from .achievements import achievements
from .loops import std_loop


class Poke:
    """The Pokete class
    ARGS:
        poke: The Pokes generic name
        _xp: Initial xp
        _hp: Initial hp ('SKIP' sets to max hp)
        _attacks: List of attack names learned
        player: Bool whether or not the Poke belongs to the player
        shiny: Bool whether or not the Poke is shiny (is extra strong)"""

    def __init__(self, poke, _xp, _hp="SKIP", _ap=None, _attacks=None,
                 _effects=None, player=True, shiny=False, nature=None,
                 stats=None):
        self.nature = PokeNature.random() if nature is None \
            else PokeNature.from_dict(nature)
        self.inf = p_data.pokes[poke]
        self.moves = Moves(self)
        # Attributes
        self.night_active = self.inf.get("night_active", None)
        self.enem = None
        self.oldhp = 0
        self.xp = _xp
        self.identifier = poke
        self.shiny = shiny
        self.atc = 0
        self.defense = 0
        self.initiative = 0
        #We set the hp to increase by 2 each time the level of Pokemon rises
        self.hp = round((self.lvl() * 2 + self.inf["hp"]))
        self.name = self.inf["name"]
        self.miss_chance = self.inf["miss_chance"]
        self.lose_xp = self.inf["lose_xp"]
        self.evolve_poke = self.inf["evolve_poke"]
        self.evolve_lvl = self.inf["evolve_lvl"]
        self.types = [getattr(types, i) for i in self.inf["types"]]
        self.type = self.types[0]
        self.effects = []
        if _attacks is not None:
            assert (len(_attacks) <= 4), f"A Pokete {poke} \
can't have more than 4 attacks!"
        else:
            _attacks = self.inf["attacks"][:4]
        self.attacks = [atc for atc in _attacks
                        if self.lvl() >= p_data.attacks[atc]["min_lvl"]]
        if self.shiny:
            self.hp += 5
        self.attack_obs = [Attack(atc, str(i + 1))
                           for i, atc in enumerate(self.attacks)
                           if self.lvl() >= p_data.attacks[atc]["min_lvl"]]
        self.set_player(player)
        # Backup vars
        self.full_hp = self.hp
        self.full_miss_chance = self.miss_chance
        # re-set hp
        if _hp != "SKIP":
            self.hp = _hp
        # Labels
        self.hp_bar = HealthBar(self)
        self.hp_bar.make(self.hp)
        self.desc = se.Text(liner(self.inf["desc"], se.screen_width - 34))
        self.ico = se.Box(4, 11)
        for ico in self.inf["ico"]:
            esccode = (str.join("", [getattr(Color, i) for i in ico["esc"]])
                       if ico["esc"] is not None
                       else "")
            self.ico.add_ob(se.Text(ico["txt"], state="float",
                                    esccode=esccode,
                                    ignore=f'{esccode} {Color.reset}'), 0, 0)
        self.text_hp = se.Text(f"HP:{self.hp}", state="float")
        self.text_lvl = se.Text(f"Lvl:{self.lvl()}", state="float")
        self.text_name = se.Text(
            (self.name.upper() if self.shiny else self.name),
            esccode=Color.underlined + self.type.color,
            state="float")
        self.text_xp = se.Text(
            f"XP:{self.xp - (self.lvl() ** 2 - 1)}/\
{((self.lvl() + 1) ** 2 - 1) - (self.lvl() ** 2 - 1)}",
            state="float")
        self.text_type = se.Text(self.type.name.capitalize(),
                                 state="float", esccode=self.type.color)
        self.tril = se.Object("<", state="float")
        self.trir = se.Object(">", state="float")
        self.pball_small = se.Object("o")
        self.set_vars()
        if _ap is not None:
            self.set_ap(_ap)
        if _effects is not None:
            for eff in _effects:
                self.effects.append(getattr(effects, eff)(self))

        self.poke_stats = PokeStats(self.name, None) if stats is None \
            else PokeStats.from_dict(stats, self.name)

    def set_player(self, player):
        """Sets the player attribute when the Pokete changes the owner
        ARGS:
            player: Bool whether or not the Poke new belongs to the player"""
        self.player = player
        self.affil = "you" if self.player else "enemy"
        self.ext_name = f'{self.name}({self.affil})'

    def set_poke_stats(self, poke_stats):
        """Sets the Poketes stats:
        ARGS:
            poke_stats: PokeStats object"""
        self.poke_stats = poke_stats

    def set_vars(self):
        """Updates/sets some vars"""
        for name in ["atc", "defense", "initiative"]:
            setattr(self, name, round((self.lvl() + self.inf[name]
                    + (2 if self.shiny else 0)) * self.nature.get_value(name)))
        #when my poke's level up
        if(self.full_hp < round(self.inf["hp"] + self.lvl() * 2)):
            self.hp += 2
            self.text_hp.rechar(f"HP:{self.hp}")
        self.full_hp = round(self.inf["hp"] + self.lvl() * 2)
        
        for atc in self.attack_obs:
            atc.set_ap(atc.max_ap)

    def dict(self):
        """RETURNS:
            A dict with all information about the Pokete"""
        return {"name": self.identifier, "xp": self.xp, "hp": self.hp,
                "ap": [atc.ap for atc in self.attack_obs],
                "effects": [eff.c_name for eff in self.effects],
                "attacks": self.attacks,
                "shiny": self.shiny,
                "nature": self.nature.dict(),
                "stats": self.poke_stats.dict()}

    def set_ap(self, aps):
        """Sets attack aps from a list
        ARGS:
            aps: List of attack ap"""
        for atc, ap in zip(self.attack_obs, aps):
            atc.set_ap(ap)

    def add_xp(self, _xp):
        """Adds xp to the current pokete
        ARGS:
            _xp: Amount of xp added to the current xp
        RETURNS:
            bool: whether or not the next level is reached"""
        old_lvl = self.lvl()
        self.xp += _xp
        self.poke_stats.add_xp(_xp)
        self.text_xp.rechar(f"XP:{self.xp - (self.lvl() ** 2 - 1)}/\
{((self.lvl() + 1) ** 2 - 1) - (self.lvl() ** 2 - 1)}")
        self.text_lvl.rechar(f"Lvl:{self.lvl()}")
        self.text_hp.rechar(f"HP:{self.oldhp}")
        logging.info("[Poke][%s] Gained %dxp (curr:%d)",
                     self.name, _xp, self.xp)
        if old_lvl < self.lvl():
            logging.info("[Poke][%s] Reached lvl. %d", self.name, self.lvl())
            return True
        return False

    def lvl(self):
        """RETURNS:
            Current level"""
        return int(math.sqrt(self.xp + 1))

    def attack(self, attack, enem, fightmap, providers):
        """Attack process
        ARGS:
            attack: Attack object
            enem: Enemy Poke
            fightmap: The map object where the fight is carried out on."""
        weather = providers[0].map.weather
        if attack.ap > 0:
            for eff in self.effects:
                eff.remove()
            for eff in self.effects:
                if eff.effect() == 1:
                    return
            if any(isinstance(i, effects.confusion) for i in self.effects) and random.randint(0, 1) == 0:
                self.enem = enem = self
            else:
                self.enem = enem
            w_eff = 1
            random_factor = random.choices([0, 0.8, 1, 1.2],
                                           weights=[attack.miss_chance
                                                    + self.miss_chance,
                                                    1, 1, 1], k=1)[0]
            if weather is not None:
                w_eff = weather.effect(attack.type)
                fightmap.outp.outp(weather.info)
                time.sleep(SPEED_OF_TIME * 1.5)
            enem.oldhp = enem.hp
            self.oldhp = self.hp
            eff = (2 if enem.type.name in attack.type.effective else 0.5
                   if enem.type.name in attack.type.ineffective else 1) * w_eff
            #We set the damage to increase as the level difference between the two Pokémon increases.
            n_hp = round(( self.atc
                          * (5 * attack.factor)
                          / (enem.defense if enem.defense >= 1 else 1))
                         * random_factor * eff)
            eff_text = {
                eff < 1: "\nThat was not effective! ",
                eff > 1: "\nThat was very effective! ",
                eff == 1 or n_hp == 0: "",
                random_factor == 0: f"{self.name} missed!"}[True]
            #Set the damage to be at least 1 if the attack is not missed
            if(random_factor != 0):
                enem.hp -= max(n_hp, 1)
            enem.hp = max(enem.hp, 0)
            time.sleep(SPEED_OF_TIME * 0.4)
            for i in attack.move:
                getattr(self.moves, i)()
            if attack.action is not None and random_factor != 0:
                getattr(AttackActions(), attack.action)(self, enem, providers)
            attack.set_ap(attack.ap - 1)
            fightmap.outp.outp(
                f'{self.ext_name} used {attack.name}! {eff_text}')
            if enem == self:
                time.sleep(SPEED_OF_TIME * 1)
                fightmap.outp.outp(f'{self.ext_name} hurt itself!')
            if random_factor != 0:
                attack.give_effect(enem)
            for obj in [enem, self] if enem != self else [enem]:
                obj.hp_bar.update(obj.oldhp)
            logging.info("[Poke][%s] Used %s: %s", self.name, attack.name,
                         str({"eff": eff, "n_hp": n_hp}))
            fightmap.show()

    def learn_attack(self, _map, overview):
        """Checks if a new attack can be learned and then teaches it the poke
        ARGS:
            _map: The map this happens on
            overview: Overview"""
        if self.lvl() % 5 == 0:
            LearnAttack(self, _map, overview)()

    def evolve(self, figure, _map):
        """Evolves the Pokete to its evolve_poke
        ARGS:
            figure: The figure object the poke belongs to
            _map: The map the evolving happens on"""
        if not self.player or self.evolve_poke == "" \
                or self.lvl() < self.evolve_lvl:
            return False
        evomap = EvoMap(_map.height, _map.width, _map)
        new = Poke(self.evolve_poke, self.xp, _attacks=self.attacks,
                   shiny=self.shiny)
        new.set_poke_stats(self.poke_stats)
        new.poke_stats.set_evolved_date(datetime.now())
        self.ico.remove()
        self.ico.add(evomap, round(evomap.width / 2 - 4),
                     round((evomap.height - 8) / 2))
        self.moves.shine()
        evomap.outp.outp("Look!")
        time.sleep(SPEED_OF_TIME * 0.5)
        evomap.outp.outp(f"{evomap.outp.text}\n{self.name} is evolving!")
        time.sleep(SPEED_OF_TIME * 1)
        for i in range(8):
            for j, k in zip([self.ico, new.ico], [new.ico, self.ico]):
                j.remove()
                k.add(evomap, round(evomap.width / 2 - 4),
                      round((evomap.height - 8) / 2))
                time.sleep(SPEED_OF_TIME * 0.7 - i * 0.09999)
                evomap.show()
                std_loop(box=evomap)
        self.ico.remove()
        new.ico.add(evomap, round(evomap.width / 2 - 4),
                    round((evomap.height - 8) / 2))
        evomap.show()
        time.sleep(SPEED_OF_TIME * 0.01)
        new.moves.shine()
        evomap.outp.outp(f"{self.name} evolved into {new.name}!")
        time.sleep(SPEED_OF_TIME * 5)
        for i in range(max(len(p_data.pokes[new.identifier]["attacks"])
                           - len(self.attack_obs), 0)):
            LearnAttack(new, evomap, evomap)()
        figure.pokes[figure.pokes.index(self)] = new
        if new.identifier not in figure.caught_pokes:
            figure.caught_pokes.append(new.identifier)
        achievements.achieve("first_evolve")
        logging.info("[Poke] %s evolved into %s", self.name, new.name)
        std_loop(box=evomap)
        del self
        return True

    @classmethod
    def from_dict(cls, _dict):
        """Assembles a Pokete from _dict"""
        return cls(_dict["name"], _dict["xp"], _dict["hp"], _dict["ap"],
                   _dict.get("attacks", None), _dict.get("effects", []),
                   shiny=_dict.get("shiny", False), nature=_dict.get("nature"),
                   stats=_dict.get("stats", None))

    @classmethod
    def wild(cls, poke, _xp):
        """Simulates learning attacks for wild poketes
        ARGS:
            poke: The poketes descriptor
            _xp: The poketes given xp"""
        obj = cls(poke, _xp)
        for i in range(obj.lvl()):
            if (
                i % 5 == 0
                and (new_attack := LearnAttack.get_attack(obj)) is not None
            ):
                obj.attacks.append(new_attack)

        while len(obj.attacks) > 4:
            obj.attacks.pop(random.randint(0, len(obj.attacks)-1))

        return cls(
            poke,
            _xp,
            _attacks=obj.attacks,
            player=False,
            shiny=(random.randint(0, 500) == 0)
        )


def upgrade_by_one_lvl(poke, figure, _map):
    """Upgrades a Pokete by exactly one level, this will only be used by treats
    ARGS:
        poke: The pokete, that will be upgraded
        figure: The figure object the Pokete belongs to
        _map: The map the upgrade happens on"""
    poke.add_xp((poke.lvl()+1)**2-1 - ((poke.lvl())**2-1))
    poke.set_vars()
    poke.learn_attack(_map, _map)
    poke.evolve(figure, _map)
