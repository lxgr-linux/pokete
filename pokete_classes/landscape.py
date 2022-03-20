import random
import scrap_engine as se
import pokete_data as p_data
import pokete_classes.game as game
import pokete_classes.fightmap as fm
from .color import Color
from .general import check_walk_back
from .poke import Poke
from .input import ask_ok


class HighGrass(se.Object):
    figure = None
    """Object on the map, that triggers a fight"""

    def action(self, ob):
        """Action triggers the fight
        ARGS:
            ob: The object triggering this action"""
        if random.randint(0, 8) == 0:
            fm.fight(Poke("__fallback__", 0)
                  if len([poke for poke in self.figure.pokes[:6]
                          if poke.hp > 0]) == 0
                  else [poke for poke in self.figure.pokes[:6] if poke.hp > 0][0],
                  Poke(random.choices(self.arg_proto["pokes"],
                                      weights=[p_data.pokes[i]["rarity"]
                                               for i in
                                               self.arg_proto["pokes"]])[0],
                       random.choices(list(range(self.arg_proto["minlvl"],
                                                 self.arg_proto["maxlvl"])))[0],
                       player=False, shiny=(random.randint(0, 500) == 0)))
            check_walk_back(self.figure)


class Meadow(se.Text):
    """Daughter of se.Text to better organize Highgrass
    ARGS:
        string: The character representing the meadow
        poke_args: Dict containing relevant information about Pokes"""
    esccode = Color.green

    def __init__(self, string, poke_args):
        super().__init__(string, ignore=self.esccode + " " + Color.reset,
                         ob_class=HighGrass, ob_args=poke_args,
                         state="float", esccode=self.esccode)


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
                               "healing_potion"],
                              weights=[10, 1.5, 1, 1],
                              k=1)[0]
        self.figure.give_item(item, amount)
        self.remove()
        mvp.movemap.full_show()
        ask_ok(mvp.movemap, f"You found {amount if amount > 1 else 'a'} \
{p_data.items[item]['pretty_name']}{'s' if amount > 1 else ''}!")
        self.figure.used_npcs.append(self.name)
