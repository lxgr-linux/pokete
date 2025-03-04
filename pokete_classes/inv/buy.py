"""Classes related to buing stuff"""

import scrap_engine as se

from pokete_classes.context import Context
from util import liner
from .box import InvBox
from .items import invitems
from ..ui import Overview
from ..input import ACTION_UP_DOWN, Action, get_action
from ..ui.elements import ChooseBox
from .. import movemap as mvp, loops


class Buy(Overview):
    """Menu to buy items in, is triggered in shop"""

    def __init__(self):
        self.box = ChooseBox(50, 35, "Shop")
        self.box2 = InvBox(7, 21, overview=self)
        self.items = [invitems.poketeball, invitems.superball,
                      invitems.healing_potion,
                      invitems.super_potion, invitems.ap_potion]
        self.box.add_c_obs([se.Text(f"{obj.pretty_name} : {obj.price}$")
                            for obj in self.items])
        self.money_label = se.Text("0$")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.box.remove()
        self.box.map.resize_view()
        self.box.resize(self.box.map.height - 3, 35)
        self.box.add(self.box.map, self.box.map.width - self.box.width, 0)
        mvp.movemap.full_show()

    def __call__(self, ctx: Context):
        """Opens the buy menu"""
        self.money_label.rechar(f"{ctx.figure.get_money()}$")
        self.box.set_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.box.resize(ctx.map.height - 3, 35)
        with self.box.add(ctx.map, ctx.map.width - 35, 0):
            self.box2.add(ctx.map, self.box.x - 19, 3)
            self.rechar()
            ctx.map.show()
            while True:
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.box.input(action)
                    self.rechar()
                elif action.triggers(Action.CANCEL):
                    break
                elif action.triggers(Action.ACCEPT):
                    obj = self.items[self.box.index.index]
                    if ctx.figure.get_money() - obj.price >= 0:
                        ctx.figure.add_money(-obj.price)
                        ctx.figure.give_item(obj.name)
                loops.std(box=self.box2, pevm=ctx.pevm)
                ctx.map.full_show()
        self.box2.remove()

    def rechar(self):
        """Rechars the detail text"""
        obj = self.items[self.box.index.index]
        self.box2.name_label.rechar(obj.pretty_name)
        self.desc_label.rechar(liner(obj.desc, 19))


buy = Buy()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
