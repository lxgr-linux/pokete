"""Classes related to buing stuff"""

from typing import Never, Optional

import scrap_engine as se

from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.classes.asset_service.service import asset_service

from .base_inv import BaseInv


class Buy(BaseInv):
    """Menu to buy items in, is triggered in shop"""

    def __init__(self):
        super().__init__("Shop")
        invitems = asset_service.get_items()
        self.items = [
            invitems[i]
            for i in [
                "poketeball",
                "superball",
                "healing_potion",
                "super_potion",
                "ap_potion",
            ]
        ]
        self.elems = [
            se.Text(f"{obj.pretty_name} : {obj.price}$") for obj in self.items
        ]

    def choose(self, ctx: Context, idx: int) -> Optional[Never]:
        obj = self.items[self.index.index]
        do_buy: bool = self.invbox(ctx, obj)
        ctx = change_ctx(ctx, self)
        if do_buy and obj.price is not None:
            if ctx.figure.get_money() - obj.price >= 0:
                ctx.figure.add_money(-obj.price)
                ctx.figure.give_item(obj.name)
                self.set_money(ctx.figure)

    def __call__(self, ctx: Context):
        self.resize(ctx.map.height - 3, 35)
        self.set_money(ctx.figure)
        self.add_elems()
        with self.add(ctx.map, ctx.map.width - self.width, 0):
            super().__call__(ctx)


buy = Buy()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
