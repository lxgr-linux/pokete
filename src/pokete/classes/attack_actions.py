"""Contains the AttackActions class"""

import time

from pokete.classes.poke.poke.poke import Poke

from .weather import Weather


class AttackActions:
    """This class contains all actions callable by an attack
    All these methods belong to one or more attacks and follow the following
    pattern:
        ARGS:
            obj: The Poke object that attacks
            enem: The Poke object that is attacked
            providers: List of the current providers"""

    @staticmethod
    def cry(obj: Poke, enem: Poke, providers: list) -> None:
        """Cry attack action"""
        enem.miss_chance += 1

    @staticmethod
    def eye_pick(obj: Poke, enem: Poke, providers: list) -> None:
        """Eye pick attack action"""
        enem.miss_chance += 2

    @staticmethod
    def chocer(obj: Poke, enem: Poke, providers: list) -> None:
        """Chocer attack action"""
        enem.atc -= 1

    @staticmethod
    def snooze(obj: Poke, enem: Poke, providers: list) -> None:
        """Snooze attack action"""
        enem.miss_chance += 0.5
        enem.atc -= 1
        enem.defense -= 1

    @staticmethod
    def politure(obj: Poke, enem: Poke, providers: list) -> None:
        """Politure attack action"""
        obj.defense += 1
        obj.atc += 1

    @staticmethod
    def bark_hardening(obj: Poke, enem: Poke, providers: list) -> None:
        """Bark hardening attack action"""
        obj.defense += 1

    @staticmethod
    def dick_energy(obj: Poke, enem: Poke, providers: list) -> None:
        """Dick energy attack action"""
        obj.atc += 2

    @staticmethod
    def hiding(obj: Poke, enem: Poke, providers: list) -> None:
        """Hiding attack action"""
        obj.defense += 2

    @staticmethod
    def brooding(obj: Poke, enem: Poke, providers: list) -> None:
        """Brooding attack action"""
        obj.hp += 2 if obj.hp + 2 <= obj.full_hp else 0

    @staticmethod
    def heart_touch(obj: Poke, enem: Poke, providers: list) -> None:
        """Heart touch attack action"""
        enem.defense -= 4

    @staticmethod
    def super_sucker(obj: Poke, enem: Poke, providers: list) -> None:
        """Super sucker attack action"""
        enem.hp -= 2
        obj.hp += 2 if obj.hp + 2 <= obj.full_hp else 0

    @staticmethod
    def sucker(obj: Poke, enem: Poke, providers: list) -> None:
        """Sucker attack action"""
        enem.hp -= 1
        obj.hp += 1 if obj.hp + 1 <= obj.full_hp else 0

    @staticmethod
    def rain_dance(obj: Poke, enem: Poke, providers: list) -> None:
        """Rain dance attack action"""
        providers[0].map.weather = Weather("rain")
        obj.ico.map.outp.outp("It started raining!")
        time.sleep(2)

    @staticmethod
    def encouragement(obj: Poke, enem: Poke, providers: list) -> None:
        """Encouragement attack action"""
        for poke in next(prov for prov in providers if prov.curr == obj).pokes[:6]:
            poke.atc += 2


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
