#!/usr/bin/env python3
# This software is licensed under the GPL3
# You should have gotten an copy of the GPL3 license anlonside this software
# Feel free to contribute what ever you want to this game
# New Pokete contributions are especially welcome
# For this see the comments in the definations area
# You can contribute here: https://github.com/lxgr-linux/pokete
# Thanks to MaFeLP for your code review and your great feedback

import random
import time
import os
import sys
import threading
import math
import socket
from pathlib import Path
import pprint as pp
import scrap_engine as se
from pokete_data import *
from pokete_classes import *
from pokete_general_use_fns import *
from release import *

__t = time.time()

# Class definition
##################

class HightGrass(se.Object):
    def action(self, ob):
        if random.randint(0,8) == 0:
            fight(Poke("__fallback__", 0)
                    if len([poke for poke in figure.pokes[:6]
                          if poke.hp > 0]) == 0
                    else [poke for poke in figure.pokes[:6] if poke.hp > 0][0],
                Poke(random.choices(self.arg_proto["pokes"],
                                    weights=[pokes[i]["rarity"]
                                            for i in self.arg_proto["pokes"]])[0],
                    random.choices(list(range(self.arg_proto["minlvl"],
                                            self.arg_proto["maxlvl"])))[0],
                    player=False, shiny=(random.randint(0, 500) == 0)))


class Poketeball(se.Object):
    def __init__(self, name):
        self.name = name
        super().__init__(Color.thicc+Color.red+"o"+Color.reset, state="float")

    def action(self, ob):
        figure.give_item("poketeball")
        used_npcs.append(self.name)
        self.remove()


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
        try:
            exclamation.add(movemap, self.x-movemap.x, self.y-1-movemap.y)
        except se.CoordinateError:
            pass
        movemap.show()
        time.sleep(1)
        exclamation.remove()
        movemap_text(self.x, self.y, self.texts)
        self.fn()

    def fn(self):
        if self.__fn is not None:
            eval(self.__fn)(*self.args)

    @staticmethod
    def give(_map, npc, name, item):
        item = getattr(Inv, item)
        _map = ob_maps[_map]
        npc = getattr(_map, npc)
        npc.will = False
        used_npcs.append(npc.name)
        if ask_bool(movemap,
                    f"{name} gifted you a '{item.pretty_name}'. Do you want to accept it?"):
            figure.give_item(item.name)


class Trainer(se.Object):
    def __init__(self, poke, name, gender, texts, lose_texts, no_poke_texts,
                win_texts, sx, sy, arg_proto={}):
        super().__init__("a", state="solid")
        for i in ["arg_proto", "name", "gender", "poke", "texts",
                "lose_texts", "no_poke_texts", "win_texts", "sx", "sy"]:
            exec(f"self.{i} = {i}")

    def do(self, map):
        if figure.has_item("shut_the_fuck_up_stone"):
            return
        if figure.x == self.x and self.poke.hp > 0 and (self.name not in used_npcs or not settings.save_trainers):
            for i in range(figure.y+1 if figure.y < self.y else self.y+1, self.y if figure.y < self.y else figure.y):
                if any(j.state == "solid" for j in map.obmap[i][self.x]):
                    return
            movemap.full_show()
            time.sleep(0.7)
            try:
                exclamation.add(movemap, self.x-movemap.x, self.y-1-movemap.y)
            except se.CoordinateError:
                pass
            movemap.show()
            time.sleep(1)
            exclamation.remove()
            while self.y != figure.y+(2 if self.y > figure.y else -2):
                self.set(self.x, self.y+(-1 if self.y > figure.y+1 or self.y == figure.y-1 else 1))
                movemap.full_show()
                time.sleep(0.3)
            if any([poke.hp > 0 for poke in figure.pokes[:6]]):
                movemap_text(self.x, self.y, self.texts)
                winner = fight([poke for poke in figure.pokes[:6] if poke.hp > 0][0],
                                self.poke, info={"type": "duel", "player": self})
                movemap_text(self.x, self.y, {True : self.lose_texts,
                            False: self.win_texts+[" < Here u go 20$"]}[winner == self.poke])
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
        movemap_text(int(movemap.width/2), 3,
                     [" < Welcome to the Pokete-Center",
                      " < What do you want to do?",
                      " < a: See your full deck\n b: Heal all your Poketes\n c: Go"])
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
                movemap_text(int(movemap.width/2), 3, [" < ...",
                                                        " < Your Poketes are now healed!"])
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
        movemap_text(int(movemap.width/2), 3, [" < Welcome to the Pokete-Shop",
                                                " < Wanna buy something?"])
        buy()
        movemap.full_show(init=True)
        movemap_text(int(movemap.width/2), 3, [" < Have a great day!"])


class CenterDor(se.Object):
    def action(self, ob):
        figure.remove()
        i = figure.map.name
        figure.add(figure.oldmap,
                   figure.oldmap.dor.x
                    if figure.map == centermap
                    else figure.oldmap.shopdor.x,
                   figure.oldmap.dor.y+1
                    if figure.map == centermap
                    else figure.oldmap.shopdor.y+1)
        figure.oldmap = ob_maps[i]
        game(figure.map)


class Dor(se.Object):
    def action(self, ob):
        figure.remove()
        i = figure.map.name
        figure.add(ob_maps[self.arg_proto["map"]], self.arg_proto["x"],
                   self.arg_proto["y"])
        figure.oldmap = ob_maps[i]
        game(ob_maps[self.arg_proto["map"]])


class ChanceDor(Dor):
    def action(self, ob):
        if random.randint(0, self.arg_proto["chance"]) == 0:
            super().action(ob)


class Poke():
    def __init__(self, poke, xp, _hp="SKIP", _attacks=None,
                 player=True, shiny=False):
        self.inf = pokes[poke]
        self.enem = None
        self.oldhp = 0
        self.xp = xp
        self.identifier = poke
        self.shiny = shiny
        if _attacks is not None:
            assert (len(_attacks) <= 4), f"A Pokete {poke} can't have more than 4 attacks!"
            self.attacks = [atc for atc in _attacks
                    if self.lvl() >= attacks[atc]["min_lvl"]]
        else:
            self.attacks = self.inf["attacks"][:4]
        for name in ["hp", "name", "miss_chance", "lose_xp",
                    "evolve_poke", "evolve_lvl"]:
            setattr(self, name, self.inf[name])
        if self.shiny:
            self.hp += 5
        self.set_player(player)
        self.types = [eval(i) for i in self.inf["types"]]
        self.type = self.types[0]
        self.full_hp = self.hp
        self.full_miss_chance = self.miss_chance
        self.hp_bar = se.Text(8*"#", esccode=Color.green, state="float")
        if _hp != "SKIP":
            self.hp = _hp if _hp <= self.full_hp else self.hp
            self.health_bar_maker(self.hp)
        self.desc = se.Text(liner(self.inf["desc"], se.screen_width-34))
        self.ico = se.Box(4, 11)
        for ico in self.inf["ico"]:
            esccode = (str.join("", [getattr(Color, i) for i in ico["esc"]])
                                if ico["esc"] is not None
                                else "")
            self.ico.add_ob(se.Text(ico["txt"], state="float",
                            esccode=esccode,
                            ignore=f'{esccode} {Color.reset}'), 0, 0)
        self.text_hp = se.Text(f"HP:{self.hp}", state="float")
        self.text_lvl = se.Text(f"Lvl:{self.lvl()}", state="float")
        self.text_name = se.Text(self.name,
                                 esccode=Color.underlined+(Color.yellow
                                     if self.shiny
                                     else ""),
                                 state="float")
        self.text_xp = se.Text(f"XP:{self.xp-(self.lvl()**2-1)}/{((self.lvl()+1)**2-1)-(self.lvl()**2-1)}", state="float")
        self.text_type = se.Text(self.type.name.capitalize(),
                                 state="float", esccode=self.type.color)
        self.tril = se.Object("<", state="float")
        self.trir = se.Object(">", state="float")
        self.attac_obs = []
        self.atc_labels = []
        self.pball_small = se.Object("o")
        self.set_vars()
        self.effects = []

    def set_player(self, player):
        self.player = player
        self.affil = "you" if self.player else "enemy"
        self.ext_name = f'{self.name}({self.affil})'

    def set_vars(self):
        for name in ["atc", "defense", "initiative"]:
            setattr(self, name, self.lvl()+self.inf[name]+(2 if self.shiny else 0))
        i = [Attack(atc) for atc in self.attacks if self.lvl() >= attacks[atc]["min_lvl"]]
        for old_ob, obj in zip(self.attac_obs, i):
            obj.ap = old_ob.ap
        self.attac_obs = i
        for obj in self.atc_labels:
            fightbox.rem_ob(obj)
        self.atc_labels = [se.Text("") for i in self.attac_obs]
        self.label_rechar()

    def dict(self):
        return {"name": self.identifier, "xp": self.xp, "hp": self.hp,
                "ap": [atc.ap for atc in self.attac_obs],
                "effects": [repr(e) for e in self.effects],
                "attacks": self.attacks,
                "shiny": self.shiny}

    def set_ap(self, dict):
        for atc, ap in zip(self.attac_obs, dict):
            atc.ap = ap if ap != "SKIP" else atc.ap
        self.label_rechar()

    def label_rechar(self):
        for i, atc in enumerate(self.attac_obs):
            self.atc_labels[i].rechar(f"{i+1}: ")
            self.atc_labels[i] += se.Text(atc.name, esccode=atc.type.color) + se.Text(f"-{atc.ap}")

    def lvl(self):
        return int(math.sqrt(self.xp+1))

    def health_bar_maker(self, oldhp):
        bar_num = round(oldhp*8/self.full_hp)
        esccode = Color.red
        for size, color in zip([6, 2], [Color.green, Color.yellow]):
            if bar_num > size:
                esccode = color
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
            for e in self.effects:
                e.remove()
            for e in self.effects:
                if (i := e.effect()) == 1:
                    self.label_rechar()
                    return
                elif i == 0:
                    pass
            if any([type(i) is EffectConfusion for i in self.effects]):
                self.enem = enem = self
            else:
                self.enem = enem
            enem.oldhp = enem.hp
            self.oldhp = self.hp
            effectivity = (1.3 if enem.type.name in attac.type.effective
                            else 0.5
                            if enem.type.name in attac.type.ineffective
                            else 1)
            n_hp = round((self.atc * attac.factor / (enem.defense if enem.defense >= 1 else 1))*random.choices([0, 0.75, 1, 1.26], weights=[attac.miss_chance+self.miss_chance, 1, 1, 1], k=1)[0]*effectivity)
            enem.hp -= max(n_hp, 0)
            enem.hp = max(enem.hp, 0)
            time.sleep(0.4)
            for i in attac.move:
                exec(f"self.move_{i}()")
            exec(attac.action)
            attac.ap -= 1
            fightmap.outp.outp(f'{self.ext_name} used {attac.name}! {self.name+" missed!" if n_hp == 0 and attac.factor != 0 else ""}\n{"That was very effective! " if effectivity == 1.3 and n_hp > 0 else ""}{"That was not effective! " if effectivity == 0.5 and n_hp > 0 else ""}')
            if enem == self:
                time.sleep(1)
                fightmap.outp.outp(f'{self.ext_name} hurt it self!')
            if n_hp != 0 or attac.factor == 0:
                attac.give_effect(enem)
            for obj in [enem, self] if enem != self else [enem]:
                obj.health_bar_updater(obj.oldhp)
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

    def move_arch(self):
        if self.enem == self:
            return
        line = se.Line(Color.thicc+Color.yellow+"-"+Color.reset,
                        self.enem.ico.x-self.ico.x+(-11 if self.player else 11),
                        self.enem.ico.y-self.ico.y, l_type="crippled")
        line.add(self.ico.map, self.ico.x+(11 if self.player else -1),
                 self.ico.y+1)
        self.ico.map.show()
        time.sleep(1)
        line.remove()
        del line

    def move_throw(self, txt="#"):
        if self.enem == self:
            return
        line = se.Line(" ", self.enem.ico.x-self.ico.x+(-11 if self.player else 11),
                        self.enem.ico.y-self.ico.y, l_type="crippled")
        line.add(self.ico.map, self.ico.x+(11 if self.player else -1),
                 self.ico.y+1)
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

    def move_shine(self, ico=Color.thicc+Color.green+"*"+Color.reset):
        shines = [se.Object(ico) for i in range(4)]
        for i, x, y in zip(shines, [self.ico.x-1, self.ico.x+11, self.ico.x-1,
                                    self.ico.x+11],
                            [self.ico.y, self.ico.y, self.ico.y+3, self.ico.y+3]):
            i.add(self.ico.map, x, y)
            self.ico.map.show()
            time.sleep(0.2)
        time.sleep(0.2)
        for i in shines:
            i.remove()
        self.ico.map.show()

    def move_downgrade(self):
        self.enem.move_shine(ico=Color.thicc+Color.red+"-"+Color.reset)

    def evolve(self):
        if not self.player:
            return
        new = Poke(self.evolve_poke, self.xp, _attacks = self.attacks)
        self.ico.remove()
        self.ico.add(evomap, round(evomap.width/2-4),
                     round((evomap.height-8)/2))
        self.move_shine()
        evomap.outp.outp("Look!")
        time.sleep(0.5)
        evomap.outp.outp(f"{evomap.outp.text}\n{self.name} is evolving!")
        time.sleep(1)
        for i in range(8):
            for j, k in zip([self.ico, new.ico], [new.ico, self.ico]):
                j.remove()
                k.add(evomap, round(evomap.width/2-4),
                      round((evomap.height-8)/2))
                time.sleep(0.7-i*0.09999)
                evomap.show()
        self.ico.remove()
        new.ico.add(evomap, round(evomap.width/2-4),
                    round((evomap.height-8)/2))
        evomap.show()
        time.sleep(0.01)
        new.move_shine()
        evomap.outp.outp(f"{self.name} evolved to {new.name}!")
        time.sleep(5)
        figure.pokes[figure.pokes.index(self)] = new
        if new.identifier not in caught_poketes:
            caught_poketes.append(new.identifier)
        del self


