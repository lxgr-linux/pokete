#!/usr/bin/env python3
# This software is licensed under the GPL3
# You should have gotten an copy of the GPL3 license anlonside this software
# Feel free to contribute what ever you want to this game
# New Pokete contributions are especially welcome
# For this see the comments in the definations area
# You can contribute here: https://github.com/lxgr-linux/pokete

import random, time, os, sys, threading, math, socket
import scrap_engine as se
from pathlib import Path
from pokete_data import *
from pokete_classes import *

# Class definition
##################

class HightGrass(se.Object):
    def action(self, ob):
        if random.randint(0,8) == 0:
            fight(Poke("__fallback__", 0) if len([poke for poke in figure.pokes[:6] if poke.hp > 0]) == 0 else [poke for poke in figure.pokes[:6] if poke.hp > 0][0], Poke(random.choices(self.arg_proto["pokes"], weights=[pokes[i]["rarity"] for i in self.arg_proto["pokes"]])[0], random.choices(list(range(self.arg_proto["minlvl"], self.arg_proto["maxlvl"])))[0], player=False))


class Poketeball(se.Object):
    def __init__(self, name):
        self.name = name
        super().__init__(Color.thicc+Color.red+"o"+Color.reset, state="float")

    def action(self, ob):
        figure.give_item("poketeball")
        used_npcs.append(self.name)
        self.remove()

# The following two classes (PC and Heal) where initially needed to manage healing
# and reviewing off all Poketes in the deck
# They are now obsolete (because of the Pokete-Center) and will be removed later,
# but I will keep them for now for testing purposes

class NPCTrigger(se.Object):
    def __init__(self, npc):
        super().__init__(" ", state="float")
        self.npc = npc

    def action(self, ob):
        self.npc.action()


class NPC(se.Box):
    def __init__(self, name, texts, fn=None, args=()):
        super().__init__(0, 0)
        self.will = True
        self.name = name
        self.texts = texts
        self.__fn = fn
        self.args = args
        for i, j in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
            self.add_ob(NPCTrigger(self), i, j)
        self.add_ob(se.Object("a"), 0, 0)

    def action(self):
        if not self.will or (self.name in used_npcs and settings.save_trainers):
            return
        movemap.full_show()
        time.sleep(0.7)
        exclamation.add(movemap, self.x-movemap.x, self.y-1-movemap.y)
        movemap.show()
        time.sleep(1)
        exclamation.remove()
        movemap_text(self.x, self.y, self.texts)
        self.fn()

    def fn(self):
        if self.__fn != None:
            eval(self.__fn)(*self.args)


class Trainer(se.Object):
    def __init__(self, name, gender, poke, texts, lose_texts, no_poke_texts, win_texts, sx, sy, state="solid", arg_proto={}):
        self.char = "a"
        self.added = False
        for i in ["state", "arg_proto", "name", "gender", "poke", "texts", "lose_texts", "no_poke_texts", "win_texts", "sx", "sy"]:
            exec("self."+i+" = "+i)

    def do(self, map):
        if figure.has_item("shut_the_fuck_up_stone"):
            return
        if figure.x == self.x and self.poke.hp > 0 and (self.name not in used_npcs or not settings.save_trainers):
            for i in range(figure.y+1 if figure.y < self.y else self.y+1, self.y if figure.y < self.y else figure.y):
                if any(j.state == "solid" for j in map.obmap[i][self.x]):
                    return
            movemap.full_show()
            time.sleep(0.7)
            exclamation.add(movemap, self.x-movemap.x, self.y-1-movemap.y)
            movemap.show()
            time.sleep(1)
            exclamation.remove()
            while self.y != figure.y+(2 if self.y > figure.y else -2):
                self.set(self.x, self.y+(-1 if self.y > figure.y+1 or self.y == figure.y-1 else 1))
                movemap.full_show()
                time.sleep(0.3)
            if any([poke.hp > 0 for poke in figure.pokes[:6]]):
                movemap_text(self.x, self.y, self.texts)
                winner = fight([poke for poke in figure.pokes[:6] if poke.hp > 0][0], self.poke, info={"type": "duel", "player": self})
                movemap_text(self.x, self.y, {True : self.lose_texts, False: self.win_texts+[" < Here u go 20$"]}[winner == self.poke])
                if (winner != self.poke):
                    figure.add_money(20)
                    used_npcs.append(self.name)
            else:
                movemap_text(self.x, self.y, self.no_poke_texts)
                used_npcs.append(self.name)
            while self.y != self.sy:
                self.set(self.x, self.y+(1 if self.y < self.sy else -1))
                movemap.full_show()
                time.sleep(0.3)


class CenterInteract(se.Object):
    def action(self, ob):
        global ev
        ev = ""
        movemap.full_show()
        movemap_text(int(movemap.width/2), 3, [" < Welcome to the Pokete-Center", " < What do you want to do?", " < a: See your full deck\n b: Heal all your Poketes\n c: Go"])
        while True:
            if ev == "'a'":
                ev = ""
                while "__fallback__" in [p.identifier for p in figure.pokes]:
                    figure.pokes.pop([p.identifier for p in figure.pokes].index("__fallback__"))
                balls_label_rechar()
                deck(figure.pokes)
                break
            elif ev == "'b'":
                ev = ""
                heal()
                time.sleep(0.5)
                movemap_text(int(movemap.width/2), 3, [" < ...", " < Your Poketes are now healed!"])
                break
            elif ev == "'c'":
                ev = ""
                break
            std_loop()
            time.sleep(0.05)
        movemap.full_show(init=True)


class ShopInteract(se.Object):
    def action(self, ob):
        global ev
        ev = ""
        movemap.full_show()
        movemap_text(int(movemap.width/2), 3, [" < Welcome to the Pokete-Shop", " < Wanna buy something?"])
        buy()
        movemap.full_show(init=True)
        movemap_text(int(movemap.width/2), 3, [" < Have a great day!"])


class CenterDor(se.Object):
    def action(self, ob):
        figure.remove()
        i = figure.map.name
        figure.add(figure.oldmap, figure.oldmap.dor.x if figure.map == centermap else figure.oldmap.shopdor.x, figure.oldmap.dor.y+1 if figure.map == centermap else figure.oldmap.shopdor.y+1)
        figure.oldmap = eval(i)
        game(figure.map)


class Dor(se.Object):
    def action(self, ob):
        figure.remove()
        i = figure.map.name
        figure.add(self.arg_proto["map"], self.arg_proto["x"], self.arg_proto["y"])
        figure.oldmap = eval(i)
        game(self.arg_proto["map"])


class ChanceDor(Dor):
    def action(self, ob):
        if random.randint(0, self.arg_proto["chance"]) == 0:
            super().action(ob)


class Poke():
    def __init__(self, poke, xp, _hp="SKIP", player=True):
        self.xp = xp
        self.player = player
        self.identifier = poke
        for name in ["hp", "attacs", "name", "miss_chance", "lose_xp", "evolve_poke", "evolve_lvl"]:
            exec(f"self.{name} = pokes[self.identifier][name]")
        self.type = eval(pokes[self.identifier]["type"])
        self.full_hp = self.hp
        self.full_miss_chance = self.miss_chance
        self.hp_bar = se.Text(8*"#", esccode=Color.green, state="float")
        if _hp != "SKIP":
            self.hp = _hp if _hp <= self.full_hp else self.hp
            self.health_bar_maker(self.hp)
        self.desc = se.Text(liner(pokes[poke]["desc"], se.width-34))
        self.ico = se.Text(pokes[poke]["ico"], state="float")
        self.text_hp = se.Text(f"HP:{self.hp}", state="float")
        self.text_lvl = se.Text(f"Lvl:{self.lvl()}", state="float")
        self.text_name = se.Text(self.name, esccode=Color.underlined, state="float")
        self.text_xp = se.Text(f"XP:{self.xp-(self.lvl()**2-1)}/{((self.lvl()+1)**2-1)-(self.lvl()**2-1)}", state="float")
        self.text_type = se.Text(f"Type:{self.type.name}", state="float")
        self.tril = se.Object("<", state="float")
        self.trir = se.Object(">", state="float")
        self.attac_obs = []
        self.atc_labels = []
        self.pball_small = se.Object("o")
        self.set_vars()
        self.text_initiative = se.Text(f"Initiative:{self.initiative}", state="float")

    def set_vars(self):
        for name in ["atc", "defense", "initiative"]:
            exec(f"self.{name} = int({pokes[self.identifier][name]})")
        i = [Attack(atc) for atc in self.attacs if self.lvl() >= attacs[atc]["min_lvl"]]
        for old_ob, ob in zip(self.attac_obs, i):
            ob.ap = old_ob.ap
        self.attac_obs = i
        for ob in self.atc_labels:
            fightbox.rem_ob(ob)
        self.atc_labels = [se.Text(str(i)+": "+atc.name+"-"+str(atc.ap)) for i, atc in enumerate(self.attac_obs)]

    def dict(self):
        return {"name": self.identifier, "xp": self.xp, "hp": self.hp, "ap": [atc.ap for atc in self.attac_obs]}

    def set_ap(self, dict):
        for atc, ap in zip(self.attac_obs, dict):
            atc.ap = ap if ap != "SKIP" else atc.ap
        self.label_rechar()

    def label_rechar(self):
        for i, atc in enumerate(self.attac_obs):
            self.atc_labels[i].rechar(str(i)+": "+atc.name+"-"+str(atc.ap))

    def lvl(self):
        return int(math.sqrt(self.xp+1))

    def health_bar_maker(self, oldhp):
        bar_num = round(oldhp*8/self.full_hp)
        esccode = Color.red
        for size, num in zip([6, 2], [2, 3]):
            if bar_num > size:
                esccode = f"\033[3{num}m"
                break
        self.hp_bar.rechar(bar_num*"#", esccode)

    def health_bar_updater(self, oldhp):
        while oldhp != self.hp and oldhp > 0:
            oldhp += -1 if oldhp > self.hp else 1
            self.text_hp.rechar(f"HP:{oldhp}", esccode=Color.yellow)
            self.health_bar_maker(oldhp)
            time.sleep(0.1)
            fightmap.show()
        self.text_hp.rechar(f"HP:{oldhp}")
        time.sleep(0.1)

    def attack(self, attac, enem):
        if attac.ap > 0:
            self.enem = enem
            enem.oldhp = enem.hp
            self.oldhp = self.hp
            effectivity = 1.3 if enem.type.name in attac.type.effective else 0.5 if enem.type.name in attac.type.ineffective else 1
            n_hp = round((self.atc * attac.factor / (enem.defense if enem.defense >= 1 else 1))*random.choices([0, 0.75, 1, 1.26], weights=[attac.miss_chance+self.miss_chance, 1, 1, 1], k=1)[0]*effectivity)
            enem.hp -= n_hp if n_hp >= 0 else 0
            if enem.hp < 0:
                enem.hp = 0
            time.sleep(0.4)
            exec(f"self.move_{attac.move}()")
            exec(attac.action)
            attac.ap -= 1
            fightmap.outp.rechar(f'{self.name}({"you" if self.player else "enemy"}) used {attac.name}! {self.name+" missed!" if n_hp == 0 and attac.factor != 0 else ""}\n{"That was very effective! " if effectivity == 1.3 and n_hp > 0 else ""}{"That was not effective! " if effectivity == 0.5 and n_hp > 0 else ""}')
            for ob in [enem, self]:
                ob.health_bar_updater(ob.oldhp)
            self.label_rechar()
            fightmap.show()

    def move_attack(self):
        for i, j, t in zip([3, -3], [2, -2], [0.3, 0]):
            self.ico.move(i if self.player else -i, -j if self.player else j)
            fightmap.show()
            time.sleep(t)

    def move_pound(self):
        for i in [-1, 1]:
            self.ico.move(0, i)
            fightmap.show()
            time.sleep(0.3)

    def move_throw(self, txt="#"):
        line = se.Line(" ", self.enem.ico.x-self.ico.x+(-11 if self.player else 11), self.enem.ico.y-self.ico.y, type="crippled")
        line.add(self.ico.map, self.ico.x+(11 if self.player else -1), self.ico.y+1)
        self.ico.map.show()
        for i in range(len(line.obs)):
            line.obs[i].rechar(txt)
            if i != 0:
                line.obs[i-1].rechar(line.char)
            time.sleep(0.05)
            self.ico.map.show()
        line.remove()
        del line

    def move_fireball(self):
        self.move_throw(txt=Color.thicc+Color.red+"*"+Color.reset)

    def move_shine(self):
        for i, x, y in zip(fightmap.shines, [self.ico.x-1, self.ico.x+11, self.ico.x-1, self.ico.x+11], [self.ico.y, self.ico.y, self.ico.y+3, self.ico.y+3]):
            i.add(self.ico.map, x, y)
            self.ico.map.show()
            time.sleep(0.2)
        time.sleep(0.2)
        for i in fightmap.shines:
            i.remove()
        self.ico.map.show()

    def evolve(self):
        new = Poke(self.evolve_poke, self.xp)
        self.ico.remove()
        self.ico.add(evomap, round(evomap.width/2-4), round((evomap.height-8)/2))
        evomap.show()
        self.move_shine()
        evomap.outp.rechar("Look!")
        evomap.show()
        time.sleep(0.5)
        evomap.outp.rechar(f"{evomap.outp.text}\n{self.name} is evolving!")
        evomap.show()
        time.sleep(1)
        for i in range(8):
            for j, k in zip([self.ico, new.ico], [new.ico, self.ico]):
                j.remove()
                k.add(evomap, round(evomap.width/2-4), round((evomap.height-8)/2))
                time.sleep(0.7-i*0.09999)
                evomap.show()
        self.ico.remove()
        new.ico.add(evomap, round(evomap.width/2-4), round((evomap.height-8)/2))
        evomap.show()
        time.sleep(0.01)
        new.move_shine()
        evomap.outp.rechar(f"{self.name} evolved to {new.name}!")
        evomap.show()
        time.sleep(5)
        figure.pokes[figure.pokes.index(self)] = new
        del self


