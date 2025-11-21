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

T = TypeVar("T")


class BetterChooseBoxView(BetterChooseBox, MouseInteractor, Generic[T], ABC):
    def __init__(
        self, columns, labels: list[se.Text], name="", _map=None, overview=None
    ):
        super().__init__(columns, labels, name, _map, overview)
        self.__special_ret: Optional[T] = None

    @abstractmethod
    def choose(self, ctx: Context, idx: int) -> Optional[T]: ...

    def get_interaction_areas(self) -> list[Area]:
        return [i.get_area() for f in self.nest_label_obs for i in f]

    def __get_index_from_area_idx(self, idx: int) -> tuple[int, int]:
        return int(idx / self.columns), idx % self.columns

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx >= 0:
            match event.type:
                case MouseEventType.MOVE:
                    self.set_index(*self.__get_index_from_area_idx(area_idx))
                case MouseEventType.LEFT:
                    self.__special_ret = self.choose(ctx, area_idx)
                    ctx = change_ctx(ctx, self)

    @override
    def get_partial_interactors(self) -> list["MouseInteractor"]:
        return [
            label
            for label in self.info_labels
            if isinstance(label, MouseInteractor)
        ]

    def __call__(self, ctx: Context) -> Optional[T]:
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        with self:
            while True:
                action = get_action()
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
