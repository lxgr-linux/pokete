"""Contains stuff related to fight inventory"""

from typing import Optional

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input_loops.ask.ok import ask_ok
from pokete.base.ui.views.choose_box import ChooseBoxView
from pokete.classes.items.invitem import InvItem


class InvBox(ChooseBoxView[InvItem]):
    def __init__(self):
        super().__init__(10, 35, "Inventory")
        self.items: list[InvItem] = []
        self.is_duel = False

    def choose(self, ctx: Context, idx: int) -> Optional[InvItem]:
        item = self.items[idx]
        if not item.usable_in_duel and self.is_duel:
            ask_ok(ctx, "You can't use this in a duel")
            return None
        return item

    def new_size(self) -> tuple[int, int]:
        return self.map.height - 3, 35

    def __call__(
        self,
        ctx: Context,
        items: list[InvItem],
        inv: dict[str, int],
        is_duel: bool,
    ) -> Optional[InvItem]:
        self.items = items
        self.is_duel = is_duel
        self.resize(ctx.map.height - 3, 35)
        self.elems = [
            se.Text(f"{i.pretty_name}s : {inv[i.name]}") for i in items
        ]
        self.add_elems()
        with self.add(ctx.map, ctx.map.width - self.width, 0):
            return super().__call__(ctx)