class Station(se.Square):
    choosen = None
    obs = []
    def __init__(self, associate, additionals, width, height, char="#",
                 w_next="", a_next="", s_next="", d_next="", state="solid",
                 arg_proto={}):
        self.org_char = char
        self.associates = [associate]+[ob_maps[i] for i in additionals]
        self.color = ""
        super().__init__(char, width, height)
        for i in ["w_next", "a_next", "s_next", "d_next"]:
            exec(f"self.{i}={i}")
        Station.obs.append(self)

    def choose(self):
        self.rechar(Color.red+Color.thicc+self.org_char+Color.reset)
        Station.choosen = self
        roadmap.info_label.rechar(self.associates[0].pretty_name if
                                    self.has_been_visited() else
                                    "???")

    def unchoose(self):
        self.rechar(self.color+self.org_char+Color.reset)

    def next(self, ev):
        ev = ev.strip("'")
        if (ne := getattr(self, ev+"_next")) != "":
            self.unchoose()
            getattr(roadmap, ne).choose()

    def has_been_visited(self):
        return self.associates[0].name in visited_maps

    def is_city(self):
        return "pokecenter" in map_data[self.associates[0].name]["hard_obs"]

    def set_color(self, choose=False):
        if self.has_been_visited() and (self.is_city() if choose else True):
            self.color = Color.yellow
        else:
            self.color = ""
        self.unchoose()

class Figure(se.Object):
    def __init__(self, char, state="solid", arg_proto={}):
        super().__init__(char, state="solid", arg_proto={})
        self.__money = 10
        self.inv = {"poketeballs": 10}
        self.name = ""
        self.pokes = []
        self.oldmap = ob_maps["playmap_1"]
        self.direction = "t"

    def set_args(self, si):
        # processing data from save file
        self.name = si["user"]
        self.pokes = [Poke((si["pokes"][poke]["name"]
                                if type(poke) is int else poke),
                            si["pokes"][poke]["xp"], si["pokes"][poke]["hp"],
                            shiny = (False
                                    if "shiny" not in si["pokes"][poke]
                                    else si["pokes"][poke]["shiny"]),
                            _attacks = (si["pokes"][poke]["attacks"]
                                        if "attacks" in si["pokes"][poke]
                                        else None)
                            )
                    for poke in si["pokes"]]
        for j, poke in enumerate(self.pokes):
            poke.set_ap(si["pokes"][j]["ap"])
            if "effects" in si["pokes"][j]:
                for e in si["pokes"][j]["effects"]:
                    poke.effects.append(eval(e)(poke))
        try:
            if si["map"] in ["centermap", "shopmap"]:  # Looking if figure would be in centermap, so the player may spawn out of the center
                _map = ob_maps[si["map"]]
                self.add(_map, _map.dor_back1.x, _map.dor_back1.y-1)
            else:
                if self.add(ob_maps[si["map"]], si["x"], si["y"]) == 1:
                    raise se.CoordinateError(self, ob_maps[si["map"]], si["x"], si["y"])
        except se.CoordinateError:
            self.add(ob_maps["playmap_1"], 6, 5)
        # Those if statemnets are important to ensure compatibility with older versions
        if "oldmap" in si:
            self.oldmap = ob_maps[si["oldmap"]]
        if "inv" in si:
            self.inv = si["inv"]
        if "money" in si:
            self.set_money(si["money"])
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
        for cls in [inv, buy]:
            cls.money_label.rechar(str(self.__money)+"$")
            cls.box.set_ob(cls.money_label,
                           cls.box.width-2-len(cls.money_label.text), 0)

    def add_poke(self, poke, idx=None):
        poke.set_player(True)
        caught_poketes.append(poke.identifier)
        if idx is None:
            self.pokes.append(poke)
        else:
            self.pokes[idx] = poke

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
        for i in attacks[index]:
            exec(f"self.{i}=attacks[index][i]")
        self.type = eval(attacks[index]["type"])
        self.max_ap = self.ap
        self.label_name = se.Text(self.name, esccode=Color.underlined,
                state="float")
        self.label_ap = se.Text(f"AP:{self.ap}/{self.max_ap}", state="float")
        self.label_factor = se.Text(f"Attack:{self.factor}", state="float")
        self.label_desc = se.Text(self.desc[:int(width/2-1)], state="float")
        self.label_type_1 = se.Text("Type:", state="float")
        self.label_type_2 = se.Text(self.type.name.capitalize(),
                                    esccode=self.type.color, state="float")

    def give_effect(self, enem):
        if self.effect is not None:
            time.sleep(1.5)
            exec(f'{self.effect}().add(enem)')


class Setting(se.Box):
    def __init__(self, text, setting, options={}):
        super().__init__(0, 0)
        self.options = options
        self.setting = setting
        self.index = eval(f"[j for j in self.options].index({self.setting})")
        self.text = se.Text(text+": ", state="float")
        self.option_text = se.Text(self.options[eval(self.setting)],
                                   state="float")
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


