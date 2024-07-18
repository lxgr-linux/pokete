"""Contains everything related to the resizescreen"""

import os
import scrap_engine as se

from .game_map import GameMap
from .ui.elements import StdFrame


class ResizeScreen:
    """Screen thats shown when the screen is resized"""

    def __init__(self):
        self.height = 0
        self.width = 0
        self.__set_dimensions()
        self.map = GameMap(self.height - 1, self.width)
        self.warning_label = se.Text("Minimum windowsize is 70x20")
        self.size_label = se.Text(f"{self.width}x{self.height}")
        self.frame = StdFrame(self.height - 1, self.width)
        self.warning_label.add(self.map, int(self.width / 2) - 13,
                               int(self.height / 2) - 1)
        self.size_label.add(self.map, 1, 0)
        self.frame.add(self.map, 0, 0)

    def __set_dimensions(self):
        width, height = os.get_terminal_size()
        change = self.width != width or self.height != height
        self.height = height
        self.width = width
        return change

    def __check(self):
        return self.width < 70 or self.height < 20

    def __call__(self):
        """Shows the map"""
        change = self.__set_dimensions()
        while self.__check():
            self.__set_dimensions()
            self.warning_label.set(1, 1)
            self.frame.remove()
            self.map.resize(self.height - 1, self.width, " ")
            self.warning_label.set(int(self.width / 2) - 13,
                                   int((self.height - 1) / 2) - 1)
            self.size_label.rechar(f"{self.width}x{self.height}")
            self.frame.resize(self.height - 1, self.width)
            self.frame.add(self.map, 0, 0)
            self.map.show(init=True)
        return change


tss = ResizeScreen()