class Station(se.Square):
    choosen = None
    obs = []
    def __init__(self, associate, width, height, char="#", w_next="", a_next="", s_next="", d_next="", state="solid", arg_proto={}):
        self.org_char = char
        self.associate = associate
        super().__init__(char, width, height)
        for i in ["w_next", "a_next", "s_next", "d_next"]:
            exec(f"self.{i}={i}")
        Station.obs.append(self)

    def choose(self):
        self.rechar(Color.red+Color.thicc+self.org_char+Color.reset)
        Station.choosen = self
        mapbox.info_label.rechar(self.associate.pretty_name)

    def unchoose(self):
        self.rechar(self.org_char)

    def next(self, ev):
        ev = eval(ev)
        ne = eval(f"self.{ev}_next")
        if ne != "":
            self.unchoose()
            exec(f"mapbox.{ne}.choose()")


class Figure(se.Object):
    def __init__(self, char, state="solid", arg_proto={}):
        super().__init__(char, state="solid", arg_proto={})
        self.__money = 10
        self.inv = {"poketeballs": 10}
        self.name = ""
        self.pokes = []
        self.oldmap = playmap_1

    def set_args(self, si):
        # processing data from save file
        self.name = si["user"]
        self.pokes = [Poke((si["pokes"][poke]["name"] if type(poke) is int else poke), si["pokes"][poke]["xp"], si["pokes"][poke]["hp"]) for poke in si["pokes"]]
        for j, poke in enumerate(self.pokes):
            poke.set_ap(si["pokes"][j]["ap"])
        try:
            if eval(si["map"]) in [centermap, shopmap]:  # Looking if figure would be in centermap, so the player may spawn out of the center
                self.add(centermap, centermap.dor_back1.x, centermap.dor_back1.y-1)
            else:
                if self.add(eval(si["map"]), si["x"], si["y"]) == 1:
                    raise se.CoordinateError(self, eval(si["map"]), si["x"], si["y"])
        except se.CoordinateError:
            self.add(playmap_1, 6, 5)
        # Those if statemnets are important to ensure compatibility with older versions
        if "oldmap" in si:
            self.oldmap = eval(si["oldmap"])
        if "inv" in si:
            self.inv = si["inv"]
        if "money" in si:
            self.__money = si["money"]
        movemap.name_label = se.Text(self.name, esccode=Color.thicc)
        movemap.balls_label = se.Text("", esccode=Color.thicc)
        movemap.code_label.rechar(self.map.pretty_name)
        balls_label_rechar()
        movemap_add_obs()

    def add_money(self, money):
        self.set_money(self.__money+money)

    def get_money(self):
        return self.__money

    def set_money(self, money):
        assert money >= 0, "money has to be positive"
        self.__money = money
        for box in [invbox, buybox]:
            box.money_label.rechar(str(self.__money)+"$")
            box.set_ob(box.money_label, box.width-2-len(box.money_label.text), 0)

    def give_item(self, item, amount=1):
        assert amount > 0, "Amounts have to be positive"
        if item not in self.inv:
            self.inv[item] = amount
        else:
            self.inv[item] += amount

    def has_item(self, item):
        if item not in self.inv:
            return False
        elif self.inv[item] > 0:
            return True
        else:
            return False

    def remove_item(self, item, amount=1):
        assert amount > 0, "Amounts have to be positive"
        assert item in self.inv, f"Item {name} is not in the inventory"
        assert self.inv[item]-amount >= 0, f"There are not enought {name}s in the inventory"
        self.inv[item] -= amount


class Attack():
    def __init__(self, index):
        for i in attacs[index]:
            exec(f"self.{i}=attacs[index][i]")
        self.type = eval(attacs[index]["type"])
        self.max_ap = self.ap
        self.label_name = se.Text(self.name, esccode=Color.underlined)
        self.label_ap = se.Text(f"AP:{self.ap}/{self.max_ap}")
        self.label_factor = se.Text(f"Attack:{self.factor}")
        self.label_desc = se.Text(self.desc[:int(width/2-1)])
        self.label_type = se.Text(f"Type:{self.type.name}")


class Setting(se.Box):
    def __init__(self, text, setting, options={}):
        super().__init__(0, 0)
        self.options = options
        self.setting = setting
        self.index = eval(f"[j for j in self.options].index({self.setting})")
        self.text = se.Text(text+": ")
        self.option_text = se.Text(self.options[eval(self.setting)])
        self.add_ob(self.text, 0, 0)
        self.add_ob(self.option_text, len(self.text.text), 0)

    def change(self):
        self.index = self.index+1 if self.index < len(self.options)-1 else 0
        exec(f"{self.setting} = [i for i in self.options][self.index]")
        self.option_text.rechar(self.options[eval(self.setting)])


class Debug:
    @classmethod
    def pos(cls):
        print(figure.x, figure.y, figure.map.name)


# General use functions
#######################

def heal():
    for poke in figure.pokes:
        poke.hp = poke.full_hp
        poke.miss_chance = poke.full_miss_chance
        poke.text_hp.rechar(f"HP:{poke.hp}")
        poke.set_vars()
        poke.health_bar_maker(poke.hp)
        for atc in poke.attac_obs:
            atc.ap = atc.max_ap
        poke.label_rechar()
        balls_label_rechar()


def liner(text, width, pre=""):
    lens = 0
    out = ""
    for name in text.split(" "):
        if "\n" in name:
            lens = len(pre)
            out += name+pre
        elif lens+len(name)+1 <= width:
            out += name+" "
            lens += len(name)+1
        else:
            lens = len(name)+1+len(pre)
            out += "\n"+pre+name+" "
    return out


def hard_liner(l_len, name):
    ret = ""
    for i in range(int(len(name)/l_len)+1):
        ret += name[i*l_len:(i+1)*l_len]+("\n" if i != int(len(name)/l_len) else "")
    return ret


def autosave():
    while True:
        time.sleep(300)
        if settings.autosave:
            save()


def save():
    session_info = {
        "user": figure.name,
        "map": figure.map.name,
        "oldmap": figure.oldmap.name,
        "x": figure.x,
        "y": figure.y,
        "pokes": {i: poke.dict() for i, poke in enumerate(figure.pokes)},
        "inv": figure.inv,
        "money": figure.get_money(),
        "settings": settings.dict(),
        "used_npcs": used_npcs
    }
    with open(home+"/.cache/pokete/pokete.py", "w+") as file:
        file.write(f"session_info={session_info}")


def on_press(key):
    global ev
    ev = str(key)


def exiter():
    global do_exit
    do_exit = True
    exit()


def std_loop():
    global ev
    if ev == "exit":
        raise KeyboardInterrupt


def text_input(ob, map, name, wrap_len, max_len=1000000):
    global ev
    ev = ""
    ob.rechar(hard_liner(wrap_len, name+"█"))
    bname = name
    map.show()
    while True:
        if ev in ["Key.enter", "Key.esc"]:
            ev = ""
            ob.rechar(hard_liner(wrap_len, name))
            map.show()
            return name
        elif ev == "Key.backspace":
            if len(name) <= 0:
                ev = ""
                ob.rechar(bname)
                map.show()
                return bname
            name = name[:-1]
            ob.rechar(hard_liner(wrap_len, name+"█"))
            map.show()
            ev = ""
        elif ev not in ["", "Key.enter", "exit", "Key.backspace", "Key.shift", "Key.shift_r", "Key.esc"] and len(name) < max_len:
            if ev == "Key.space":
                ev = "' '"
            name += str(eval(ev))
            ob.rechar(hard_liner(wrap_len, name+"█"))
            map.show()
            ev = ""
        std_loop()


# Functions needed for movemap
##############################

def fast_change(arr, setob):
    _i = 1
    while _i < len(arr):
        arr[_i-1].remove()
        arr[_i].add(fightmap, setob.x, setob.y)
        fightmap.show()
        time.sleep(0.1)
        _i += 1