class Deck:
    def __init__(self):
        self.map = se.Map(height-1, width, " ")
        self.submap = se.Submap(self.map, 0, 0, height=height-1, width=width)
        self.exit_label = se.Text("1: Exit  ")
        self.move_label = se.Text("2: Move    ")
        self.move_free = se.Text("3: Free")
        self.index = se.Object("*")
        # adding
        self.exit_label.add(self.submap, 0, self.submap.height-1)
        self.move_label.add(self.submap, 9, self.submap.height-1)
        self.move_free.add(self.submap, 20, self.submap.height-1)

    def rem_pokes(self, pokes):
        for poke in pokes:
            self.remove(poke)

    def __call__(self, pokes, label="Your full deck", in_fight=False):
        global ev
        ev = ""
        ret_action = None
        self.map.resize(5*int((len(pokes)+1)/2)+2, width, self.map.background)
        #decksubmap.resize(height-1, width)
        se.Text(label, esccode=Color.thicc).add(self.map, 2, 0)
        se.Square("|", 1, self.map.height-2).add(self.map,
                                                 round(self.map.width/2), 1)
        StdFrame2(self.map.height-1, self.map.width).add(self.map, 0, 0)
        self.move_label.rechar("2: Move    ")
        indici = []
        self.add_all(pokes, True)
        self.index.index = 0
        if len(pokes) > 0:
            self.index.add(self.map,
                           pokes[self.index.index].text_name.x+len(pokes[self.index.index].text_name.text)+1,
                           pokes[self.index.index].text_name.y)
        self.submap.full_show(init=True)
        while True:
            if ev in ["'1'", "Key.esc", "'q'"]:
                ev = ""
                self.rem_pokes(pokes)
                while len(self.map.obs) > 0:
                    self.map.obs[0].remove()
                self.submap.set(0, 0)
                if ret_action != None:
                    eval(ret_action)
                return
            elif ev == "'2'":
                ev = ""
                if len(pokes) == 0:
                    continue
                if indici == []:
                    indici.append(self.index.index)
                    self.move_label.rechar("2: Move to ")
                else:
                    indici.append(self.index.index)
                    figure.pokes[indici[0]], figure.pokes[indici[1]] = pokes[indici[1]], pokes[indici[0]]
                    pokes = figure.pokes[:len(pokes)]
                    indici = []
                    self.rem_pokes(pokes)
                    self.index.set(0, self.map.height-1)
                    self.add_all(pokes)
                    self.index.set(pokes[self.index.index].text_name.x+len(pokes[self.index.index].text_name.text)+1, pokes[self.index.index].text_name.y)
                    self.move_label.rechar("2: Move    ")
                    self.submap.full_show()
            elif ev == "'3'":
                ev = ""
                if ask_bool(self.submap, f"Do you really want to free {figure.pokes[self.index.index].name}?"):
                    self.rem_pokes(pokes)
                    figure.pokes[self.index.index] = Poke("__fallback__", 10, 0)
                    pokes = figure.pokes[:len(pokes)]
                    self.add_all(pokes)
                    self.index.set(pokes[self.index.index].text_name.x+len(pokes[self.index.index].text_name.text)+1, pokes[self.index.index].text_name.y)
                    balls_label_rechar()
            elif ev in ["'w'", "'a'", "'s'", "'d'"]:
                self.control(pokes, ev)
                ev = ""
            elif ev == "Key.enter":
                ev = ""
                if len(pokes) == 0:
                    continue
                if in_fight:
                    if pokes[self.index.index].hp > 0:
                        self.rem_pokes(pokes)
                        while len(self.map.obs) > 0:
                            self.map.obs[0].remove()
                        self.submap.set(0, 0)
                        return self.index.index
                else:
                    self.rem_pokes(pokes)
                    ret_action = detail(pokes[self.index.index])
                    self.add_all(pokes)
                    if ret_action is not None:
                        ev = "'q'"
                        continue
                    self.submap.full_show(init=True)
            std_loop()
            if len(pokes) > 0 and self.index.y-self.submap.y +6 > self.submap.height:
                self.submap.set(self.submap.x, self.submap.y+1)
            elif len(pokes) > 0 and self.index.y-1 < self.submap.y:
                self.submap.set(self.submap.x, self.submap.y-1)
            time.sleep(0.05)
            self.submap.full_show()

    def add(self, poke, map, x, y, in_deck=True):
        poke.text_name.add(map, x+12, y+0)
        if poke.identifier != "__fallback__":
            for obj, _x, _y in zip([poke.ico, poke.text_lvl, poke.text_hp,
                                    poke.tril, poke.trir, poke.hp_bar, poke.text_xp],
                                    [0, 12, 12, 18, 27, 19, 12],
                                    [0, 1, 2, 2, 2, 2, 3]):
                obj.add(map, x+_x, y+_y)
            if figure.pokes.index(poke) < 6 and in_deck:
                poke.pball_small.add(map, round(map.width/2)-1 if figure.pokes.index(poke) % 2 == 0 else map.width-2, y)
            for e in poke.effects:
                e.add_label()


    def remove(self, poke):
        for obj in [poke.ico, poke.text_name, poke.text_lvl, poke.text_hp,
                    poke.tril, poke.trir, poke.hp_bar, poke.text_xp,
                    poke.pball_small]:
            obj.remove()
        for e in poke.effects:
            e.cleanup()

    def add_all(self, pokes, init=False):
        j = 0
        for i, poke in enumerate(pokes):
            self.add(poke, self.map, 1 if i % 2 == 0 else round(self.map.width/2)+1, j*5+1)
            if i % 2 == 0 and init:
                se.Square("-", self.map.width-2, 1).add(self.map, 1, j*5+5)
            if i % 2 == 1:
                j += 1

    def control(self, pokes, ev):
        if len(pokes) <= 1:
            return
        for con, stat, fir, sec in zip(["'a'", "'d'", "'s'", "'w'"],
                                    [self.index.index != 0, self.index.index != len(pokes)-1, self.index.index+2 < len(pokes), self.index.index-2 >= 0],
                                    [-1, 1, 2, -2],
                                    [len(pokes)-1, 0, self.index.index % 2, [i for i in range(len(pokes)) if i % 2 == self.index.index % 2][-1]]):
            if ev == con:
                if stat:
                    self.index.index += fir
                else:
                    self.index.index = sec
                break
        self.index.set(pokes[self.index.index].text_name.x+len(pokes[self.index.index].text_name.text)+1, pokes[self.index.index].text_name.y)


class Detail(Deck):
    def __init__(self):
        self.map = se.Map(height-1, width, " ")
        self.name_label = se.Text("Details", esccode=Color.thicc)
        self.name_attacks = se.Text("Attacks", esccode=Color.thicc)
        self.frame = StdFrame2(17, self.map.width, state="float")
        self.attack_defense = se.Text("Attack:   Defense:")
        self.world_actions_label = se.Text("Abilities:")
        self.type_label = se.Text("Type:")
        self.initiative_label = se.Text("Initiative:")
        self.exit_label = se.Text("1: Exit")
        self.ability_label = se.Text("2: Use ability")
        self.line_sep1 = se.Square("-", self.map.width-2, 1, state="float")
        self.line_sep2 = se.Square("-", self.map.width-2, 1, state="float")
        self.line_middle = se.Square("|", 1, 10, state="float")
        # adding
        self.name_label.add(self.map, 2, 0)
        self.name_attacks.add(self.map, 2, 6)
        self.attack_defense.add(self.map, 13, 5)
        self.world_actions_label.add(self.map, 24, 4)
        self.type_label.add(self.map, 36, 5)
        self.initiative_label.add(self.map, 49, 5)
        self.exit_label.add(self.map, 0, self.map.height-1)
        self.ability_label.add(self.map, 9, self.map.height-1)
        self.line_sep1.add(self.map, 1, 6)
        self.line_sep2.add(self.map, 1, 11)
        self.frame.add(self.map, 0, 0)
        self.line_middle.add(self.map, round(self.map.width/2), 7)

    def __call__(self, poke, abb=True):
        global ev
        ret_action = None
        self.add(poke, self.map, 1, 1, False)
        abb_obs = [i for i in poke.attac_obs
                    if i.world_action != ""]
        if abb_obs != [] and abb:
            self.world_actions_label.rechar("Abilities:"+" ".join([i.name
                                                for i in abb_obs]))
            self.ability_label.rechar("2: Use ability")
        else:
            self.world_actions_label.rechar("")
            self.ability_label.rechar("")
        self.attack_defense.rechar(f"Attack:{poke.atc}{(4-len(str(poke.atc)))*' '}Defense:{poke.defense}")
        self.initiative_label.rechar(f"Initiative:{poke.initiative}")
        for obj, x, y in zip([poke.desc, poke.text_type], [34, 41], [2, 5]):
            obj.add(self.map, x, y)
        for atc, x, y in zip(poke.attac_obs, [1, round(self.map.width/2)+1, 1,
                            round(self.map.width/2)+1], [7, 7, 12, 12]):
            atc.temp_i = 0
            atc.temp_j = -30
            atc.label_desc.rechar(atc.desc[:int(width/2-1)])
            atc.label_ap.rechar(f"AP:{atc.ap}/{atc.max_ap}")
            for label, _x, _y in zip([atc.label_name, atc.label_factor,
                                        atc.label_type_1, atc.label_type_2,
                                        atc.label_ap, atc.label_desc],
                                        [0, 0, 11, 16, 0, 0], [0, 1, 1, 1, 2, 3]):
                label.add(self.map, x+_x, y+_y)
        self.map.show(init=True)
        while True:
            if ev in ["'1'", "Key.esc", "'q'"]:
                ev = ""
                self.remove(poke)
                for obj in [poke.desc, poke.text_type]:
                    obj.remove()
                for atc in poke.attac_obs:
                    for obj in [atc.label_name, atc.label_factor, atc.label_ap,
                                atc.label_desc, atc.label_type_1, atc.label_type_2]:
                        obj.remove()
                    del atc.temp_i, atc.temp_j
                return ret_action
            elif ev == "'2'" and abb_obs != [] and abb:
                with ChooseBox(len(abb_obs)+2, 25, name="Abilities",
                        c_obs=[se.Text(i.name)
                            for i in abb_obs]).center_add(self.map) as box:
                     while True:
                        if ev in ["'s'", "'w'"]:
                            box.input(ev)
                            self.map.show()
                            ev = ""
                        elif ev == "Key.enter":
                            ret_action = abb_obs[box.index.index].world_action
                            ev = "'q'"
                            break
                        elif ev in ["Key.esc", "'q'"]:
                            ev = ""
                            break
                        std_loop()
                        time.sleep(0.05)
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
            self.map.show()


class Inv:
    def __init__(self):
        self.box = ChooseBox(height-3, 35, "Inventory", "R:remove")
        self.box2 = Box(7, 21)
        self.money_label = se.Text(str(figure.get_money())+"$")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label, self.box.width-2-len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def __call__(self):
        global ev
        ev = ""
        items = self.add()
        with self.box.add(movemap, movemap.width-35, 0):
            while True:
                if ev in ["'s'", "'w'"]:
                    self.box.input(ev)
                    ev = ""
                elif ev in ["'4'", "Key.esc", "'q'"]:
                    break
                elif ev == "Key.enter":
                    obj = items[self.box.index.index]
                    self.box2.name_label.rechar(obj.pretty_name)
                    self.desc_label.rechar(liner(obj.desc, 19))
                    self.box2.add(movemap, self.box.x-19, 3)
                    ev = ""
                    while True:
                        if ev == "exit":
                            raise KeyboardInterrupt
                        elif ev in ["Key.enter", "Key.esc", "'q'"]:
                            ev = ""
                            self.box2.remove()
                            if type(obj) is LearnDisc:
                                if ask_bool(movemap, f"Do you want to teach '{obj.attack_dict['name']}'?"):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck(figure.pokes[:6],
                                                    label="Your deck",
                                                    in_fight=True)
                                        if index is None:
                                            ex_cond = False
                                            movemap.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        if eval(obj.attack_dict['type']) in poke.types:
                                            break
                                        else:
                                            ex_cond = ask_bool(movemap, f"You cant't teach '{obj.attack_dict['name']}' to '{poke.name}'! \nDo you want to continue?")
                                    if not ex_cond:
                                        break
                                    if  LearnAttack(poke, movemap)(obj.attack_name):
                                        items = self.rem_item(obj.name, items)
                                        if len(items) == 0:
                                            break
                                    ev = ""
                            break
                        time.sleep(0.05)
                        movemap.show()
                elif ev == "'r'":
                    if ask_bool(movemap, f"Do you really want to throw {items[self.box.index.index].pretty_name} away?"):
                        items = self.rem_item(items[self.box.index.index].name, items)
                        if len(items) == 0:
                            break
                    ev = ""
                std_loop()
                time.sleep(0.05)
                movemap.show()
        self.box.remove_c_obs()

    def rem_item(self, name, items):
        figure.remove_item(name)
        for obj in self.box.c_obs:
            obj.remove()
        self.box.remove_c_obs()
        items = self.add()
        if items == []:
            return items
        if self.box.index.index >= len(items):
            self.box.set_index(len(items)-1)
        return items

    def add(self):
        items = [getattr(self, i) for i in figure.inv if figure.inv[i] > 0]
        self.box.add_c_obs([se.Text(f"{i.pretty_name}s : {figure.inv[i.name]}") for i in items])
        return items


