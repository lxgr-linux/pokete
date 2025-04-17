"""Contains the map used for evolving"""
import logging
import time
import scrap_engine as se

from pokete.base.exception_propagation import exception_propagating_periodic_event
from pokete.release import SPEED_OF_TIME
import pokete.base.game_map as gm
from pokete.base import loops
from pokete.base.context import Context
from pokete.base.periodic_event_manager import PeriodicEventManager
from pokete.base.tss import tss
from pokete.base.ui import Overview
from ..achievements import achievements
from ..asset_service.service import asset_service
from ..classes import OutP
from ..learnattack import LearnAttack
from .poke import Poke


class EvoMap(gm.GameMap, Overview):
    """Map for evolutions to take place on
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height, width):
        super().__init__(height, width, name="evomap")
        self.frame_small = se.Frame(height=4, width=width, state="float")
        self.outp = OutP("", state="float")
        self.overview = None
        # adding
        self.frame_small.add(self, 0, self.height - 5)
        self.outp.add(self, 1, self.height - 4)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.frame_small.remove()
        self.outp.remove()
        self.resize(tss.height - 1, tss.width, " ")
        self.overview.resize_view()
        self.frame_small.resize(4, self.width)
        self.frame_small.add(self, 0, self.height - 5)
        self.outp.add(self, 1, self.height - 4)

    def __call__(self, ctx: Context, poke: Poke) -> bool:
        if not poke.player or poke.evolve_poke == "" \
            or poke.lvl() < poke.evolve_lvl:
            return False
        self.overview = ctx.overview
        ctx = Context(PeriodicEventManager([exception_propagating_periodic_event]), self, self, ctx.figure)
        new = poke.get_evolve_poke()
        poke.ico.remove()
        poke.ico.add(self, round(self.width / 2 - 4),
                     round((self.height - 8) / 2))
        poke.moves.shine()
        self.outp.outp("Look!")
        time.sleep(SPEED_OF_TIME * 0.5)
        self.outp.outp(f"{self.outp.text}\n{poke.name} is evolving!")
        time.sleep(SPEED_OF_TIME * 1)
        for i in range(8):
            for j, k in zip([poke.ico, new.ico], [new.ico, poke.ico]):
                j.remove()
                k.add(self, round(self.width / 2 - 4),
                      round((self.height - 8) / 2))
                time.sleep(SPEED_OF_TIME * 0.7 - i * 0.09999)
                loops.std(ctx)
        poke.ico.remove()
        new.ico.add(self, round(self.width / 2 - 4),
                    round((self.height - 8) / 2))
        self.show()
        time.sleep(SPEED_OF_TIME * 0.01)
        new.moves.shine()
        self.outp.outp(f"{self.name} evolved into {new.name}!")
        time.sleep(SPEED_OF_TIME * 5)
        for i in range(max(len(
            asset_service.get_base_assets().pokes[new.identifier].attacks)
                           - len(poke.attack_obs), 0)):
            LearnAttack(new)(ctx)
        ctx.figure.pokes[ctx.figure.pokes.index(self)] = new
        if new.identifier not in ctx.figure.caught_pokes:
            ctx.figure.caught_pokes.append(new.identifier)
        achievements.achieve("first_evolve")
        logging.info("[Poke] %s evolved into %s", self.name, new.name)
        loops.std(ctx)
        del self
        return True
