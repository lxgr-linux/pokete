"""Contains the Attack class"""

import time
import scrap_engine as se
from .effects import effects
from .types import Types
from .color import Color


class Attack:
    """Attack that can be used by a Pokete
    ARGS:
        index: The attacks basic name
        p_data: p_data module"""

    def __init__(self, index, p_data):
        inf = p_data.attacks[index]
        # Attributes
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
        self.type = getattr(Types(p_data), inf["types"][0])
        self.max_ap = self.ap
        # labels
        self.label_name = se.Text(self.name, esccode=Color.underlined,
                                  state="float")
        self.label_ap = se.Text(f"AP:{self.ap}/{self.max_ap}", state="float")
        self.label_factor = se.Text(f"Attack:{self.factor}", state="float")
        self.label_desc = se.Text(self.desc[:10], state="float")
        self.label_type = se.Text("Type:", state="float") \
                        + se.Text(self.type.name.capitalize(),
                                  esccode=self.type.color, state="float")

    def give_effect(self, enem):
        """Gives the associated effect to a Pokete
        ARGS:
            enem: Enemy object"""
        if self.effect is not None:
            time.sleep(1.5)
            getattr(effects, self.effect)().add(enem)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
