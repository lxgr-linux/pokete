from abc import ABC, abstractmethod
from ast import TypeVar
from typing import Optional

import scrap_engine as se

from pokete.base import loops
from pokete.base.context import Context
from pokete.base.input.hotkeys import ACTION_DIRECTIONS, Action, get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import Area, MouseInteractor, mouse_interaction_manager
from pokete.base.ui.elements.choose import BetterChooseBox

T = TypeVar("T")


class BetterChooseBoxView[T](BetterChooseBox, MouseInteractor, ABC):
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
        return (int(idx / self.columns), idx % self.columns)

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        match event.type:
            case MouseEventType.MOVE:
                self.set_index(*self.__get_index_from_area_idx(area_idx))
            case MouseEventType.LEFT:
                self.__special_ret = self.choose(ctx, area_idx)

    def __enter__(self):
        mouse_interaction_manager.attach([self])
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, exc_tb):
        mouse_interaction_manager.attach([])
        return super().__exit__(exc_type, exc_value, exc_tb)

    def __call__(self, ctx: Context) -> Optional[T]:
        self.set_ctx(ctx)
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
                        if res is not None:
                            return res
                loops.std(ctx.with_overview(self))
                if self.__special_ret is not None:
                    return self.__special_ret
        return None
