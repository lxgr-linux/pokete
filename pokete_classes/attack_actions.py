"""Contains the AttackActions class"""

class AttackActions:
    """This class contains all actions callable by an attack
    All these methods belong to one or more attacks and follow the following
    pattern:
        ARGS:
            obj: The Poke object that attacks
            enem: The Poke object that is attacked"""

    def cry(self, obj, enem):
        enem.miss_chance += 1

    def eye_pick(self, obj, enem):
        enem.miss_chance += 2

    def chocer(self, obj, enem):
        enem.atc -= 1

    def snooze(self, obj, enem):
        enem.miss_chance += 0.5
        enem.atc -= 1
        enem.defense -= 1

    def politure(self, obj, enem):
        obj.defense += 1
        obj.atc += 1

    def bark_hardening(self, obj, enem):
        obj.defense += 1

    def dick_energy(self, obj, enem):
        obj.atc += 2

    def hiding(self, obj, enem):
        obj.defense += 2

    def brooding(self, obj, enem):
        obj.hp += 2 if obj.hp + 2 <= obj.full_hp else 0

    def heart_touch(self, obj, enem):
        enem.defense -= 4

    def super_sucker(self, obj, enem):
        enem.hp -=2
        obj.hp +=2 if obj.hp+2 <= obj.full_hp else 0

    def sucker(self, obj, enem):
        enem.hp -= 1
        obj.hp += 1 if obj.hp+1 <= obj.full_hp else 0


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
