"""Contains classes that can be placed on playmaps"""

import random
import scrap_engine as se
import pokete_data as p_data
from pokete_classes import timer, movemap as mvp
from .fight import Fight, NatureProvider
from .color import Color
from .general import check_walk_back
from .poke import Poke
from .input_loops import ask_ok


class HighGrass(se.Object):
    """Object on the map, that triggers a fight"""
    figure = None

    def action(self, ob):
        """Action triggers the fight
        ARGS:
            ob: The object triggering this action"""
        is_night = (360 > timer.time.normalized
                    or timer.time.normalized > 1320)
        pokes = {i: p_data.pokes[i]
                 for i in self.arg_proto["pokes"]
                 if (n_a := p_data.pokes[i].get("night_active", None)) is None
                 or (not n_a and not is_night)
                 or (n_a and is_night)}
        if random.randint(0, 8) == 0:
            Fight()(
                [
                    self.figure,
                    NatureProvider(
                        Poke.wild(
                            random.choices(
                                list(pokes),
                                weights=[i["rarity"] for i in pokes.values()]
                            )[0],
                            random.choice(
                                range(
                                    self.arg_proto["minlvl"],
                                    self.arg_proto["maxlvl"]
                                )
                            )
                        )
                    )
                ]
            )
            check_walk_back(self.figure)


class Meadow(se.Text):
    """Daughter of se.Text to better organize Highgrass
    ARGS:
        string: The character representing the meadow
        poke_args: Dict containing relevant information about Pokes"""
    esccode = Color.green
    all_grass = []
    all_water = []
    all_sand = []

    def __init__(self, string, poke_args):
        super().__init__(string, ignore=self.esccode + " " + Color.reset,
                         ob_class=HighGrass, ob_args=poke_args,
                         state="float", esccode=self.esccode)
        {
            Color.green: Meadow.all_grass,
            Color.blue: Meadow.all_water,
            Color.yellow: Meadow.all_sand,
        }[self.esccode].append(self)


class Water(Meadow):
    """Same as Meadow, but for Water"""
    esccode = Color.blue


class Sand(Meadow):
    """Same as Meadow, but for Sand"""
    esccode = Color.yellow


class Poketeball(se.Object):
    """Poketeball that can be picked up on the map
    ARGS:
        name: Generic name of the ball"""
    figure = None

    def __init__(self, name):
        self.name = name
        super().__init__(Color.thicc + Color.red + "o" + Color.reset,
                         state="float")

    def action(self, ob):
        """Action triggers the pick up
        ARGS:
            ob: The object triggering this action"""
        amount = random.choices([1, 2, 3],
                                weights=[10, 2, 1], k=1)[0]
        item = random.choices(["poketeball", "hyperball", "superball",
                               "healing_potion", "treat"],
                              weights=[10, 1.5, 1, 1, 1],
                              k=1)[0]
        self.figure.give_item(item, amount)
        self.remove()
        mvp.movemap.full_show()
        ask_ok(mvp.movemap, f"You found {amount if amount > 1 else 'a'} \
{p_data.items[item]['pretty_name']}{'s' if amount > 1 else ''}!", mvp.movemap)
        self.figure.used_npcs.append(self.name)
