from typing import override

from scrap_engine import Area

from pokete.base.context import Context
from pokete.base.input import (
    Action,
)
from pokete.base.input.event import _ev
from pokete.base.input.key import Key
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements.text import HightlightableText


class GenericActionLabel(HightlightableText, MouseInteractor):
    def __init__(self, action: Action, text: str, esccode: str = "") -> None:
        self.action = action
        assert action.mapping is not None and len(action.mapping) == 1, (
            "Trying to create Actionlabel with noch char mapping"
        )
        self.key = Key(action.mapping)
        super().__init__(f"{action.mapping}:{text}", esccode=esccode)

    @override
    def get_interaction_areas(self) -> list[Area]:
        return [self.get_area()]

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent) -> None:
        if area_idx == 0:
            match event.type:
                case MouseEventType.MOVE:
                    self.highlight()
                case MouseEventType.LEFT:
                    if event.pressed:
                        _ev.set(self.key)
        else:
            self.un_highlight()


class CloseLabel(GenericActionLabel):
    def __init__(self) -> None:
        super().__init__(Action.CANCEL, "close")
