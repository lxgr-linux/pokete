"""Contains everything related to Effects"""

import time
import random
import logging
import scrap_engine as se
from .color import Color


class Effect():
    """An effect that can be given to a Pokete and that effects the Pokete
    during fights
    ARGS:
        name: The effects displayed name (paralysed etc)
        rem_chance: The chance the effect gets removed
        catch_chance: The number with which the catch chance of the Poke is
            increased
        text: The text shown near the Pokes name ("(Bur)")
        str_esccode: The color of said label,
        obj: The Poke the effect is added to
        exclude: A list of type names that the effect can't be added to
    CLASS VARS:
        desc: The effects description
        c_name: The class' simplified name"""
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
        """Adds the effect to a Pokete
        ARGS:
            obj: The Poke the effect is added to"""
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
            logging.info("[Effect][%s] Added to %s", self.name, obj.name)
        else:
            obj.ico.map.outp.rechar(f'{obj.ext_name} is already ')
            obj.ico.map.outp.append(se.Text(self.name,
                                            esccode=self.str_esccode,
                                            state="float"),
                                    se.Text("!", state="float"))
        time.sleep(2)

    def add_label(self):
        """Adds the label to the fightmap"""
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
        """Readds label and shows text"""
        self.add_label()
        self.obj.ico.map.outp.outp(f'{self.obj.ext_name} is still ')
        self.obj.ico.map.outp.append(se.Text(self.name,
                                             esccode=self.str_esccode,
                                             state="float"),
                                     se.Text("!", state="float"))
        self.obj.ico.map.show()

    def remove(self):
        """Removes itself from the current pokete with a certain chance"""
        if random.randint(0, self.rem_chance) == 0:
            self.obj.ico.map.outp.outp(f'{self.obj.ext_name} isn\'t ')
            self.obj.ico.map.outp.append(se.Text(self.name,
                                                 esccode=self.str_esccode,
                                                 state="float"),
                                         se.Text(" anymore!", state="float"))
            i = self.obj.effects.index(self)
            del self.obj.effects[i]
            self.cleanup(i)
            logging.info("[Effect][%s] Removed from  %s", self.name,
                         self.obj.name)
            self.obj = None
            time.sleep(2)

    def cleanup(self, j=None):
        """Does a cleanup
        ARGS:
            j: The former index in self.obs.effects"""
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
        """The action that's executed every attack round"""
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
        """Returns a descriptive markdown string"""
        return f"""
### {cls.c_name.capitalize()}
{cls.desc}
"""


class EffectParalyzation(Effect):
    """Effect see desc"""
    desc = "Paralyses the enemy and stops it from attacking. \
This is reverted randomly."
    c_name = "paralyzation"

    def __init__(self, obj=None):
        super().__init__("paralyzed", 3, 2, "(Par)", Color.thicc + Color.yellow,
                         obj)


class EffectSleep(Effect):
    """Effect see desc"""
    desc = "Makes the enemy fall asleep and stops it from attacking. \
This is reverted randomly."
    c_name = "sleep"

    def __init__(self, obj=None):
        super().__init__("sleeping", 4, 3, "(Sle)", Color.white, obj)


class EffectBurning(Effect):
    """Effect see desc"""
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
    """Effect see desc"""
    desc = "Poisons the enemy and damages the enemy with 1 HP every round.\
 This is reverted randomly."
    c_name = "poison"

    def __init__(self, obj=None):
        super(EffectBurning, self).__init__("poisoned", 4, 2, "(Poi)",
                                            Color.purple, obj)
        self.hurt_text = "got damaged through poison!"
        self.damage = 1


class EffectConfusion(Effect):
    """Effect see desc"""
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
    """Effect see desc"""
    desc = "Freezes the enemy and stops it from attacking. \
This is reverted randomly."
    c_name = "freezing"

    def __init__(self, obj=None):
        super().__init__("frozen", 3, 3, "(Fro)", Color.cyan, obj,
                         exclude=["ice", "fire"])


effect_list = [EffectParalyzation, EffectSleep, EffectBurning, EffectPoison,
               EffectConfusion, EffectFreezing]


class Effects:
    """Contains all effects"""

    def __init__(self):
        self.effect_list = effect_list
        for i in self.effect_list:
            setattr(self, i.c_name, i)


effects = Effects()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
