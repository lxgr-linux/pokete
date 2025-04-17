import scrap_engine as se

from pokete.base.ui.elements import ChooseBox
from pokete.base.ui import Overview
from .box import InvBox


class BaseInv(Overview):
    def __init__(self, name:str, info=""):
        self.box = ChooseBox(50, 35, name, info)
        self.invbox = InvBox(7, 21, overview=self)
        self.money_label = se.Text("$0")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.invbox.add_ob(self.desc_label, 1, 1)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.box.remove()
        self.box.overview.resize_view()
        self.box.resize(self.box.map.height - 3, 35)
        self.box.add(self.box.map, self.box.map.width - self.box.width, 0)
        self.box.map.full_show()

    def set_money(self, figure):
        self.money_label.rechar(f"${figure.get_money()}")
        self.box.set_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
