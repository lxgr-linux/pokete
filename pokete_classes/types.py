"""Type and PokeType class"""

import pokete_data as p_data
from .color import Color


class Types:
    """Class to organize PokeTypes
    ARGS:
        p_data: p_data module"""

    def __init__(self):
        for i, typ in p_data.types.items():
            setattr(self, i, PokeType(i, **typ))
        for i in p_data.sub_types:
            setattr(self, i, PokeSubType(i))


class PokeType():
    """Type for Poketes and attacks
    ARGS:
        name: The types name
        effective: List of type names the type is effective against
        ineffective: List of type names the type is ineffectice against
        color: Color string"""

    def __init__(self, name, effective, ineffective, color):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color is None else "".join(getattr(Color, i)
                                                      for i in color)


class PokeSubType(PokeType):
    """Subtype class to better organize generic attacks
    ARGS:
        name: The types name"""

    def __init__(self, name):
        super().__init__(name, [], [], None)


types = Types()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