def balls_label_rechar():
    movemap.balls_label.text = ""
    for i in range(6):
        movemap.balls_label.text += "-" if i >= len(figure.pokes) or figure.pokes[i].identifier == "__fallback__" else "o" if figure.pokes[i].hp > 0 else "x"
    movemap.balls_label.rechar(movemap.balls_label.text, esccode=Color.thicc)


def mapresize(map):
    width, height = os.get_terminal_size()
    if map.width != width or map.height != height-1:
        map.resize(height-1, width, " ")
        return True
    return False


def codes(string):
    for i in string:
        if i == "w":
            save()
        elif i == "!":
            exec(string[string.index("!")+2:])
            return
        elif i == "e":
            try:
                exec(string[string.index("e")+2:])
            except Exception as exc:
                print(exc)
            return
        elif i == "q":
            exiter()


def movemap_text(x, y, arr):
    global ev
    multitext.rechar("")
    multitext.add(movemap, x-movemap.x+1, y-movemap.y)
    for t in arr:
        ev = ""
        multitext.rechar("")
        for i in range(len(t)+1):
            multitext.rechar(liner(t[:i], movemap.width-(x-movemap.x+1), "   "))
            movemap.show()
            time.sleep(0.045)
            std_loop()
            if ev != "":
                ev = ""
                break
        multitext.rechar(liner(t, movemap.width-(x-movemap.x+1), "   "))
        movemap.show()
        while True:
            std_loop()
            if ev != "":
                break
            time.sleep(0.05)
    multitext.remove()


def movemap_add_obs():
    movemap.underline = se.Square("-", movemap.width, 1)
    movemap.name_label.add(movemap, 2, movemap.height-2)
    movemap.balls_label.add(movemap, 4+len(movemap.name_label.text), movemap.height-2)
    movemap.underline.add(movemap, 0, movemap.height-2)
    movemap.label.add(movemap, 0, movemap.height-1)
    movemap.code_label.add(movemap, 0, 0)


# Functions for deck
####################

def deck_add(poke, map, x, y, in_deck=True):
    poke.text_name.add(map, x+12, y+0)
    if poke.identifier != "__fallback__":
        for ob, _x, _y in zip([poke.ico, poke.text_lvl, poke.text_hp, poke.tril, poke.trir, poke.hp_bar, poke.text_xp], [0, 12, 12, 18, 27, 19, 12], [0, 1, 2, 2, 2, 2, 3]):
            ob.add(map, x+_x, y+_y)
        if figure.pokes.index(poke) < 6 and in_deck:
            poke.pball_small.add(map, round(deckmap.width/2)-1 if figure.pokes.index(poke) % 2 == 0 else deckmap.width-2, y)


def deck_remove(poke):
    for ob in [poke.ico, poke.text_name, poke.text_lvl, poke.text_hp, poke.tril, poke.trir, poke.hp_bar, poke.text_xp, poke.pball_small]:
        ob.remove()


def deck_add_all(pokes, init=False):
    j = 0
    for i, poke in enumerate(pokes):
        deck_add(poke, deckmap, 1 if i % 2 == 0 else round(deckmap.width/2)+1, j*5+1)
        if i % 2 == 0 and init:
            se.Square("-", deckmap.width-2, 1).add(deckmap, 1, j*5+5)
        if i % 2 == 1:
            j += 1


def deck_control(pokes, ev, index):
    if len(pokes) <= 1:
        return
    for control, statement, first, second in zip(
    ["'a'", "'d'", "'s'", "'w'"],
    [index.index != 0, index.index != len(pokes)-1, index.index+2 < len(pokes), index.index-2 >= 0],
    [-1, 1, 2, -2],
    [len(pokes)-1, 0, index.index % 2, [i for i in range(len(pokes)) if i % 2 == index.index % 2][-1]]):
        if ev == control:
            if statement:
                index.index += first
            else:
                index.index = second
            break
    index.set(pokes[index.index].text_name.x+len(pokes[index.index].text_name.text)+1, pokes[index.index].text_name.y)


# Functions for fight
#####################

def fight_clean_up(player, enemy):
    for ob in [enemy.text_name, enemy.text_lvl, enemy.text_hp, enemy.ico, enemy.hp_bar, enemy.tril, enemy.trir, player.text_name, player.text_lvl, player.text_hp, player.ico, player.hp_bar, player.tril, player.trir, enemy.pball_small]:
        ob.remove()
    for ob in player.atc_labels:
        fightbox.rem_ob(ob)


def fight_add_3(player, enemy):
    if player.identifier != "__fallback__":
        player.text_name.add(fightmap, fightmap.width-17, fightmap.height-9)
        player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-8)
        player.tril.add(fightmap, fightmap.width-11, fightmap.height-7)
        player.trir.add(fightmap, fightmap.width-2, fightmap.height-7)
        player.hp_bar.add(fightmap, fightmap.width-10, fightmap.height-7)
        player.text_hp.add(fightmap, fightmap.width-17, fightmap.height-7)
        player.ico.add(fightmap, 3, fightmap.height-10)
    return [player, enemy]


def fight_add_1(player, enemy):
    for ob, x, y in zip([enemy.tril, enemy.trir, enemy.text_name, enemy.text_lvl, enemy.text_hp, enemy.ico, enemy.hp_bar], [7, 16, 1, 1, 1, fightmap.width-14, 8], [3, 3, 1, 2, 3, 2, 3]):
        ob.add(fightmap, x, y)
    if enemy.name in [ob.name for ob in figure.pokes]:
        enemy.pball_small.add(fightmap, len(fightmap.e_underline.text)-1, 1)
    for ob, y in zip(player.atc_labels, range(4)):
        fightbox.add_ob(ob, 2, 1+y)
    return [player, enemy]


def fight_add_2(player, enemy):
    if player.identifier != "__fallback__":
        player.text_name.add(fightmap, fightmap.width-17, fightmap.height-9)
        time.sleep(0.05)
        fightmap.show()
        player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-8)
        time.sleep(0.05)
        fightmap.show()
        player.tril.add(fightmap, fightmap.width-11, fightmap.height-7)
        player.trir.add(fightmap, fightmap.width-2, fightmap.height-7)
        player.hp_bar.add(fightmap, fightmap.width-10, fightmap.height-7)
        player.text_hp.add(fightmap, fightmap.width-17, fightmap.height-7)
        time.sleep(0.05)
        fightmap.show()
        player.ico.add(fightmap, 3, fightmap.height-10)


def fight_throw(ob, enem, info, chance, name):
    if ob.identifier == "__fallback__" or info["type"] == "duel":
        return 1
    fightmap.outp.rechar(f"You threw a {name.capitalize()}!")
    fast_change([enem.ico, deadico1, deadico2, pball], enem.ico)
    time.sleep(random.choice([1,2,3,4]))
    figure.remove_item(name)
    if random.choices([True, False], weights=[(enem.full_hp/enem.hp)*chance, enem.full_hp], k=1)[0]:
        enem.player = True
        figure.pokes.append(enem)
        fightmap.outp.rechar(f"You catched {enem.name}")
        fightmap.show()
        time.sleep(1)
        pball.remove()
        fight_clean_up(ob, enem)
        balls_label_rechar()
        return 2
    else:
        fightmap.outp.rechar("You missed!")
        fightmap.show()
        pball.remove()
        enem.ico.add(fightmap, enem.ico.x, enem.ico.y)
        fightmap.show()


def fight_potion(ob, enem, info, i, name):
    figure.remove_item(name)
    ob.oldhp = ob.hp
    if ob.hp + i > ob.full_hp:
        ob.hp = ob.full_hp
    else:
        ob.hp += i
    ob.health_bar_updater(ob.oldhp)
    return

def fight_heal_potion(ob, enem, info):
    return fight_potion(ob, enem, info, 5, "healing_potion")

def fight_super_potion(ob, enem, info):
    return fight_potion(ob, enem, info, 15, "super_potion")

def fight_poketeball(ob, enem, info):
    return fight_throw(ob, enem, info, 1, "poketeball")

def fight_superball(ob, enem, info):
    return fight_throw(ob, enem, info, 6, "superball")

def fight_hyperball(ob, enem, info):
    return fight_throw(ob, enem, info, 1000, "hyperball")

def fight_ap_potion(ob, enem, info):
    for atc in ob.attac_obs:
        atc.ap = atc.max_ap
    ob.label_rechar()

# Functions for buy
#####################

def buy_rechar(items):
    ob = items[buybox.index.index]
    buybox2.name_label.rechar(ob.pretty_name)
    buybox2.desc_label.rechar(liner(ob.desc, 19))


# Functions for inv
#####################

def inv_add():
    invbox.add(movemap, movemap.width-35, 0)
    items = [eval("invbox."+i) for i in figure.inv if figure.inv[i] > 0]
    obs = [se.Text(i.pretty_name+"s : "+str(figure.inv[i.name])) for i in items]
    for i, ob in enumerate(obs):
        invbox.add_ob(ob, 4, 1+i)
    return items, obs


def inv_remove(obs):
    invbox.remove()
    for ob in obs:
        invbox.rem_ob(ob)


# Playmap extra action functions
# Those are adding additional actions to playmaps
#################################################

def playmap_water_extra_action(obs):
    if settings.animations:
        for ob in obs:
            if random.randint(0, 9) == 0:
                if " " not in ob.char:
                    ob.rechar([i for i in [Color.lightblue+"~"+Color.reset, Color.blue+"~"+Color.reset] if i != ob.char][0])
                    if ob.x == figure.x and ob.y == figure.y:
                        figure.redraw()

def playmap_4_extra_action():
    playmap_water_extra_action(playmap_4.lake_1.obs)

def playmap_11_extra_action():
    playmap_water_extra_action(playmap_11.lake_1.obs)

def playmap_18_extra_action():
    playmap_water_extra_action(playmap_18.lake_1.obs)

def playmap_7_extra_action():
    for ob in playmap_7.inner_walls.obs + playmap_7.trainers + [eval("playmap_7."+i) for i in map_data["playmap_7"]["balls"] if "playmap_7."+i not in used_npcs or not save_trainers]:
        if ob.added and math.sqrt((ob.y-figure.y)**2+(ob.x-figure.x)**2) <= 3:
            ob.rechar(ob.bchar)
        else:
            ob.rechar(" ")

# NPC functions
###############

def playmap_10_old_man():
    playmap_10.old_man.will = False
    used_npcs.append(playmap_10.old_man.name)
    if ask_bool(movemap, "Old man gifted you a Hyperball. Do you want to accept it?"):
        figure.give_item("hyperball")


def playmap_17_boy():
    if "choka" in [i.identifier for i in figure.pokes[:6]]:
        movemap_text(playmap_17.boy_1.x, playmap_17.boy_1.y, [" < Oh, cool!", " < You have a Choka!", " < I've never seen one before!", " < Here you go, 200$"])
        if ask_bool(movemap, "Young boy gifted you 200$. Do you want to accept it?"):
            figure.add_money(200)
        playmap_17.boy_1.will = False
        used_npcs.append(playmap_17.boy_1.name)
    else:
        movemap_text(playmap_17.boy_1.x, playmap_17.boy_1.y, [" < In this region lives the würgos Pokete.", f" < At level {pokes['würgos']['evolve_lvl']} it evolves to Choka.", " < I have never seen one before!"])


