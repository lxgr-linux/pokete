from abc import ABC, abstractmethod
from typing import override

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements import HightlightableText


class Pageable(ABC):
    @abstractmethod
    def change_page(self, add_page: int, n_idx: int) -> None: ...


class UpDownSwitch(se.Box, MouseInteractor):
    def __init__(self, pageable: Pageable) -> None:
        super().__init__(1, 1)
        self.pageable = pageable
        self.up = HightlightableText("<")
        self.down = HightlightableText(">")
        self.add_ob(self.up, 0, 0)
        self.add_ob(self.down, 1, 0)

    @override
    def get_interaction_areas(self) -> list[se.Area]:
        return [self.up.get_area(), self.down.get_area()]

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent) -> None:
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
                            self.pageable.change_page(-1, self.pageable.height - 3)
                        else:
                            self.pageable.change_page(1, 0)
        else:
            self.up.un_highlight()
            self.down.un_highlight()
