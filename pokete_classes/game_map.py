"""Map wrapper for compatibility purposes"""

import scrap_engine as se
class GameMap(se.Map):
    """Wraps the se.Map class and adds a name attribute
    ARGS:
        height: The map's height
        width: The map's width
        background: The map's background
        name: The map's name"""

    def __init__(self, height, width, background=" ", name=""):
        super().__init__(height, width, background)
        self.name = name


class GameSubmap(se.Submap):
    """Wraps the se.Submap class and adds a name attribute
    ARGS:
        bmap: The maps parrent map
        x: The maps x coordinate on the parent map
        y: The maps y coordinate on the parent map
        height: The maps height
        width: The maps width
        name: The maps name"""

    def __init__(self, bmap, x, y, height, width, name=""):
        super().__init__(bmap, x, y, height, width)
        self.name = name
