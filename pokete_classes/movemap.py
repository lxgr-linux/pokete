"""This file caontains the Movemap class with all related mothods"""

import time
import scrap_engine as se
from pokete_general_use_fns import liner
from . import ob_maps as obmp, game_map as gm
from release import SPEED_OF_TIME
from .loops import std_loop
from .classes import OutP
from .color import Color
from .event import _ev
from .hotkeys import Action


class Movemap(gm.GameSubmap):
    """Movemap class to remove bad code
    ARGS:
        ob_maps: Dict that contains all PlayMaps
        height: Height of the map
        width: Width of the map"""

    def __init__(self, height, width):
        super().__init__(obmp.ob_maps["playmap_1"], 0, 0,
                         height=height, width=width, name="movemap")
        self.name_label = se.Text("")
        self.balls_label = se.Text("")
        self.label_bg = se.Square(" ", self.width, 1, state="float")
        self.label = se.Text(
            f"{Action.DECK.mapping}: Deck  "
            f"{Action.EXIT_GAME.mapping}: Quit  "
            f"{Action.MAP.mapping}: Map  "
            f"{Action.INVENTORY.mapping}: Inv.  "
            f"{Action.POKEDEX.mapping}: Pokedex  "
            f"{Action.CLOCK.mapping}: Clock  "
            f"{Action.HELP.mapping}: help"
        )
        self.code_label = OutP("")
        self.multitext = OutP("", state="float")
        self.underline = se.Square("-", self.width, 1, state="float")
        self.code_label.add(self, 0, 0)

    def add_obs(self):
        """Adds needed labels to movemap"""
        self.underline.add(self, 0, self.height - 2)
        self.name_label.add(self, 2, self.height - 2)
        self.balls_label.add(self, 4 + len(self.name_label.text),
                             self.height - 2)
        self.label_bg.add(self, 0, self.height - 1)
        self.label.add(self, 0, self.height - 1)

    def assure_distance(self, _x, _y, width, height):
        """This ensures the game does not crash when big
        chunks of text are displayed
        ARGS:
            _x: The x coordinate the distance should be assured from
            _y: The y coordinate the distance should be assured from
            width: The distances width
            height: The distances height"""
        for _c, i, j, _k in zip([_x, _y], ["x", "y"],
                                [self.width, self.height], [width, height]):
            while _c - getattr(self, i) + _k >= j:
                self.set(self.x + (1 if i == "x" else 0),
                         self.y + (1 if i == "y" else 0))
                self.show()
                time.sleep(SPEED_OF_TIME * 0.045)

    def text(self, _x, _y, inp_arr):
        """Shows dialog text on movemap
        ARGS:
            _x: The message's X
            _y: And y-coordinate
            inp_arr: List of messages that will be displayed"""
        self.assure_distance(_x, _y, 17, 10)
        self.multitext.rechar("")
        self.multitext.add(self, _x - self.x + 1, _y - self.y)
        arr = [" < " + i + (" >" if j != len(inp_arr) - 1 else "")
               for j, i in enumerate(inp_arr)]
        for text in arr:
            # Clear events and animate text appearing until any key is pressed.
            # Then wait until another key is pressed to close dialogue.
            _ev.clear()
            self.multitext.rechar("")
            for i in range(len(text) + 1):
                self.multitext.outp(
                    liner(
                        text[:i],
                        self.width - (_x - self.x + 1),
                        "   "
                    )
                )
                std_loop()
                if _ev.get() != "":
                    _ev.clear()
                    break
            self.multitext.outp(
                liner(
                    text,
                    self.width - (_x - self.x + 1),
                    "   "
                )
            )
            while _ev.get() == "":
                std_loop()
        self.multitext.remove()

    def resize(self, height, width, background=" "):
        """Resizes the map and its attributes
        See se.Map.resize"""
        for obj in [self.underline, self.label, self.label_bg,
                    self.name_label, self.balls_label]:
            obj.remove()
        super().resize(height, width, background)
        self.underline.resize(self.width, 1)
        self.label_bg.resize(self.width, 1)
        self.add_obs()

    def balls_label_rechar(self, pokes):
        """Rechars the ball's label
        ARGS:
            pokes: The player's Pokes"""
        self.balls_label.rechar("".join("-" if i >= len(pokes)
                                or pokes[i].identifier == "__fallback__"\
                                        else "o" if pokes[i].hp > 0
                                        else "x"
                                        for i in range(6)), esccode=Color.thicc)

    def name_label_rechar(self, name):
        """Rechars name_label and sets balls_label correctly
        ARGS:
            name: The player's new name"""
        self.balls_label.set(0, 1)
        self.name_label.rechar(name, esccode=Color.thicc)
        self.balls_label.set(4 + len(self.name_label.text), self.height - 2)


movemap = None

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
