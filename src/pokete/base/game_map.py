"""Map wrapper for compatibility purposes"""

from abc import ABC

import scrap_engine as se


class OutP(se.Text):
    """Output label to better organize output"""

    def outp(self, text: str):
        """Rechar and show wrapper
        ARGS:
            text: String that's printed out"""
        self.rechar(text)
        if self.map:
            self.map.full_show()

    def append(self, *args: se.Text):
        """Appends another se.Text to the outp
        ARGS:
            args: se.Texts that will be appended"""
        for i in args:
            self += i
        if self.map:
            self.map.full_show()


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

    def __init__(
        self,
        height: int,
        width: int,
        background: str = " ",
        name: str = "",
    ):
        super().__init__(height, width, background)
        self.name = name


class GameMapWithOutp(GameMap):
    def __init__(
        self,
        height: int,
        width: int,
        background: str = " ",
        name: str = "",
    ):
        super().__init__(height, width, background, name)
        self.outp = OutP("", state="float")


class GameSubmap(se.Submap, CompatMap):
    """Wraps the se.Submap class and adds a name attribute
    ARGS:
        bmap: The map's parent map
        x: The map's x coordinate on the parent map
        y: The map's y coordinate on the parent map
        height: The map's height
        width: The map's width
        name: The map's name"""

    def __init__(
        self,
        bmap: se.Map,
        x: int,
        y: int,
        height: int,
        width: int,
        name: str = "",
    ):
        super().__init__(bmap, x, y, height, width)
        self.name = name
