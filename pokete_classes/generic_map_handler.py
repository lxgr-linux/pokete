"""Contains the generic map handler that creates a full blown map object
from a string
This is not in use yet!"""

import scrap_engine as se
from .classes import PlayMap
from .landscape import Meadow


class GenericMapHandler:
    """Generates a full blown map object from a string
    ARGS:
        name: The maps name
        pretty_name: The maps pretty name
        raw_map: The string the maps ist created from"""

    def __init__(self, name: str, pretty_name: str, raw_map: str):
        self.string_map = raw_map.split("\n")
        self.map = PlayMap(*self.get_dimensions(), name=name,
                           pretty_name=pretty_name)
        self.add_grass()
        self.add_solid()

    def get_dimensions(self):
        """Return the maps dimensions"""

        height = len(self.string_map)
        width = len(self.string_map[0])
        return height, width

    def add_grass(self):
        """Adds a Meadow to the map"""

        self.grass_raw = ""
        for l in self.string_map:
            for i in l:
                if i == ";":
                    self.grass_raw += i
                else:
                    self.grass_raw += " "
            self.grass_raw += "\n"
        self.meadow = Meadow(self.grass_raw, {})
        self.meadow.add(self.map, 0, 0)

    def add_solid(self):
        """Adds all solid objects to the map"""

        self.solid_raw = ""
        for l in self.string_map:
            for i in l:
                if i not in [";", "~", "."]:
                    self.solid_raw += i
                else:
                    self.solid_raw += " "
            self.solid_raw += "\n"
        self.solid = se.Text(self.solid_raw, ignore=" ")
        self.solid.add(self.map, 0, 0)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
