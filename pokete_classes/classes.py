import scrap_engine as se
import time, random

class Color:
    reset = "\033[0m"
    thicc = "\033[1m"
    underlined = "\033[4m"
    grey = "\033[1;30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    lightblue = "\033[1;34m"
    blue = "\033[34m"
    purple = "\033[1;35m"
    cyan = "\033[1;36m"
    lightgrey = "\033[37m"
    white = "\033[1;37m"


class NoColor(Color):
    grey = ""
    red = ""
    green = ""
    yellow = ""
    lightblue = ""
    blue = ""
    purple = ""
    cyan = ""
    lightgrey = ""
    white = ""


class PlayMap(se.Map):
    def __init__(self, height=se.height-1, width=se.width, trainers=[], name="", pretty_name="", poke_args={}, extra_actions=None, dynfps=True):
        super().__init__(height=height, width=width, background=" ", dynfps=dynfps)
        for i in ["trainers", "name", "pretty_name", "poke_args"]:
            exec(f"self.{i}={i}")
        self.__extra_actions = extra_actions

    def extra_actions(self):
        if self.__extra_actions != None:
            self.__extra_actions()


class PokeType():
    def __init__(self, name, effective, ineffective, color):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color == None else eval(color)


class InvItem:
    def __init__(self, name, pretty_name, desc, price, fn=None):
        self.name = name
        self.pretty_name = pretty_name
        self.desc = desc
        self.price = price
        self.fn = fn


class Settings():
    def __init__(self, autosave=True, animations=True, save_trainers=True, colors=True):
        self.keywords = ["autosave", "animations", "save_trainers", "colors"]
        for key in self.keywords:
            exec(f"self.{key} = {key}")

    def dict(self):
        return {i: eval("self."+i, {"self": self,}) for i in self.keywords}


class Effect():
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


class EffectParalyzation(Effect):
    def __init__(self, ob=None):
        super().__init__("paralyzed", 3, "(Par)", Color.thicc+Color.yellow, ob)


class EffectSleep(Effect):
    def __init__(self, ob=None):
        super().__init__("sleeping", 4, "(Sle)", Color.white, ob)


class EffectBurning(Effect):
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
    def __init__(self, ob=None):
        super(EffectBurning, self).__init__("poisoned", 4, "(Poi)", Color.purple, ob)
        self.hurt_text = "got damaged through poison!"
        self.damage = 1


class EffectConfusion(Effect):
    def __init__(self, ob=None):
        super().__init__("confused", 3, "(Con)", Color.lightblue, ob)

    def effect(self):
        self.ob.ico.map.outp.outp(f'{self.ob.name}({"you" if self.ob.player else "enemy"}) is still ')
        self.ob.ico.map.outp.append(se.Text(self.name, esccode=self.str_esccode, state="float"), se.Text("!", state="float"))
        time.sleep(0.5)
        return 0


class OutP(se.Text):
    def outp(self, text):
        self.rechar(text)
        self.map.show()

    def append(self, *args):
        for i in args:
            self += i
        self.map.show()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
