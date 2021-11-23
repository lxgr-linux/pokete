import scrap_engine as se
from .ui_elements import StdFrame2, ChooseBox
from .classes import OutP


class FightMap(se.Map):
    """Wrapper for se.Map"""

    def __init__(self, height, width):
        super().__init__(height, width, " ")
        self.box = ChooseBox(6, 25, "Attacks", index_x=1)
        self.invbox = ChooseBox(height - 3, 35, "Inventory")
        # visual objects
        self.frame_big = StdFrame2(self.height - 5, self.width,
                                       state="float")
        self.frame_small = se.Frame(height=4, width=self.width,
                                                  state="float")
        self.e_underline = se.Text("----------------+", state="float")
        self.e_sideline = se.Square("|", 1, 3, state="float")
        self.p_upperline = se.Text("+----------------", state="float")
        self.p_sideline = se.Square("|", 1, 4, state="float")
        self.outp = OutP("", state="float")
        self.label = se.Text("1: Attack  2: Run!  3: Inv.  4: Deck")
        # adding
        self.outp.add(self, 1, self.height - 4)
        self.e_underline.add(self, 1, 4)
        self.e_sideline.add(self, len(self.e_underline.text), 1)
        self.p_upperline.add(self,
                                 self.width - 1 - len(self.p_upperline.text),
                                 self.height - 10)
        self.frame_big.add(self, 0, 0)
        self.p_sideline.add(self,
                                self.width - 1 - len(self.p_upperline.text),
                                self.height - 9)
        self.frame_small.add(self, 0, self.height - 5)
        self.label.add(self, 0, self.height - 1)

