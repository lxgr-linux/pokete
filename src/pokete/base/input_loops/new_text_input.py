from typing import Optional, override

import scrap_engine as se

from pokete.base import loops
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.input import key
from pokete.base.input.hotkeys import get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse.interactor import MouseInteractor
from pokete.util.liner import hard_liner


class TextInput(MouseInteractor):
    def __init__(
        self,
        label: se.Text,
        wrap_len: int,
        max_len: int = -1,
    ) -> None:
        self.__label = label
        self.__idx = 0
        self.wrap_len = wrap_len
        self.__text = ""
        self.max_len = max_len
        super().__init__()

    @override
    def get_interaction_areas(self) -> list[se.Area]:
        return [i.get_area() for i in self.__label.obs]

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        if area_idx >= 0:
            if event.type == MouseEventType.LEFT:
                self.__change_idx(area_idx - self.__idx)

    def __change_idx(self, amount: int):
        self.__idx = min(max(0, self.__idx + amount), len(self.__text))

    def __rechar_text(self):
        self.__label.rechar(hard_liner(self.wrap_len, self.__text + " "))
        pointer = self.__label.obs[self.__idx]
        pointer.rechar(Color.bg_cyan + pointer.char + Color.reset)

    def __call__(self, ctx: Context) -> Optional[str]:
        self.__text = self.__label.text
        fallback_text = self.__text
        self.__idx = len(self.__text)
        self.__rechar_text()
        safed_idx = self.__idx

        while True:
            if safed_idx != self.__idx:
                self.__rechar_text()
                safed_idx = self.__idx
            _, input_key = get_action()
            if input_key is not None:
                if input_key == key.ESC:
                    self.__label.rechar(fallback_text)
                    return None
                if input_key == key.ENTER:
                    break
                if input_key == key.LEFT:
                    self.__change_idx(-1)
                elif input_key == key.RIGHT:
                    self.__change_idx(1)
                elif input_key == key.BACKSPACE:
                    self.__change_idx(-1)
                    self.__text = (
                        self.__text[: self.__idx]
                        + self.__text[self.__idx + 1 :]
                    )
                elif input_key.has_char():
                    if self.max_len < 0 or len(self.__text) < self.max_len:
                        self.__text = (
                            self.__text[: self.__idx]
                            + input_key.char
                            + self.__text[self.__idx :]
                        )
                        self.__change_idx(1)
                self.__rechar_text()
            loops.std(ctx)
        self.__label.rechar(hard_liner(self.wrap_len, self.__text))
        return self.__text
