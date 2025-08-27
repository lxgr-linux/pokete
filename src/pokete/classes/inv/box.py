import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.ui.elements import Box
from pokete.base.ui.overview import Overview
from pokete.classes.items.invitem import InvItem
from pokete.util import liner


class InvBox(Box):
    """Box wrapper for inv"""

    def __init__(self, overview: Overview):
        super().__init__(7, 21, overview=overview)
        self.desc_label = se.Text(" ")
        self.add_ob(self.desc_label, 1, 1)

    def __call__(self, ctx: Context, obj: InvItem) -> bool:
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        self.name_label.rechar(obj.pretty_name)
        self.desc_label.rechar(liner(obj.desc, 19))
        with self.add(self.map, self.overview.x - 19, 3):
            return loops.easy_exit(ctx)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        self.add(self.map, self.overview.x - 19, 3)
