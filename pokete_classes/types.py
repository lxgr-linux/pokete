"""Type and PokeType class"""
from .color import Color


class Types:
    """Class to organize PokeTypes"""

    def __init__(self, p_data):
        for i in p_data.types:
            setattr(self, i, PokeType(i, **p_data.types[i]))
        for i in p_data.sub_types:
            setattr(self, i, PokeSubType(i))


class PokeType():
    """Type for Poketes and attacks"""

    def __init__(self, name, effective, ineffective, color):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color is None else "".join(getattr(Color, i)
                                                      for i in color)


class PokeSubType(PokeType):
    """Subtype class to better organize generic attacks"""

    def __init__(self, name):
        super().__init__(name, [], [], None)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
