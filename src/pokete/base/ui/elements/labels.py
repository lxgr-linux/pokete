from scrap_engine import Area

from pokete.base.context import Context
from pokete.base.input import (
    Action,
)
from pokete.base.input.event import _ev
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements.text import HightlightableText


class GenericActionLabel(HightlightableText, MouseInteractor):
    def __init__(self, action: Action, text: str):
        self.action = action
        super().__init__(f"{action.mapping}:{text}")

    def get_interaction_areas(self) -> list[Area]:
        return [self.get_area()]

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx == 0:
            match event.type:
                case MouseEventType.MOVE:
                    self.highlight()
                case MouseEventType.LEFT:
                    _ev.set(self.action.mapping)
        else:
            self.un_highlight()


class CloseLabel(GenericActionLabel):
    def __init__(self):
        super().__init__(Action.CANCEL, "close")
