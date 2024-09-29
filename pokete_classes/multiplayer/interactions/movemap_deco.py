import scrap_engine as se

from ...color import Color
from ...input import Action


class MovemapDeco(se.Text):
    def __init__(self):
        super().__init__(self.__get_text())

    @staticmethod
    def __get_text():
        return f"{Action.INTERACT.mapping}: act"

    def set_active(self):
        self.rechar(self.__get_text())

    def set_inactive(self):
        self.rechar(self.__get_text(), esccode=Color.grey)
