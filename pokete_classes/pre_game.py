import scrap_engine as se

from pokete_classes.context import Context
from pokete_classes.game import PeriodicEventManager
from pokete_classes.game_map import GameSubmap
from pokete_classes.multiplayer.menu import ModeChooser
from pokete_classes.tss import tss
from pokete_classes.ui import Overview


class PreGameMap(GameSubmap, Overview):
    """Map for background"""

    def __init__(self):
        super().__init__(
            se.Map(0, 0, " "),
            0, 0,
            tss.height - 1, tss.width,
            "PreGameMap"
        )

    def resize_view(self):
        """Manages recursive view resizing"""
        self.resize(tss.height - 1, tss.width, " ")
        self.remap()

    def __call__(self, figure):
        pevm = PeriodicEventManager([])
        ctx = Context(pevm, self, self, figure)
        ModeChooser()(ctx)
