from types import TracebackType
from typing import Self, override

import scrap_engine as se

from ...context import Context
from ..overview import Overview
from .frame import StdFrame


class Box(se.Box, Overview):
    """Box to show content in
    ARGS:
        height: The boxes height
        width: The boxes width
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box"""

    def __init__(
        self,
        height: int,
        width: int,
        name: str = "",
        info: list[se.Text] | None = None,
        overview: Overview | None = None,
        ctx: Context | None = None,
    ) -> None:
        super().__init__(height, width)
        self.map: se.Map | None
        self.overview: Overview | None = overview
        if ctx:
            self.overview = ctx.overview
            self.map = ctx.map
        self.frame = StdFrame(height, width)
        self.inner = se.Square(
            char=" ", width=width - 2, height=height - 2, state="float"
        )
        self.name_label = se.Text(name, state="float")
        self.info_labels: list[se.Text] = []
        if info is not None:
            self.info_labels = info
        # adding
        self.add_ob(self.frame, 0, 0)
        self.add_ob(self.inner, 1, 1)
        self.add_ob(self.name_label, 2, 0)
        self.add_info_labels()

    def add_info_labels(self) -> None:
        label_length = 0
        for label in self.info_labels:
            self.add_ob(label, label_length + 2, self.height - 1)
            label_length += label.width + 1

    def resize_view(self) -> None:
        """Manages recursive view resizing"""
        if self.overview is not None:
            self.remove()
            self.overview.resize_view()
            self.center_add(self.map)
            self.map.show()

    def center_add(self, _map: se.Map) -> "Box":
        """Adds the box to the maps center
        ARGS:
            _map: se.Map the box will be added to"""
        _ = self.add(
            _map,
            round((_map.width - self.width) / 2),
            round((_map.height - self.height) / 2),
        )
        return self

    @override
    def resize(self, height: int, width: int) -> None:
        """Resizes the box to a certain size
        See se.Box.resize"""
        super().resize(height, width)
        self.inner.resize(width - 2, height - 2)
        self.frame.resize(height, width)
        self.set_ob(self.name_label, 2, 0)
        self.add_info_labels()

    def add(self, _map: se.Map, x: int, y: int) -> "Box":
        """Adds the box to a map
        See se.Box.add"""
        super().add(_map, x, y)
        return self

    def set_ctx(self, ctx: Context) -> "Box":
        self.map = ctx.map
        self.overview = ctx.overview
        return self

    def __enter__(self) -> Self:
        """Enter dunder for context management"""
        assert self.map
        self.map.show()
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """Exit dunder for context management"""
        assert self.map
        self.remove()
        self.map.show()
