"""Contains the map used for evolving"""

import scrap_engine as se
import pokete_classes.game_map as gm
from .classes import OutP
from .tss import tss


class EvoMap(gm.GameMap):
    """Map for evolutions to take place on
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height, width, overview):
        super().__init__(height, width, name="evomap")
        self.overview = overview
        self.frame_small = se.Frame(height=4, width=width, state="float")
        self.outp = OutP("", state="float")
        # adding
        self.frame_small.add(self, 0, self.height - 5)
        self.outp.add(self, 1, self.height - 4)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.frame_small.remove()
        self.outp.remove()
        self.resize(tss.height - 1, tss.width)
        self.overview.resize_view()
        self.frame_small.resize(self.height, self.width)
        self.frame_small.add(self, 0, self.height - 5)
        self.outp.add(self, 1, self.height - 4)
