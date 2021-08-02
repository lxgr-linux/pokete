import scrap_engine as se
from pokete_classes.classes import *

class Effect():
    desc = ""
    c_name = ""
    def __init__(self, name, rem_chance, str, str_esccode="", ob=None):
        self.name = name
        self.rem_chance = rem_chance
        self.str_esccode = str_esccode
        self.label = se.Text(str, state="float", esccode=str_esccode)
        self.ob = ob

    def __repr__(self):
        return f"{type(self).__name__}"

    def add(self, ob):
        if all(type(i) is not type(self) for i in ob.effects):
            self.ob = ob
            self.ob.effects.append(self)
            self.add_label()
            self.ob.ico.map.outp.rechar(f'{ob.name}({"you" if ob.player else "enemy"}) is now ')
            self.ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text("!", state="float"))
        else:
            ob.ico.map.outp.rechar(f'{ob.name}({"you" if ob.player else "enemy"}) is allready ')
            ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text("!", state="float"))
        time.sleep(2)

    def add_label(self):
        try:
            self.label.add(self.ob.ico.map, (self.ob.text_lvl.obs[-1].x if self.ob.effects.index(self) == 0 else self.ob.effects[self.ob.effects.index(self)-1].label.obs[-1].x)+2, self.ob.text_lvl.obs[-1].y)
        except se.CoordinateError:
            pass

    def readd(self):
        self.add_label()
        self.ob.ico.map.outp.outp(f'{self.ob.name}({"you" if self.ob.player else "enemy"}) is still ')
        self.ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text("!", state="float"))
        self.ob.ico.map.show()

    def remove(self):
        if random.randint(0, self.rem_chance) == 0:
            self.ob.ico.map.outp.outp(f'{self.ob.name}({"you" if self.ob.player else "enemy"}) isn\'t ')
            self.ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text(" anymore!", state="float"))
            i = self.ob.effects.index(self)
            del self.ob.effects[i]
            self.cleanup(i)
            self.ob = None
            time.sleep(2)

    def cleanup(self, j=None):
        if j == None:
            j = self.ob.effects.index(self)
        else:
            j -= 1
        self.label.remove()
        if len(self.ob.effects) > j+1:
            i = self.ob.effects[j+1]
            i.cleanup()
            i.add_label()

    def effect(self):
        self.ob.ico.map.outp.outp(f'{self.ob.name}({"you" if self.ob.player else "enemy"}) is still ')
        self.ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text(" and can\'t attack!", state="float"))
        time.sleep(0.5)
        return 1

    @classmethod
    def ret_md(cls):
        return f"""
### {cls.c_name.capitalize()}
{cls.desc}
"""


class EffectParalyzation(Effect):
    desc = "Paralyses the enemy and stops it from attacking. This is reverted randomly."
    c_name = "paralyzation"
    def __init__(self, ob=None):
        super().__init__("paralyzed", 3, "(Par)", Color.thicc+Color.yellow, ob)


class EffectSleep(Effect):
    desc = "Makes the enemy fall asleep and stops it from attacking. This is reverted randomly."
    c_name = "sleep"
    def __init__(self, ob=None):
        super().__init__("sleeping", 4, "(Sle)", Color.white, ob)


class EffectBurning(Effect):
    desc = "Sets the enemy on fire and damages the enemy with 2 HP every round. This is reverted randomly."
    c_name = "burning"
    def __init__(self, ob=None):
        super().__init__("burning", 3, "(Bur)", Color.thicc+Color.red, ob)
        self.hurt_text = "burned it self!"
        self.damage = 2

    def effect(self):
        self.ob.ico.map.outp.outp(f'{self.ob.name}({"you" if self.ob.player else "enemy"}) is still ')
        self.ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text("!", state="float"))
        self.ob.ico.map.show()
        time.sleep(1)
        for i in range(random.randint(1, 4)):
            oldhp = self.ob.hp
            if self.ob.hp - self.damage <= 0:
                self.ob.hp = 0
            else:
                self.ob.hp -= self.damage
            self.ob.health_bar_updater(oldhp)
            self.ob.ico.map.outp.outp(f'{self.ob.name}({"you" if self.ob.player else "enemy"}) {self.hurt_text}')
            time.sleep(0.5)
        return 0


class EffectPoison(EffectBurning):
    desc = "Poisons the enemy and damages the enemy with 1 HP every round. This is reverted randomly."
    c_name = "poison"
    def __init__(self, ob=None):
        super(EffectBurning, self).__init__("poisoned", 4, "(Poi)", Color.purple, ob)
        self.hurt_text = "got damaged through poison!"
        self.damage = 1


class EffectConfusion(Effect):
    desc = "Makes the enemy hurt it self. This is reverted randomly."
    c_name = "confusion"
    def __init__(self, ob=None):
        super().__init__("confused", 3, "(Con)", Color.lightblue, ob)

    def effect(self):
        self.ob.ico.map.outp.outp(f'{self.ob.name}({"you" if self.ob.player else "enemy"}) is still ')
        self.ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text("!", state="float"))
        time.sleep(0.5)
        return 0


class EffectFreezing(Effect):
    desc = "Freezes the enemy and stops it from attacking. This is reverted randomly."
    c_name = "freezing"
    def __init__(self, ob=None):
        super().__init__("frozen", 3, "(Fro)", Color.cyan, ob)


effects = [EffectParalyzation, EffectSleep, EffectBurning, EffectPoison, EffectConfusion, EffectFreezing]


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
