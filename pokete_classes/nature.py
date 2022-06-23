"""Contains everything related to the nature of Poketes, which influences some
of their stats"""

import random
import scrap_engine as se
import pokete_data as p_data
from pokete_general_use_fns import liner
from .hotkeys import Action
from .ui_elements import LabelBox
from .color import Color
from .loops import easy_exit_loop


class Nature:
    """The Nature class itself holds basic information about the Nature,
    that means:
    ARGS:
        name: The nature name
        atc: The attack change
        _def: The defense change
        init: The initiative change"""

    def __init__(self, name, esc=None, atc=1, _def=1, init=1):
        self.name = name
        if esc is not None:
            self.esccode = getattr(Color, esc)
        else:
            self.esccode = ""
        self.atc = atc
        self.defense = _def
        self.initiative = init


class PokeNature:
    """Holds specific information about a Pokete
    ARGS:
        nature: The Nature of the Pokete
        grade: The Nature's grade, 1 or 2"""

    natures = {name: Nature(name, **_dict) for name, _dict in p_data.natures.items()}

    def __init__(self, nature, grade):
        self.nature = nature
        self.grade = grade
        self.info = NatureInfo(self)

    def get_value(self, name):
        """Gets one attribute value by its name
        ARGS:
            name: The name of the attribute"""
        return getattr(self.nature, name)**self.grade

    def dict(self):
        """RETURNS:
            A dict containing information to reconstruct the object"""
        return {"nature": self.nature.name, "grade": self.grade}

    @classmethod
    def from_dict(cls, _dict):
        """Constructs an object from a
        ARGS:
            _dict: dict"""
        nature = cls.natures.get(_dict.get("nature"), cls.natures["normal"])
        grade = _dict.get("grade", 1)
        return cls(nature, grade)

    @classmethod
    def random(cls):
        """Creates an instance with random values"""
        nature = random.choice([i for _, i in cls.natures.items()])
        grade = random.randint(1, 2)
        return cls(nature, grade)

    @classmethod
    def dummy(cls):
        """Returns a dummy nature"""
        nature = cls.natures["normal"]
        grade = 1
        return cls(nature, grade)


class NatureInfo(LabelBox):
    """Box to show information in Detail
    ARGS:
        p_n: PoketeNature object"""

    def __init__(self, p_n):
        atc = self.get_amount(p_n.nature.atc)
        defense = self.get_amount(p_n.nature.defense)
        init = self.get_amount(p_n.nature.initiative)
        text = se.Text(f"Nature: {'very ' if p_n.grade == 2 else ''}") \
            + se.Text(p_n.nature.name, esccode=Color.thicc
                      + p_n.nature.esccode) \
            + se.Text(liner(f"\n\n That means it has {atc} attack, \
{defense} defense and {init} initiative points compared to normal Poketes \
of its kind.", 40, pre=""))
        super().__init__(
            text, name="Nature", info=f"{Action.CANCEL.mapping}:close"
        )

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
        with self.center_add(_map):
            easy_exit_loop(False)
