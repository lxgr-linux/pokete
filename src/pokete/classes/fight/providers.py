"""Providers are any instance that is able to paticipate in a fight"""

import random
import time
from abc import ABC, abstractmethod

from pokete.base.context import Context
from pokete.base.input_loops import ask_bool
from ..achievements import achievements
from .fight_decision import FightDecision
from ..poke import Poke

class Provider(ABC):
    """Provider can hold and manage Poketes
    ARGS:
        pokes: The Poketes the Provider holds"""

    def __init__(self,
        pokes: list[Poke], escapable:bool, xp_multiplier:int,
        inv: dict[str, int] | None = None
    ):
        self.pokes = pokes
        self.escapable = escapable
        self.xp_multiplier = xp_multiplier
        self.play_index = 0
        self.inv: dict[str, int] = {} if inv is None else inv

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
                self.balls_label_rechar()

    @property
    def curr(self) -> Poke:
        """Returns the currently used Pokete"""
        return self.pokes[self.play_index]

    def index_conf(self):
        """Sets index correctly"""
        self.play_index = next(
            i for i, poke in enumerate(self.pokes) if poke.hp > 0
        )

    def remove_item(self, item:str, amount:int=1):
        """Removes and item from the providers inventory
            Accept for the player implementation that shouldnt do anything"""
        return

    @abstractmethod
    def get_decision(
        self, ctx: Context, fightmap: "FightMap",
        enem
    ) -> FightDecision:
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            enem: The enemy Provider"""

    @abstractmethod
    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""

    @abstractmethod
    def handle_defeat(self, ctx: Context, fightmap, winner):
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider
        RETURNS:
            bool: whether or not a Pokete was choosen"""

    def handle_win(self, ctx: Context, loser):
        pass


class NatureProvider(Provider):
    """The Natures Provider
    ARGS:
        poke: One Pokete"""

    def __init__(self, poke):
        super().__init__([poke], escapable=True, xp_multiplier=1)

    def get_decision(self, ctx: Context, fightmap, enem) -> FightDecision:
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            enem: The enemy Provider"""
        return FightDecision.attack(random.choices(
            self.curr.attack_obs,
            weights=[
                i.ap for i in self.curr.attack_obs
            ]
        )[0])

    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        fightmap.outp.outp(f"A wild {self.curr.name} appeared!")

    def handle_defeat(self, ctx: Context, fightmap, winner):
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

    def get_decision(self, ctx: Context, fightmap, enem) -> FightDecision:
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            enem: The enemy Provider"""
        return fightmap.get_figure_attack(ctx, self, enem)

    def handle_defeat(self, ctx: Context, fightmap, winner):
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider
        RETURNS:
            bool: whether or not a Pokete was choosen"""
        if winner.escapable:
            if ask_bool(
                ctx, "Do you want to choose another Pokete?",
            ):
                success = fightmap.choose_poke(ctx, self)
                if not success:
                    return False
                self.curr.poke_stats.add_battle(False)
            else:
                return False
        else:
            time.sleep(2)
            self.curr.poke_stats.add_battle(False)
            fightmap.choose_poke(ctx, self, False)
        return True

    def handle_win(self, ctx:Context, loser):
        if hasattr(loser, "trainer"):
            achievements.achieve("first_duel")
        self.balls_label_rechar()
