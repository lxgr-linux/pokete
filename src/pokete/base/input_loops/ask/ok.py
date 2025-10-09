import scrap_engine as se
from scrap_engine.addable.area import Area

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input import Action, _ev, get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements.box import Box
from pokete.base.ui.elements.text import HightlightableText


class AskOkBox(Box, MouseInteractor):
    def __init__(self, text: str):
        assert len(text) >= 4, "Text has to be longer then 4 characters!"
        self.__do_exit = False
        self.__text_label = se.Text(text)
        self.__ok_label = HightlightableText("[O]k")
        super().__init__(
            self.__text_label.height + 3,
            self.__text_label.width + 4,
            "info",
        )
        self.add_ob(self.__text_label, 2, 1)
        self.add_ob(
            self.__ok_label,
            round(self.__text_label.width / 2),
            self.__text_label.height + 1,
        )

    def get_interaction_areas(self) -> list[Area]:
        return [self.__ok_label.get_area()]

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx == 0:
            match event.type:
                case MouseEventType.MOVE:
                    self.__ok_label.highlight()
                case MouseEventType.LEFT:
                    self.__do_exit = True
        else:
            match event.type:
                case MouseEventType.MOVE:
                    self.__ok_label.un_highlight()

    def __call__(self, ctx: Context):
        self.set_ctx(ctx)
        with self.center_add(self.map):
            ctx = change_ctx(ctx, self)
            while True:
                action = get_action()
                if action.triggers(Action.ACCEPT or action == Action.CANCEL):
                    break
                loops.std(ctx)
                if self.__do_exit:
                    break
            _ev.clear()


def ask_ok(ctx: Context, text):
    """Shows the player some information
    ARGS:
        ctx:Context
        text: The question it self"""

    AskOkBox(text)(ctx)
