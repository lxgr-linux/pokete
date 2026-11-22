"""Contains the Healthbar class"""

import time
from typing import override

import scrap_engine as se

from pokete.base.color import Color
from pokete.classes.i import IHealthbar, IPoke
from pokete.release import SPEED_OF_TIME


class HealthBar(se.Text[se.Object]):
    """Healthbar class
    ARGS:
        poke: The Poke the healthbar belongs to"""

    def __init__(self, poke: IPoke) -> None:
        self.poke = poke
        super().__init__(8 * "#", esccode=Color.green, state="float")

    def make(self, oldhp: int) -> None:
        """Creates the healthbar
        ARGS:
            oldhp: The hp the bar should be made for"""
        bar_num = round(oldhp * 8 / self.poke.full_hp)
        esccode = Color.red
        for size, color in zip([6, 2], [Color.green, Color.yellow]):
            if bar_num > size:
                esccode = color
                break
        self.rechar(bar_num * "#", esccode)


class HealthBarWrapper(se.Box, IHealthbar):
    def __init__(self, poke: IPoke) -> None:
        self.__hp_bar = HealthBar(poke)
        self.__pre = se.Text("<", "float")
        self.__post = se.Text(">", "float")
        self.__text_hp = se.Text(f"HP:{poke.hp}", "float")
        super().__init__(1, self.__hp_bar.width + 2)
        self.add_ob(self.__text_hp, 0, 0)
        self.add_ob(self.__pre, 6, 0)
        self.add_ob(self.__hp_bar, 7, 0)
        self.add_ob(self.__post, self.__hp_bar.width + 7, 0)

    @override
    def update(self, oldhp: int, hp: int) -> None:
        """Updates the healthbar in steps with easing effect
        ARGS:
            oldhp: The pokes former hp"""
        diff = abs(oldhp - hp)
        step = 0
        while oldhp != hp and oldhp > 0:
            oldhp += -1 if oldhp > hp else 1
            step += 1
            self.__text_hp.rechar(f"HP:{oldhp}", esccode=Color.yellow)
            self.make(oldhp)
            # Easing: starts fast, slows down towards end
            progress = step / max(diff, 1)
            delay = 0.03 + (0.12 * progress * progress)
            time.sleep(SPEED_OF_TIME * delay)
            self.map.show()
        self.__text_hp.rechar(f"HP:{oldhp}")
        time.sleep(SPEED_OF_TIME * 0.1)

    @override
    def make(self, hp: int) -> None:
        self.__text_hp.rechar(f"HP:{hp}")
        self.__hp_bar.make(hp)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
