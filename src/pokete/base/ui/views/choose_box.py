import math
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, override

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
from pokete.base.ui.elements.text import HightlightableText

T = TypeVar("T")


class Pageable(ABC):
    @abstractmethod
    def change_page(self, add_page, n_idx): ...


class UpDownSwitch(se.Box, MouseInteractor):
    def __init__(self, pageable: Pageable):
        super().__init__(1, 1)
        self.pageable = pageable
        self.up = HightlightableText("<")
        self.down = HightlightableText(">")
        self.add_ob(self.up, 0, 0)
        self.add_ob(self.down, 1, 0)

    def get_interaction_areas(self) -> list[Area]:
        return [self.up.get_area(), self.down.get_area()]

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx >= 0:
            match event.type:
                case MouseEventType.MOVE:
                    if area_idx == 0:
                        self.down.un_highlight()
                        self.up.highlight()
                    else:
                        self.up.un_highlight()
                        self.down.highlight()
                case MouseEventType.LEFT:
                    if event.pressed:
                        if area_idx == 0:
                            self.pageable.change_page(
                                -1, self.pageable.height - 3
                            )
                        else:
                            self.pageable.change_page(1, 0)
        else:
            self.up.un_highlight()
            self.down.un_highlight()


class ChooseBoxView(ChooseBox, MouseInteractor, Generic[T], Pageable, ABC):
    def __init__(
        self,
        height,
        width,
        name="",
        info="",
        index_x=2,
        c_obs=None,
        overview=None,
    ):
        super().__init__(height, width, name, info, index_x, c_obs, overview)
        self.page = 0
        self.elems: list[HasArea] = []
        self.up_down_switch = UpDownSwitch(self)
        self.__special_ret: Optional[T] = None
        self.add_ob(
            self.up_down_switch,
            self.width - 3 - self.up_down_switch.width,
            self.height - 1,
        )

    @override
    def get_partial_interactors(self) -> list[MouseInteractor]:
        up_down: list[MouseInteractor] = [self.up_down_switch]
        return [
            label
            for label in self.info_labels
            if isinstance(label, MouseInteractor)
        ] + up_down

    @abstractmethod
    def choose(self, ctx: Context, idx: int) -> Optional[T]: ...

    def on_index_change(self, area_idx: int): ...

    def set_index(self, index: int):
        super().set_index(index)
        self.on_index_change(self.page * (self.height - 2) + index)

    def get_interaction_areas(self) -> list[Area]:
        return [
            (
                (i.x, i.y),
                (self.x + self.width - 2, i.y + i.height - 1),
            )
            for i in self.elems[
                self.page * (self.height - 2) : (self.page + 1)
                * (self.height - 2)
            ]
        ]

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
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

    def add_elems(self):
        """Adds c_obs to box"""
        self.remove_c_obs()
        self.add_c_obs(
            self.elems[
                self.page * (self.height - 2) : (self.page + 1)
                * (self.height - 2)
            ]
        )

    @abstractmethod
    def new_size(self) -> tuple[int, int]: ...

    def resize(self, height, width):
        super().resize(height, width)
        self.add_ob(
            self.up_down_switch,
            self.width - 3 - self.up_down_switch.width,
            self.height - 1,
        )

    def resize_view(self):
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        self.resize(*self.new_size())
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

    def rem_elems(self):
        """Removes c_obs to box"""
        for c_ob in self.c_obs:
            c_ob.remove()
        self.remove_c_obs()

    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool:
        return False

    def change_page(self, add_page, n_idx):
        if (
            0
            <= (self.page + add_page)
            < math.ceil(len(self.elems) / (self.height - 2))
        ):
            self.rem_elems()
            self.page += add_page
            self.add_elems()
            self.set_index(n_idx)

    def __call__(self, ctx: Context) -> Optional[T]:
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)

        while True:
            action = get_action()
            for event, idx, n_idx, add_page in zip(
                [Action.DOWN, Action.UP],
                [len(self.c_obs) - 1, 0],
                [0, self.height - 3],
                [1, -1],
            ):
                if action.triggers(event) and self.index.index == idx:
                    self.change_page(add_page, n_idx)
                    action = get_action()
            if action.triggers(Action.ACCEPT):
                res = self.choose(
                    ctx, self.page * (self.height - 2) + self.index.index
                )
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
