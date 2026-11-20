import scrap_engine as se

from pokete.classes.attack import Attack


class AttackDescs:
    def __init__(self, attacks: list[Attack], width: int) -> None:
        self.__attacks = attacks
        self.__width = width
        self.labels: list[se.Text[se.Object]] = [
            se.Text(atc.desc[: int(width / 2 - 1)]) for atc in attacks
        ]
        self.__offsets: list[int] = [0 for _ in attacks]
        self.__tics: list[int] = [0 for _ in attacks]

    def resize(self, width: int):
        self.__width = width
        for atc, label in zip(self.__attacks, self.labels):
            label.rechar(atc.desc[: int(width / 2 - 1)])

    def inc(self):
        for idx, (atc, label) in enumerate(zip(self.__attacks, self.labels)):
            if len(atc.desc) > int((self.__width - 3) / 2 - 1):
                if self.__tics[idx] == 5:
                    self.__offsets[idx] += 1
                    self.__tics[idx] = 0
                    if (
                        self.__offsets[idx]
                        == len(atc.desc) - int(self.__width / 2 - 1) + 10
                    ):
                        self.__offsets[idx] = 0
                        self.__tics[idx] = -30  # Wait after turnover
                    label.rechar(
                        atc.desc[
                            self.__offsets[idx] : int(self.__width / 2 - 1)
                            + self.__offsets[idx]
                        ]
                    )
                else:
                    self.__tics[idx] += 1
