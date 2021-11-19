import time
import scrap_engine as se
from .classes import OutP
from pokete_general_use_fns import std_loop, liner


class Movemap(se.Submap):

    def __init__(self, ob_maps, height, width):
        super().__init__(ob_maps["playmap_1"], 0, 0,
                         height=height - 1, width=width)
        self.name_label = se.Text("")
        self.balls_label = se.Text("")
        self.label_bg = se.Square(" ", self.width, 1, state="float")
        self.label = se.Text("1: Deck  2: Exit  3: Map  4: Inv.  5: Dex  ?: Help")
        self.code_label = OutP("")
        self.multitext = OutP("", state="float")
        self.add_obs()

    def add_obs(self):
        """Adds needed labels to movemap"""
        self.underline = se.Square("-", self.width, 1)
        self.name_label.add(self, 2, self.height - 2)
        self.balls_label.add(self, 4 + len(self.name_label.text),
                            self.height - 2)
        self.underline.add(self, 0, self.height - 2)
        self.label_bg.add(self, 0, self.height - 1)
        self.label.add(self, 0, self.height - 1)
        self.code_label.add(self, 0, 0)

    def text(self, x, y, arr, ev):
        """Shows dialog text on movemap"""
        # This ensures the game does not crash when big chunks of text are displayed
        for c, i, j, k in zip([x, y], ["x", "y"],
                              [self.width, self.height], [17, 10]):
            while c - getattr(self, i) + k >= j:
                self.set(self.x + (1 if i == "x" else 0),
                            self.y + (1 if i == "y" else 0))
                self.show()
                time.sleep(0.045)
        # End section
        self.multitext.rechar("")
        self.multitext.add(self, x - self.x + 1, y - self.y)
        arr = [arr[i] + (" >" if i != len(arr) - 1 else "") for i in range(len(arr))]
        for text in arr:
            ev.clear()
            self.multitext.rechar("")
            for i in range(len(text) + 1):
                self.multitext.outp(liner(text[:i],
                               self.width - (x - self.x + 1), "   "))
                time.sleep(0.045)
                std_loop(ev)
                if ev.get() != "":
                    ev.clear()
                    break
            self.multitext.outp(liner(text, self.width - (x - self.x + 1), "   "))
            while True:
                std_loop(ev)
                if ev.get() != "":
                    break
                time.sleep(0.05)
        self.multitext.remove()