# main functions
################

def swap_poke():
    PORT = 65432
    if ask_bool(movemap, "Do you want to be the host?"):
        index = deck(figure.pokes[:6], "Your deck", True)
        infobox = InfoBox("Waiting...")
        infobox.center_add(movemap)
        movemap.show()
        HOST = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    data = eval(data.decode())
                    conn.sendall(str.encode(str(figure.pokes[index].dict())))
                    infobox.remove()
                    infobox = InfoBox(f"You received: {data['name']}")
                    infobox.center_add(movemap)
                    movemap.show()
                    time.sleep(3)
                    infomap.remove()
                    figure.pokes[index] = Poke(data["name"], data["xp"], data["hp"])
                    figure.pokes[index].set_ap(data["ap"])
    else:
        HOST = ""
        while HOST == "":
            HOST = ask_text(movemap, "Please type in the hosts hostname", "Host:", "", 30)
        index = deck(figure.pokes[:6], "Your deck", True)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(str.encode(str(figure.pokes[index].dict())))
            data = s.recv(1024)
            data = eval(data.decode())
            infobox = InfoBox(f"You received: {data['name']}")
            infobox.center_add(movemap)
            movemap.show()
            time.sleep(3)
            infomap.remove()
            figure.pokes[index] = Poke(data["name"], data["xp"], data["hp"])
            figure.pokes[index].set_ap(data["ap"])


def ask_bool(map, text):
    global ev
    assert len(text) >= 12, "Text has to be longer then 12 characters!"
    infobox = InfoBox(f"{text}\n{round(len(text)/2-6)*' '}[Y]es   [N]o")
    infobox.center_add(map)
    map.show()
    while True:
        if ev == "'y'":
            ret = True
            break
        elif ev in ["'n'", "Key.esc", "'q'"]:
            ret = False
            break
        std_loop()
        time.sleep(0.05)
        map.show()
    ev = ""
    infobox.remove()
    del infobox
    return ret


def ask_text(map, infotext, introtext, text, max_len):
    inputbox = InputBox(infotext, introtext, text, max_len)
    inputbox.center_add(map)
    map.show()
    ret = text_input(inputbox.text, map, text, max_len+1, max_len=max_len)
    inputbox.remove()
    del inputbox
    return ret


def inv():
    global ev
    ev = ""
    items, obs = inv_add()
    movemap.show()
    while True:
        if ev in ["'s'", "'w'"]:
            invbox.input(ev, obs)
            ev = ""
        elif ev in ["'4'", "Key.esc", "'q'"]:
            inv_remove(obs)
            return
        elif ev == "Key.enter":
            ob = items[invbox.index.index]
            invbox2.name_label.rechar(ob.pretty_name)
            invbox2.desc_label.rechar(liner(ob.desc, 19))
            invbox2.add(movemap, invbox.x-19, 3)
            ev = ""
            while True:
                if ev == "exit":
                    raise KeyboardInterrupt
                elif ev in ["Key.enter", "Key.esc", "'q'"]:
                    ev = ""
                    invbox2.remove()
                    break
                time.sleep(0.05)
                movemap.show()
        elif ev == "'r'":
            if ask_bool(movemap, f"Do you really want to throw {items[invbox.index.index].pretty_name} away?"):
                figure.remove_item(items[invbox.index.index].name)
                inv_remove(obs)
                items, obs = inv_add()
                if obs == []:
                    inv_remove(obs)
                    return
                if invbox.index.index >= len(obs):
                    invbox.index.index = len(obs)-1
                    invbox.set_index(obs)
            ev = ""
        std_loop()
        time.sleep(0.05)
        movemap.show()


def buy():
    global ev
    ev = ""
    buybox.add(movemap, movemap.width-35, 0)
    buybox2.add(movemap, buybox.x-19, 3)
    items = [invbox.poketeball, invbox.superball, invbox.healing_potion, invbox.super_potion, invbox.ap_potion]
    obs = [se.Text(f"{ob.pretty_name} : {ob.price}$") for ob in items]
    for i, ob in enumerate(obs):
        buybox.add_ob(ob, 4, 1+i)
    buy_rechar(items)
    movemap.show()
    while True:
        if ev in ["'s'", "'w'"]:
            buybox.input(ev, obs)
            buy_rechar(items)
            ev = ""
        elif ev in ["Key.esc", "'q'"]:
            buybox.remove()
            buybox2.remove()
            for ob in obs:
                buybox.rem_ob(ob)
            return
        elif ev == "Key.enter":
            ob = items[buybox.index.index]
            if figure.get_money()-ob.price >= 0:
                figure.add_money(-ob.price)
                figure.give_item(ob.name)
            ev = ""
        std_loop()
        time.sleep(0.05)
        movemap.show()


def roadmap():
    global ev
    ev = ""
    mapbox.add(movemap, movemap.width-mapbox.width, 0)
    [i for i in Station.obs if i.associate == [j for j in [figure.map, figure.oldmap] if j in [k.associate for k in Station.obs]][0]][0].choose()
    movemap.show()
    while True:
        if ev in ["'w'", "'a'", "'s'", "'d'"]:
            Station.choosen.next(ev)
            ev = ""
        elif ev in ["'3'", "Key.esc", "'q'"]:
            ev = ""
            mapbox.remove()
            Station.choosen.unchoose()
            return
        std_loop()
        time.sleep(0.05)
        movemap.show()


def menu():
    global ev
    ev = ""
    menubox.add(movemap, movemap.width-menubox.width, 0)
    movemap.show()
    while True:
        if ev == "Key.enter":
            i = menubox.ob_list[menubox.index.index]  # Fuck python for not having case statements
            if i == menubox.playername_label:
                figure.name = text_input(menubox.realname_label, movemap, figure.name, 18, 17)
                movemap.underline.remove()
                movemap.balls_label.set(0, 1)
                movemap.name_label.rechar(figure.name, esccode=Color.thicc)
                movemap.balls_label.set(4+len(movemap.name_label.text), movemap.height-2)
                movemap.underline.add(movemap, 0, movemap.height-2)
            elif i == menubox.save_label:  # When will python3.10 come out?
                # Shows a box displaying "Saving...." while saving
                savebox = InfoBox("Saving....")
                savebox.center_add(movemap)
                movemap.show()
                save()
                time.sleep(1.5)
                savebox.remove()
                del savebox
            elif i == menubox.exit_label:
                save()
                exiter()
            else:
                i.change()
            ev = ""
        elif ev in ["'s'", "'w'"]:
            menubox.input(ev, menubox.ob_list)
            ev = ""
        elif ev in ["'e'", "Key.esc", "'q'"]:
            ev = ""
            menubox.remove()
            return
        std_loop()
        time.sleep(0.05)
        movemap.show()


def fight(player, enemy, info={"type": "wild", "player": " "}):
    global ev
    # fancy stuff
    if settings.animations:
        fancymap = se.Map(background=" ", width=width, height=height-1)
        vec_list = [se.Line(" ", i*int(width/2), j*int((height-1)/2)) for i, j in zip([1, 1, -1, -1], [1, -1, -1, 1])]
        for i in vec_list:
            i.add(fancymap, int(width/2), int((height-1)/2))
        fancymap.show()
        for j, l in zip(list(zip(*[i.obs for i in vec_list])), list(zip(*[list(2*" ")+k for k in [i.obs for i in vec_list]])),):
            for i in j:
                i.rechar("-")
            for k in l:
                if k != " ":
                    k.rechar(" ")
            fancymap.show()
            time.sleep(0.005)
        for i in vec_list:
            i.remove()
        del fancymap
    # fancy stuff end
    players = fight_add_1(player, enemy)
    if info["type"] == "wild":
        fightmap.outp.rechar(f"A wild {enemy.name} appeared!")
    elif info["type"] == "duel":
        fightmap.outp.rechar(f"{info['player'].name} started a fight!")
        fightmap.show(init=True)
        time.sleep(1)
        fightmap.outp.rechar(f'{fightmap.outp.text}\n{info["player"].gender} used {enemy.name} against you!')
    fightmap.show(init=True)
    time.sleep(1)
    fight_add_2(player, enemy)
    if player.identifier != "__fallback__":
        fast_change([player.ico, deadico2, deadico1, player.ico], player.ico)
        fightmap.outp.rechar(f"You used {player.name}")
    fightbox.index.index = 0
    fightbox.set_index(player.atc_labels)
    fightmap.show()
    time.sleep(0.5)
    enem = sorted(zip([i.initiative for i in players], [1, 0], players))[0][-1]  # The [1, 0] array is needed to avoid comparing two Poke objects
    ob = [i for i in players if i != enem][-1]
    while True:
        if ob.player:
            fightmap.outp.rechar(fightmap.outp.text+("\n" if "\n" not in fightmap.outp.text else "")+ "What do you want to do?")
            fightmap.show()
            if ob.identifier == "__fallback__":
                time.sleep(1)
                fightmap.outp.rechar("You don't have any living poketes left!")
                fightmap.show()
            while True:  # Inputloop for general options
                if ev == "'1'":
                    ev = ""
                    fightbox.add(fightmap, 1, fightmap.height-7)
                    fightmap.show()
                    while True:  # Inputloop for attack options
                        if ev in ["'s'", "'w'"]:
                            fightbox.input(ev, ob.atc_labels)
                            fightmap.show()
                            ev = ""
                        elif ev in ["'"+str(i)+"'" for i in range(len(ob.attac_obs))]+["Key.enter"]:
                            if ev == "Key.enter":
                                attack = ob.attac_obs[fightbox.index.index]
                            else:
                                attack = ob.attac_obs[int(eval(ev))]
                            ev = ""
                            if attack.ap == 0:
                                continue
                            fightbox.remove()
                            fightmap.show()
                            break
                        elif ev in ["Key.esc", "'q'"]:
                            ev = ""
                            attack = ""
                            fightbox.remove()
                            fightmap.show()
                            break
                        std_loop()
                        time.sleep(0.05)
                    if attack != "":
                        break
                elif ev == "'2'":
                    ev = ""
                    if info["type"] == "duel" and player.identifier != "__fallback__":
                        continue
                    fightmap.outp.rechar("You ran away!")
                    fightmap.show()
                    time.sleep(1)
                    fight_clean_up(player, enemy)
                    return enem
                elif ev == "'3'":
                    ev = ""
                    items = [eval("invbox."+i) for i in figure.inv if eval("invbox."+i).fn != None and figure.inv[i] > 0]
                    if items == []:
                        fightmap.outp.rechar("You don't have any items left!\nWhat do you want to do?")
                        fightmap.show()
                        continue
                    fight_invbox.add(fightmap, fightmap.width-35, 0)
                    obs = [se.Text(f"{i.pretty_name}s : {figure.inv[i.name]}") for i in items]
                    for i, j in enumerate(obs):
                        fight_invbox.add_ob(j, 4, 1+i)
                    fight_invbox.index.index = 0
                    fight_invbox.set_index(obs)
                    fightmap.show()
                    while True:
                        if ev in ["'s'", "'w'"]:
                            fight_invbox.input(ev, obs)
                            ev = ""
                        elif ev in ["Key.esc", "'q'"]:
                            item = ""
                            fight_invbox.remove()
                            for i in obs:
                                fight_invbox.rem_ob(i)
                            break
                        elif ev == "Key.enter":
                            item = items[fight_invbox.index.index]
                            fight_invbox.remove()
                            for i in obs:
                                fight_invbox.rem_ob(i)
                            break
                        std_loop()
                        time.sleep(0.05)
                        fightmap.show()
                    fightmap.show()
                    if item == "":
                        continue
                    a = item.fn(ob, enem, info)  # I hate you python for not having switch statements
                    if a == 1:
                        continue
                    elif a == 2:
                        return
                    attack = ""
                    break
                elif ev == "'4'":
                    ev = ""
                    if ob.identifier == "__fallback__":
                        continue
                    fight_clean_up(player, enemy)
                    new_player = figure.pokes[deck(figure.pokes[:6], "Your deck", True)]
                    player = new_player if new_player != None else player
                    fight_add_1(player, enemy)
                    fightbox.set_ob(fightbox.index, fightbox.index.rx, 1)
                    fightbox.index.index = 0
                    players = fight_add_3(player, enemy)
                    fightmap.outp.rechar(f"You have choosen {player.name}")
                    fightmap.show(init=True)
                    attack = ""
                    break
                std_loop()
                time.sleep(0.1)
        else:
            attack = random.choices([i for i in ob.attac_obs], weights=[i.ap*((1.5 if enem.type.name in i.type.effective else 0.5 if enem.type.name in i.type.ineffective else 1) if info["type"] == "duel" else 1) for i in ob.attac_obs])[0]
        time.sleep(0.3)
        if attack != "":
            ob.attack(attack, enem)
        fightmap.show()
        time.sleep(0.5)
        if enem.hp <= 0:
            winner = ob
            break
        elif all([i.ap == 0 for i in ob.attac_obs]):
            winner = [i for i in players if i != ob][0]
            time.sleep(2)
            fightmap.outp.rechar(f"{ob.name}({'you' if winner.player else 'enemy'}) has used all its' attacks!")
            fightmap.show()
            time.sleep(3)
            break
        fightmap.show()
        ob = [i for i in players if i != ob][-1]
        enem = [i for i in players if i != ob][-1]
    loser = [ob for ob in players if ob != winner][0]
    xp = (loser.lose_xp+(1 if loser.lvl() > winner.lvl() else 0))*(2 if info["type"] == "duel" else 1)
    fightmap.outp.rechar(f"{winner.name}({'you' if winner.player else 'enemy'}) won!"+(f'\nXP + {xp}' if winner.player else ''))
    fightmap.show()
    if winner.player:
        old_lvl = winner.lvl()
        winner.xp += xp
        winner.text_xp.rechar(f"XP:{winner.xp-(winner.lvl()**2-1)}/{((winner.lvl()+1)**2-1)-(winner.lvl()**2-1)}")
        winner.text_lvl.rechar(f"Lvl:{winner.lvl()}")
        if old_lvl < winner.lvl():
            time.sleep(1)
            fightmap.outp.rechar(f"{winner.name} reached lvl {winner.lvl()}!")
            winner.move_shine()
            time.sleep(0.5)
            winner.set_vars()
            if winner.evolve_poke != "" and winner.lvl() >= winner.evolve_lvl:
                winner.evolve()
    fightmap.show()
    time.sleep(1)
    ico = [ob for ob in players if ob != winner][0].ico
    fast_change([ico, deadico1, deadico2], ico)
    deadico2.remove()
    fightmap.show()
    fight_clean_up(player, enemy)
    balls_label_rechar()
    return winner


