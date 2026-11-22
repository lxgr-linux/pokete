"""Contains Weather class"""

from pokete.classes.types import PokeType
from pokete.data import weathers


class Weather:
    """Behaviour for a certain weather
    ARGS:
        index: The weathers name"""

    def __init__(self, index: str) -> None:
        self.info = weathers[index]["info"]
        self.effected = weathers[index]["effected"]

    def effect(self, typ: PokeType) -> None:
        """Gives an additional attackfactor
        ARGS:
            typ: The attacks type
        RETURNS:
            attackfactor"""
        return self.effected.get(typ.name, 1)
