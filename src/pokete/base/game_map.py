"""Map wrapper for compatibility purposes"""
from abc import ABC

import scrap_engine as se


class CompatMap(ABC):
    height: int
    width: int

    def show(self):
        pass

    def full_show(self):
        self.show()


class GameMap(se.Map, CompatMap):
    """Wraps the se.Map class and adds a name attribute
    ARGS:
        height: The map's height
        width: The map's width
        background: The map's background
        name: The map's name"""

    def __init__(self, height, width, background=" ", name=""):
        super().__init__(height, width, background)
        self.name = name


class GameSubmap(se.Submap, CompatMap):
    """Wraps the se.Submap class and adds a name attribute
    ARGS:
        bmap: The map's parent map
        x: The map's x coordinate on the parent map
        y: The map's y coordinate on the parent map
        height: The map's height
        width: The map's width
        name: The map's name"""

    def __init__(self, bmap, x, y, height, width, name=""):
        super().__init__(bmap, x, y, height, width)
        self.name = name
