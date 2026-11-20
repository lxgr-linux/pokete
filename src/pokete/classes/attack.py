"""Contains the Attack class"""

import scrap_engine as se

from pokete.base.color import Color
from pokete.data.attacks import attacks

from .types import types


class Attack:
    """Attack that can be used by a Pokete
    ARGS:
        index: The attacks basic name
        pref: Prefix used for the attack label"""

    def __init__(self, index: str, pref: str = "", ap: int | None = None) -> None:
        inf = attacks[index]
        # Attributes
        self.index = index
        self.name = inf["name"]
        self.factor = inf["factor"]
        self.action = inf["action"]
        self.world_action = inf["world_action"]
        self.move = inf["move"]
        self.miss_chance = inf["miss_chance"]
        self.min_lvl = inf["min_lvl"]
        self.desc = inf["desc"]
        self.effect = inf["effect"]
        self.is_generic = inf["is_generic"]
        self.ap = inf["ap"]
        self.type = types[inf["types"][0]]
        self.max_ap = self.ap
        # labels
        self.label_name = se.Text(self.name, esccode=Color.underlined, state="float")
        self.label_ap = se.Text(f"AP:{self.ap}/{self.max_ap}", state="float")
        self.label_factor = se.Text(f"Attack:{self.factor}", state="float")
        self.label_type = se.Text("Type:", state="float") + se.Text(
            self.type.name.capitalize(), esccode=self.type.color, state="float"
        )
        self.pref = pref
        self.label = self.make_label()
        if ap is not None:
            self.set_ap(ap)

    def make_label(self) -> se.Text:
        """Creates label
        RETURNS:
            New label"""
        return (
            se.Text(f"{self.pref}: ", state="float")
            + se.Text(self.name, esccode=self.type.color)
            + se.Text(f"-{self.ap}")
        )

    def set_ap(self, _ap: int | str) -> None:
        """Sets attack points
        ARGS:
            _ap: Attack points"""
        if _ap != "SKIP":
            self.ap = min(_ap, self.max_ap)
            self.label.rechar("")
            self.label += self.make_label()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
