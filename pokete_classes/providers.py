"""Providers are any instance that is able to paticipate in a fight"""

import random
import time
from abc import ABC, abstractmethod
from pokete_classes import movemap as mvp
from .input import ask_bool

class Provider(ABC):
    """Provider can hold and manage Poketes
    ARGS:
        pokes: The Poketes the Provider holds"""

    def __init__(self, pokes, escapable, xp_multiplier):
        self.pokes = pokes
        self.escapable = escapable
        self.xp_multiplier = xp_multiplier
        self.play_index = 0

    def heal(self):
        """Heals all poketes"""
        if self.pokes:
            for poke in self.pokes:
                poke.hp = poke.full_hp
                poke.effects = []
                poke.miss_chance = poke.full_miss_chance
                poke.text_hp.rechar(f"HP:{poke.hp}")
                poke.set_vars()
                poke.hp_bar.make(poke.hp)
            if poke.player:
                mvp.movemap.balls_label_rechar(self.pokes)

    @property
    def curr(self):
        """Returns the currently used Pokete"""
        return self.pokes[self.play_index]

    def index_conf(self):
        """Sets index correctly"""
        self.play_index = next(
            i for i, poke in enumerate(self.pokes) if poke.hp > 0
        )

    @abstractmethod
    def get_attack(self, fightmap, enem):
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            anem: The enemy Provider"""

    @abstractmethod
    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""

    @abstractmethod
    def handle_defeat(self, fightmap, winner):
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider
        RETURNS:
            bool: whether or not a Pokete was choosen"""

class NatureProvider(Provider):
    """The Natures Provider
    ARGS:
        poke: One Pokete"""
    def __init__(self, poke):
        super().__init__([poke], escapable=True, xp_multiplier=1)

    def get_attack(self, fightmap, enem):
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            anem: The enemy Provider"""
        return random.choices(
            self.curr.attack_obs,
            weights=[
                i.ap for i in self.curr.attack_obs
            ]
        )[0]

    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        fightmap.outp.outp(f"A wild {self.curr.name} appeared!")

    def handle_defeat(self, fightmap, winner):
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider
        RETURNS:
            bool: whether or not a Pokete was choosen"""
        return False


class ProtoFigure(Provider):
    """Class Figure inherits from to avoid injecting the Figure class
    into fight"""

    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        return

    def get_attack(self, fightmap, enem):
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            anem: The enemy Provider"""
        return fightmap.get_figure_attack(self, enem)

    def handle_defeat(self, fightmap, winner):
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider
        RETURNS:
            bool: whether or not a Pokete was choosen"""
        if winner.escapable:
            if ask_bool(fightmap, "Do you want to choose another Pokete?"):
                success = fightmap.choose_poke(self)
                if not success:
                    return False
            else:
                return False
        else:
            time.sleep(2)
            fightmap.choose_poke(self, False)
        return True