class Buy:
    def __init__(self):
        self.box = ChooseBox(height-3, 35, "Shop")
        self.box2 = Box(7, 21,)
        self.items = [Inv.poketeball, Inv.superball, Inv.healing_potion,
                    Inv.super_potion, Inv.ap_potion]
        self.box.add_c_obs([se.Text(f"{obj.pretty_name} : {obj.price}$")
                                for obj in self.items])
        self.money_label = se.Text(str(figure.get_money())+"$")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width-2-len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def __call__(self):
        global ev
        ev = ""
        with self.box.add(movemap, movemap.width-35, 0):
            self.box2.add(movemap, self.box.x-19, 3)
            self.rechar()
            movemap.show()
            while True:
                if ev in ["'s'", "'w'"]:
                    self.box.input(ev)
                    self.rechar()
                    ev = ""
                elif ev in ["Key.esc", "'q'"]:
                    break
                elif ev == "Key.enter":
                    obj = self.items[self.box.index.index]
                    if figure.get_money()-obj.price >= 0:
                        figure.add_money(-obj.price)
                        figure.give_item(obj.name)
                    ev = ""
                std_loop()
                time.sleep(0.05)
                movemap.show()
        self.box2.remove()

    def rechar(self):
        obj = self.items[self.box.index.index]
        self.box2.name_label.rechar(obj.pretty_name)
        self.desc_label.rechar(liner(obj.desc, 19))


class Menu:
    def __init__(self):
        self.box = ChooseBox(height-3, 35, "Menu")
        self.playername_label = se.Text("Playername: ", state="float")
        self.about_label = se.Text("About", state="float")
        self.save_label = se.Text("Save", state="float")
        self.exit_label = se.Text("Exit", state="float")
        self.realname_label = se.Text(session_info["user"], state="float")
        self.box.add_c_obs([self.playername_label,
                            Setting("Autosave", "settings.autosave",
                                    {True: "On", False: "Off"}),
                            Setting("Animations", "settings.animations",
                                    {True: "On", False: "Off"}),
                            Setting("Save trainers", "settings.save_trainers",
                                    {True: "On", False: "Off"}),
                            Setting("Colors", "settings.colors",
                                    {True: "On", False: "Off"}),
                            self.about_label, self.save_label,
                            self.exit_label])
        # adding
        self.box.add_ob(self.realname_label,
                        self.playername_label.rx+len(self.playername_label.text),
                        self.playername_label.ry)

    def __call__(self):
        global ev
        ev = ""
        self.realname_label.rechar(figure.name)
        with self.box.add(movemap, movemap.width-self.box.width, 0):
            while True:
                if ev == "Key.enter":
                    # Fuck python for not having case statements
                    if ((i := self.box.c_obs[self.box.index.index]) ==
                            self.playername_label):
                        figure.name = text_input(self.realname_label, movemap,
                                                 figure.name, 18, 17)
                        movemap.underline.remove()
                        movemap.balls_label.set(0, 1)
                        movemap.name_label.rechar(figure.name,
                                                  esccode=Color.thicc)
                        movemap.balls_label.set(4+len(movemap.name_label.text), movemap.height-2)
                        movemap.underline.add(movemap, 0, movemap.height-2)
                    elif i == self.save_label:  # When will python3.10 come out?
                        with InfoBox("Saving....", movemap):  # Shows a box displaying "Saving...." while saving
                            save()
                            time.sleep(1.5)
                    elif i == self.exit_label:
                        save()
                        exiter()
                    elif i == self.about_label:
                        about()
                    else:
                        i.change()
                    ev = ""
                elif ev in ["'s'", "'w'"]:
                    self.box.input(ev)
                    ev = ""
                elif ev in ["'e'", "Key.esc", "'q'"]:
                    ev = ""
                    break
                std_loop()
                time.sleep(0.05)
                movemap.show()


class About:
    def __init__(self):
        self.box = InfoBox(liner(f"Pokete v{VERSION} -- {CODENAME}\n by lxgr-linux <lxgr@protonmail.com>\n \n This software is licensed under the GPL3, you should have gotten a copy of the GPL3 license alongside this software.\n Feel free to contribute what ever you want to this game, new Pokete contributions are especially welcome.\n For this see the comments in the definations area.\n You can contribute here: https://github.com/lxgr-linux/pokete", 60, pre=""), map=movemap)

    def __call__(self):
        global ev
        with self.box:
            while True:
                if ev in ["Key.esc", "'q'"]:
                    ev = ""
                    break
                std_loop()
                time.sleep(0.05)


class RoadMap:
    def __init__(self, stations):
        self.box = Box(11, 40, "Roadmap")
        self.info_label = se.Text("")
        self.box.add_ob(self.info_label, 1, 1)
        for s in stations:
            obj = Station(ob_maps[s], **stations[s]['gen'])
            self.box.add_ob(obj, **stations[s]['add'])
            setattr(self, s, obj)

    def __call__(self, choose=False):
        global ev
        ev = ""
        for i in Station.obs:
            i.set_color(choose)
        [i for i in Station.obs
                if (figure.map
                    if figure.map not in [shopmap, centermap]
                    else figure.oldmap)
                in i.associates][0].choose()
        with self.box.add(movemap, movemap.width-self.box.width, 0):
            while True:
                if ev in ["'w'", "'a'", "'s'", "'d'"]:
                    Station.choosen.next(ev)
                    ev = ""
                elif ev in ["'3'", "Key.esc", "'q'"]:
                    ev = ""
                    break
                elif (ev == "Key.enter" and choose
                        and Station.choosen.has_been_visited()
                        and Station.choosen.is_city()):
                    return Station.choosen.associates[0]
                std_loop()
                time.sleep(0.05)
                movemap.show()
        Station.choosen.unchoose()


class Dex:
    def __init__(self, map):
        self.box = ChooseBox(map.height-3, 35, "Poketedex")
        self.detail_box = Box(16, 35)
        self.map = map
        self.idx = 0
        self.obs = []
        self.detail_info = se.Text("", state="float")
        self.detail_desc = se.Text("", state="float")
        self.detail_box.add_ob(self.detail_info, 16, 1)
        self.detail_box.add_ob(self.detail_desc, 3, 7)

    def add_c_obs(self):
        self.box.add_c_obs(self.obs[self.idx*(self.box.height-2):(self.idx+1)*(self.box.height-2)])

    def rem_c_obs(self):
        for c_ob in self.box.c_obs:
            c_ob.remove()
        self.box.remove_c_obs()

    def detail(self, poke):
        global ev
        ev = ""

        poke = Poke(poke, 0)
        desc_text = liner(poke.desc.text.replace("\n", " ")+
               (f"\n\n Evolves to {poke.evolve_poke if poke.evolve_poke in caught_poketes else '???'}."
                if poke.evolve_lvl != 0 else ""), 29)
        self.detail_box.resize(9+len(desc_text.split("\n")), 35)
        self.detail_box.name_label.rechar(poke.name)
        self.detail_box.add_ob(poke.ico, 3, 2)
        self.detail_desc.rechar(desc_text)
        self.detail_info.rechar("Type: ")
        self.detail_info += se.Text(poke.type.name.capitalize(),
                                    esccode=poke.type.color) + se.Text((f"""
HP: {poke.hp}
Attack: {poke.atc}
Defense: {poke.defense}
Initiative: {poke.initiative}"""))
        with self.detail_box.center_add(self.map):
            while True:
                if ev in ["'e'", "Key.esc", "'q'"]:
                    ev = ""
                    break
                std_loop()
                time.sleep(0.05)
                self.map.show()
        self.detail_box.rem_ob(poke.ico)


    def __call__(self, pokes):
        global ev
        ev = ""
        self.idx = 0

        p_dict = {i[1]: i[-1] for i in
            sorted([(pokes[j]["types"][0], j, pokes[j])
                        for j in list(pokes)[1:]])}
        self.obs = [se.Text(f"{i+1} {p_dict[poke]['name'] if poke in caught_poketes else '???'}", state="float")
                for i, poke in enumerate(p_dict)]
        self.add_c_obs()
        with self.box.add(self.map, self.map.width-self.box.width, 0):
            while True:
                for event, idx, n_idx, add, idx_2 in zip(["'s'", "'w'"],
                        [len(self.box.c_obs)-1, 0], [0, self.box.height-3],
                        [1, -1], [-1, 0]):
                    if ev == event and self.box.index.index == idx:
                        if self.box.c_obs[self.box.index.index] != self.obs[idx_2]:
                            self.rem_c_obs()
                            self.idx += add
                            self.add_c_obs()
                            self.box.set_index(n_idx)
                        ev = ""
                if ev == "Key.enter":
                    if "???" not in self.box.c_obs[self.box.index.index].text:
                        self.detail(list(p_dict)[self.idx*(self.box.height-2)
                                                 +self.box.index.index])
                    ev = ""
                elif ev in ["'s'", "'w'"]:
                    self.box.input(ev)
                    ev = ""
                elif ev in ["'e'", "Key.esc", "'q'"]:
                    ev = ""
                    break
                std_loop()
                time.sleep(0.05)
                self.map.show()
            self.rem_c_obs()


class Help(About):
    def __init__(self, map):
        self.map = map
        self.help_text = """
Controls:
'w':up, 'a':left,
's':down, 'd':right,
'e':menu

When walking into the high grass (';') you may get attacked
by wild Poketes, those can be killed or weakened and caught.
NPCs will talk to you when walking up to them.
For more information about how to play this game, check out
https://git.io/JRRqe
"""
        self.box = InfoBox(self.help_text, self.map)
        self.box.name_label.rechar("Help")
        self.box.info_label.rechar("q:close")


