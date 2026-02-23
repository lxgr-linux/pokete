from typing import Optional, override

import scrap_engine as se

from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input_loops.new_text_input import TextInput
from pokete.base.mouse.interactor import MouseInteractor
from pokete.base.ui.elements.labels import CloseLabel
from pokete.base.ui.views.box import BoxView


class LabelBoxView(BoxView):
    """A Box just containing one label
    ARGS:
        label: The se.Text label
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box"""

    def __init__(
        self,
        label: se.Text,
        name="",
        info: Optional[list[se.Text]] = None,
        ctx: Optional[Context] = None,
    ):
        self.label: se.Text = label
        super().__init__(label.height + 2, label.width + 4, name, info, ctx=ctx)
        self.add_ob(label, 2, 1)

    def resize(self, height, width):
        super().resize(height, width)
        self.set_ob(self.label, 2, 1)


class InfoBoxView(LabelBoxView):
    """Box to display basic text information in
    ARGS:
        text: String displayed
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box"""

    def __init__(
        self,
        text,
        name="",
        info: Optional[list[se.Text]] = [CloseLabel()],
        ctx=None,
    ):
        super().__init__(se.Text(text), name=name, info=info, ctx=ctx)

    def __enter__(self):  # Contextmanagement is fucking awesome!
        """Enter dunder for contextmanagement"""
        self.center_add(self.map)
        self.map.show()
        return self


class InputBoxView(InfoBoxView):
    """Box that promps the user to input a text
    ARGS:
        infotext: The information text about the input
        introtext: The text that introduces the text field
        text: The default text in the text field
        name: The boxes desplayed name
        max_len: Max length of the text"""

    def __init__(self, infotext, introtext, text, max_len, name=""):
        height = len(infotext.split("\n")) + 3
        width = (
            sorted(
                [len(i) for i in infotext.split("\n")]
                + [len(introtext) + 1 + max_len]
            )[-1]
            + 4
        )
        super(LabelBoxView, self).__init__(height, width, name)
        self.infotext = se.Text(infotext)
        self.introtext = se.Text(introtext)
        self.text = se.Text(text)
        self.add_ob(self.infotext, 2, 1)
        self.add_ob(self.introtext, 2, len(infotext.split("\n")) + 1)
        self.add_ob(
            self.text, self.introtext.rx + len(introtext) + 1, self.introtext.ry
        )
        self.__input = TextInput(
            self.text,
            wrap_len=max_len,
        )

    @override
    def get_partial_interactors(self) -> list[MouseInteractor]:
        return super().get_partial_interactors() + [self.__input]

    def __call__(self, ctx: Context):
        self.set_ctx(ctx)
        with self:
            ctx = change_ctx(ctx, self)
            return self.__input(ctx)
