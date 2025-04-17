import scrap_engine as se

from pokete.base.color import Color
from pokete.base.input import Action


class MovemapDeco(se.Text):
    def __init__(self):
        self.blank = False
        super().__init__(self.__get_text())

    def __get_text(self):
        if self.blank:
            return ""
        return f"{Action.INTERACT.mapping}: act"

    def set_active(self):
        self.rechar(self.__get_text())

    def set_inactive(self):
        self.rechar(self.__get_text(), esccode=Color.lightgrey)

    def set_blank(self):
        self.blank = True
        self.rechar("")


movemap_deco = MovemapDeco()