class LearnAttack():
    def __init__(self, poke, _map=None):
        if _map is None:
            self.map = fightmap
        else:
            self.map = _map
        self.poke = poke
        self.box = ChooseBox(6, 25, name="Attacks", info="1: Details")

    def __call__(self, attack=None):
        global ev
        if attack is None:
            pool = [i for i in attacks
                    if attacks[i]["type"] in
                        [i.name for i in self.poke.types]
                        and attacks[i]["is_generic"]]
            full_pool = [i for i in self.poke.inf["attacks"]+
                        self.poke.inf["pool"]+pool
                            if i not in self.poke.attacks
                            and attacks[i]["min_lvl"] <= self.poke.lvl()]
            if len(full_pool) == 0:
                return False
            new_attack = random.choice(full_pool)
        else:
            new_attack = attack
        if ask_bool(self.map, f"{self.poke.name} wants to learn {attacks[new_attack]['name']}!"):
            if len(self.poke.attac_obs) != len(self.poke.attacks):
                self.poke.attacks[-1] = new_attack
            elif len(self.poke.attacks) < 4:
                self.poke.attacks.append(new_attack)
            else:
                self.box.add_c_obs([se.Text(f"{i+1}: {j.name}", state=float)
                    for i, j in enumerate(self.poke.attac_obs)])
                with self.box.center_add(self.map):
                    while True:
                        if ev in ["'s'", "'w'"]:
                            self.box.input(ev)
                            self.map.show()
                            ev = ""
                        elif ev == "Key.enter":
                            self.poke.attacks[self.box.index.index] = new_attack
                            with InfoBox(f"{self.poke.name} learned {attacks[new_attack]['name']}!", self.map):
                                time.sleep(3)
                            ev = ""
                            break
                        elif ev == "'1'":
                            ev = ""
                            detail(self.poke, False)
                            self.map.show(init=True)
                        elif ev in ["Key.esc", "'q'"]:
                            ev = ""
                            break
                        std_loop()
                        time.sleep(0.05)
                self.box.remove_c_obs()
            self.poke.set_vars()
            return True
        else:
            return False


# General use functions
#######################

def heal():
    for poke in figure.pokes:
        poke.hp = poke.full_hp
        poke.effects = []
        poke.miss_chance = poke.full_miss_chance
        poke.text_hp.rechar(f"HP:{poke.hp}")
        poke.set_vars()
        poke.health_bar_maker(poke.hp)
        for atc in poke.attac_obs:
            atc.ap = atc.max_ap
        poke.label_rechar()
        balls_label_rechar()


def autosave():
    while True:
        time.sleep(300)
        if settings.autosave:
            save()


def save():
    session_info = {
        "user": figure.name,
        "ver": VERSION,
        "map": figure.map.name,
        "oldmap": figure.oldmap.name,
        "x": figure.x,
        "y": figure.y,
        "pokes": {i: poke.dict() for i, poke in enumerate(figure.pokes)},
        "inv": figure.inv,
        "money": figure.get_money(),
        "settings": settings.dict(),
        "caught_poketes": list(dict.fromkeys(caught_poketes + [i.identifier for i in figure.pokes])),
        "visited_maps": visited_maps,
        "startup_time": __t,
        "used_npcs": list(dict.fromkeys(used_npcs)),  # filters doublicates from used_npcs
    }
    with open(home+SAVEPATH+"/pokete.py", "w+") as file:
        # writes the data to the save file in a nice format
        file.write(f"session_info = {pp.pformat(session_info, sort_dicts=False)}")


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


def text_input(obj, map, name, wrap_len, max_len=1000000):
    global ev
    ev = ""
    obj.rechar(hard_liner(wrap_len, name+"█"))
    bname = name
    map.show()
    while True:
        if ev in ["Key.enter", "Key.esc"]:
            ev = ""
            obj.rechar(hard_liner(wrap_len, name))
            map.show()
            return name
        elif ev == "Key.backspace":
            if len(name) <= 0:
                ev = ""
                obj.rechar(bname)
                map.show()
                return bname
            name = name[:-1]
            obj.rechar(hard_liner(wrap_len, name+"█"))
            map.show()
            ev = ""
        elif ev not in ["", "Key.enter", "exit", "Key.backspace", "Key.shift",
                        "Key.shift_r", "Key.esc"] and len(name) < max_len:
            if ev == "Key.space":
                ev = "' '"
            name += str(ev.strip("'"))
            obj.rechar(hard_liner(wrap_len, name+"█"))
            map.show()
            ev = ""
        std_loop()
        time.sleep(0.05)


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
    # This ensures the game does not crash when big chunks of text are displayed
    for c, i, j, k in zip([x, y], ["x", "y"], 
                          [movemap.width, movemap.height], [17, 10]):
        while c - getattr(movemap, i) + k >= j:
            movemap.set(movemap.x+(1 if i == "x" else 0),
                        movemap.y+(1 if i == "y" else 0))
            movemap.show()
            time.sleep(0.045)
    # End section
    multitext.rechar("")
    multitext.add(movemap, x-movemap.x+1, y-movemap.y)
    arr = [arr[i]+(" >" if i != len(arr)-1 else "") for i in range(len(arr))]
    for t in arr:
        ev = ""
        multitext.rechar("")
        for i in range(len(t)+1):
            multitext.outp(liner(t[:i], movemap.width-(x-movemap.x+1), "   "))
            time.sleep(0.045)
            std_loop()
            if ev != "":
                ev = ""
                break
        multitext.outp(liner(t, movemap.width-(x-movemap.x+1), "   "))
        while True:
            std_loop()
            if ev != "":
                break
            time.sleep(0.05)
    multitext.remove()


def movemap_add_obs():
    movemap.underline = se.Square("-", movemap.width, 1)
    movemap.name_label.add(movemap, 2, movemap.height-2)
    movemap.balls_label.add(movemap, 4+len(movemap.name_label.text),
                            movemap.height-2)
    movemap.underline.add(movemap, 0, movemap.height-2)
    movemap.label.add(movemap, 0, movemap.height-1)
    movemap.code_label.add(movemap, 0, 0)


# Functions for fight
#####################

def fight_clean_up(player, enemy):
    for obj in [enemy.text_name, enemy.text_lvl, enemy.text_hp, enemy.ico,
                enemy.hp_bar, enemy.tril, enemy.trir, player.text_name,
                player.text_lvl, player.text_hp, player.ico, player.hp_bar,
                player.tril, player.trir, enemy.pball_small]:
        obj.remove()
    fightbox.remove_c_obs()
    for i in [player, enemy]:
        for j in i.effects:
            j.cleanup()


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
    for obj, x, y in zip([enemy.tril, enemy.trir,
                          enemy.text_name, enemy.text_lvl,
                         enemy.text_hp, enemy.ico, enemy.hp_bar],
                         [7, 16, 1, 1, 1, fightmap.width-14, 8],
                         [3, 3, 1, 2, 3, 2, 3]):
        obj.add(fightmap, x, y)
    if enemy.identifier in caught_poketes:
        enemy.pball_small.add(fightmap, len(fightmap.e_underline.text)-1, 1)
    if player.identifier != "__fallback__":
        fightbox.add_c_obs(player.atc_labels)
        fightbox.set_index(0)
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


def fight_throw(obj, enem, info, chance, name):
    if obj.identifier == "__fallback__" or info["type"] == "duel":
        return 1
    fightmap.outp.rechar(f"You threw a {name.capitalize()}!")
    fast_change([enem.ico, deadico1, deadico2, pball], enem.ico)
    time.sleep(random.choice([1,2,3,4]))
    figure.remove_item(name)
    catch_chance = 20 if figure.map == ob_maps["playmap_1"] else 0
    for effect in enem.effects:
        catch_chance += effect.catch_chance
    if random.choices([True, False],
                      weights=[(enem.full_hp/enem.hp)*chance+catch_chance,
                      enem.full_hp], k=1)[0]:
        figure.add_poke(enem)
        fightmap.outp.outp(f"You catched {enem.name}")
        time.sleep(2)
        pball.remove()
        fight_clean_up(obj, enem)
        balls_label_rechar()
        return 2
    else:
        fightmap.outp.outp("You missed!")
        fightmap.show()
        pball.remove()
        enem.ico.add(fightmap, enem.ico.x, enem.ico.y)
        fightmap.show()


def fight_potion(obj, enem, info, hp, name):
    figure.remove_item(name)
    obj.oldhp = obj.hp
    if obj.hp + hp > obj.full_hp:
        obj.hp = obj.full_hp
    else:
        obj.hp += hp
    obj.health_bar_updater(obj.oldhp)
    return

def fight_heal_potion(obj, enem, info):
    return fight_potion(obj, enem, info, 5, "healing_potion")

def fight_super_potion(obj, enem, info):
    return fight_potion(obj, enem, info, 15, "super_potion")

def fight_poketeball(obj, enem, info):
    return fight_throw(obj, enem, info, 1, "poketeball")

def fight_superball(obj, enem, info):
    return fight_throw(obj, enem, info, 6, "superball")

def fight_hyperball(obj, enem, info):
    return fight_throw(obj, enem, info, 1000, "hyperball")

def fight_ap_potion(obj, enem, info):
    figure.remove_item("ap_potion")
    for atc in obj.attac_obs:
        atc.ap = atc.max_ap
    obj.label_rechar()


# Playmap extra action functions
# Those are adding additional actions to playmaps
#################################################

class Extra_Actions:

    @staticmethod
    def water(obs):
        if settings.animations and colors:
            for obj in obs:
                if random.randint(0, 9) == 0:
                    if " " not in obj.char:
                        obj.rechar([i for i in 
                                    [Color.lightblue+"~"+Color.reset,
                                        Color.blue+"~"+Color.reset]
                                        if i != obj.char][0])
                        if obj.x == figure.x and obj.y == figure.y:
                            figure.redraw()
    
    @staticmethod
    def playmap_4():
        Extra_Actions.water(ob_maps["playmap_4"].lake_1.obs)

    @staticmethod
    def playmap_11():
        Extra_Actions.water(ob_maps["playmap_11"].lake_1.obs)

    @staticmethod
    def playmap_18():
        Extra_Actions.water(ob_maps["playmap_18"].lake_1.obs)

    @staticmethod
    def playmap_21():
        Extra_Actions.water(ob_maps["playmap_21"].lake_1.obs)

    @staticmethod
    def playmap_7():
        for obj in ob_maps["playmap_7"].inner_walls.obs + ob_maps["playmap_7"].trainers + [getattr(ob_maps["playmap_7"], i) for i in map_data["playmap_7"]["balls"] if "playmap_7."+i not in used_npcs or not save_trainers]:
            if obj.added and math.sqrt((obj.y-figure.y)**2+(obj.x-figure.x)**2) <= 3:
                obj.rechar(obj.bchar)
            else:
                obj.rechar(" ")

