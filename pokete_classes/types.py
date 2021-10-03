"""Type and PokeType class"""
from pokete_classes.color import Color


class Types:
    """Class to organize PokeTypes"""

    def __init__(self, types):
        for i in types:
            setattr(self, i, PokeType(i, **types[i]))


class PokeType():
    """Type for Poketes and attacks"""

    def __init__(self, name, effective, ineffective, color):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color is None else str.join("", [getattr(Color, i) for i in color])
