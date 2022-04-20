import random
import logging
from pokete_general_use_fns import liner
from .ui_elements import InfoBox
from .loops import easy_exit_loop

class Nature:
    def __init__(self, name, atc=1, _def=1, init=1):
        self.name = name
        self.atc = atc
        self.defense = _def
        self.initiative = init

class PokeNature:
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
        }
    }.items()}

    def __init__(self, nature, grade):
        self.nature = nature
        self.grade = grade
        self.info = NatureInfo(self)

    def get_value(self, name):
        return getattr(self.nature, name)

    def dict(self):
        return {"nature": self.nature.name, "grade": self.grade}

    @classmethod
    def from_dict(cls, _dict):
        nature = cls.natures.get(_dict.get("nature"), cls.natures["relaxed"])
        grade = _dict.get("grade", 1)
        return cls(nature, grade)

    @classmethod
    def random(cls):
        nature = random.choice([i for _, i in cls.natures.items()])
        grade = random.randint(1, 2)
        return cls(nature, grade)


class NatureInfo(InfoBox):
    def __init__(self, p_n):
        atc = self.get_amount(p_n.nature.atc)
        defense = self.get_amount(p_n.nature.defense)
        init = self.get_amount(p_n.nature.initiative)
        text = f"""This pokete has a {"very " if p_n == 2 else ""}{p_n.nature.name} nature,
that  means it has {atc} attack, {defense} defense and {init} initiative then normal Poketes of its' kind."""
        super().__init__(liner(text, 40, pre=""), "Nature")

    @staticmethod
    def get_amount(val):
        if val == 1:
            return "the same"
        elif val < 1:
            return "less"
        return "more"

    def __call__(self, _map):
        self.map = _map
        with self:
            easy_exit_loop()
