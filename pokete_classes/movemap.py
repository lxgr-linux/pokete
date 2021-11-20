"""This file caontains the Movemap class with all related mothods"""

import time
import scrap_engine as se
from pokete_general_use_fns import std_loop, liner
from .classes import OutP


class Movemap(se.Submap):
    """Movemap class to remove bad code"""

    def __init__(self, ob_maps, height, width):
        super().__init__(ob_maps["playmap_1"], 0, 0,
                         height=height, width=width)
        self.name_label = se.Text("")
        self.balls_label = se.Text("")
        self.label_bg = se.Square(" ", self.width, 1, state="float")
        self.label = se.Text("1: Deck  2: Exit  3: Map  4: Inv.  5: Dex  ?: Help")
        self.code_label = OutP("")
        self.multitext = OutP("", state="float")

    def add_obs(self):
        """Adds needed labels to movemap"""
        self.underline = se.Square("-", self.width, 1, state="float")
        self.underline.add(self, 0, self.height - 2)
        self.name_label.add(self, 2, self.height - 2)
        self.balls_label.add(self, 4 + len(self.name_label.text),
                            self.height - 2)
        self.label_bg.add(self, 0, self.height - 1)
        self.label.add(self, 0, self.height - 1)
        self.code_label.add(self, 0, 0)

    def text(self, x, y, arr, _ev):
        """Shows dialog text on movemap"""
        # This ensures the game does not crash when big
        # chunks of text are displayed
        for _c, i, j, _k in zip([x, y], ["x", "y"],
                              [self.width, self.height], [17, 10]):
            while _c - getattr(self, i) + _k >= j:
                self.set(self.x + (1 if i == "x" else 0),
                         self.y + (1 if i == "y" else 0))
                self.show()
                time.sleep(0.045)
        # End section
        self.multitext.rechar("")
        self.multitext.add(self, x - self.x + 1, y - self.y)
        for i in range(len(arr) - 1):
            arr[i] += " >"
        for text in arr:
            _ev.clear()
            self.multitext.rechar("")
            for i in range(len(text) + 1):
                self.multitext.outp(liner(text[:i],
                                          self.width - (x - self.x + 1), "   "))
                time.sleep(0.045)
                std_loop(_ev)
                if _ev.get() != "":
                    _ev.clear()
                    break
            self.multitext.outp(liner(text,
                                      self.width - (x - self.x + 1), "   "))
            while _ev.get() == "":
                std_loop(_ev)
                time.sleep(0.05)
        self.multitext.remove()
