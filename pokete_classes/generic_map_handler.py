import scrap_engine as se
from .classes import PlayMap
from .landscape import Meadow

class GenericMapHandler:
    def __init__(self, name: str, pretty_name: str, raw_map: str):
        self.string_map = raw_map.split("\n")
        self.map = PlayMap(*self.get_dimentions, name=name, pretty_name=pretty_name)
        self.add_grass()
        self.add_solid()

    def get_dimentions(self):
        height = len(self.string_map)
        width = len(string_map[0])
        return height, width

    def add_grass(self):
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
        self.solid_raw = ""
        for l in self.string_map:
            for i in l:
                if i not in [";", "~", "."]:
                    self.solid_raw += i
                else:
                    self.solid_raw += " "
            self.grass_raw += "\n"
        self.solid = se.Text(self.solid_raw, ignore=" ")
        self.solid.add(self.map, 0, 0)
