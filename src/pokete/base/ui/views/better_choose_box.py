from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, override

import scrap_engine as se
from scrap_engine.addable.area import Area

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input.hotkeys import ACTION_DIRECTIONS, Action, get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements.choose import BetterChooseBox
from pokete.base.ui.views.pageable import Pageable, UpDownSwitch

T = TypeVar("T")


class BetterChooseBoxView(BetterChooseBox, MouseInteractor, Generic[T], Pageable, ABC):
    def __init__(
        self, columns, rows, labels: list[se.HasArea], name="", _map=None, overview=None
    ):
        self.elems: list[se.HasArea] = labels
        self.rows = rows
        self.page = 0
        self.__special_ret: Optional[T] = None
        self.up_down_switch = UpDownSwitch(self)
        super().__init__(
            columns, self.elems[: rows * columns], name, _map, overview, max_rows=rows
        )
        self.__add_up_down_switch()

    def __add_up_down_switch(self):
        if len(self.elems) / self.columns > self.rows:
            self.add_ob(
                self.up_down_switch,
                self.width - 3 - self.up_down_switch.width,
                self.height - 1,
            )

    @abstractmethod
    def choose(self, ctx: Context, idx: int) -> Optional[T]: ...

    @override
    def get_interaction_areas(self) -> list[Area]:
        return [i.get_area() for f in self.nest_label_obs for i in f]

    def __get_index_from_area_idx(self, idx: int) -> tuple[int, int]:
        return int(idx / self.columns), idx % self.columns

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx >= 0:
            match event.type:
                case MouseEventType.MOVE:
                    self.set_index(*self.__get_index_from_area_idx(area_idx))
                case MouseEventType.LEFT:
                    if event.pressed:
                        self.__special_ret = self.choose(ctx, area_idx)
                        ctx = change_ctx(ctx, self)

    @override
    def get_partial_interactors(self) -> list[MouseInteractor]:
        up_down: list[MouseInteractor] = [self.up_down_switch]
        return [
            label for label in self.info_labels if isinstance(label, MouseInteractor)
        ] + up_down

    @override
    def resize(self, height, width):
        self.rem_ob(self.up_down_switch)
        self.up_down_switch.remove()
        super().resize(height, width)
        self.__add_up_down_switch()

    def set_elems(self, columns, rows, labels: list[se.HasArea]):
        self.rows = rows
        self.page = 0
        self.elems = labels
        super().set_items(columns, self.elems[: rows * columns])

    def change_page(self, add_page, n_idx):
        if 0 <= (self.page + add_page) < (len(self.elems) / (self.rows * self.columns)):
            self.page += add_page
            super().set_items(
                self.columns,
                self.elems[
                    (self.rows * self.columns) * self.page : (self.rows * self.columns)
                    * (self.page + 1)
                ],
            )

    def __call__(self, ctx: Context) -> Optional[T]:
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        self.__add_up_down_switch()

        with self:
            while True:
                action, _ = get_action()
                if action.triggers(*ACTION_DIRECTIONS):
                    self.input(action)
                else:
                    if action.triggers(Action.CANCEL):
                        break
                    if action.triggers(Action.ACCEPT):
                        res = self.choose(
                            ctx, self.index[0] + self.index[1] * self.columns
                        )
                        ctx = change_ctx(ctx, self)
                        if res is not None:
                            return res
                loops.std(ctx)
                if self.__special_ret is not None:
                    return self.__special_ret
        return None
