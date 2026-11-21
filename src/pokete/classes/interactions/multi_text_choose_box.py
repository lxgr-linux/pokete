import scrap_engine as se

from pokete.base.context import Context
from pokete.base.ui.views.choose_box import ChooseBoxView

from .. import movemap as mvp


class MultiTextChooseBox(ChooseBoxView[tuple[int, str]]):
    """ChooseBox wrapper for multitext conversations"""

    def __init__(self, keys: list[str], name: str) -> None:
        super().__init__(
            len(keys) + 2,
            max(len(i) for i in keys) + 6,
            name=name,
        )
        self.keys = keys
        self.elems: list[se.ObjectGroup] = [se.Text(i, state="float") for i in keys]
        self.fig: se.Text | None = None

    def new_size(self) -> tuple[int, int]:
        return self.height, self.width

    def choose(self, ctx: Context, idx: int) -> tuple[int, str] | None:
        if idx >= 0:
            return idx, self.keys[idx]
        else:
            return None

    def add_relative(self, _map: "GameSubmap", x: int, y: int) -> None:
        assert self.fig
        mvp.movemap.assure_distance(
            self.fig.x, self.fig.y, self.width + 2, self.height + 2
        )
        return super().add(
            _map, self.fig.x - mvp.movemap.x, self.fig.y - mvp.movemap.y + 1
        )

    def __call__(self, ctx: Context) -> tuple[int, str]:
        self.fig = ctx.figure
        ret: tuple[int, str] | None = None

        while ret is None:
            self.add_elems()
            with self.add_relative(ctx.map, -1, -1):
                ret = super().__call__(ctx)
        return ret
