import scrap_engine as se
from .classes import OutP

class EvoMap(se.Map):
    """Map for evolutions to take place on
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height, width):
        super().__init__(height, width, " ")
        self.name = "evomap"
        self.frame_small = se.Frame(height=4, width=width, state="float")
        self.outp = OutP("", state="float")
        # adding
        self.frame_small.add(self, 0, self.height - 5)
        self.outp.add(self, 1, self.height - 4)