# NPC functions
###############

def playmap_17_boy():
    if "choka" in [i.identifier for i in figure.pokes[:6]]:
        npc = ob_maps["playmap_17"].boy_1
        movemap_text(npc.x, npc.y,
                    [" < Oh, cool!", " < You have a Choka!",
                    " < I've never seen one before!", " < Here you go, 200$"])
        if ask_bool(movemap, "Young boy gifted you 200$. Do you want to accept it?"):
            figure.add_money(200)
        npc.will = False
        used_npcs.append(npc.name)
    else:
        movemap_text(npc.x, npc.y,
                    [" < In this region lives the würgos Pokete.",
                    f" < At level {pokes['würgos']['evolve_lvl']} it evolves to Choka.",
                    " < I have never seen one before!"])


def playmap_20_trader():
    npc = ob_maps["playmap_20"].trader_2
    movemap_text(npc.x, npc.y,
                [" < I've lived in this town for long time and therefore have found some cool Poketes.",
                " < Do you want to trade my cool Pokete?"])
    if ask_bool(movemap, "Do you want to trade a Pokete?"):
        if (index := deck(figure.pokes[:6], "Your deck", True)) is None:
            return
        figure.add_poke(Poke("ostri", 500), index)
        used_npcs.append(npc.name)
        with InfoBox(f"You received: {figure.pokes[index].name.capitalize()} at level {figure.pokes[index].lvl()}.", movemap):
            time.sleep(3)
        movemap_text(npc.x, npc.y, [" < Cool, huh?"])


def playmap_23_npc_8():
    npc = ob_maps["playmap_23"].npc_8
    if ask_bool(movemap, "The man gifted you 100$. Do you want to accept it?"):
        npc.will = False
        used_npcs.append(npc.name)
        figure.add_money(100)


# main functions
################

def teleport():
    if (obj := roadmap(choose=True)) is None:
        return
    else:
        cen_d = map_data[obj.name]["hard_obs"]["pokecenter"]
        Dor("", state="float", arg_proto={"map": obj.name,
                "x": cen_d["x"]+5, "y": cen_d["y"]+6}).action(None)


def swap_poke():
    if not ask_bool(movemap, "Do you want to trade with another trainer?"):
        return
    PORT = 65432
    save()
    do = ask_bool(movemap, "Do you want to be the host?")
    if (index := deck(figure.pokes[:6], "Your deck", True)) is None:
        return
    if do:
        with InfoBox(f"Hostname: {socket.gethostname()}\nWaiting...", movemap):
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
                        decode_data = eval(data.decode())
                        conn.sendall(str.encode(str({"name": figure.name,
                                                     "poke": figure.pokes[index].dict()})))
    else:
        HOST = ""
        while HOST == "":
            HOST = ask_text(movemap, "Please type in the hosts hostname",
                            "Host:", "", 30)
            if HOST in ["localhost", "127.0.0.1", socket.gethostname()]:
                with InfoBox("You're not allowed trade with your self!\nYou fool!", movemap):
                    time.sleep(5)
                HOST = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
            except Exception as err:
                with InfoBox(str(err), movemap):
                    time.sleep(5)
                return
            s.sendall(str.encode(str({"name": figure.name,
                                    "poke": figure.pokes[index].dict()})))
            data = s.recv(1024)
            decode_data = eval(data.decode())
    figure.add_poke(Poke(decode_data["poke"]["name"],
                        decode_data["poke"]["xp"],
                        decode_data["poke"]["hp"]), index)
    figure.pokes[index].set_ap(decode_data["poke"]["ap"])
    save()  # to avoid duping
    with InfoBox(f"You received: {figure.pokes[index].name.capitalize()} at level {figure.pokes[index].lvl()} from {decode_data['name']}.", movemap):
        time.sleep(3)


def ask_bool(map, text):
    global ev
    assert len(text) >= 12, "Text has to be longer then 12 characters!"
    text_len = sorted([len(i) for i in text.split('\n')])[-1]
    with InfoBox(f"{text}\n{round(text_len/2-6)*' '}[Y]es   [N]o", map):
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
    return ret


def ask_text(map, infotext, introtext, text, max_len):
    with InputBox(infotext, introtext, text, max_len, map) as inputbox:
        ret = text_input(inputbox.text, map, text, max_len+1, max_len=max_len)
    return ret


def fight(player, enemy, info={"type": "wild", "player": " "}):
    global ev
    # fancy stuff
    if settings.animations:
        fancymap = se.Map(background=" ", width=width, height=height-1)
        vec_list = [se.Line(" ", i*int(width/2), j*int((height-1)/2))
                    for i, j in zip([1, 1, -1, -1], [1, -1, -1, 1])]
        for i in vec_list:
            i.add(fancymap, int(width/2), int((height-1)/2))
        fancymap.show()
        for j, l in zip(list(zip(*[i.obs for i in vec_list])),
                        list(zip(*[list(2*" ")+k
                                for k in [i.obs for i in vec_list]])),):
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
        fightmap.outp.outp(f"A wild {enemy.name} appeared!")
    elif info["type"] == "duel":
        fightmap.outp.outp(f"{info['player'].name} started a fight!")
        time.sleep(1)
        fightmap.outp.outp(f'{fightmap.outp.text}\n{info["player"].gender} used {enemy.name} against you!')
    time.sleep(1)
    fight_add_2(player, enemy)
    if player.identifier != "__fallback__":
        fast_change([player.ico, deadico2, deadico1, player.ico], player.ico)
        fightmap.outp.outp(f"You used {player.name}")
    fightmap.show()
    time.sleep(0.5)
    if player.identifier ==  "__fallback__":
        obj, enem = players
    else:
        enem = sorted(zip([i.initiative for i in players],
                        [1, 0], players))[0][-1]  # The [1, 0] array is needed to avoid comparing two Poke objects
        obj = [i for i in players if i != enem][-1]
    for i in players:
        for j in i.effects:
            j.readd()
    while True:
        if obj.player:
            fightmap.outp.append(se.Text(("\n"
                                    if "\n" not in fightmap.outp.text
                                    else "")+
                                    "What do you want to do?", state="float"))
            if obj.identifier == "__fallback__":
                time.sleep(1)
                fightmap.outp.outp("You don't have any living poketes left!")
            while True:  # Inputloop for general options
                if ev == "'1'":
                    ev = ""
                    if player.identifier == "__fallback__":
                        continue
                    with fightbox.add(fightmap, 1, fightmap.height-7):
                        while True:  # Inputloop for attack options
                            if ev in ["'s'", "'w'"]:
                                fightbox.input(ev)
                                fightmap.show()
                                ev = ""
                            elif ev in [f"'{i+1}'" for i in
                                    range(len(obj.attac_obs))]+["Key.enter"]:
                                attack = obj.attac_obs[fightbox.index.index
                                            if ev == "Key.enter"
                                            else int(ev.strip("'"))-1]
                                ev = ""
                                if attack.ap == 0:
                                    continue
                                break
                            elif ev in ["Key.esc", "'q'"]:
                                ev = ""
                                attack = ""
                                break
                            std_loop()
                            time.sleep(0.05)
                    if attack != "":
                        break
                elif ev == "'2'":
                    ev = ""
                    if ((info["type"] == "duel"
                            and player.identifier != "__fallback__")
                        or not ask_bool(fightmap, "Do you really want to run away?")):
                        continue
                    fightmap.outp.outp("You ran away!")
                    time.sleep(1)
                    fight_clean_up(player, enemy)
                    return enem
                elif ev == "'3'":
                    ev = ""
                    items = [getattr(Inv, i)
                             for i in figure.inv
                                if getattr(Inv, i).fn is not None
                                and figure.inv[i] > 0]
                    if items == []:
                        fightmap.outp.outp("You don't have any items left!\nWhat do you want to do?")
                        continue
                    fight_invbox.add_c_obs([se.Text(f"{i.pretty_name}s : {figure.inv[i.name]}") for i in items])
                    fight_invbox.set_index(0)
                    with fight_invbox.add(fightmap, fightmap.width-35, 0):
                        while True:
                            if ev in ["'s'", "'w'"]:
                                fight_invbox.input(ev)
                                fightmap.show()
                                ev = ""
                            elif ev in ["Key.esc", "'q'"]:
                                item = ""
                                break
                            elif ev == "Key.enter":
                                item = items[fight_invbox.index.index]
                                break
                            std_loop()
                            time.sleep(0.05)
                    fight_invbox.remove_c_obs()
                    if item == "":
                        continue
                    i = eval(item.fn)(obj, enem, info)  # I hate you python for not having switch statements
                    if i == 1:
                        continue
                    elif i == 2:
                        return
                    attack = ""
                    break
                elif ev == "'4'":
                    ev = ""
                    if obj.identifier == "__fallback__":
                        continue
                    fight_clean_up(player, enemy)
                    index = deck(figure.pokes[:6], "Your deck", True)
                    player = player if index is None else figure.pokes[index]
                    fight_add_1(player, enemy)
                    fightbox.set_index(0)
                    players = fight_add_3(player, enemy)
                    fightmap.outp.outp(f"You have choosen {player.name}")
                    for i in players:
                        for j in i.effects:
                            time.sleep(1)
                            j.readd()
                    attack = ""
                    break
                std_loop()
                time.sleep(0.1)
        else:
            attack = random.choices([i for i in obj.attac_obs],
                            weights=[i.ap*((1.5
                                    if enem.type.name in i.type.effective
                                    else 0.5
                                    if enem.type.name in i.type.ineffective
                                    else 1)
                                        if info["type"] == "duel"
                                        else 1)
                                    for i in obj.attac_obs])[0]
        time.sleep(0.3)
        if attack != "":
            obj.attack(attack, enem)
        fightmap.show()
        time.sleep(0.5)
        if any([i.hp <= 0 for i in players]):
            winner = [i for i in players if i.hp > 0][0]
            break
        elif all([i.ap == 0 for i in obj.attac_obs]):
            winner = [i for i in players if i != obj][0]
            time.sleep(2)
            fightmap.outp.outp(f"{obj.ext_name} has used all its' attacks!")
            time.sleep(3)
            break
        obj = [i for i in players if i != obj][-1]
        enem = [i for i in players if i != obj][-1]
    loser = [obj for obj in players if obj != winner][0]
    xp = (loser.lose_xp+(1 if loser.lvl() > winner.lvl() else 0))*(2 if info["type"] == "duel" else 1)
    fightmap.outp.outp(f"{winner.ext_name} won!"+(f'\nXP + {xp}'
        if winner.player else ''))
    if winner.player:
        old_lvl = winner.lvl()
        winner.xp += xp
        winner.text_xp.rechar(f"XP:{winner.xp-(winner.lvl()**2-1)}/{((winner.lvl()+1)**2-1)-(winner.lvl()**2-1)}")
        winner.text_lvl.rechar(f"Lvl:{winner.lvl()}")
        if old_lvl < winner.lvl():
            time.sleep(1)
            fightmap.outp.outp(f"{winner.name} reached lvl {winner.lvl()}!")
            winner.move_shine()
            time.sleep(0.5)
            winner.set_vars()
            if winner.lvl() % 5 == 0:
                LearnAttack(winner)()
            if winner.evolve_poke != "" and winner.lvl() >= winner.evolve_lvl:
                winner.evolve()
    fightmap.show()
    time.sleep(1)
    ico = [obj for obj in players if obj != winner][0].ico
    fast_change([ico, deadico1, deadico2], ico)
    deadico2.remove()
    fightmap.show()
    fight_clean_up(player, enemy)
    balls_label_rechar()
    return winner