def deck(pokes, label="Your full deck", in_fight=False):
    global ev
    deckmap.resize(5*int((len(pokes)+1)/2)+2, width, deckmap.background)
    #decksubmap.resize(height-1, width)
    se.Text(label, esccode=Color.thicc).add(deckmap, 2, 0)
    se.Square("|", 1, deckmap.height-2).add(deckmap, round(deckmap.width/2), 1)
    se.Frame(height=deckmap.height-1, width=deckmap.width, corner_chars=["_", "_", "|", "|"], horizontal_chars=["_", "_"]).add(deckmap, 0, 0)
    decksubmap.move_label.rechar("2: Move    ")
    ev = ""
    j = 0
    indici = []
    deck_add_all(pokes, True)
    deck_index = se.Object("*")
    deck_index.index = 0
    if len(pokes) > 0:
        deck_index.add(deckmap, pokes[deck_index.index].text_name.x+len(pokes[deck_index.index].text_name.text)+1, pokes[deck_index.index].text_name.y)
    decksubmap.full_show(init=True)
    while True:
        if ev in ["'1'", "Key.esc", "'q'"]:
            ev = ""
            for poke in pokes:
                deck_remove(poke)
            while len(deckmap.obs) > 0:
                deckmap.obs[0].remove()
            decksubmap.set(0, 0)
            return
        elif ev == "'2'":
            ev = ""
            if len(pokes) == 0:
                continue
            if indici == []:
                indici.append(deck_index.index)
                decksubmap.move_label.rechar("2: Move to ")
            else:
                indici.append(deck_index.index)
                figure.pokes[indici[0]], figure.pokes[indici[1]] = pokes[indici[1]], pokes[indici[0]]
                pokes = figure.pokes[:len(pokes)]
                indici = []
                for poke in pokes:
                    deck_remove(poke)
                deck_index.set(0, deckmap.height-1)
                deck_add_all(pokes)
                deck_index.set(pokes[deck_index.index].text_name.x+len(pokes[deck_index.index].text_name.text)+1, pokes[deck_index.index].text_name.y)
                decksubmap.move_label.rechar("2: Move    ")
                decksubmap.full_show()
        elif ev == "'3'":
            ev = ""
            if ask_bool(decksubmap, f"Do you really want to free {figure.pokes[deck_index.index].name}?"):
                for poke in pokes:
                    deck_remove(poke)
                figure.pokes[deck_index.index] = Poke("__fallback__", 10, 0)
                pokes = figure.pokes[:len(pokes)]
                deck_add_all(pokes)
                deck_index.set(pokes[deck_index.index].text_name.x+len(pokes[deck_index.index].text_name.text)+1, pokes[deck_index.index].text_name.y)
                balls_label_rechar()
        elif ev in ["'w'", "'a'", "'s'", "'d'"]:
            deck_control(pokes, ev, deck_index)
            ev = ""
        elif ev == "Key.enter":
            ev = ""
            if len(pokes) == 0:
                continue
            if in_fight:
                if pokes[deck_index.index].hp > 0:
                    for poke in pokes:
                        deck_remove(poke)
                    while len(deckmap.obs) > 0:
                        deckmap.obs[0].remove()
                    decksubmap.set(0, 0)
                    return deck_index.index
            else:
                for poke in pokes:
                    deck_remove(poke)
                detail(pokes[deck_index.index])
                deck_add_all(pokes)
                decksubmap.full_show(init=True)
        std_loop()
        if len(pokes) > 0 and deck_index.y-decksubmap.y +6 > decksubmap.height:
            decksubmap.set(decksubmap.x, decksubmap.y+1)
        elif len(pokes) > 0 and deck_index.y-1 < decksubmap.y:
            decksubmap.set(decksubmap.x, decksubmap.y-1)
        time.sleep(0.05)
        decksubmap.full_show()


def detail(poke):
    global ev
    deck_add(poke, detailmap, 1, 1, False)
    detailmap.attack_defense.rechar(f"Attack:{poke.atc}{(4-len(str(poke.atc)))*' '}Defense:{poke.defense}")
    poke.text_initiative.rechar(f"Initiative:{poke.initiative}")
    for ob, x, y in zip([poke.desc, poke.text_type, poke.text_initiative], [34, 36, 49], [2, 5, 5]):
        ob.add(detailmap, x, y)
    for atc, x, y in zip(poke.attac_obs, [1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1], [7, 7, 12, 12]):
        atc.temp_i = 0
        atc.temp_j = -30
        atc.label_desc.rechar(atc.desc[:int(width/2-1)])
        atc.label_ap.rechar("AP:"+str(atc.ap)+"/"+str(atc.max_ap))
        for label, _x, _y in zip([atc.label_name, atc.label_factor, atc.label_type, atc.label_ap, atc.label_desc], [0, 0, 11, 0, 0], [0, 1, 1, 2, 3]):
            label.add(detailmap, x+_x, y+_y)
    detailmap.show(init=True)
    while True:
        if ev in ["'1'", "Key.esc", "'q'"]:
            ev = ""
            deck_remove(poke)
            for ob in [poke.desc, poke.text_type, poke.text_initiative]:
                ob.remove()
            for atc in poke.attac_obs:
                for ob in [atc.label_name, atc.label_factor, atc.label_ap, atc.label_desc, atc.label_type]:
                    ob.remove()
                del atc.temp_i, atc.temp_j
            return
        std_loop()
        for atc in poke.attac_obs:  # This section generates the Text effect for attack labels
            if len(atc.desc) > int((width-3)/2-1):
                if atc.temp_j == 5:
                    atc.temp_i += 1
                    atc.temp_j = 0
                    if atc.temp_i == len(atc.desc)-int(width/2-1)+10:
                        atc.temp_i = 0
                        atc.temp_j = -30
                    atc.label_desc.rechar(atc.desc[atc.temp_i:int(width/2-1)+atc.temp_i])
                else:
                    atc.temp_j += 1
        time.sleep(0.05)
        detailmap.show()


def game(map):
    global ev, width, height
    ev = ""
    print("\033]0;Pokete - "+map.pretty_name+"\a", end="")
    movemap.code_label.rechar(figure.map.pretty_name)
    movemap.set(0, 0)
    movemap.bmap = map
    movemap.full_show()
    while True:
        for name, dir, x, y in zip(["'w'", "'a'", "'s'", "'d'"], ["t", "l", "b", "r"], [0, -1, 0, 1], [-1, 0, 1, 0]):
            if ev == name:
                figure.direction = dir
                figure.set(figure.x+x, figure.y+y)
                ev = ""
        if ev in ["'1'", "'3'", "'4'"]:
            exec({"'1'": 'deck(figure.pokes[:6], "Your deck")', "'3'": 'roadmap()', "'4'": 'inv()'}[ev])
            ev = ""
            movemap.show(init=True)
        elif ev == "'2'":
            ev = ""
            save()
            exiter()
        elif ev == "':'":
            ev = ""
            inp = text_input(movemap.code_label, movemap, ":", movemap.width, (movemap.width-2)*movemap.height-1)[1:]
            movemap.code_label.rechar(figure.map.pretty_name)
            movemap.show()
            codes(inp)
            ev = ""
        elif ev == "'e'":
            ev = ""
            menu()
            movemap.show(init=True)
        std_loop()
        map.extra_actions()
        for trainer in map.trainers:
            trainer.do(map)
        time.sleep(0.05)
        for statement, x, y in zip(
        [figure.x+6 > movemap.x+movemap.width, figure.x < movemap.x+6, figure.y+6 > movemap.y+movemap.height, figure.y < movemap.y+6],
        [1, -1, 0, 0],
        [0, 0, 1, -1]):
            if statement:
                movemap.set(movemap.x+x, movemap.y+y)
        # checking for resizing
        width, height = os.get_terminal_size()
        if movemap.width != width or movemap.height != height-1:
            for ob in [movemap.underline, movemap.label, movemap.code_label, movemap.name_label, movemap.balls_label]:
                ob.remove()
            movemap.resize(height-1, width, " ")
            movemap_add_obs()
        movemap.full_show()


