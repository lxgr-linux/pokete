import time
import random
import scrap_engine as se
from .color import Color


class Effect():
    desc = ""
    c_name = ""

    def __init__(self, name, rem_chance, catch_chance, text, str_esccode="",
                 obj=None, exclude=None):
        self.name = name
        self.rem_chance = rem_chance
        self.catch_chance = catch_chance
        self.str_esccode = str_esccode
        if exclude is not None:
            self.exclude = exclude
        else:
            self.exclude = []
        self.label = se.Text(text, state="float", esccode=str_esccode)
        self.obj = obj

    def __repr__(self):
        return f"{type(self).__name__}"

    def add(self, obj):
        if obj.type.name in self.exclude:
            obj.ico.map.outp.rechar(f'{obj.ext_name} is not affected by ')
            obj.ico.map.outp.append(se.Text(self.name,
                                            esccode=self.str_esccode,
                                            state="float"),
                                    se.Text("!", state="float"))
        elif all(type(i) is not type(self) for i in obj.effects):
            self.obj = obj
            self.obj.effects.append(self)
            self.add_label()
            self.obj.ico.map.outp.rechar(f'{obj.ext_name} is now ')
            self.obj.ico.map.outp.append(se.Text(self.name,
                                                 esccode=self.str_esccode,
                                                 state="float"),
                                         se.Text("!", state="float"))
        else:
            obj.ico.map.outp.rechar(f'{obj.ext_name} is allready ')
            obj.ico.map.outp.append(se.Text(self.name,
                                            esccode=self.str_esccode,
                                            state="float"),
                                    se.Text("!", state="float"))
        time.sleep(2)

    def add_label(self):
        try:
            self.label.add(self.obj.ico.map,
                           (self.obj.text_lvl.obs[-1].x
                            if self.obj.effects.index(self) == 0
                            else self.obj.effects[self.obj.effects
                                                  .index(self) - 1]
                                .label.obs[-1].x) + 2,
                           self.obj.text_lvl.obs[-1].y)
        except se.CoordinateError:
            pass

    def readd(self):
        self.add_label()
        self.obj.ico.map.outp.outp(f'{self.obj.ext_name} is still ')
        self.obj.ico.map.outp.append(se.Text(self.name,
                                             esccode=self.str_esccode,
                                             state="float"),
                                     se.Text("!", state="float"))
        self.obj.ico.map.show()

    def remove(self):
        if random.randint(0, self.rem_chance) == 0:
            self.obj.ico.map.outp.outp(f'{self.obj.ext_name} isn\'t ')
            self.obj.ico.map.outp.append(se.Text(self.name,
                                                 esccode=self.str_esccode,
                                                 state="float"),
                                         se.Text(" anymore!", state="float"))
            i = self.obj.effects.index(self)
            del self.obj.effects[i]
            self.cleanup(i)
            self.obj = None
            time.sleep(2)

    def cleanup(self, j=None):
        if j is None:
            j = self.obj.effects.index(self)
        else:
            j -= 1
        self.label.remove()
        if len(self.obj.effects) > j + 1:
            i = self.obj.effects[j + 1]
            i.cleanup()
            i.add_label()

    def effect(self):
        self.obj.ico.map.outp.outp(f'{self.obj.ext_name} is still ')
        self.obj.ico.map.outp.append(se.Text(self.name,
                                             esccode=self.str_esccode,
                                             state="float"),
                                     se.Text(" and can\'t attack!",
                                             state="float"))
        time.sleep(0.5)
        return 1

    @classmethod
    def ret_md(cls):
        return f"""
### {cls.c_name.capitalize()}
{cls.desc}
"""


class EffectParalyzation(Effect):
    desc = "Paralyses the enemy and stops it from attacking. \
This is reverted randomly."
    c_name = "paralyzation"

    def __init__(self, obj=None):
        super().__init__("paralyzed", 3, 2, "(Par)", Color.thicc + Color.yellow,
                         obj)


class EffectSleep(Effect):
    desc = "Makes the enemy fall asleep and stops it from attacking. \
This is reverted randomly."
    c_name = "sleep"

    def __init__(self, obj=None):
        super().__init__("sleeping", 4, 3, "(Sle)", Color.white, obj)


class EffectBurning(Effect):
    desc = "Sets the enemy on fire and damages them with 2 HP every round. \
This is reverted randomly."
    c_name = "burning"

    def __init__(self, obj=None):
        super().__init__("burning", 3, 0, "(Bur)", Color.thicc + Color.red, obj,
                         exclude=["fire", "water"])
        self.hurt_text = "burned it self!"
        self.damage = 2

    def effect(self):
        self.obj.ico.map.outp.outp(f'{self.obj.ext_name} is still ')
        self.obj.ico.map.outp.append(se.Text(self.name,
                                             esccode=self.str_esccode,
                                             state="float"),
                                     se.Text("!", state="float"))
        self.obj.ico.map.show()
        time.sleep(1)
        for _ in range(random.randint(1, 3)):
            oldhp = self.obj.hp
            self.obj.hp = max(self.obj.hp - self.damage, 0)
            self.obj.hp_bar.update(oldhp)
            self.obj.ico.map.outp.outp(f'{self.obj.ext_name} {self.hurt_text}')
            time.sleep(0.5)
        return 0


class EffectPoison(EffectBurning):
    desc = "Poisons the enemy and damages the enemy with 1 HP every round.\
 This is reverted randomly."
    c_name = "poison"

    def __init__(self, obj=None):
        super(EffectBurning, self).__init__("poisoned", 4, 2, "(Poi)",
                                            Color.purple, obj)
        self.hurt_text = "got damaged through poison!"
        self.damage = 1


class EffectConfusion(Effect):
    desc = "Makes the enemy hurt it self. This is reverted randomly."
    c_name = "confusion"

    def __init__(self, obj=None):
        super().__init__("confused", 3, 2, "(Con)", Color.lightblue, obj,
                         exclude=["undead"])

    def effect(self):
        self.obj.ico.map.outp.outp(f'{self.obj.ext_name} is still ')
        self.obj.ico.map.outp.append(se.Text(self.name,
                                             esccode=self.str_esccode,
                                             state="float"),
                                     se.Text("!", state="float"))
        time.sleep(0.5)
        return 0


class EffectFreezing(Effect):
    desc = "Freezes the enemy and stops it from attacking. \
This is reverted randomly."
    c_name = "freezing"

    def __init__(self, obj=None):
        super().__init__("frozen", 3, 3, "(Fro)", Color.cyan, obj,
                         exclude=["ice", "fire"])


effect_list = [EffectParalyzation, EffectSleep, EffectBurning, EffectPoison,
               EffectConfusion, EffectFreezing]


class Effects:
    def __init__(self):
        for i in effect_list:
            setattr(self, i.c_name, i)


effects = Effects()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