def game(map):
    global ev, width, height
    ev = ""
    print("\033]0;Pokete - "+map.pretty_name+"\a", end="")
    if map.name not in visited_maps:
        visited_maps.append(map.name)
    movemap.code_label.rechar(figure.map.pretty_name)
    movemap.set(0, 0)
    movemap.bmap = map
    movemap.full_show()
    inp_dict = {"'1'": 'deck(figure.pokes[:6], "Your deck")',
                    "'3'": 'roadmap()', "'4'": 'inv()',
                    "'5'": 'pokete_dex(pokes)', "'e'": 'menu()',
                    "'?'": 'help_page()'}
    while True:
        for name, dir, x, y in zip(["'w'", "'a'", "'s'", "'d'"],
                                    ["t", "l", "b", "r"],  # Directions are not beening used yet
                                    [0, -1, 0, 1], [-1, 0, 1, 0]):
            if ev == name:
                figure.direction = dir
                figure.set(figure.x+x, figure.y+y)
                ev = ""
                break
        else:
            if ev in inp_dict:
                exec(inp_dict[ev])
                ev = ""
                movemap.show(init=True)
            elif ev == "'2'":
                ev = ""
                if ask_bool(movemap, "Do you realy want to exit?"):
                    save()
                    exiter()
            elif ev == "':'":
                ev = ""
                inp = text_input(movemap.code_label, movemap, ":",
                                movemap.width,
                                (movemap.width-2)*movemap.height-1)[1:]
                movemap.code_label.outp(figure.map.pretty_name)
                codes(inp)
                ev = ""
        std_loop()
        map.extra_actions()
        for trainer in map.trainers:
            trainer.do(map)
        time.sleep(0.05)
        for statement, x, y in zip([figure.x+6 > movemap.x+movemap.width,
                                    figure.x < movemap.x+6,
                                    figure.y+6 > movemap.y+movemap.height,
                                    figure.y < movemap.y+6],
                                    [1, -1, 0, 0], [0, 0, 1, -1]):
            if statement:
                movemap.set(movemap.x+x, movemap.y+y)
        # checking for resizing
        width, height = os.get_terminal_size()
        if movemap.width != width or movemap.height != height-1:
            for obj in [movemap.underline, movemap.label, movemap.code_label,
                        movemap.name_label, movemap.balls_label]:
                obj.remove()
            movemap.resize(height-1, width, " ")
            movemap_add_obs()
        movemap.full_show()


def intro():
    movemap.set(0, 0)
    movemap.bmap = ob_maps["intromap"]
    movemap.full_show()
    while figure.name in ["DEFAULT", ""]:
        figure.name = ask_text(movemap,
                            "Welcome to Pokete!\nPlease choose your name!\n",
                            "Name:", "", 17)
    movemap.underline.remove()
    movemap.balls_label.set(0, 1)
    movemap.name_label.rechar(figure.name, esccode=Color.thicc)
    movemap.balls_label.set(4+len(movemap.name_label.text), movemap.height-2)
    movemap.underline.add(movemap, 0, movemap.height-2)
    movemap_text(4, 3, [" < Hello my child.",
                        " < You're now ten years old.",
                        " < And I think it's now time for you to travel the world and be a Pokete-trainer.",
                        " < Therefore I give you this powerfull 'Steini', 15 'Poketeballs' to catch Poketes and a 'Healing potion'.",
                        " < You will be the best Pokete-Trainer in Nice town.",
                        " < Now go out and become the best!"])
    game(ob_maps["intromap"])


def parse_obj(_map, name, obj, _dict):
    setattr(_map, name, obj)
    obj.add(_map, _dict["x"], _dict["y"])


def gen_obs():
    # generating objects from map_data
    for ob_map in map_data:
        _map = ob_maps[ob_map]
        for hard_ob in map_data[ob_map]["hard_obs"]:
            parse_obj(_map, hard_ob,
                      se.Text(map_data[ob_map]["hard_obs"][hard_ob]["txt"],
                              ignore=" "),
                      map_data[ob_map]["hard_obs"][hard_ob])
        for soft_ob in map_data[ob_map]["soft_obs"]:
            parse_obj(_map, soft_ob,
                      se.Text(map_data[ob_map]["soft_obs"][soft_ob]["txt"],
                              ignore=Color.green+" "+Color.reset,
                              ob_class=HightGrass,
                              ob_args=_map.poke_args,
                              state="float", esccode=Color.green),
                      map_data[ob_map]["soft_obs"][soft_ob])
        for dor in map_data[ob_map]["dors"]:
            parse_obj(_map, dor,
                      Dor(" ", state="float",
                          arg_proto=map_data[ob_map]["dors"][dor]["args"]),
                      map_data[ob_map]["dors"][dor])
        for ball in map_data[ob_map]["balls"]:
            if f'{ob_map}.{ball}' not in used_npcs or not settings.save_trainers:
                parse_obj(_map, ball,
                          Poketeball(f"{ob_map}.{ball}"),
                          map_data[ob_map]["balls"][ball])
    # NPCs
    for npc in npcs:
        parse_obj(ob_maps[npcs[npc]["map"]], npc,
                  NPC(npc, npcs[npc]["texts"], npcs[npc]["fn"],
                      npcs[npc]["args"]),
                  npcs[npc])

    # adding all trainer to map
    for i in trainers:
        _map = ob_maps[i]
        for j in trainers[i]:
            _map.trainers.append(Trainer(Poke(*j["poke"], player=False),
                                 *j["args"]))
    for ob_map in map_data:
        _map = ob_maps[ob_map]
        for trainer in _map.trainers:
            trainer.add(_map, trainer.sx, trainer.sy)


def check_version(sinfo):
    if "ver" not in sinfo:
        return
    else:
        ver = sinfo["ver"]
    if VERSION != ver and sort_vers([VERSION, ver])[-1] == ver:
        if not ask_bool(loading_screen.map,
                        liner(f"The save file was created \
on version '{ver}', the current version is '{VERSION}', \
such a downgrade may result in data loss! \
Do you want to continue?", int(width*2/3))):
            exiter()


def main():
    os.system("")
    recognising = threading.Thread(target=recogniser)
    autosaveing = threading.Thread(target=autosave)
    recognising.daemon = True
    autosaveing.daemon = True
    recognising.start()
    autosaveing.start()
    check_version(session_info)
    if figure.name == "DEFAULT":
        intro()
    game(figure.map)


# Actual code execution
#######################

# deciding on wich input to use
if sys.platform == "linux":  # Use another (not on xserver relying) way to read keyboard input, to make this shit work in tty or via ssh, where no xserver is available
    def recogniser():
        import tty, termios
        global ev, old_settings, termios, fd, do_exit

        do_exit = False
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            ev = {ord(char): f"'{char.rstrip()}'", 13: "Key.enter",
                    127: "Key.backspace", 32: "Key.space",
                    27: "Key.esc"}[ord(char)]
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

# resizing screen
tss = ResizeScreen()
width, height = tss()
# loading screen
loading_screen = LoadingScreen(VERSION, CODENAME)
loading_screen()
# validating data
validate()
# types
for i in types:
    exec(i+" = PokeType(i, **types[i])")

# reading config file
home = str(Path.home())
Path(home+SAVEPATH).mkdir(parents=True, exist_ok=True)
Path(home+SAVEPATH+"/pokete.py").touch(exist_ok=True)
# Default test session_info
session_info = {
    "user": "DEFAULT",
    "ver": VERSION,
    "map": "intromap",
    "oldmap": "playmap_1",
    "x": 4,
    "y": 5,
    "pokes": {
        0: {"name": "steini", "xp": 50, "hp": "SKIP", "ap": ["SKIP", "SKIP"]}
    },
    "inv": {"poketeball": 15, "healing_potion": 1},
    "settings": {},
    "caught_poketes": ["steini"],
    "visited_maps": ["playmap_1"],
    "startup_time": 0,
    "used_npcs": []
}
with open(home+SAVEPATH+"/pokete.py") as file:
    exec(file.read())

if "settings" in session_info:
    settings = Settings(**session_info["settings"])
else:
    settings = Settings()

if "used_npcs" in session_info:
    used_npcs = session_info["used_npcs"]
else:
    used_npcs = []

if "caught_poketes" in session_info:
    caught_poketes = session_info["caught_poketes"]
else:
    caught_poketes = []

if "visited_maps" in session_info:
    visited_maps = session_info["visited_maps"]
else:
    visited_maps = ["playmap_1"]

# comprehending settings
colors = settings.colors
save_trainers = settings.save_trainers  # This is needed to just apply some changes when restarting the game to avoid running into errors
if not settings.colors:
    Color = NoColor


# Defining and adding of objetcs and maps
#########################################

# maps
ob_maps = {}
for ob_map in maps:
    args = maps[ob_map]
    args["extra_actions"] = (getattr(Extra_Actions, args["extra_actions"], None)
                            if args["extra_actions"] is not None
                            else None)
    ob_maps[ob_map] = PlayMap(name = ob_map, **args)

# Those two maps cant to sourced out, because `height` and `width`
# are global variables exclusive to pokete.py
centermap = PlayMap(height-1, width, name = "centermap",
                    pretty_name = "Pokete-Center")
