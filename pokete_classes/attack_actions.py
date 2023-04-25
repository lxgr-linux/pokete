"""Contains the AttackActions class"""

import time
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
    def cry(_, enem, __):
        """Cry attack action"""
        enem.miss_chance += 1

    @staticmethod
    def eye_pick(_, enem, __):
        """Eye pick attack action"""
        enem.miss_chance += 2

    @staticmethod
    def chocer(_, enem, __):
        """Chocer attack action"""
        enem.atc -= 1

    @staticmethod
    def snooze(_, enem, __):
        """Snooze attack action"""
        enem.miss_chance += 0.5
        enem.atc -= 1
        enem.defense -= 1

    @staticmethod
    def politure(obj, _, __):
        """Politure attack action"""
        obj.defense += 1
        obj.atc += 1

    @staticmethod
    def bark_hardening(obj, _, __):
        """Bark hardening attack action"""
        obj.defense += 1

    @staticmethod
    def dick_energy(obj, _, __):
        """Dick energy attack action"""
        obj.atc += 2

    @staticmethod
    def hiding(obj, _, __):
        """Hiding attack action"""
        obj.defense += 2

    @staticmethod
    def brooding(obj, _, __):
        """Brooding attack action"""
        obj.hp += 2 if obj.hp + 2 <= obj.full_hp else 0

    @staticmethod
    def heart_touch(_, enem, __):
        """Heart touch attack action"""
        enem.defense -= 4

    @staticmethod
    def super_sucker(obj, enem, _):
        """Super sucker attack action"""
        enem.hp -= 2
        obj.hp += 2 if obj.hp+2 <= obj.full_hp else 0

    @staticmethod
    def sucker(obj, enem, __):
        """Sucker attack action"""
        enem.hp -= 1
        obj.hp += 1 if obj.hp+1 <= obj.full_hp else 0

    @staticmethod
    def rain_dance(obj, _, providers):
        """Rain dance attack action"""
        providers[0].map.weather = Weather("rain")
        obj.ico.map.outp.outp("It started raining!")
        time.sleep(2)

    @staticmethod
    def encouragement(obj, _, providers):
        """Encouragement attack action"""
        for poke in next(
            prov for prov in providers if prov.curr == obj
        ).pokes[:6]:
            poke.atc += 2


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
