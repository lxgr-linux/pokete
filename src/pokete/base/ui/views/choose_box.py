from abc import ABC, abstractmethod
from typing import Never, Optional

import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input.hotkeys import ACTION_UP_DOWN, Action, get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import Area, MouseInteractor
from pokete.base.ui.elements.choose import ChooseBox


class ChooseBoxView(ChooseBox, MouseInteractor, ABC):
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
        self.elems: list[se.Text] = []

    @abstractmethod
    def choose(self, ctx: Context, idx: int) -> Optional[Never]: ...

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
                    self.set_index(area_idx)
                case MouseEventType.LEFT:
                    self.__special_ret = self.choose(
                        ctx, self.page * (self.height - 2) + area_idx
                    )
                    ctx = change_ctx(ctx, self)

    def add_elems(self):
        """Adds c_obs to box"""
        self.add_c_obs(
            self.elems[
                self.page * (self.height - 2) : (self.page + 1)
                * (self.height - 2)
            ]
        )

    def resize_view(self):
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        self.resize(self.map.height - 3, 35)
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

    def __call__(self, ctx: Context):
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)

        while True:
            action = get_action()
            for event, idx, n_idx, add_page, idx_2 in zip(
                [Action.DOWN, Action.UP],
                [len(self.c_obs) - 1, 0],
                [0, self.height - 3],
                [1, -1],
                [-1, 0],
            ):
                if action.triggers(event) and self.index.index == idx:
                    if self.c_obs[self.index.index] != self.elems[idx_2]:
                        self.rem_elems()
                        self.page += add_page
                        self.add_elems()
                        self.set_index(n_idx)
                    action = get_action()
            if action.triggers(Action.ACCEPT):
                self.choose(
                    ctx, self.page * (self.height - 2) + self.index.index
                )
                ctx = change_ctx(ctx, self)
            elif action.triggers(*ACTION_UP_DOWN):
                self.input(action)
            elif action.triggers(Action.CANCEL, Action.POKEDEX):
                break
            loops.std(ctx)
        self.rem_elems()