shopmap = PlayMap(height-1, width, name = "shopmap",
                    pretty_name = "Pokete-Shop")

ob_maps["centermap"] = centermap
ob_maps["shopmap"] = shopmap

# movemap
movemap = se.Submap(ob_maps["playmap_1"], 0, 0, height=height-1, width=width)
figure = Figure("a")
exclamation = se.Object("!")
multitext = OutP("", state="float")
movemap.label = se.Text("1: Deck  2: Exit  3: Map  4: Inv.  5: Dex  ?: Help")
movemap.code_label = OutP("")


# Definiton of objects for the playmaps
# Most of the objects ar generated from map_data for maps.py
# .poke_arg is relevant for meadow genration
############################################################


__t_1 = time.time()
gen_obs()
__t_1 = time.time()-__t_1
# side fn definitions
detail = Detail()
pokete_dex = Dex(movemap)
help_page = Help(movemap)  # It's called help_page and not help, because I want to stop shadowing buildins
roadmap = RoadMap(stations)
deck = Deck()
menu = Menu()
about = About()
inv = Inv()
# items
for name in items:
    obj = InvItem(name, items[name]["pretty_name"], items[name]["desc"],
                  items[name]["price"], items[name]["fn"])
    setattr(Inv, name, obj)
Inv.ld_bubble_bomb = LearnDisc("bubble_bomb", attacks)
Inv.ld_flying = LearnDisc("flying", attacks)

buy = Buy()

# playmap_1
_map = ob_maps["playmap_1"]
_map.dor = Dor("#", state="float",
               arg_proto={"map": "centermap",
                          "x": int(centermap.width/2), "y": 7})
# adding
_map.dor.add(_map, 25, 4)

# cave_1
_map = ob_maps["cave_1"]
_map.inner = se.Text("""##########################################
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
##############  ##########################""", ignore="#",
    ob_class=HightGrass,
    ob_args={"pokes": ["steini", "bato", "lilstone", "rato"], "minlvl": 40,
            "maxlvl": 128},
    state="float")
# adding
_map.inner.add(_map, 0, 0)

# playmap_3
_map = ob_maps["playmap_3"]
_map.dor = Dor("#", state="float",
               arg_proto={"map": "centermap",
                          "x": int(centermap.width/2), "y": 7})
_map.shopdor = Dor("#", state="float",
                   arg_proto={"map": "shopmap",
                              "x": int(shopmap.width/2), "y": 7})
# playmap_3.npc = NPC([" < Hey", " < What up?"])
# adding
_map.dor.add(_map, 25, 6)
_map.shopdor.add(_map, 61, 6)
# playmap_3.npc.add(playmap_3, 49, 14)

# playmap_4
_map = ob_maps["playmap_4"]
_map.dor_playmap_5 = ChanceDor("~", state="float",
                               arg_proto={"chance": 6,
                                          "map": "playmap_5",
                                          "x": 17, "y": 16})
_map.lake_1 = se.Text("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~         ~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~                 ~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~                    ~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~                                ~~~~~~~~~~~~~~
~~~~~~~~~                                           ~~~~~~~~
~~~""", esccode=Color.blue, ignore=Color.blue+" "+Color.reset,
    ob_class=HightGrass,
    ob_args={"pokes": ["karpi", "blub"], "minlvl": 180, "maxlvl": 230},
    state="float")
# adding
_map.dor_playmap_5.add(_map, 56, 1)
_map.lake_1.add(_map, 0, 0)

# playmap_5
_map = ob_maps["playmap_5"]
_map.inner = se.Square(" ", 11, 11, state="float", ob_class=HightGrass,
                      ob_args=_map.poke_args)
# adding
_map.inner.add(_map, 26, 1)

# playmap_7
_map = ob_maps["playmap_7"]
_map.inner = se.Text("""##############################
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
##############################""", ignore="#", ob_class=HightGrass,
    ob_args=_map.poke_args, state="float")
for ob in (_map.inner_walls.obs + _map.trainers +
        [getattr(_map, i) for i in map_data["playmap_7"]["balls"]
                if "playmap_7."+i not in used_npcs
                or not settings.save_trainers]):
    ob.bchar = ob.char
    ob.rechar(" ")
# adding
_map.inner.add(_map, 0, 0)

# playmap_9
_map = ob_maps["playmap_9"]
_map.inner = se.Text("""
#########################
#########################
###       #  #         ##
#         ####          #
#                       #
##                      #
#               #########
############ ############
#########################""", ignore="#", ob_class=HightGrass,
    ob_args=_map.poke_args, state="float")
# adding
_map.inner.add(_map, 2, 1)

# playmap_11
_map = ob_maps["playmap_11"]
_map.lake_1 =  se.Text("""~~~~~                                                 ~~~~~~
~~~~~~~~~~~~                                 ~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~                       ~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~                   ~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~          ~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""",
    esccode=Color.blue, ignore=Color.blue+" "+Color.reset,
    ob_class=HightGrass,
    ob_args={"pokes": ["karpi", "clampi", "clampi"], "minlvl": 290,
             "maxlvl": 350},
    state="float")
# adding
_map.lake_1.add(_map, 0, 12)

# playmap_13
_map = ob_maps["playmap_13"]
_map.dor = Dor("#", state="float",
               arg_proto={"map": "centermap",
                          "x": int(centermap.width/2), "y": 7})
_map.shopdor = Dor("#", state="float",
                   arg_proto={"map": "shopmap",
                              "x": int(shopmap.width/2), "y": 7})
# adding
_map.dor.add(_map, 14, 29)
_map.shopdor.add(_map, 52, 29)

# playmap_18
_map = ob_maps["playmap_18"]
_map.lake_1 =  se.Text("""  ~~
 ~~~~
~~~~~~~
~~~~~~~~
~~~~~~~~
~~~~~~~~
~~~~~~
 ~~~~
 ~~""", esccode=Color.blue, ignore=Color.blue+" "+Color.reset,
    ob_class=HightGrass,
    ob_args={"pokes": ["karpi", "blub", "clampi"],
             "minlvl": 540, "maxlvl": 640},
    state="float")
# adding
_map.lake_1.add(_map, 72, 7)

# playmap_19
_map = ob_maps["playmap_19"]
_map.inner = se.Text("""                         ####
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
            ###""", ignore="#", ob_class=HightGrass,
            ob_args=_map.poke_args, state="float")
# adding
_map.inner.add(_map, 0, 0)

# playmap_21
_map = ob_maps["playmap_21"]
_map.dor_playmap_19 = Dor("_", state="float",
                          arg_proto={"map": ob_maps["playmap_19"],
                                     "x": 26, "y": 1})
_map.dor = Dor("#", state="float",
               arg_proto={"map": "centermap",
                          "x": int(centermap.width/2), "y": 7})
_map.shopdor = Dor("#", state="float",
                   arg_proto={"map": "shopmap",
                              "x": int(shopmap.width/2), "y": 7})
_map.lake_1 = se.Text("""       ~~~~~~~~~~~
   ~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~
       ~~~~~~~~""", esccode=Color.blue, ignore=Color.blue+" "+Color.reset,
       ob_class=HightGrass,
       ob_args={"pokes": ["karpi", "blub"], "minlvl": 540, "maxlvl": 640},
       state="float")

# adding
_map.dor_playmap_19.add(_map, 5, 26)
_map.dor.add(_map, 10, 7)
_map.shopdor.add(_map, 34, 7)
_map.lake_1.add(_map, 65, 10)

# playmap_30
_map = ob_maps["playmap_30"]
_map.dor = Dor("#", state="float",
               arg_proto={"map": "centermap",
                          "x": int(centermap.width/2), "y": 7})
_map.shopdor = Dor("#", state="float",
                   arg_proto={"map": "shopmap",
                              "x": int(shopmap.width/2), "y": 7})
# adding
_map.dor.add(_map, 13, 7)
_map.shopdor.add(_map, 30, 7)


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
centermap.trader = NPC("trader",
                       [" < I'm a trader.",
                        " < Here you can trade one of your Poketes for another players' one."],
                       "swap_poke", ())
# adding
centermap.dor_back1.add(centermap, int(centermap.width/2), 8)
centermap.dor_back2.add(centermap, int(centermap.width/2)+1, 8)
centermap.inner.add(centermap, int(centermap.width/2)-8, 1)
centermap.interact.add(centermap, int(centermap.width/2), 4)
centermap.trader.add(centermap, int(centermap.width/2)-6, 3)

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

# objects relevant for fight()
fightmap = se.Map(height-1, width, " ")
fightbox = ChooseBox(6, 25, "Attacks", index_x=1)
fight_invbox = ChooseBox(height-3, 35, "Inventory")
fightmap.frame_big = StdFrame2(fightmap.height-5, fightmap.width, state="float")
fightmap.frame_small = se.Frame(height=4, width=fightmap.width, state="float")
fightmap.e_underline = se.Text("----------------+", state="float")
fightmap.e_sideline = se.Square("|", 1, 3, state="float")
fightmap.p_upperline = se.Text("+----------------", state="float")
fightmap.p_sideline = se.Square("|", 1, 4, state="float")
fightmap.outp = OutP("", state="float")
fightmap.label = se.Text("1: Attack  2: Run!  3: Inv.  4: Deck")
deadico1 = se.Text(r"""
    \ /
     o
    / \ """)
deadico2 = se.Text("""

     o
""")
pball = se.Text(r"""   _____
  /_____\
  |__O__|
  \_____/""")
# adding
fightmap.outp.add(fightmap, 1, fightmap.height-4)
fightmap.e_underline.add(fightmap, 1, 4)
fightmap.e_sideline.add(fightmap, len(fightmap.e_underline.text), 1)
fightmap.p_upperline.add(fightmap,
                        fightmap.width-1-len(fightmap.p_upperline.text),
                        fightmap.height-10)
fightmap.frame_big.add(fightmap, 0, 0)
fightmap.p_sideline.add(fightmap,
                        fightmap.width-1-len(fightmap.p_upperline.text),
                        fightmap.height-9)
fightmap.frame_small.add(fightmap, 0, fightmap.height-5)
fightmap.label.add(fightmap, 0, fightmap.height-1)

# evomap
evomap = se.Map(height-1, width, " ")
evomap.frame_small = se.Frame(height=4, width=evomap.width, state="float")
evomap.outp = OutP("", state="float")
# adding
evomap.frame_small.add(evomap, 0, evomap.height-5)
evomap.outp.add(evomap, 1, evomap.height-4)

figure.set_args(session_info)

__t = time.time() - __t
ev = ""

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
