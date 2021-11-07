"""Type and PokeType class"""
from .color import Color


class Types:
    """Class to organize PokeTypes"""

    def __init__(self, types, sub_types):
        for i in types:
            setattr(self, i, PokeType(i, **types[i]))
        for i in sub_types:
            setattr(self, i, PokeSubType(i))


class PokeType():
    """Type for Poketes and attacks"""

    def __init__(self, name, effective, ineffective, color):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color is None else str.join("", [getattr(Color, i) for i in color])


class PokeSubType(PokeType):
    """Subtype class to better organize generic attacks"""

    def __init__(self, name):
        super().__init__(name, [], [], None)
