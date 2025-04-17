"""Contains stuff related to fight inventory"""

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.ui.elements import ChooseBox
from pokete.base.input import ACTION_UP_DOWN, Action, get_action
from pokete.base import loops
from pokete.classes.items.invitem import InvItem


class InvBox(ChooseBox):
    """Inventory box for fight"""

    def resize_view(self):
        """Resizes the view"""
        self.remove()
        self.overview.resize_view()
        self.resize(self.map.height - 3, 35)
        self.add(self.map, self.map.width - 35, 0)
        self.map.show()

    def __call__(self, ctx: Context, items: list[InvItem],
                 inv) -> InvItem | None:
        """Inputloop for inv
        ARGS:
            items: List of InvItems that can be choosen from
            inv: The Figures inv"""
        self.set_ctx(ctx)
        self.add_c_obs([se.Text(f"{i.pretty_name}s : {inv[i.name]}")
                        for i in items])
        self.set_index(0)
        self.resize(ctx.map.height - 3, 35)
        with self.add(ctx.map, ctx.map.width - 35, 0):
            while True:
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.input(action)
                    ctx.map.show()
                elif action.triggers(Action.CANCEL):
                    item = None
                    break
                elif action.triggers(Action.ACCEPT):
                    item = items[self.index.index]
                    break
                loops.std(ctx.with_overview(self))
        self.remove_c_obs()
        return item
