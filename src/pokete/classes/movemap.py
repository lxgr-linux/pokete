"""This file contains the Movemap class with all related mothods"""

import time

import scrap_engine as se

from pokete.base.game_map import GameSubmap
from pokete.util import liner
from pokete.release import SPEED_OF_TIME
from pokete.base.context import Context
from pokete.base.color import Color
from pokete.base.input import _ev, Action
from pokete.base.ui import notifier, Overview
from pokete.base.tss import tss
from pokete.base import loops
from .multiplayer.interactions import movemap_deco
from .classes import OutP
import pokete.classes.multiplayer.pc_manager as pc_manager


class Movemap(GameSubmap, Overview):
    """Movemap class to remove bad code
    ARGS:
        height: Height of the map
        width: Width of the map"""

    def __init__(self):
        super().__init__(se.Map(), 0, 0,
                         height=50, width=100, name="movemap")
        self.name_label = se.Text("")
        self.balls_label = se.Text("")
        self.label_bg = se.Square(" ", self.width, 1, state="float")
        self.label = se.Text(
            f"{Action.DECK.mapping}: Deck  "
            f"{Action.EXIT_GAME.mapping}: Quit  "
            f"{Action.MAP.mapping}: Map  "
            f"{Action.INVENTORY.mapping}: Inv.  "
            f"{Action.POKEDEX.mapping}: Dex  "
            f"{Action.CLOCK.mapping}: Clock  "
            f"{Action.HELP.mapping}: help  "
        )
        self.code_label = OutP("", state="float")
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
        movemap_deco.add(self, self.label.width, self.height - 1)

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

    def text(self, ctx: Context, _x, _y, inp_arr, passthrough=False):
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
                loops.std(ctx.with_overview(self))
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
                loops.std(ctx.with_overview(self))
                self.full_show()
        self.multitext.remove()
        if not passthrough:
            _ev.clear()

    def resize_view(self):
        """Manages recursive view resizing"""
        if notifier.notified:
            notifier.notification.remove()
            saved_coords = (self.width - notifier.notification.x)
        for _, rmtplr in pc_manager.pc_manager.reg.items():
            rmtplr.name_tag.remove()
        self.resize(tss.height - 1, tss.width, " ")
        self.remap()
        if notifier.notified:
            notifier.notification.add(self, self.width - saved_coords, 0)
        for _, rmtplr in pc_manager.pc_manager.reg.items():
            rmtplr.add_name_tag()

    def resize(self, height, width, background=" "):
        """Resizes the map and its attributes
        See se.Map.resize"""
        for obj in [self.underline, self.label, self.label_bg,
                    self.name_label, self.balls_label, movemap_deco]:
            obj.remove()
        super().resize(height, width, background)
        self.underline.resize(self.width, 1)
        self.label_bg.resize(self.width, 1)
        self.add_obs()

    def balls_label_rechar(self, pokes):
        """Rechars the ball's label
        ARGS:
            pokes: The player's Pokes"""
        self.balls_label.rechar(
            "".join("-" if i >= len(pokes)
                           or pokes[
                               i].identifier == "__fallback__"
                    else "o" if pokes[i].hp > 0
            else "x"
                    for i in range(6)),
            esccode=Color.thicc)

    def name_label_rechar(self, name):
        """Rechars name_label and sets balls_label correctly
        ARGS:
            name: The player's new name"""
        self.balls_label.set(0, 1)
        self.name_label.rechar(name, esccode=Color.thicc)
        self.balls_label.set(4 + len(self.name_label.text), self.height - 2)


movemap: Movemap = Movemap()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
