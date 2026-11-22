"""Contains everything related to the resizescreen"""

import os
from types import TracebackType
from typing import Self

import scrap_engine as se

from .game_map import GameMap
from .ui.elements import StdFrame


class ResizeScreen:
    """Screen thats shown when the screen is resized"""

    def __init__(self) -> None:
        self.height = 0
        self.width = 0
        self.__do_check: bool = True
        _ = self.__set_dimensions()
        self.map = GameMap(self.height - 1, self.width)
        self.warning_label = se.Text("Minimum windowsize is 70x20")
        self.size_label = se.Text(f"{self.width}x{self.height}")
        self.frame = StdFrame(self.height - 1, self.width)
        self.warning_label.add(
            self.map, int(self.width / 2) - 13, int(self.height / 2) - 1
        )
        self.size_label.add(self.map, 1, 0)
        self.frame.add(self.map, 0, 0)

    def set_fixed_size(self, height: int, width: int):
        self.height = height
        self.width = width
        self.__do_check = False

    def __set_dimensions(self) -> bool:
        if not self.__do_check:
            return False
        width, height = os.get_terminal_size()
        change = self.width != width or self.height != height
        self.height = height
        self.width = width
        return change

    def __check(self) -> bool:
        return self.width < 70 or self.height < 20

    def __call__(self) -> bool:
        """Shows the map"""
        change = self.__set_dimensions()
        while self.__check():
            self.__set_dimensions()
            self.warning_label.set(1, 1)
            self.frame.remove()
            self.map.resize(self.height - 1, self.width, " ")
            self.warning_label.set(
                int(self.width / 2) - 13, int((self.height - 1) / 2) - 1
            )
            self.size_label.rechar(f"{self.width}x{self.height}")
            self.frame.resize(self.height - 1, self.width)
            self.frame.add(self.map, 0, 0)
            self.map.show(init=True)
        return change


tss = ResizeScreen()


class FixedScreenSizeContext:
    def __init__(self, height: int, width: int) -> None:
        self.__height = height
        self.__width = width

    def __enter__(self) -> Self:
        tss.set_fixed_size(self.__height, self.__width)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass
