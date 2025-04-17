"""Classes related to buing stuff"""

import scrap_engine as se

from pokete.classes.asset_service.service import asset_service
from pokete.util import liner
from pokete.base.context import Context
from pokete.base.input import ACTION_UP_DOWN, Action, get_action
from pokete.base import loops
from .base_inv import BaseInv

class Buy(BaseInv):
    """Menu to buy items in, is triggered in shop"""

    def __init__(self):
        super().__init__("Shop")
        invitems = asset_service.get_items()
        self.items = [
            invitems[i] for i in [
                "poketeball", "superball",
                "healing_potion", "super_potion", "ap_potion"
            ]
        ]
        self.box.add_c_obs([se.Text(f"{obj.pretty_name} : {obj.price}$")
                            for obj in self.items])

    def __call__(self, ctx: Context):
        """Opens the buy menu"""
        self.box.set_ctx(ctx)
        self.box.resize(ctx.map.height - 3, 35)
        self.set_money(ctx.figure)
        with self.box.add(ctx.map, ctx.map.width - 35, 0):
            self.invbox.add(ctx.map, self.box.x - 19, 3)
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
                        self.set_money(ctx.figure)
                loops.std(ctx=ctx.with_overview(self.invbox))
                ctx.map.full_show()
        self.invbox.remove()

    def rechar(self):
        """Rechars the detail text"""
        obj = self.items[self.box.index.index]
        self.invbox.name_label.rechar(obj.pretty_name)
        self.desc_label.rechar(liner(obj.desc, 19))


buy = Buy()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
