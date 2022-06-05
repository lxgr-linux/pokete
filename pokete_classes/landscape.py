"""Contains classes that can be placed on playmaps"""

import random
import scrap_engine as se
import pokete_data as p_data
from pokete_classes import timer, movemap as mvp, fightmap as fm
from .color import Color
from .general import check_walk_back
from .poke import Poke
from .input import ask_ok


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
            fm.fight(Poke("__fallback__", 0)
                     if len([poke for poke in self.figure.pokes[:6]
                             if poke.hp > 0]) == 0
                     else
                     [poke for poke in self.figure.pokes[:6] if poke.hp > 0][0],
                     Poke(random.choices(list(pokes),
                                         weights=[i["rarity"] for _, i in
                                                  pokes.items()])[0],
                          random.choices(list(range(self.arg_proto["minlvl"],
                                                    self.arg_proto["maxlvl"])))[
                              0],
                          player=False, shiny=(random.randint(0, 500) == 0)))
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
    max_tick = 100
    curr_tick = max_tick

    def __init__(self, string, poke_args):
        super().__init__(string, ignore=self.esccode + " " + Color.reset,
                         ob_class=HighGrass, ob_args=poke_args,
                         state="float", esccode=self.esccode)
        {
            Color.green: Meadow.all_grass,
            Color.blue: Meadow.all_water,
            Color.yellow: Meadow.all_sand,
        }[self.esccode].append(self)

    @classmethod
    def moving_grass(cls, objs):
        """Animation for moving grass
        ARGS:
            objs: List of Highgrass objects this is done for"""
        if cls.curr_tick < cls.max_tick:
            cls.curr_tick += 1
            return
        cls.curr_tick = 0

        for obj in objs:
            if obj.char == cls.esccode + ";" + Color.reset:
                if random.randint(0, 600) == 0:
                    obj.rechar(Color.thicc + cls.esccode + ";" + Color.reset)
                    cls.check_figure_redraw(obj)
            else:
                obj.rechar(cls.esccode + ";" + Color.reset)
                cls.check_figure_redraw(obj)

    @classmethod
    def moving_water(cls, objs):
        """Water animation
        ARGS:
            objs: The water objects this will happen for"""
        for obj in objs:
            if random.randint(0, 9) == 0:
                if " " not in obj.char:
                    obj.rechar([i for i in
                                [Color.lightblue + "~" + Color.reset,
                                 Color.blue + "~" + Color.reset]
                                if i != obj.char][0])
                    cls.check_figure_redraw(obj)

    @staticmethod
    def check_figure_redraw(obj):
        """Checks whether or not the figure has to be redrawn
        ARGS:
            obj: The obj that this is checked for"""
        if obj.x == HighGrass.figure.x and obj.y == HighGrass.figure.y:
            HighGrass.figure.redraw()


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
{p_data.items[item]['pretty_name']}{'s' if amount > 1 else ''}!")
        self.figure.used_npcs.append(self.name)
