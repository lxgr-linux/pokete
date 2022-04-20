"""Contains everything related to the nature of Poketes, which influences some
of their stats"""

import random
import logging
from pokete_general_use_fns import liner
from .ui_elements import InfoBox
from .loops import easy_exit_loop

class Nature:
    """The Nature class itself holds basic information about the Nature,
    that means:
    ARGS:
        name: The nature name
        atc: The attack change
        _def: The defense change
        init: The initiative change"""

    def __init__(self, name, atc=1, _def=1, init=1):
        self.name = name
        self.atc = atc
        self.defense = _def
        self.initiative = init


class PokeNature:
    """Holds specific information about a Pokete
    ARGS:
        nature: The Nature of the Pokete
        grade: The Natures grade, 1 or 2"""

    natures = {name: Nature(name, **_dict) for name, _dict in {
        "brave": {
            "atc": 1.1,
            "_def": 0.9
        },
        "relaxed": {
            "atc": 0.9,
            "_def": 1.1,
        },
        "hasty": {
            "_def": 0.9,
            "init": 1.1
        },
        "normal": {}
    }.items()}

    def __init__(self, nature, grade):
        self.nature = nature
        self.grade = grade
        self.info = NatureInfo(self)

    def get_value(self, name):
        """Gets one attribute value by
        ARGS:
            name"""
        return getattr(self.nature, name)

    def dict(self):
        """RETURNS:
            A dict containing inforamtion to reconstruct the object"""
        return {"nature": self.nature.name, "grade": self.grade}

    @classmethod
    def from_dict(cls, _dict):
        """Constructs an object from a
        ARGS:
            _dict: dict"""
        nature = cls.natures.get(_dict.get("nature"), cls.natures["relaxed"])
        grade = _dict.get("grade", 1)
        return cls(nature, grade)

    @classmethod
    def random(cls):
        """Creates an instance with random values"""
        nature = random.choice([i for _, i in cls.natures.items()])
        grade = random.randint(1, 2)
        return cls(nature, grade)


class NatureInfo(InfoBox):
    """Box to show information in Detail
    ARGS:
        p_n: PoketeNature object"""

    def __init__(self, p_n):
        atc = self.get_amount(p_n.nature.atc)
        defense = self.get_amount(p_n.nature.defense)
        init = self.get_amount(p_n.nature.initiative)
        text = f"""This pokete has a {"very " if p_n == 2 else ""}{p_n.nature.name} nature,
that  means it has {atc} attack, {defense} defense and {init} initiative then normal Poketes of its' kind."""
        super().__init__(liner(text, 40, pre=""), "Nature")

    @staticmethod
    def get_amount(val):
        """Gets the amount denominator for a value"""
        if val == 1:
            return "the same"
        elif val < 1:
            return "less"
        return "more"

    def __call__(self, _map):
        """Shows the box
        ARGS:
            _map: Map to show on"""
        self.map = _map
        with self:
            easy_exit_loop()
