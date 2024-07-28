import scrap_engine as se

from pokete_classes import ob_maps as obmp
from pokete_classes.context import Context
from pokete_classes.game import PeriodicEventManager, PeriodicEvent
from pokete_classes.game_map import GameSubmap
from pokete_classes.multiplayer.menu import ModeChooser
from pokete_classes.tss import tss
from pokete_classes.ui import Overview


class BGMoverEvent(PeriodicEvent):
    def __init__(self, _map: se.Submap):
        self.map = _map
        self.up = True
        self.right = True

    def tick(self, tick: int):
        if tick % 2 == 0:
            if self.map.x + self.map.width >= self.map.bmap.width:
                self.right = False
            elif self.map.x == 0:
                self.right = True
            if self.map.y + self.map.height >= self.map.bmap.height:
                self.up = False
            elif self.map.y == 0:
                self.up = True
            self.map.set(
                self.map.x + (1 if self.right else -1),
                self.map.y + (1 if self.up else -1)
            )


class PreGameMap(GameSubmap, Overview):
    """Map for background"""

    def __init__(self):
        super().__init__(
            obmp.ob_maps["playmap_39"],
            0, 0,
            tss.height - 1, tss.width,
            "PreGameMap"
        )

    def resize_view(self):
        """Manages recursive view resizing"""
        self.resize(tss.height - 1, tss.width, " ")
        self.remap()

    def __call__(self, figure):
        pevm = PeriodicEventManager([BGMoverEvent(self)])
        ctx = Context(pevm, self, self, figure)
        ModeChooser()(ctx)