def intro():
    movemap.set(0, 0)
    movemap.bmap = intromap
    movemap.full_show()
    while figure.name in ["DEFAULT", ""]:
        figure.name = ask_text(movemap, "Welcome to Pokete!\nPlease choose your name!\n", "Name:", "", 17)
    movemap.underline.remove()
    movemap.balls_label.set(0, 1)
    movemap.name_label.rechar(figure.name, esccode=Color.thicc)
    movemap.balls_label.set(4+len(movemap.name_label.text), movemap.height-2)
    movemap.underline.add(movemap, 0, movemap.height-2)
    movemap_text(4, 3, [" < Hello my child.",
                        " < You're now ten years old.",
                        " < And I think it's now time for you to travel the world and be a Pokete-trainer.",
                        " < Therefore I give you this powerfull 'Steini', 15 'Poketeballs' to catch Poketes and a 'Healing potion'.",
                        " < You will be the best Pokete-Trainer in in Nice town.",
                        " < Now go out and become the best!"])
    game(intromap)


def main():
    os.system("")
    recognising = threading.Thread(target=recogniser)
    autosaveing = threading.Thread(target=autosave)
    recognising.daemon = True
    autosaveing.daemon = True
    recognising.start()
    autosaveing.start()
    if figure.name == "DEFAULT":
        intro()
    game(figure.map)


# Actual code execution
#######################

# validating data
validate()

# deciding on wich input to use
if sys.platform == "linux":  # Use another (not on xserver relying) way to read keyboard input, to make this shit work in tty or via ssh, where no xserver is available
    def recogniser():
        import tty, sys, termios
        global ev, old_settings, termios, fd, do_exit

        do_exit = False
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            ev = {ord(char): "'"+char.rstrip()+"'", 13: "Key.enter", 127: "Key.backspace", 32: "Key.space", 27: "Key.esc"}[ord(char)]
            if ord(char) == 3 or do_exit:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                ev = "exit"
else:
    from pynput.keyboard import Key, Listener
    def recogniser():
        global ev
        while True:
            with Listener(on_press=on_press) as listener:
                listener.join()

__t = time.time()
# resizing screen
width, height = os.get_terminal_size()
tss = se.Map(background=" ")
tss.warning_label = se.Text("Minimum windowsize is 70x20")
tss.size_label = se.Text(str(width)+"x"+str(height))
tss.frame = se.Frame(width=width, height=height-1, corner_chars=["┌", "┐", "└", "┘"], horizontal_chars=["─", "─"], vertical_chars=["│", "│"])

tss.warning_label.add(tss, int(tss.width/2)-13, int(tss.height/2)-1)
tss.size_label.add(tss, 1, 0)
tss.frame.add(tss, 0, 0)
while width < 70 or height < 20:
    width, height = os.get_terminal_size()
    tss.warning_label.set(1, 1)
    tss.frame.remove()
    tss.resize(height-1, width, " ")
    tss.warning_label.set(int(tss.width/2)-13, int(tss.height/2)-1)
    tss.size_label.rechar(str(width)+"x"+str(height))
    tss.frame = se.Frame(width=width, height=height-1, corner_chars=["┌", "┐", "└", "┘"], horizontal_chars=["─", "─"], vertical_chars=["│", "│"])
    tss.frame.add(tss, 0, 0)
    tss.show()

# loading screen
loading_screen = se.Map(background=" ", width=width, height=height-1)
se.Text("""  _____      _        _
 |  __ \    | |      | |
 | |__) |__ | | _____| |_ ___
 |  ___/ _ \| |/ / _ \ __/ _ \\
 | |  | (_) |   <  __/ ||  __/
 |_|   \___/|_|\_\___|\__\___|""").add(loading_screen, int(loading_screen.width/2)-15, int(loading_screen.height/2)-4)
loading_screen.show()

# types
for i in types:
    exec(i+" = PokeType(i, **types[i])")

# reading config file
home = str(Path.home())
Path(home+"/.cache/pokete").mkdir(parents=True, exist_ok=True)
Path(home+"/.cache/pokete/pokete.py").touch(exist_ok=True)
# Default test session_info
session_info = {
    "user": "DEFAULT",
    "map": "intromap",
    "oldmap": "playmap_1",
    "x": 4,
    "y": 5,
    "pokes": {
        0: {"name": "steini", "xp": 50, "hp": "SKIP", "ap": ["SKIP", "SKIP"]}
    },
    "inv": {"poketeball": 15, "healing_potion": 1},
    "settings": {},
    "used_npcs": []
}
with open(home+"/.cache/pokete/pokete.py") as file:
    exec(file.read())

if "settings" in session_info:
    settings = Settings(**session_info["settings"])
else:
    settings = Settings()
save_trainers = settings.save_trainers  # This is needed to just apply some changes when restarting the game to avoid running into errors

if "used_npcs" in session_info:
    used_npcs = session_info["used_npcs"]
else:
    used_npcs = []


# Defining and adding of objetcs and maps
#########################################

# maps
centermap = PlayMap(height-1, width, " ", name = "centermap", pretty_name = "Pokete-Center")
shopmap = PlayMap(height-1, width, " ", name = "shopmap", pretty_name = "Pokete-Shop")
intromap = PlayMap(background=" ", height=15, width=30, name="intromap", pretty_name="Your home")
playmap_1 = PlayMap(background=" ", height=30, width=90, name="playmap_1", pretty_name="Nice Town",
                    trainers=[Trainer("Franz", "He", Poke("poundi", 60, player=False), [" < Wanna fight?"], [" < Hahaha!", " < You're a loser!"], [" < I see you don't have a living Pokete"], [" < Your a very good trainer!"], 30, 10)],
                    poke_args={"pokes": ["rato", "horny", "vogli"], "minlvl": 15, "maxlvl": 40})
cave_1 = PlayMap(background=" ", height=30, width=90, name="cave_1", pretty_name="Nice Town cave",
                trainers=[Trainer("Monica", "She", Poke("hornita", 128, player=False), [" < Hello noble traveler", " < Are you willing to fight with me?"], [" < Hahaha!", " < Looooser!"], [" < I see you don't have a living Pokete"], [" < Congratulations!", " < Have a great day!"], 23, 10)])
playmap_2 = PlayMap(background=" ", height=30, width=180, name="playmap_2", pretty_name="Route 1",
                    trainers = [Trainer("Wanderer Murrad", "He", Poke("ostri", 160, player=False), [" < Isn't that a great day?", " < I traveled here from a far country", " < Do you want to fight against my rare Pokete?"], [" < It is stronger than you might have exspected"], [" < I see you don't have a living Pokete"], [" < Oh, i didn't think you can defeat my Pokete!", " < You are a very good trainer!"], 32, 12)],
                    poke_args = {"pokes": ["rato", "hornita", "steini", "voglo", "wolfior"], "minlvl": 60, "maxlvl": 128})
playmap_3 = PlayMap(background=" ", height=30, width=90, name="playmap_3", pretty_name="Josi Town",
                    trainers=[Trainer("Josi", "She", Poke("hornita", 200, player=False), [" < Hey!", " < I'm Josi", " < Welcome to Josi Town", " < But first we have to fight!"], [" < Hahaha!", " < Hahaha!", " < You're a fucking loser!"], [" < I see you don't have a living Pokete", " < Loooser!"], [" < Damn, I lost!"], 11, 5)])
playmap_4 = PlayMap(background=" ", height=60, width=60, name="playmap_4", pretty_name="Josi Lake",
                    trainers=[Trainer("Kevin", "He", Poke("karpi", 340, player=False), [" < Jo!", " < What up?", " < Wanna see my sick ass Pokete?"], [" < Yeaaah!", " < My Pokete is sooo sick!"], [" < I see you don't have a living Pokete"], [" < Daaaamn", " < Your Pokete is noot from this planet!"], 32, 31)],
                    poke_args={"pokes": ["rato", "hornita", "steini", "voglo", "wolfior"], "minlvl": 180, "maxlvl": 230},
                    extra_actions = playmap_4_extra_action)
playmap_5 = PlayMap(background=" ", height=60, width=60, name="playmap_5", pretty_name="Mysterious cave",
                    trainers = [Trainer("Caveman Marc", "He", Poke("bator", 350, player=False), [" < Oh!", " < I've not seen anyone down here for while", " < Can I show you my rare Pokete, that can only be found in this cave?"], [" < Oh!", " < My Pokete is not just rare", " < It's also strong"], [" < I see you don't have a living Pokete"], [" < Congratulations!", " < I hope you can also catch one!"], 23, 12)],
                    poke_args = {"pokes": ["bato", "bator", "steini"], "minlvl": 180, "maxlvl": 230})
playmap_6 = PlayMap(background=" ", height=60, width=60, name="playmap_6", pretty_name="Route 2",
                    trainers = [Trainer("Eva", "She", Poke("treenator", 400, player=False), [" < Hi!", " < Fight?"], [" < Loser"], [" < I see you don't have a living Pokete"], [" < I lost!"], 47, 43)],
                    poke_args = {"pokes": ["steini", "voglo", "bushy", "rollator"], "minlvl": 200, "maxlvl": 260})
playmap_7 = PlayMap(background=" ", height=30, width=60, name="playmap_7", pretty_name="Dark cave",
                    trainers = [Trainer("Caveman Dieter", "He", Poke("steini", 400, player=False), [" < Oh!", " < I didn't see you comming"], [" < My steini is old but classy"], [" < I see you don't have a living Pokete"], [" < You're a great trainer!"], 18, 7)],
                    extra_actions = playmap_7_extra_action,
                    poke_args = {"pokes": ["steini", "bato", "lilstone", "rollator", "gobost"], "minlvl": 200, "maxlvl": 260})
playmap_8 = PlayMap(background=" ", height=20, width=80, name="playmap_8", pretty_name="Abandoned village",
                    trainers = [Trainer("Wood man Bert", "He", Poke("gobost", 400, player=False), [" < Do you see this abandoned house?", " < I catched this Pokete in there!"], [" < It's pretty cool huh?!"], [" < I see you don't have a living Pokete"], [" < Oh, yours is better than mine!"], 39, 6)],
                    poke_args = {"pokes": ["steini", "voglo", "wolfior", "owol"], "minlvl": 230, "maxlvl": 290})
playmap_9 = PlayMap(background=" ", height=15, width=30, name="playmap_9", pretty_name="Abandoned house",
                    poke_args = {"pokes": ["gobost", "rato"], "minlvl": 230, "maxlvl": 290})
