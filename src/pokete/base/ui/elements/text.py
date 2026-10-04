import scrap_engine as se
from scrap_engine.addable.object import ArgProto

from pokete.base.color import Color


class HightlightableText(se.Text):
    def __init__(
        self,
        text: str,
        state: se.State = "float",
        esccode: str = "",
        ob_class: type[se.Object] = se.Object,
        ob_args: ArgProto = None,
        ignore: str = "",
    ):
        self.default_esccode = esccode
        super().__init__(text, state, esccode, ob_class, ob_args, ignore)

    def highlight(self):
        self.rechar(self.text, Color.thicc + self.default_esccode)

    def un_highlight(self):
        self.rechar(self.text, self.default_esccode)
