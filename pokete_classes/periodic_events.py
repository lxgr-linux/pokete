import random

from . import timer
from .color import Color
from .landscape import Meadow, HighGrass
from .npcs import NPC
from .game import PeriodicEvent
from .settings import settings
from .ui import notifier


def check_figure_redraw(obj):
    """Checks whether or not the figure has to be redrawn
    ARGS:
        obj: The obj that this is checked for"""
    if obj.x == HighGrass.figure.x and obj.y == HighGrass.figure.y:
        HighGrass.figure.redraw()


class MovingGrassEvent(PeriodicEvent):
    max_tick = 100

    def __init__(self, _map):
        self.all_grass_objs = []
        for meadow in Meadow.all_grass:
            if meadow.map == _map:
                self.all_grass_objs += meadow.obs

    def tick(self, tick: int):
        if tick % self.max_tick == 0 and settings("animations").val:
            for obj in self.all_grass_objs:
                if obj.char == Color.green + ";" + Color.reset:
                    if random.randint(0, 600) == 0:
                        obj.rechar(
                            Color.thicc + Color.green + ";" + Color.reset)
                        check_figure_redraw(obj)
                else:
                    obj.rechar(Color.green + ";" + Color.reset)
                    check_figure_redraw(obj)


class MovingWaterEvent(PeriodicEvent):
    def __init__(self, _map):
        self.all_water_objs = []
        for water in Meadow.all_water:
            if water.map == _map:
                self.all_water_objs += water.obs

    def tick(self, tick: int):
        if settings("animations").val:
            for obj in self.all_water_objs:
                if random.randint(0, 9) == 0:
                    if " " not in obj.char:
                        obj.rechar([i for i in
                                    [Color.lightblue + "~" + Color.reset,
                                     Color.blue + "~" + Color.reset]
                                    if i != obj.char][0])
                        check_figure_redraw(obj)


class TreatNPCEvent(PeriodicEvent):
    def tick(self, tick: int):
        if timer.time.normalized == 6 * 60:
            NPC.get("npc_28").unset_used()


class NotifierEvent(PeriodicEvent):
    def tick(self, tick: int):
        notifier.next()