playmap_10 = PlayMap(background=" ", height=15, width=30, name="playmap_10", pretty_name="Old house")
playmap_11 = PlayMap(background=" ", height=20, width=60, name="playmap_11", pretty_name="Route 3",
                    trainers = [Trainer("Fishermans friend", "He", Poke("clampi", 450, player=False), [" < G'day young trainer", " < I've lived here for years"], [" < Those years of training were worth it"], [" < I see you don't have a living Pokete"], [" < I did't train it in years!"], 42, 7)],
                    poke_args = {"pokes": ["steini", "voglo", "wolfior", "owol"], "minlvl": 230, "maxlvl": 290},
                    extra_actions = playmap_11_extra_action)
playmap_12 = PlayMap(background=" ", height=15, width=80, name="playmap_12", pretty_name="Route 4",
                    trainers = [Trainer("Brother Justin", "He", Poke("blub", 600, player=False), [" < Hey, my brother and me want to fight!"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Damn!"], 26, 10),
                                Trainer("Brother Justus", "He", Poke("poundi", 600, player=False), [" < Now it's my turn!"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Damn!"], 27, 10)],
                    poke_args = {"pokes": ["voglo", "vogli", "owol", "rato"], "minlvl": 300, "maxlvl": 480})
playmap_13 = PlayMap(background=" ", height=35, width=70, name="playmap_13", pretty_name="Deepens forest",
                    trainers = [Trainer("Citizen", "He", Poke("vogli", 600, player=False), [" < Hello fellow stranger!", " < This town is known for it's bird Poketes"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Damn!"], 5, 31),],
                    poke_args = {"pokes": ["voglo", "vogli", "owol", "rato"], "minlvl": 300, "maxlvl": 480})
playmap_14 = PlayMap(background=" ", height=15, width=30, name="playmap_14", pretty_name="Arena",
                    trainers = [Trainer("First trainer", "He", Poke("owol", 650, player=False), [" < Welcome to the Deepest forest Pokete Arena", " < I'm your first enemy!"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Good luck!"], 17, 10),
                                Trainer("Second trainer", "She", Poke("voglo", 700, player=False), [" < Now it's my turn!"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Good luck with the next trainer!"], 22, 10),
                                Trainer("Third trainer", "She", Poke("treenator", 750, player=False), [" < Let's see what Poketes else you have!"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Good luck with the last trainer!"], 22, 5),
                                Trainer("Last trainer", "He", Poke("ostri", 780, player=False), [" < I'm your last enemy!"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Oh!", " < You were able to defeat me?", " < You can now leave Deepest forest"], 17, 5)])
playmap_15 = PlayMap(background=" ", height=25, width=120, name="playmap_15", pretty_name="Route 5",
                    trainers = [Trainer("Samantha", "She", Poke("clampi", 650, player=False), [" < Hey you!", " < My Pokete is very effective against bird Poketes"], [" < You see, it's effective"], [" < I see you don't have a living Pokete"], [" < Oh no", " < I guess yours is even more effective than mine!"], 43, 17),
                                Trainer("Jessica", "She", Poke("angrilo", 650, player=False), [" < Hey you!"], [" < Haha, you're a loser!"], [" < I see you don't have a living Pokete"], [" < Oh no"], 31, 6)],
                    poke_args = {"pokes": ["voglo", "owol", "würgos", "hornita"], "minlvl": 400, "maxlvl": 550})
playmap_16 = PlayMap(background=" ", height=17, width=65, name="playmap_16", pretty_name="Route 6",
                    poke_args = {"pokes": ["voglo", "owol", "würgos", "hornita"], "minlvl": 480, "maxlvl": 600})
playmap_17 = PlayMap(background=" ", height=15, width=30, name="playmap_17", pretty_name="House")
playmap_18 = PlayMap(background=" ", height=23, width=98, name="playmap_18", pretty_name="Big mountain see",
                    trainers = [Trainer("Bert", "He", Poke("poundi", 700, player=False), [" < Hey!", " < This region is full of stone and ground Poketes"], [" < Haha, you're bad!"], [" < I see you don't have a living Pokete"], [" < Oh, I lost!"], 6, 4),
                                Trainer("Karen", "She", Poke("clampi", 700, player=False), [" < I don't think you can walk here", " < I demand a fight with you!"], [" < Go home little zoomer."], [" < I see you don't have a living Pokete"], [" < I want to talk to your manager."], 56, 11)],
                    poke_args = {"pokes": ["poundi", "rollator", "würgos", "rato"], "minlvl": 540, "maxlvl": 640},
                    extra_actions = playmap_18_extra_action)
playmap_19 = PlayMap(background=" ", height=30, width=60, name="playmap_19", pretty_name="Big mountain cave",
                    trainers = [Trainer("Brian", "He", Poke("choka", 850, player=False), [" < Hello fellow cava man!"], [" < Oooooh!", " < You're fucking loooser!"], [" < I see you don't have a living Pokete"], [" < Oh!", " < You were lucky!"], 16, 15),
                                Trainer("Simon", "He", Poke("wolfiro", 850, player=False), [" < Joooo!", " < What up?"], [" < You're fucking loooser!"], [" < I see you don't have a living Pokete"], [" < Duck!"], 15, 7)],
                    poke_args = {"pokes": ["poundi", "steini", "lilstone", "bato"], "minlvl": 540, "maxlvl": 640})

# mapmap
mapbox = Box(11, 40, "Roadmap")
mapbox.info_label = se.Text("")
mapbox.add_ob(mapbox.info_label, 1, 1)
for s in stations:
    exec(f"mapbox.{s} = Station({s}, **stations[s]['gen'])")
    exec(f"mapbox.add_ob(mapbox.{s}, **stations[s]['add'])")

# movemap
movemap = se.Submap(playmap_1, 0, 0, height=height-1, width=width)
figure = Figure("a")
exclamation = se.Object("!")
multitext = se.Text("", state="float")
movemap.label = se.Text("1: Deck  2: Exit  3: Map  4: Inv.")
movemap.code_label = se.Text("")

# menubox
menubox = ChooseBox(height-3, 35, "Menu")
menubox.playername_label = se.Text("Playername: ")
menubox.save_label = se.Text("Save")
menubox.exit_label = se.Text("Exit")
menubox.realname_label = se.Text(session_info["user"])
menubox.ob_list = [menubox.playername_label, Setting("Autosave", "settings.autosave", {True: "On", False: "Off"}), Setting("Animations", "settings.animations", {True: "On", False: "Off"}), Setting("Save trainers", "settings.save_trainers", {True: "On", False: "Off"}), menubox.save_label, menubox.exit_label]
# adding
for i, ob in enumerate(menubox.ob_list):
    menubox.add_ob(ob, 4, i+1)
menubox.add_ob(menubox.realname_label, menubox.playername_label.rx+len(menubox.playername_label.text), menubox.playername_label.ry)


# Definiton of objects for the playmaps
# Most of the objects ar generated from map_data for maps.py
# .poke_arg is relevant for meadow genration
############################################################

# generating objects from map_data
for map in map_data:
    for hard_ob in map_data[map]["hard_obs"]:
        exec(f'{map}.{hard_ob} = se.Text(map_data[map]["hard_obs"][hard_ob]["txt"], ignore=" ")')
        exec(f'{map}.{hard_ob}.add({map}, map_data[map]["hard_obs"][hard_ob]["x"], map_data[map]["hard_obs"][hard_ob]["y"])')
    for soft_ob in map_data[map]["soft_obs"]:
        exec(f'{map}.{soft_ob} = se.Text(map_data[map]["soft_obs"][soft_ob]["txt"], ignore=Color.green+" "+Color.reset, ob_class=HightGrass, ob_args='+map+'.poke_args, state="float", esccode=Color.green)')
        exec(f'{map}.{soft_ob}.add({map}, map_data[map]["soft_obs"][soft_ob]["x"], map_data[map]["soft_obs"][soft_ob]["y"])')
    for dor in map_data[map]["dors"]:
        exec(f'{map}.{dor} = Dor(" ", state="float", arg_proto={map_data[map]["dors"][dor]["args"]})')
        exec(f'{map}.{dor}.add({map}, map_data[map]["dors"][dor]["x"], map_data[map]["dors"][dor]["y"])')
    for ball in map_data[map]["balls"]:
        if f'{map}.{ball}' not in used_npcs or not settings.save_trainers:
            exec(f'{map}.{ball} = Poketeball("{map}.{ball}")')
            exec(f'{map}.{ball}.add({map}, map_data[map]["balls"][ball]["x"], map_data[map]["balls"][ball]["y"])')

# playmap_1
playmap_1.meadow = se.Square(Color.green+";"+Color.reset, 10, 5, state="float", ob_class=HightGrass, ob_args=playmap_1.poke_args)
playmap_1.dor = Dor("#", state="float", arg_proto={"map": centermap, "x": int(centermap.width/2), "y": 7})
# adding
playmap_1.dor.add(playmap_1, 25, 4)
playmap_1.meadow.add(playmap_1, 5, 7)

# cave_1
cave_1.inner = se.Text("""##########################################
##        ################################
#         ################################
#         ######################        ##
#                    ###########   #######
#         #########  ###########   #######
#         #########  ###########   #######
###################  ###########   #######
##############                     #######
##############                     #######
##############  ##########################
##############  ##########################
########        ##########################
#######  ###    ##########################
#######  ###    ##########################
#######         ##########################
##############  ##########################
##############  ##########################
##############  ##########################
##############  ##########################""", ignore="#", ob_class=HightGrass, ob_args={"pokes": ["steini", "bato", "lilstone", "rato"], "minlvl": 40, "maxlvl": 128}, state="float")
# adding
cave_1.inner.add(cave_1, 0, 0)

# playmap_3
playmap_3.dor = Dor("#", state="float", arg_proto={"map": centermap, "x": int(centermap.width/2), "y": 7})
playmap_3.shopdor = Dor("#", state="float", arg_proto={"map": shopmap, "x": int(shopmap.width/2), "y": 7})
# playmap_3.npc = NPC([" < Hey", " < What up?"])
# adding
playmap_3.dor.add(playmap_3, 25, 6)
playmap_3.shopdor.add(playmap_3, 61, 6)
# playmap_3.npc.add(playmap_3, 49, 14)

# playmap_4
playmap_4.dor_playmap_5 = ChanceDor("~", state="float", arg_proto={"chance": 6, "map": playmap_5, "x": 17, "y": 16})
playmap_4.lake_1 =  se.Text("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~         ~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~                 ~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~                    ~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~                                ~~~~~~~~~~~~~~
~~~~~~~~~                                           ~~~~~~~~
~~~""", esccode=Color.blue, ignore=Color.blue+" "+Color.reset, ob_class=HightGrass, ob_args={"pokes": ["karpi", "blub"], "minlvl": 180, "maxlvl": 230}, state="float")
# adding
playmap_4.dor_playmap_5.add(playmap_4, 56, 1)
playmap_4.lake_1.add(playmap_4, 0, 0)

# playmap_5
playmap_5.inner = se.Square(" ", 11, 11, state="float", ob_class=HightGrass, ob_args=playmap_5.poke_args)
# adding
playmap_5.inner.add(playmap_5, 26, 1)

# playmap_7
playmap_7.inner = se.Text("""##############################
#########        #############
#########        #############
#########        #############
#########        #############
#########               ######
##   ####     ####      ######
#    ####     ####     #######
#             ################
#    ####     ################
#########     ################
#########     ################
#########                   ##
#########     ################
#########     ################
#########     ################
#########             ########
###################   ########
####################  ########
##############################""", ignore="#", ob_class=HightGrass, ob_args=playmap_7.poke_args, state="float")
for ob in playmap_7.inner_walls.obs + playmap_7.trainers + [eval("playmap_7."+i) for i in map_data["playmap_7"]["balls"] if "playmap_7."+i not in used_npcs or not settings.save_trainers]:
    ob.bchar = ob.char
    ob.rechar(" ")
# adding
playmap_7.inner.add(playmap_7, 0, 0)

# playmap_9
playmap_9.inner = se.Text("""
#########################
#########################
###       #  #         ##
#         ####          #
#                       #
##                      #
#               #########
############ ############
#########################""", ignore="#", ob_class=HightGrass, ob_args=playmap_9.poke_args, state="float")
# adding
playmap_9.inner.add(playmap_9, 2, 1)

# playma_11
playmap_11.lake_1 =  se.Text("""~~~~~                                                 ~~~~~~
~~~~~~~~~~~~                                 ~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~                       ~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~                   ~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~          ~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""", esccode=Color.blue, ignore=Color.blue+" "+Color.reset, ob_class=HightGrass, ob_args={"pokes": ["karpi", "clampi", "clampi"], "minlvl": 290, "maxlvl": 350}, state="float")
# adding
playmap_11.lake_1.add(playmap_11, 0, 12)

# playmap_13
playmap_13.dor = Dor("#", state="float", arg_proto={"map": centermap, "x": int(centermap.width/2), "y": 7})
playmap_13.shopdor = Dor("#", state="float", arg_proto={"map": shopmap, "x": int(shopmap.width/2), "y": 7})
# adding
playmap_13.dor.add(playmap_13, 14, 29)
playmap_13.shopdor.add(playmap_13, 52, 29)

# playmap_18
playmap_18.lake_1 =  se.Text("""  ~~
 ~~~~
~~~~~~~
~~~~~~~~
~~~~~~~~
~~~~~~~~
~~~~~~
 ~~~~
 ~~""", esccode=Color.blue, ignore=Color.blue+" "+Color.reset, ob_class=HightGrass, ob_args={"pokes": ["karpi", "blub", "clampi"], "minlvl": 540, "maxlvl": 640}, state="float")
# adding
playmap_18.lake_1.add(playmap_18, 72, 7)

# playmap_19
playmap_19.inner = se.Text("""                         ####
                         #  #   ############
                         #  #   #          #
                         #  #   #          #
        ##############   #  #####          #
        ##           #   #                 #
        #            #   #  #####          #
        #            #####  #   #          #
        #                   #   #         ##
        #            #####  #   ############
        ##############   #  #
                         #  #
         #################  ####################
         #                                    ##
     #####                                     #
     #                                         #
     #                        #######          #
     #                        #     #          #
     ######## #################     ######  ####
            # #                          #  #
            # #                          #  #
            # #                          #  #
            # #                          #  #
            # #                          #  #
            # #                   ########  #
            # #                  ##         #
            # #                   ###########
            # #
            # #
            ###""", ignore="#", ob_class=HightGrass, ob_args=playmap_19.poke_args, state="float")
# adding
playmap_19.inner.add(playmap_19, 0, 0)


# adding all trainer to map
for map in map_data:
    for trainer in eval(map).trainers:
        trainer.add(eval(map), trainer.sx, trainer.sy)

# centermap
centermap.trainers = []
centermap.inner = se.Text(""" ________________
 |______________|
 |     |a |     |
 |     ¯ ¯¯     |
 |              |
 |______  ______|
 |_____|  |_____|""", ignore=" ")
centermap.interact = CenterInteract("¯", state="float")
centermap.dor_back1 = CenterDor(" ", state="float")
centermap.dor_back2 = CenterDor(" ", state="float")
# adding
centermap.dor_back1.add(centermap, int(centermap.width/2), 8)
centermap.dor_back2.add(centermap, int(centermap.width/2)+1, 8)
centermap.inner.add(centermap, int(centermap.width/2)-8, 1)
centermap.interact.add(centermap, int(centermap.width/2), 4)

# shopmap
shopmap.trainers = []
shopmap.inner = se.Text(""" __________________
 |________________|
 |      |a |      |
 |      ¯ ¯¯      |
 |                |
 |_______  _______|
 |______|  |______|""", ignore=" ")
shopmap.interact = ShopInteract("¯", state="float")
shopmap.dor_back1 = CenterDor(" ", state="float")
shopmap.dor_back2 = CenterDor(" ", state="float")
# adding
shopmap.dor_back1.add(shopmap, int(shopmap.width/2), 8)
shopmap.dor_back2.add(shopmap, int(shopmap.width/2)+1, 8)
shopmap.inner.add(shopmap, int(shopmap.width/2)-9, 1)
shopmap.interact.add(shopmap, int(shopmap.width/2), 4)

figure.set_args(session_info)

# objects for detail
detailmap = se.Map(height-1, width, " ")
detailmap.name_label = se.Text("Details", esccode=Color.thicc)
detailmap.name_attacks = se.Text("Attacks", esccode=Color.thicc)
detailmap.frame = se.Frame(height=17, width=detailmap.width, corner_chars=["_", "_", "|", "|"], horizontal_chars=["_", "_"])
detailmap.attack_defense = se.Text("Attack:   Defense:")
detailmap.exit_label = se.Text("1: Exit")
detailmap.line_sep1 = se.Square("-", detailmap.width-2, 1)
detailmap.line_sep2 = se.Square("-", detailmap.width-2, 1)
detailmap.line_middle = se.Square("|", 1, 10)
# adding
detailmap.name_label.add(detailmap, 2, 0)
detailmap.name_attacks.add(detailmap, 2, 6)
detailmap.attack_defense.add(detailmap, 13, 5)
detailmap.exit_label.add(detailmap, 0, detailmap.height-1)
detailmap.line_middle.add(detailmap, round(detailmap.width/2), 7)
detailmap.line_sep1.add(detailmap, 1, 6)
detailmap.line_sep2.add(detailmap, 1, 11)
detailmap.frame.add(detailmap, 0, 0)

# Objects for deckmap
deckmap = se.Map(height-1, width, " ")
decksubmap = se.Submap(deckmap, 0, 0, height=height-1, width=width)
decksubmap.exit_label = se.Text("1: Exit  ")
decksubmap.move_label = se.Text("2: Move    ")
decksubmap.move_free = se.Text("3: Free")
# adding
decksubmap.exit_label.add(decksubmap, 0, decksubmap.height-1)
decksubmap.move_label.add(decksubmap, 9, decksubmap.height-1)
decksubmap.move_free.add(decksubmap, 20, decksubmap.height-1)

# objects relevant for fight()
fightmap = se.Map(height-1, width, " ")
fightmap.frame_big = se.Frame(height=fightmap.height-5, width=fightmap.width, corner_chars=["_", "_", "|", "|"], horizontal_chars=["_", "_"], state="float")
fightmap.frame_small = se.Frame(height=4, width=fightmap.width, state="float")
fightmap.e_underline = se.Text("----------------+", state="float")
fightmap.e_sideline = se.Square("|", 1, 3, state="float")
fightmap.p_upperline = se.Text("+----------------", state="float")
fightmap.p_sideline = se.Square("|", 1, 4, state="float")
fightmap.outp = se.Text("", state="float")
fightmap.label = se.Text("1: Attack  2: Run!  3: Inv.  4: Deck")
fightmap.shines = [se.Object(Color.thicc+Color.green+"*"+Color.reset) for i in range(4)]
deadico1 = se.Text("""
    \ /
     o
    / \\""")
deadico2 = se.Text("""

     o
""")
pball = se.Text("""   _____
  /_____\\
  |__O__|
  \_____/""")
# adding
fightmap.outp.add(fightmap, 1, fightmap.height-4)
fightmap.e_underline.add(fightmap, 1, 4)
fightmap.e_sideline.add(fightmap, len(fightmap.e_underline.text), 1)
fightmap.p_upperline.add(fightmap, fightmap.width-1-len(fightmap.p_upperline.text), fightmap.height-10)
fightmap.frame_big.add(fightmap, 0, 0)
fightmap.p_sideline.add(fightmap, fightmap.width-1-len(fightmap.p_upperline.text), fightmap.height-9)
fightmap.frame_small.add(fightmap, 0, fightmap.height-5)
fightmap.label.add(fightmap, 0, fightmap.height-1)

# evomap
evomap = se.Map(height-1, width, " ")
evomap.frame_small = se.Frame(height=4, width=evomap.width, state="float")
evomap.outp = se.Text("", state="float")
# adding
evomap.frame_small.add(evomap, 0, evomap.height-5)
evomap.outp.add(evomap, 1, evomap.height-4)

# fightbox
fightbox = ChooseBox(6, 25, "Attacks", index_x=1)

# invbox
invbox = ChooseBox(height-3, 35, "Inventory", "R:remove")
invbox.money_label = se.Text(str(figure.get_money())+"$")
# adding
invbox.add_ob(invbox.money_label, invbox.width-2-len(invbox.money_label.text), 0)
# invbox2
invbox2 = Box(7, 21)
invbox2.desc_label = se.Text(" ")
# adding
invbox2.add_ob(invbox2.desc_label, 1, 1)
# every possible item for the inv has to have such an object
# invbox.poketeball = InvItem("poketeball", "Poketeball", "A ball you can use to catch Poketes", 2, fight_poketeball)

# items
for name in items:
    exec(f'invbox.{name} = InvItem(name, items[name]["pretty_name"], items[name]["desc"], items[name]["price"], {items[name]["fn"]})')

# NPCs
for npc in npcs:
    exec(f'{npcs[npc]["map"]}.{npc} = NPC(npc, npcs[npc]["texts"], npcs[npc]["fn"], npcs[npc]["args"])')
    exec(f'{npcs[npc]["map"]}.{npc}.add({npcs[npc]["map"]}, npcs[npc]["x"], npcs[npc]["y"])')

# fight_invbox
fight_invbox = ChooseBox(height-3, 35, "Inventory")

# buybox
buybox = ChooseBox(height-3, 35, "Shop")
buybox.money_label = se.Text(str(figure.get_money())+"$")
# adding
buybox.add_ob(buybox.money_label, buybox.width-2-len(buybox.money_label.text), 0)
# shopbox2
buybox2 = Box(7, 21,)
buybox2.desc_label = se.Text(" ")
# adding
buybox2.add_ob(buybox2.desc_label, 1, 1)

__t = time.time() - __t

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
