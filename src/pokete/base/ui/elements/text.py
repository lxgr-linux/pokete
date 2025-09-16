from typing import Type

import scrap_engine as se

from pokete.base.color import Color


class HightlightableText(se.Text):
    def __init__(
        self,
        text,
        state: se.State = se.DEFAULT_STATE,
        esccode="",
        ob_class: Type[se.Object] = se.Object,
        ob_args=None,
        ignore="",
    ):
        self.default_esccode = esccode
        super().__init__(text, state, esccode, ob_class, ob_args, ignore)

    def highlight(self):
        self.rechar(self.text, Color.thicc + self.default_esccode)

    def un_highlight(self):
        self.rechar(self.text, self.default_esccode)
