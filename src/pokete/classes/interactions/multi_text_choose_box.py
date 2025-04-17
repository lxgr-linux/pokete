import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input import get_action, ACTION_UP_DOWN, Action
from pokete.base.ui.elements import ChooseBox
from pokete.base import loops
from .. import movemap as mvp


class MultiTextChooseBox(ChooseBox):
    """ChooseBox wrapper for multitext conversations"""

    def __init__(self, keys: list[str], name: str):
        super().__init__(
            len(keys) + 2,
            sorted(len(i) for i in keys)[-1] + 6,
            name=name,
            c_obs=[se.Text(i, state="float") for i in keys],
        )
        self.fig = None
        self.keys = keys

    def resize_view(self):
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        mvp.movemap.assure_distance(
            self.fig.x, self.fig.y,
            self.width + 2, self.height + 2
        )
        self.add(
            mvp.movemap,
            self.fig.x - mvp.movemap.x,
            self.fig.y - mvp.movemap.y + 1
        )

    def __call__(self, ctx: Context) -> str:
        self.set_ctx(ctx)
        self.fig = ctx.figure
        self.frame.corners[0].rechar("^")
        mvp.movemap.assure_distance(self.fig.x, self.fig.y,
                                    self.width + 2, self.height + 2)
        with self.add(ctx.map, self.fig.x - mvp.movemap.x,
                      self.fig.y - mvp.movemap.y + 1):
            while True:
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.input(action)
                    mvp.movemap.full_show()
                elif action.triggers(Action.ACCEPT):
                    key = self.keys[self.index.index]
                    break
                loops.std(ctx.with_overview(self))
        return key
