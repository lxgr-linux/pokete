from typing import Optional
import scrap_engine as se

from pokete.base.game_map import CompatMap

from .frame import StdFrame
from ..overview import Overview
from ...context import Context

class Box(se.Box, Overview):
    """Box to show content in
    ARGS:
        height: The boxes height
        width: The boxes width
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box"""

    def __init__(self, height, width, name="", info="",
                 overview:Optional[Overview]=None, ctx:Optional[Context]=None):
        super().__init__(height, width)
        self.map: Optional[CompatMap]
        self.overview: Optional[Overview] = overview
        if ctx:
            self.overview = ctx.overview
            self.map = ctx.map
        self.frame = StdFrame(height, width)
        self.inner = se.Square(char=" ", width=width - 2, height=height - 2,
                               state="float")
        self.name_label = se.Text(name, state="float")
        self.info_label = se.Text(info, state="float")
        # adding
        self.add_ob(self.frame, 0, 0)
        self.add_ob(self.inner, 1, 1)
        self.add_ob(self.name_label, 2, 0)
        self.add_ob(self.info_label, 2, self.height - 1)

    def resize_view(self):
        """Manages recursive view resizing"""
        if self.overview is not None:
            self.remove()
            self.overview.resize_view()
            self.center_add(self.map)
            self.map.show()

    def center_add(self, _map):
        """Adds the box to the maps center
        ARGS:
            _map: se.Map the box will be added to"""
        self.add(_map, round((_map.width - self.width) / 2),
                 round((_map.height - self.height) / 2))
        return self

    def resize(self, height, width):
        """Resizes the box to a certain size
        See se.Box.resize"""
        super().resize(height, width)
        self.inner.resize(width - 2, height - 2)
        self.frame.resize(height, width)
        self.set_ob(self.name_label, 2, 0)
        self.set_ob(self.info_label, 2, self.height - 1)

    def add(self, _map, x, y):
        """Adds the box to a map
        See se.Box.add"""
        super().add(_map, x, y)
        return self

    def set_ctx(self, ctx):
        self.map = ctx.map
        self.overview = ctx.overview
        return self

    def __enter__(self):
        """Enter dunder for context management"""
        self.map.show()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit dunder for context management"""
        self.remove()
        self.map.show()
