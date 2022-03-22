import scrap_engine as se
from .classes import PlayMap

class GenericTypeHandler:
    def __init__(self, name: string, pretty_name: string, raw_map: string):
        self.string_map = raw_map.split("\n")
        self.map = PlayMap(*self.get_dimentions, name=name, pretty_name=pretty_name)

    def get_dimentions(self):
        height = len(self.string_map)
        width = len(string_map[0])
        return height, width

    def get_grass(self):
        self.grass_raw = ""
        for l in self.string_map:
            for i in l:
                if i == ";":
                    self.grass_raw += i
                else:
                    self.grass_raw += " "
            
