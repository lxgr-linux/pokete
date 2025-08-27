import scrap_engine as se
from scrap_engine.addable.misc.frame import Optional

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input.hotkeys import Action, get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import Area, MouseInteractor
from pokete.base.ui.elements.box import Box
from pokete.base.ui.elements.text import HightlightableText


class AskBoolBox(Box, MouseInteractor):
    def __init__(self, text: str):
        assert len(text) >= 12, "Text has to be longer then 12 characters!"
        self.__result: Optional[bool] = None
        self.__text_label = se.Text(text)
        self.__yes_label = HightlightableText("[Y]es")
        self.__no_label = HightlightableText("[N]o")
        self.__labels = [self.__yes_label, self.__no_label]
        super().__init__(
            self.__text_label.height + 3,
            self.__text_label.width + 4,
            "info",
        )
        self.add_ob(self.__text_label, 2, 1)
        self.add_ob(
            self.__yes_label,
            round(self.__text_label.width / 2 - 4),
            self.__text_label.height + 1,
        )
        self.add_ob(
            self.__no_label,
            round(self.__text_label.width / 2 + 4),
            self.__text_label.height + 1,
        )

    def get_interaction_areas(self) -> list[Area]:
        return [i.get_area() for i in self.__labels]

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx < 0:
            match event.type:
                case MouseEventType.MOVE:
                    for i in self.__labels:
                        i.un_highlight()
        else:
            match event.type:
                case MouseEventType.MOVE:
                    self.__labels[area_idx].highlight()
                case MouseEventType.LEFT:
                    self.__result = not area_idx

    def __call__(self, ctx: Context) -> bool:
        self.set_ctx(ctx)
        ret: bool
        with self.center_add(self.map):
            ctx = change_ctx(ctx, self)
            while True:
                action = get_action()
                if action.triggers(Action.ACCEPT):
                    ret = True
                    break
                if action.triggers(Action.CANCEL):
                    ret = False
                    break
                loops.std(ctx)
                if self.__result is not None:
                    ret = self.__result
                    break
        return ret


def ask_bool(ctx: Context, text) -> bool:
    """Asks the player to aswer a yes/no question
    ARGS:
        ctx: Context
        text: The actual question"""

    return AskBoolBox(text)(ctx)
