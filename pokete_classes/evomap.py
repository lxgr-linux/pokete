"""Contains the map used for evolving"""

import scrap_engine as se
import pokete_classes.game_map as gm
from .classes import OutP


class EvoMap(gm.GameMap):
    """Map for evolutions to take place on
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height, width):
        super().__init__(height, width, name="evomap")
        self.frame_small = se.Frame(height=4, width=width, state="float")
        self.outp = OutP("", state="float")
        # adding
        self.frame_small.add(self, 0, self.height - 5)
        self.outp.add(self, 1, self.height - 4)
