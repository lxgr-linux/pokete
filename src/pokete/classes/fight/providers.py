"""Providers are any instance that is able to paticipate in a fight"""

import random
import time
from abc import ABC, abstractmethod
from typing import Protocol, override

from pokete.base.context import Context
from pokete.base.input_loops import ask_bool
from pokete.classes.achievements import achievements
from pokete.classes.poke.poke import Poke

from .fight_decision import FightDecision


class IOutp(Protocol):
    def outp(self, text: str) -> None: ...


class IFightMap(Protocol):
    """Interface representing FightMap, avoiding a circular import with
    pokete.classes.fight.fightmap.fightmap, which itself imports Provider"""

    outp: IOutp

    def get_figure_attack(
        self, ctx: Context, player: "Provider", enem: "Provider"
    ) -> FightDecision: ...

    def choose_poke(
        self, ctx: Context, player: "Provider", allow_exit: bool = True
    ) -> None: ...


class Provider(ABC):
    """Provider can hold and manage Poketes
    ARGS:
        pokes: The Poketes the Provider holds"""

    def __init__(
        self,
        pokes: list[Poke],
        escapable: bool,
        xp_multiplier: int,
        inv: dict[str, int] | None = None,
    ) -> None:
        self.pokes = pokes
        self.escapable = escapable
        self.xp_multiplier = xp_multiplier
        self.play_index = 0
        self.__inv: dict[str, int] = {} if inv is None else inv

    def get_inv(self) -> dict[str, int]:
        return self.__inv

    def heal(self) -> None:
        """Heals all poketes"""
        if self.pokes:
            for poke in self.pokes:
                poke.hp = poke.full_hp
                poke.effects = []
                poke.miss_chance = poke.full_miss_chance
                poke.set_vars()
            if poke.player:
                self.balls_label_rechar()

    @property
    def curr(self) -> Poke:
        """Returns the currently used Pokete"""
        return self.pokes[self.play_index]

    def index_conf(self) -> None:
        """Sets index correctly"""
        self.play_index = next(i for i, poke in enumerate(self.pokes) if poke.hp > 0)

    def remove_item(self, item: str, amount: int = 1) -> None:
        """Removes and item from the providers inventory
        Accept for the player implementation that shouldnt do anything"""
        return

    @abstractmethod
    def get_decision(
        self, ctx: Context, fightmap: IFightMap, enem: "Provider"
    ) -> FightDecision:
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            enem: The enemy Provider"""

    @abstractmethod
    def greet(self, fightmap: IFightMap) -> None:
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""

    @abstractmethod
    def handle_defeat(
        self, ctx: Context, fightmap: IFightMap, winner: "Provider"
    ) -> None:
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider
        RETURNS:
            bool: whether or not a Pokete was choosen"""

    def handle_win(self, ctx: Context, loser: "Provider") -> None:
        pass


class NatureProvider(Provider):
    """The Natures Provider
    ARGS:
        poke: One Pokete"""

    def __init__(self, poke: Poke) -> None:
        super().__init__([poke], escapable=True, xp_multiplier=1)

    @override
    def get_decision(
        self, ctx: Context, fightmap: IFightMap, enem: "Provider"
    ) -> FightDecision:
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            enem: The enemy Provider"""
        return FightDecision.attack(
            random.choices(
                self.curr.attack_obs,
                weights=[i.ap for i in self.curr.attack_obs],
            )[0]
        )

    @override
    def greet(self, fightmap: IFightMap) -> None:
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        fightmap.outp.outp(f"A wild {self.curr.name} appeared!")

    @override
    def handle_defeat(
        self, ctx: Context, fightmap: IFightMap, winner: "Provider"
    ) -> None:
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

    @override
    def greet(self, fightmap: IFightMap) -> None:
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        return

    @override
    def get_decision(
        self, ctx: Context, fightmap: IFightMap, enem: "Provider"
    ) -> FightDecision:
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            enem: The enemy Provider"""
        return fightmap.get_figure_attack(ctx, self, enem)

    @override
    def handle_defeat(
        self, ctx: Context, fightmap: IFightMap, winner: "Provider"
    ) -> bool:
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider
        RETURNS:
            bool: whether or not a Pokete was choosen"""
        if winner.escapable:
            if ask_bool(
                ctx,
                "Do you want to choose another Pokete?",
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

    @override
    def handle_win(self, ctx: Context, loser: "Provider") -> None:
        if hasattr(loser, "trainer"):
            achievements.achieve("first_duel")
        self.balls_label_rechar()
