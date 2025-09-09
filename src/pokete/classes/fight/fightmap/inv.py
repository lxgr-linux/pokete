"""Contains stuff related to fight inventory"""

from typing import Optional

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.ui.views.choose_box import ChooseBoxView
from pokete.classes.items.invitem import InvItem


class InvBox(ChooseBoxView[InvItem]):
    def __init__(self):
        super().__init__(10, 35, "Inventory")
        self.items: list[InvItem] = []

    def choose(self, ctx: Context, idx: int) -> Optional[InvItem]:
        return self.items[idx]

    def new_size(self) -> tuple[int, int]:
        return self.map.height - 3, 35

    def __call__(
        self, ctx: Context, items: list[InvItem], inv
    ) -> Optional[InvItem]:
        self.items = items
        self.resize(ctx.map.height - 3, 35)
        self.elems = [
            se.Text(f"{i.pretty_name}s : {inv[i.name]}") for i in items
        ]
        self.add_elems()
        with self.add(ctx.map, ctx.map.width - self.width, 0):
            return super().__call__(ctx)
