import random
import logging

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
