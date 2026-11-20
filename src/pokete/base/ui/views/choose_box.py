import math
from abc import ABC, abstractmethod
from typing import TypeVar, override

import scrap_engine as se
from scrap_engine.addable.area import Area, HasArea

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input.hotkeys import (
    ACTION_UP_DOWN,
    Action,
    ActionList,
    get_action,
)
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements.choose import ChooseBox
from pokete.base.ui.views.pageable import Pageable, UpDownSwitch

T = TypeVar("T")


class ChooseBoxView[T](ChooseBox, MouseInteractor, Pageable, ABC):
    def __init__(
        self,
        height: int,
        width: int,
        name: str = "",
        info: list[se.Text] | None = None,
        index_x: int = 2,
        c_obs: list[HasArea] | None = None,
        overview=None,
    ) -> None:
        super().__init__(height, width, name, info, index_x, c_obs, overview)
        self.page = 0
        self.elems: list[HasArea] = []
        self.up_down_switch = UpDownSwitch(self)
        self.__special_ret: T | None = None
        self.__add_up_down_switch()

    def __add_up_down_switch(self) -> None:
        if len(self.elems) / (self.height - 2) > 1:
            self.add_ob(
                self.up_down_switch,
                self.width - 3 - self.up_down_switch.width,
                self.height - 1,
            )

    @override
    def get_partial_interactors(self) -> list[MouseInteractor]:
        up_down: list[MouseInteractor] = [self.up_down_switch]
        return [
            label for label in self.info_labels if isinstance(label, MouseInteractor)
        ] + up_down

    @abstractmethod
    def choose(self, ctx: Context, idx: int) -> T | None: ...

    def on_index_change(self, area_idx: int) -> None: ...

    @override
    def set_index(self, index: int) -> None:
        super().set_index(index)
        self.on_index_change(self.page * (self.height - 2) + index)

    @override
    def get_interaction_areas(self) -> list[Area]:
        return [
            (
                (i.x, i.y),
                (self.x + self.width - 2, i.y + i.height - 1),
            )
            for i in self.elems[
                self.page * (self.height - 2) : (self.page + 1) * (self.height - 2)
            ]
        ]

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent) -> None:
        if area_idx >= 0:
            match event.type:
                case MouseEventType.MOVE:
                    if area_idx < len(self.c_obs):
                        self.set_index(area_idx)
                case MouseEventType.LEFT:
                    if event.pressed:
                        self.__special_ret = self.choose(
                            ctx, self.page * (self.height - 2) + area_idx
                        )
                        ctx = change_ctx(ctx, self)
        match event.type:
            case MouseEventType.SCROLL_UP:
                self.change_page(-1, self.height - 3)
            case MouseEventType.SCROLL_DOWN:
                self.change_page(1, 0)

    def add_elems(self) -> None:
        """Adds c_obs to box"""
        self.remove_c_obs()
        self.add_c_obs(
            self.elems[
                self.page * (self.height - 2) : (self.page + 1) * (self.height - 2)
            ]
        )

    @abstractmethod
    def new_size(self) -> tuple[int, int]: ...

    @override
    def resize_view(self) -> None:
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        self.rem_ob(self.up_down_switch)
        self.resize(*self.new_size())
        self.__add_up_down_switch()
        self.rem_elems()
        self.add_elems()
        if len(self.c_obs) == 0:
            self.page -= 1
            self.rem_elems()
            self.add_elems()
            self.set_index(len(self.c_obs) - 1)
        if self.index.index >= len(self.c_obs):
            self.set_index(len(self.c_obs) - 1)
        self.add(self.map, self.map.width - self.width, 0)
        self.map.full_show()

    def rem_elems(self) -> None:
        """Removes c_obs to box"""
        for c_ob in self.c_obs:
            c_ob.remove()
        self.remove_c_obs()

    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool:
        return False

    @override
    def change_page(self, add_page: int, n_idx: int) -> None:
        if 0 <= (self.page + add_page) < math.ceil(len(self.elems) / (self.height - 2)):
            self.rem_elems()
            self.page += add_page
            self.add_elems()
            self.set_index(n_idx)

    def __call__(self, ctx: Context) -> T | None:
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        self.__add_up_down_switch()

        while True:
            action, _ = get_action()
            for event, idx, n_idx, add_page in zip(
                [Action.DOWN, Action.UP],
                [len(self.c_obs) - 1, 0],
                [0, self.height - 3],
                [1, -1],
            ):
                if action.triggers(event) and self.index.index == idx:
                    self.change_page(add_page, n_idx)
                    action, _ = get_action()
            if action.triggers(Action.ACCEPT):
                res = self.choose(ctx, self.page * (self.height - 2) + self.index.index)
                ctx = change_ctx(ctx, self)
                if res is not None:
                    return res
            elif action.triggers(*ACTION_UP_DOWN):
                self.input(action)
            elif action.triggers(Action.CANCEL):
                break
            if self.handle_extra_actions(ctx, action):
                break
            loops.std(ctx)
            if (ret := self.__special_ret) is not None:
                self.rem_elems()
                self.__special_ret = None
                return ret
        self.rem_elems()
        return None
