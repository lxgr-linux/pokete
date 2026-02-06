from typing import Optional

import scrap_engine as se

from ...context import Context
from .box import Box


class LabelBox(Box):
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
