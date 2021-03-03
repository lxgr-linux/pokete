#!/usr/bin/env python3
# This software is licensed under the GPL3
# You should have gotten an copy of the GPL3 license anlonside this software
# Feel free to contribute what ever you want to this game
# New Pokete contributions are especially welcome
# For this see the comments in the definations area

import scrap_engine as se
import random, time, os, sys, threading, math
from pathlib import Path

class HightGrass(se.Object):
    def action(self, ob):
        if random.randint(0,6) == 0:
            fight(Poke("__fallback__", 0) if len([poke for poke in figure.pokes[:6] if poke.hp > 0]) == 0 else [poke for poke in figure.pokes[:6] if poke.hp > 0][0], Poke(random.choices(self.arg_proto["pokes"], weights=[pokes[i]["rarity"] for i in self.arg_proto["pokes"]])[0], random.choices(list(range(self.arg_proto["minlvl"], self.arg_proto["maxlvl"])))[0], player=False))

# The following two classes (PC and Heal) where initially needed to manage healing
# and reviewing off all Poketes in the deck
# They are now obsolete (because of the Pokete-Center) and will be removed later,
# but I will keep them for now for testing purposes

class PC(se.Object):
    def action(self, ob):
        deck(figure.pokes)
        movemap.remap()
        movemap.show(init=True)


class Heal(se.Object):
    def action(self, ob):
        heal()


class CenterInteract(se.Object):
    def action(self, ob):
        global ev
        ev = ""
        movemap.remap()
        movemap.show()
        movemap_text(int(movemap.width/2), 3, [" < Welcome to the Pokete-Center", " < What do you want to do?", " < a: See your full deck\n   b: Heal all your Poketes\n   c: Go"])
        while True:
            if ev == "'a'":
                ev = ""
                deck(figure.pokes)
                break
            elif ev == "'b'":
                ev = ""
                heal()
                break
            elif ev == "'c'":
                ev = ""
                break
            elif ev == "exit":
                raise KeyboardInterrupt
            time.sleep(0.05)
        multitext.remove()
        movemap.remap()
        movemap.show(init=True)


class Dor(se.Object):
    def action(self, ob):
        figure.remove()
        i = figure.map.name
        figure.add(self.arg_proto["map"], self.arg_proto["x"], self.arg_proto["y"])
        exec("figure.oldmap = "+i)
        game(self.arg_proto["map"])

class CenterDor(se.Object):
    def action(self, ob):
        figure.remove()
        i = figure.map.name
        figure.add(figure.oldmap, figure.oldmap.dor.x, figure.oldmap.dor.y+1)
        exec("figure.oldmap = "+i)
        game(figure.map)

class Poke():
    def __init__(self, poke, xp, _hp="SKIP", player=True):
        self.xp = xp
        self.player = player
        self.identifier = poke
        self.set_vars()
        for name in ["hp", "attacs", "name", "miss_chance", "lose_xp"]:
            exec("self."+name+" = pokes[self.identifier][name]")
        self.full_hp = self.hp
        self.full_miss_chance = self.miss_chance
        self.hp_bar = se.Text(8*"#", esccode="\033[32m")
        if _hp != "SKIP":
            self.hp = _hp if _hp <= self.full_hp else self.hp
            self.health_bar_maker(self.hp)
        self.desc = se.Text(liner(pokes[poke]["desc"], se.width-34))
        self.ico = se.Text(pokes[poke]["ico"])
        self.text_hp = se.Text("HP:"+str(self.hp))
        self.text_lvl = se.Text("Lvl:"+str(self.lvl()))
        self.text_name = se.Text(str(self.name), esccode="\033[4m")
        self.text_xp = se.Text("XP:"+str(self.xp-(self.lvl()**2-1))+"/"+str(((self.lvl()+1)**2-1)-(self.lvl()**2-1)))
        self.tril = se.Object("<")
        self.trir = se.Object(">")
        self.attac_obs = [Attack(atc) for atc in self.attacs]
        self.atc_labels = [se.Text(str(i)+": "+atc.name+"-"+str(atc.ap)) for i, atc in enumerate(self.attac_obs)]
        self.pball_small = se.Object("o")

    def set_vars(self):
        for name in ["atc", "defense"]:
            exec("self."+name+" = int("+pokes[self.identifier][name]+")")

    def label_rechar(self):
        for i, atc in enumerate(self.attac_obs):
            self.atc_labels[i].rechar(str(i)+": "+atc.name+"-"+str(atc.ap))

    def lvl(self):
        return int(math.sqrt(self.xp+1))

    def health_bar_maker(self, oldhp):
        bar_num = round(oldhp*8/self.full_hp)
        esccode = "\033[31m"
        for size, num in zip([6, 2 ], [2, 3]):
            if bar_num > size:
                esccode = "\033[3"+str(num)+"m"
                break
        self.hp_bar.rechar(bar_num*"#", esccode)

    def attack(self, attac, enem):
        if attac.ap > 0:
            time.sleep(0.4)
            exec("self.move_"+attac.move+"()")
            enem.oldhp = enem.hp
            self.oldhp = self.hp
            n_hp = round((self.atc * attac.factor / (enem.defense if enem.defense > 1 else 1))*random.choices([0, 0.75, 1, 1.26], weights=[attac.miss_chance+self.miss_chance, 1, 1, 1], k=1)[0])
            enem.hp -= n_hp if n_hp >= 0 else 0
            if enem.hp < 0:
                enem.hp = 0
            exec(attac.action)
            attac.ap -= 1
            fightmap.outp.rechar(self.name+"("+("you" if self.player else "enemy")+") used "+attac.name+" against "+enem.name+"("+("you" if not self.player else "enemy")+") "+(self.name+" missed!" if n_hp == 0 and attac.factor != 0 else ""))
            for ob in [enem, self]:
                while ob.oldhp != ob.hp and ob.oldhp > 0:
                    ob.oldhp += -1 if ob.oldhp > ob.hp else 1
                    ob.text_hp.rechar("HP:"+str(ob.oldhp), esccode="\033[33m")
                    ob.health_bar_maker(ob.oldhp)
                    time.sleep(0.1)
                    fightmap.show()
                ob.text_hp.rechar("HP:"+str(ob.oldhp))
                time.sleep(0.1)
            self.label_rechar()
            fightmap.show()

    def move_attack(self):
        self.ico.move(3 if self.player else -3, -2 if self.player else 2)
        fightmap.show()
        time.sleep(0.3)
        self.ico.move(-3 if self.player else 3, 2 if self.player else -2)
        fightmap.show()

    def move_pound(self):
        self.ico.move(0, -1)
        fightmap.show()
        time.sleep(0.3)
        self.ico.move(0, 1)
        fightmap.show()

    def move_shine(self):
        for i, x, y in zip(fightmap.shines, [self.ico.x-1, self.ico.x+11, self.ico.x-1, self.ico.x+11], [self.ico.y, self.ico.y, self.ico.y+3, self.ico.y+3]):
            i.add(fightmap, x, y)
            fightmap.show()
            time.sleep(0.2)
        time.sleep(0.2)
        for i in fightmap.shines:
            i.remove()
        fightmap.show()


class Attack():
    def __init__(self, index):
        for i in attacs[index]:
            exec("self."+i+"=attacs[index][i]")
        self.max_ap = self.ap
        self.label_name = se.Text(self.name, esccode="\033[4m")
        self.label_ap = se.Text("AP:"+str(self.ap)+"/"+str(self.max_ap))
        self.label_factor = se.Text("Attack:"+str(self.factor))
        self.desc = se.Text(self.desc[:int(se.width/2-1)])


def heal():
    for poke in figure.pokes:
        poke.hp = poke.full_hp
        poke.miss_chance = poke.full_miss_chance
        poke.text_hp.rechar("HP:"+str(poke.hp))
        poke.set_vars()
        poke.health_bar_maker(poke.hp)
        for atc in poke.attac_obs:
            atc.ap = atc.max_ap
        poke.label_rechar()
        balls_label_rechar()

def liner(text, width):
    lens = 0
    out = ""
    for name in text.split(" "):
        if lens+len(name)+1 < width:
            out += name+" "
            lens += len(name)+1
        else:
            lens = len(name)+1
            out += "\n"+name+" "
    return out

def codes(string):
    for i in string:
        if i == "w":
            save()
        elif i == "e":
            exec(string[string.index("e")+2:])
            return
        elif i == "q":
            exiter()

def save():
    session_info = {
        "user": figure.name,
        "map": figure.map.name,
        "oldmap": figure.oldmap.name,
        "x": figure.x,
        "y": figure.y,
        "pokes": {poke.identifier: {"xp": poke.xp, "hp": poke.hp, "ap": [atc.ap for atc in poke.attac_obs]} for poke in figure.pokes}
    }
    with open(home+"/.cache/pokete/pokete.py", "w+") as file:
        file.write("session_info="+str(session_info))

def on_press(key):
    global ev
    ev=str(key)

def exiter():
    global do_exit
    do_exit = True
    exit()

def deck_add(poke, map, x, y, in_deck=True):
    for ob, _x, _y in zip([poke.ico, poke.text_name, poke.text_lvl, poke.text_hp, poke.tril, poke.trir, poke.hp_bar, poke.text_xp], [0, 12, 12, 12, 18, 27, 19, 12], [0, 0, 1, 2, 2, 2, 2, 3]):
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
    if ev == "'a'":
        ev=""
        if index.index != 0:
            index.index -= 1
        else:
            index.index = len(pokes)-1
        index.set(pokes[index.index].text_name.x+len(pokes[index.index].text_name.text)+1, pokes[index.index].text_name.y)
    elif ev == "'d'":
        ev=""
        if index.index != len(pokes)-1:
            index.index += 1
        else:
            index.index = 0
        index.set(pokes[index.index].text_name.x+len(pokes[index.index].text_name.text)+1, pokes[index.index].text_name.y)
    elif ev == "'s'":
        ev=""
        if index.index+2 < len(pokes):
            index.index += 2
        else:
            index.index = index.index % 2
        index.set(pokes[index.index].text_name.x+len(pokes[index.index].text_name.text)+1, pokes[index.index].text_name.y)
    elif ev == "'w'":
        ev=""
        if index.index-2 >= 0:
            index.index -= 2
        else:
            index.index = [i for i in range(len(pokes)) if i % 2 == index.index % 2][-1]
        index.set(pokes[index.index].text_name.x+len(pokes[index.index].text_name.text)+1, pokes[index.index].text_name.y)

def fight_clean_up(player, enemy):
    for ob in [enemy.text_name, enemy.text_lvl, enemy.text_hp, enemy.ico, enemy.hp_bar, enemy.tril, enemy.trir, player.text_name, player.text_lvl, player.text_hp, player.ico, player.hp_bar, player.tril, player.trir, enemy.pball_small]+player.atc_labels:
        ob.remove()

def fight_add(player, enemy):
    enemy.tril.add(fightmap, 7, 3)
    enemy.trir.add(fightmap, 16, 3)
    enemy.text_name.add(fightmap, 1, 1)
    enemy.text_lvl.add(fightmap, 1, 2)
    enemy.text_hp.add(fightmap, 1, 3)
    enemy.ico.add(fightmap, fightmap.width-14, 2)
    enemy.hp_bar.add(fightmap, 8, 3)
    if player.identifier != "__fallback__":
        player.tril.add(fightmap, fightmap.width-11, fightmap.height-8)
        player.trir.add(fightmap, fightmap.width-2, fightmap.height-8)
        player.text_name.add(fightmap, fightmap.width-17, fightmap.height-10)
        player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-9)
        player.text_hp.add(fightmap, fightmap.width-17, fightmap.height-8)
        player.ico.add(fightmap, 3, fightmap.height-11)
        player.hp_bar.add(fightmap, fightmap.width-10, fightmap.height-8)
    if enemy.name in [ob.name for ob in figure.pokes]:
        enemy.pball_small.add(fightmap, len(fightmap.e_underline.text)-1, 1)
    for ob, x, y in zip(player.atc_labels, [1, 1, 19, 19], [fightmap.height-2, fightmap.height-1, fightmap.height-2, fightmap.height-1]):
        ob.add(fightmap, x, y)
    return [player, enemy]

def fight_add_1(player, enemy):
    enemy.tril.add(fightmap, 7, 3)
    enemy.trir.add(fightmap, 16, 3)
    enemy.text_name.add(fightmap, 1, 1)
    enemy.text_lvl.add(fightmap, 1, 2)
    enemy.text_hp.add(fightmap, 1, 3)
    enemy.ico.add(fightmap, fightmap.width-14, 2)
    enemy.hp_bar.add(fightmap, 8, 3)
    if enemy.name in [ob.name for ob in figure.pokes]:
        enemy.pball_small.add(fightmap, len(fightmap.e_underline.text)-1, 1)
    for ob, x, y in zip(player.atc_labels, [1, 1, 19, 19], [fightmap.height-2, fightmap.height-1, fightmap.height-2, fightmap.height-1]):
        ob.add(fightmap, x, y)
    return [player, enemy]

def fight_add_2(player, enemy):
    if player.identifier != "__fallback__":
        player.text_name.add(fightmap, fightmap.width-17, fightmap.height-10)
        time.sleep(0.05)
        fightmap.show()
        player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-9)
        time.sleep(0.05)
        fightmap.show()
        player.tril.add(fightmap, fightmap.width-11, fightmap.height-8)
        player.trir.add(fightmap, fightmap.width-2, fightmap.height-8)
        player.hp_bar.add(fightmap, fightmap.width-10, fightmap.height-8)
        player.text_hp.add(fightmap, fightmap.width-17, fightmap.height-8)
        time.sleep(0.05)
        fightmap.show()
        player.ico.add(fightmap, 3, fightmap.height-11)

def balls_label_rechar():
    movemap.balls_label.text = ""
    for i in ["o" if j.hp > 0 else "x" for j in figure.pokes[:6]]:
        movemap.balls_label.text += i
    movemap.balls_label.rechar(movemap.balls_label.text, esccode="\033[1m")

def fight(player, enemy, info={"type": "wild", "player": " "}):
    global ev, attack, fightmap

    players = fight_add_1(player, enemy)

    if info["type"] == "wild":
        fightmap.outp.rechar("A wild "+enemy.name+" appeared!")
    elif info["type"] == "duel":
        fightmap.outp.rechar(info["player"].name+" started a fight!")
        fightmap.show(init=True)
        time.sleep(1)
        fightmap.outp.rechar(fightmap.outp.text+"\n"+info["player"].gender+" used "+enemy.name+" against you!")

    fightmap.show(init=True)
    time.sleep(1)
    fight_add_2(player, enemy)
    if player.identifier != "__fallback__":
        fast_change([player.ico, deadico2, deadico1, player.ico], player.ico)
        fightmap.outp.rechar("You used "+player.name)
    fightmap.show()
    time.sleep(0.5)
    fight_running = True

    while fight_running:
        for ob in players:
            enem = [i for i in players if i != ob][0]
            if ob.player:
                fightmap.outp.rechar(fightmap.outp.text+("\n" if fightmap.outp.text != "" else "")+ "What do you want to do?")
                fightmap.show()
                if ob.identifier == "__fallback__":
                    time.sleep(1)
                    fightmap.outp.rechar("You don't have any living poketes left!")
                    fightmap.show()
                while True:
                    if ev in ["'"+str(i)+"'" for i in range(len(ob.attacs))]:
                        exec("global attack; attack = ob.attac_obs[int("+ev+")]")
                        if attack.ap == 0:
                            continue
                        ev=""
                        break
                    elif ev == "'5'":
                        ev = ""
                        if info["type"] == "duel":
                            continue
                        fightmap.outp.rechar("You ran away!")
                        fightmap.show()
                        time.sleep(1)
                        fight_clean_up(player, enemy)
                        return enem
                    elif ev == "'6'":
                        ev = ""
                        if ob.identifier == "__fallback__" or info["type"] == "duel":
                            continue
                        fightmap.outp.rechar("You threw a poketeball!")
                        fast_change([enem.ico, deadico1, deadico2, pball], enem.ico)
                        time.sleep(random.choice([1,2,3,4]))
                        if random.choices([True, False], weights=[enem.full_hp/enem.hp, enem.full_hp], k=1)[0]:
                            enem.player = True
                            figure.pokes.append(enem)
                            fightmap.outp.rechar("You catched "+enem.name)
                            fightmap.show()
                            time.sleep(1)
                            pball.remove()
                            fight_clean_up(player, enemy)
                            return
                        else:
                            fightmap.outp.rechar("You missed!")
                            fightmap.show()
                            pball.remove()
                            enem.ico.add(fightmap, enem.ico.x, enem.ico.y)
                            fightmap.show()
                        attack = ""
                        break
                    elif ev == "'7'":
                        ev = ""
                        if ob.identifier == "__fallback__":
                            continue
                        fight_clean_up(player, enemy)
                        new_player = deck(figure.pokes[:6], "Your deck", True)
                        player = new_player if new_player != None else player
                        players = fight_add(player, enemy)
                        fightmap.outp.rechar("You have choosen "+player.name)
                        fightmap.show(init=True)
                        attack = ""
                        break
                    elif ev == "exit":
                        raise KeyboardInterrupt
                    time.sleep(0.1)
            else:
                attack = random.choices([ob for ob in ob.attac_obs], weights=[ob.ap for ob in ob.attac_obs])[0]
            time.sleep(0.3)
            if attack != "":
                ob.attack(attack, enem)
            fightmap.show()
            time.sleep(0.5)
            if enem.hp <= 0:
                winner = ob
                fight_running = False
                break
        fightmap.show()
    loser = [ob for ob in players if ob != winner][0]
    fightmap.outp.rechar(winner.name+"("+("you" if winner.player else "enemy")+") won!"+("\nXP + "+str(loser.lose_xp*(2 if info["type"] == "duel" else 1)) if winner.player else ""))
    fightmap.show()
    if winner.player:
        old_lvl = winner.lvl()
        winner.xp += loser.lose_xp*(2 if info["type"] == "duel" else 1)
        winner.text_xp.rechar("XP:"+str(winner.xp-(winner.lvl()**2-1))+"/"+str(((winner.lvl()+1)**2-1)-(winner.lvl()**2-1)))
        winner.text_lvl.rechar("Lvl:"+str(winner.lvl()))
        if old_lvl < winner.lvl():
            time.sleep(1)
            fightmap.outp.rechar(winner.name+" reached lvl "+str(winner.lvl())+"!")
            winner.move_shine()
            time.sleep(0.5)
    #winner.set_vars()
    fightmap.show()
    time.sleep(1)
    ico = [ob for ob in players if ob != winner][0].ico
    fast_change([ico, deadico1, deadico2], ico)
    deadico2.remove()
    fightmap.show()
    fight_clean_up(player, enemy)
    balls_label_rechar()
    return winner

def fast_change(arr, setob):
    _i = 1
    while _i < len(arr):
        arr[_i-1].remove()
        arr[_i].add(fightmap, setob.x, setob.y)
        fightmap.show()
        time.sleep(0.1)
        _i += 1

def deck(pokes, label="Your full deck", in_fight=False):
    global ev

    deckmap.resize(5*int((len(pokes)+1)/2)+2, deckmap.width, deckmap.background)
    se.Text(label, esccode="\033[1m").add(deckmap, 2, 0)
    se.Square("_", deckmap.width, 1).add(deckmap, 0, 0)
    se.Square("|", 1, deckmap.height-2).add(deckmap, 0, 1)
    se.Square("|", 1, deckmap.height-2).add(deckmap, deckmap.width-1, 1)
    se.Square("|", 1, deckmap.height-2).add(deckmap, round(deckmap.width/2), 1)
    se.Square("_", deckmap.width-2, 1).add(deckmap, 1, deckmap.height-2)
    decksubmap.move_label.rechar("2: Move    ")
    ev = ""
    j = 0
    _first_index = ""
    _second_index = ""
    deck_add_all(pokes, True)
    deck_index = se.Object("*")
    deck_index.index = 0
    if len(pokes) > 0:
        deck_index.add(deckmap, pokes[deck_index.index].text_name.x+len(pokes[deck_index.index].text_name.text)+1, pokes[deck_index.index].text_name.y)
    decksubmap.remap()
    decksubmap.show(init=True)
    while True:
        if ev == "'1'":
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
            if _first_index == "":
                _first_index = deck_index.index
                decksubmap.move_label.rechar("2: Move to?")
            else:
                _second_index = deck_index.index
                _first_item = pokes[_first_index]
                _second_item = pokes[_second_index]
                pokes[_first_index] = figure.pokes[_first_index] = _second_item
                pokes[_second_index] = figure.pokes[_second_index] = _first_item
                _first_index = ""
                _second_index = ""
                for poke in pokes:
                    deck_remove(poke)
                deck_index.set(0, deckmap.height-1)
                deck_add_all(pokes)
                deck_index.set(pokes[deck_index.index].text_name.x+len(pokes[deck_index.index].text_name.text)+1, pokes[deck_index.index].text_name.y)
                decksubmap.move_label.rechar("2: Move    ")
                decksubmap.remap()
                decksubmap.show()
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
                    return pokes[deck_index.index]
            else:
                for poke in pokes:
                    deck_remove(poke)
                detail(pokes[deck_index.index])
                deck_add_all(pokes)
                decksubmap.remap()
                decksubmap.show(init=True)
        elif ev == "exit":
            raise KeyboardInterrupt
        if len(pokes) > 0 and deck_index.y-decksubmap.y +6 > decksubmap.height:
            decksubmap.set(decksubmap.x, decksubmap.y+1)
        elif len(pokes) > 0 and deck_index.y-1 < decksubmap.y:
            decksubmap.set(decksubmap.x, decksubmap.y-1)
        time.sleep(0.05)
        decksubmap.remap()
        decksubmap.show()

def detail(poke):
    global ev
    deck_add(poke, detailmap, 1, 1, False)
    detailmap.attack_defense.rechar("Attack:"+str(poke.atc)+(4-len(str(poke.atc)))*" "+"Defense:"+str(poke.defense))
    poke.desc.add(detailmap, 34, 2)
    for atc, x, y in zip(poke.attac_obs, [1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1], [7, 7, 12, 12]):
        atc.label_name.add(detailmap, x, y)
        atc.label_factor.add(detailmap, x, y+1)
        atc.label_ap.rechar("AP:"+str(atc.ap)+"/"+str(atc.max_ap))
        atc.label_ap.add(detailmap, x, y+2)
        try:
            atc.desc.add(detailmap, x, y+3)
        except:
            continue
    detailmap.show(init=True)
    while True:
        if ev == "'1'":
            ev=""
            deck_remove(poke)
            poke.desc.remove()
            for atc in poke.attac_obs:
                for ob in [atc.label_name, atc.label_factor, atc.label_ap, atc.desc]:
                    ob.remove()
            return
        elif ev == "exit":
            raise KeyboardInterrupt
        time.sleep(0.05)
        detailmap.show()

def game(map):
    global ev, exec_string
    ev=""
    print("\033]0;Pokete - "+map.pretty_name+"\a", end="")
    movemap.code_label.rechar(figure.map.pretty_name)
    movemap.set(0, 0)
    movemap.bmap = map

    movemap.remap()
    movemap.show()

    while True:
        for name, dir, x, y in zip(["'w'", "'a'", "'s'", "'d'"], ["t", "l", "b", "r"], [0, -1, 0, 1], [-1, 0, 1, 0]):
            if ev == name:
                figure.direction = dir
                figure.set(figure.x+x, figure.y+y)
                ev=""
        if ev == "'1'":
            ev=""
            deck(figure.pokes[:6], "Your deck")
            movemap.show(init=True)
        elif ev == "'2'":
            ev=""
            save()
            exiter()
        elif ev == "':'":
            ev=""
            exec_string = ""
            movemap.code_label.rechar(":"+exec_string+"█")
            movemap.show()
            while True:
                if ev == "Key.enter":
                    movemap.code_label.rechar(figure.map.pretty_name)
                    movemap.show()
                    codes(exec_string)
                    break
                elif ev == "exit":
                    movemap.code_label.rechar(figure.map.pretty_name)
                    movemap.show()
                    break
                elif ev == "Key.backspace":
                    if len(exec_string) == 0:
                        movemap.code_label.rechar(figure.map.pretty_name)
                        movemap.show()
                        break
                    exec_string = exec_string[:-1]
                    movemap.code_label.rechar(":"+exec_string+"█")
                    movemap.show()
                    ev = ""
                elif ev not in ["", "Key.enter", "exit", "Key.backspace", "Key.shift"]:
                    if ev == "Key.space":
                        ev = "' '"
                    exec("global exec_string; exec_string += str("+ev+")")
                    movemap.code_label.rechar(":"+exec_string+"█")
                    movemap.show()
                    ev = ""
            ev=""
        elif ev == "exit":
            raise KeyboardInterrupt
        for trainer in map.trainers:
            if figure.x == trainer.x and trainer.poke.hp > 0 and trainer.will:
                arr = []
                for i in range(figure.y+2 if figure.y < trainer.y else trainer.y+1, trainer.y if figure.y < trainer.y else figure.y-2):
                    arr += map.obmap[i][trainer.x]
                if any(ob.state == "solid" for ob in arr):
                    continue
                movemap.remap()
                movemap.show()
                time.sleep(0.7)
                exclamation.add(movemap, trainer.x-movemap.x, trainer.y-1-movemap.y)
                movemap.show()
                time.sleep(1)
                exclamation.remove()
                while trainer.y != figure.y+(2 if trainer.y > figure.y else -2):
                    trainer.set(trainer.x, trainer.y+(-1 if trainer.y > figure.y+1 or trainer.y == figure.y-1 else 1))
                    movemap.remap()
                    movemap.show()
                    time.sleep(0.3)
                if any([poke.hp > 0 for poke in figure.pokes[:6]]):
                    movemap_text(trainer.x, trainer.y, trainer.texts)
                    winner = fight([poke for poke in figure.pokes[:6] if poke.hp > 0][0], trainer.poke, info={"type": "duel", "player": trainer})
                    if winner == trainer.poke:
                        movemap_text(trainer.x, trainer.y, trainer.lose_texts)
                    else:
                        movemap_text(trainer.x, trainer.y, trainer.win_texts)
                        trainer.will = False
                else:
                    movemap_text(trainer.x, trainer.y, trainer.no_poke_texts)
                    trainer.will = False
                multitext.remove()
                while trainer.y != trainer.sy:
                    trainer.set(trainer.x, trainer.y+(1 if trainer.y < trainer.sy else -1))
                    movemap.remap()
                    movemap.show()
                    time.sleep(0.3)
        time.sleep(0.05)
        if figure.x+5 > movemap.x+movemap.width:
            movemap.set(movemap.x+1, movemap.y)
        if figure.x < movemap.x+5:
            movemap.set(movemap.x-1, movemap.y)
        if figure.y+4 > movemap.y+movemap.height:
            movemap.set(movemap.x, movemap.y+1)
        if figure.y < movemap.y+4:
            movemap.set(movemap.x, movemap.y-1)
        movemap.remap()
        movemap.show()

def movemap_text(x, y, arr):
    global ev
    for t in arr:
        ev = ""
        multitext.rechar("")
        multitext.add(movemap, x-movemap.x+1, y-movemap.y)
        for i in range(len(t)+1):
            multitext.rechar(t[:i])
            movemap.show()
            time.sleep(0.045)
            if ev == "exit":
                raise KeyboardInterrupt
            elif ev != "":
                ev = ""
                break
        multitext.rechar(t)
        movemap.show()
        while True:
            if ev == "exit":
                raise KeyboardInterrupt
            elif ev != "":
                break
            time.sleep(0.05)

def main():
    os.system("")
    recognising=threading.Thread(target=recogniser)
    recognising.daemon=True
    recognising.start()
    game(figure.map)

attacs = {
    "tackle": {
        "name": "Tackle",
        "factor": 3/2,
        "action": "",
        "move": "attack",
        "miss_chance": 0.2,
        "desc": "Tackles the enemy very hard",
        "ap": 20,
    },
    "pick": {
        "name": "Pick",
        "factor": 1.7,
        "action": "",
        "move": "attack",
        "miss_chance": 0.1,
        "desc": "A pick at the enemys weakest spot",
        "ap": 20,
    },
    "apple_drop": {
        "name": "Apple drop",
        "factor": 1.7,
        "action": "",
        "move": "attack",
        "miss_chance": 0.3,
        "desc": "Lets an apple drop on the enemys head",
        "ap": 20,
    },
    "eye_pick": {
        "name": "Eye pick",
        "factor": 2.5,
        "action": "enem.miss_chance += 2",
        "move": "attack",
        "miss_chance": 0.6,
        "desc": "Picks out one of the enemys eyes",
        "ap": 5,
    },
    "earch_quake": {
        "name": "Earch quake",
        "factor": 0,
        "action": "enem.hp -= 4",
        "move": "pound",
        "miss_chance": 0,
        "desc": "Brings the earth to shift",
        "ap": 5,
    },
    "wing_hit": {
        "name": "Wing hit",
        "factor": 2.5,
        "action": "",
        "move": "attack",
        "miss_chance": 0.5,
        "desc": "Hits the enemy with a wing",
        "ap": 5,
    },
    "super_sucker": {
        "name": "Super sucker",
        "factor": 0,
        "action": "enem.hp -=2; self.hp +=2 if self.hp+2 <= self.full_hp else 0",
        "move": "attack",
        "miss_chance": 0,
        "desc": "Sucks 2 HP from the enemy and adds it to it's own",
        "ap": 5,
    },
    "sucker": {
        "name": "Sucker",
        "factor": 0,
        "action": "enem.hp -=1; self.hp +=1 if self.hp+1 <= self.full_hp else 0",
        "move": "attack",
        "miss_chance": 0,
        "desc": "Sucks 1 HP from the enemy and adds it to it's own",
        "ap": 20,
    },
    "brooding": {
        "name": "Brooding",
        "factor": 0,
        "action": "self.hp += 2 if self.hp+2 <= self.full_hp else 0",
        "move": "shine",
        "miss_chance": 0,
        "desc": "Regenerates 2 HP",
        "ap": 5,
    },
    "pepple_fire": {
        "name": "Pepple fire",
        "factor": 1,
        "action": "enem.miss_chance += 1",
        "move": "attack",
        "miss_chance": 0,
        "desc": "Fires pepples at the enemy and makes it blind",
        "ap": 3,
    },
    "cry": {
        "name": "Cry",
        "factor": 0,
        "action": "enem.miss_chance += 1",
        "move": "attack",
        "miss_chance": 0,
        "desc": "So loud, it confuses the enemy",
        "ap": 5,
    },
    "bite": {
        "name": "Bite",
        "factor": 1.75,
        "action": "",
        "move": "attack",
        "miss_chance": 0.1,
        "desc": "A hard bite the sharp teeth",
        "ap": 20,
    },
    "politure": {
        "name": "Politure",
        "factor": 0,
        "action": "self.defense += 1; self.atc += 1",
        "move": "shine",
        "miss_chance": 0,
        "desc": "Upgrades defense and attack points",
        "ap": 10,
    },
    "bark_hardening": {
        "name": "Bark hardening",
        "factor": 0,
        "action": "self.defense += 1",
        "move": "shine",
        "miss_chance": 0,
        "desc": "Hardens the bark to protect it better",
        "ap": 10,
    },
    "chocer": {
        "name": "Chocer",
        "factor": 1,
        "action": "enem.atc -= 1",
        "move": "attack",
        "miss_chance": 0.2,
        "desc": "Choces the enemy and makes it weaker",
        "ap": 10,
    },
    "poison_bite": {
        "name": "Poison bite",
        "factor": 1,
        "action": "enem.atc -= 1; enem.defense -= 1",
        "move": "attack",
        "miss_chance": 0.3,
        "desc": "Makes the enemy weaker",
        "ap": 5,
    },
    "power_pick": {
        "name": "Power pick",
        "factor": 2,
        "action": "",
        "move": "attack",
        "miss_chance": 0.4,
        "desc": "A harsh picking on the enemys head",
        "ap": 5,
    },
    "bubble_bomb": {
        "name": "Bubble bomb",
        "factor": 6,
        "action": "enem.miss_chance += 1",
        "move": "attack",
        "miss_chance": 0,
        "desc": "A deadly bubble",
        "ap": 5,
    },
    "bubble_shield": {
        "name": "Bubble shield",
        "factor": 0,
        "action": "self.defense += 2",
        "move": "shine",
        "miss_chance": 0,
        "desc": "Creates a giant bubble that protects the Pokete",
        "ap": 5,
    },
    "mind_blow": {
        "name": "Mind blow",
        "factor": 0,
        "action": "enem.miss_chance += 2",
        "move": "attack",
        "miss_chance": 0,
        "desc": "Causes confusion deep in the enemys mind",
        "ap": 10,
    },
    "tail_wipe": {
        "name": "Tail wipe",
        "factor": 2.5,
        "action": "",
        "move": "attack",
        "miss_chance": 0.5,
        "desc": "Wipes throught the enemys face",
        "ap": 5,
    },
    "meat_skewer": {
        "name": "Meat skewer",
        "factor": 3.5,
        "action": "",
        "move": "attack",
        "miss_chance": 0.7,
        "desc": "Drills the horn deep in the enemys flesh",
        "ap": 5,
    },
}

# Here starts to definition of all the Poketes
# If you want to contribute Poketes, you have to keep in mind, that "ico" can be max 11x4 chars big
# and that the max for attacks is (until now) 4
# All attributes have to be present make a Pokete work
# Hornita was inspired and partly designed by Pia <pialandrath@gmail.com>

pokes = {
    "__fallback__": {
        "name": "",
        "hp": 0,
        "atc": "0",
        "defense": "0",
        "attacs": [],
        "miss_chance": 0,
        "desc": "",
        "lose_xp": 0,
        "rarity": 0,
        "ico": """ """,
    },
    "steini": {
        "name": "Steini",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+4",
        "attacs": ["tackle", "politure"],
        "miss_chance": 0,
        "desc": "A squared stone that can casually be found on the ground",
        "lose_xp": 2,
        "rarity": 1,
        "ico": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
    },
    "poundi": {
        "name": "Poundi",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+3",
        "attacs": ["tackle", "politure", "earch_quake"],
        "miss_chance": 0,
        "desc": "A powerfull and heavy stone Pokete that lives in mountain caves",
        "lose_xp": 3,
        "rarity": 0.7,
        "ico": """   A-A-A
  < o o >
  < --- >
   VvVvV""",
   },
   "lilstone": {
       "name": "Lilstone",
       "hp": 20,
       "atc": "self.lvl()+1",
       "defense": "self.lvl()+2",
       "attacs": ["tackle", "politure", "pepple_fire"],
       "miss_chance": 0,
       "desc": "A small but powerfull stone Pokete that lives in the mountains",
       "lose_xp": 2,
       "rarity": 1,
       "ico": """
   _____
   |'ᵕ'|
   ‾‾‾‾‾""",
  },
  "rosi": {
      "name": "Rosi",
      "hp": 20,
      "atc": "self.lvl()",
      "defense": "self.lvl()+1",
      "attacs": ["sucker", "super_sucker"],
      "miss_chance": 0,
      "desc": "A plant Pokete, that's often mistaken for a normal flower",
      "lose_xp": 2,
      "rarity": 0.8,
      "ico": """
    (@)
     |
    \|/""",
 },
  "gobost": {
      "name": "Gobost",
      "hp": 20,
      "atc": "self.lvl()+2",
      "defense": "self.lvl()+1",
      "attacs": ["tackle", "mind_blow"],
      "miss_chance": 0,
      "desc": "A scary ghost Pokete that lives in caves and old houses",
      "lose_xp": 2,
      "rarity": 1,
      "ico": """ .░░░░░░░.
 ░░o░░░o░░
 ░░░░░░░░░
 ░ ░ ░ ░ ░""",
  },
  "vogli": {
        "name": "Vogli",
        "hp": 20,
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "power_pick"],
        "miss_chance": 0,
        "desc": "A very common bird Pokete that lives in town but also in the nature",
        "lose_xp": 2,
        "rarity": 1,
        "ico":"""    A
   <')
    www*
    ||     """
    },
    "voglo": {
        "name": "Voglo",
        "hp": 20,
        "atc": "self.lvl()+7",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "power_pick", "wing_hit", "brooding"],
        "miss_chance": 0,
        "desc": "A very agressive bird Pokete that can only be found in the woods",
        "lose_xp": 2,
        "rarity": 0.8,
        "ico":"""    ?
   >´)
    www*
    ||     """
    },
    "ostri": {
        "name": "Ostri",
        "hp": 20,
        "atc": "self.lvl()+8",
        "defense": "self.lvl()",
        "attacs": ["tackle", "eye_pick", "brooding"],
        "miss_chance": 0,
        "desc": "A very agressive bird Pokete that lives near deserts and will try to pick out your eyes",
        "rarity": 0.6,
        "lose_xp": 2,
        "ico":"""   !
  >´)
    \www'
     ||"""
    },
    "karpi": {
        "name": "Karpi",
        "hp": 15,
        "atc": "self.lvl()",
        "defense": "self.lvl()/2",
        "attacs": ["tackle"],
        "miss_chance": 0,
        "desc": "A very harmless water Pokete that can be found everywhere",
        "lose_xp": 1,
        "rarity": 1.5,
        "ico":"""

  <°))))><
           """
    },
    "würgos": {
        "name": "Würgos",
        "hp": 20,
        "atc": "self.lvl()+3",
        "defense": "self.lvl()",
        "attacs": ["chocer", "bite", "poison_bite"],
        "miss_chance": 0,
        "desc": "A dangerous snake Pokete",
        "lose_xp": 2,
        "rarity": 1,
        "ico": """  >'({{{
  }}}}}}}
 {{{{{{{{{
           """
    },
    "treenator": {
        "name": "Treenator",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+2",
        "attacs": ["apple_drop", "bark_hardening"],
        "miss_chance": 0,
        "desc": "A scary an dangerous apple tree",
        "lose_xp": 2,
        "rarity": 1,
        "ico": """    (()
   (()))
     H
     H"""
    },
    "bato": {
        "name": "Bato",
        "hp": 20,
        "atc": "self.lvl()+3",
        "defense": "self.lvl()+1",
        "attacs": ["bite", "cry"],
        "miss_chance": 0,
        "desc": "An annoying flying rat",
        "lose_xp": 2,
        "rarity": 1.3,
        "ico": """    ___
WW\/* *\/WW
   \\v-v/
"""
    },
    "blub": {
        "name": "Blub",
        "hp": 20,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "bubble_bomb", "bubble_shield"],
        "miss_chance": 0,
        "desc": "Very delicious and low fat water Pokete",
        "lose_xp": 2,
        "rarity": 1,
        "ico": """  _____
 / o   \\
 >   v  ><
 \_____/"""
    },
    "owol": {
        "name": "Owol",
        "hp": 20,
        "atc": "self.lvl()+7",
        "defense": "self.lvl()+2",
        "attacs": ["pick", "wing_hit", "cry"],
        "miss_chance": 0,
        "desc": "A night active Pokete, that is looking for lil children as a midnight snack",
        "lose_xp": 2,
        "rarity": 0.5,
        "ico": """   ,___,
   {o,o}
   /)_)
    ""
"""
    },
    "rato": {
        "name": "Rato",
        "hp": 20,
        "atc": "self.lvl()+4",
        "defense": "self.lvl()+2",
        "attacs": ["tackle", "tail_wipe"],
        "miss_chance": 0,
        "desc": "An annoying rat",
        "lose_xp": 2,
        "rarity": 1.3,
        "ico": """   ^---^
   \o o/
   >\./<
"""
    },
    "hornita": {
        "name": "Hornita",
        "hp": 20,
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+2",
        "attacs": ["tackle", "meat_skewer", "tail_wipe"],
        "miss_chance": 0,
        "desc": "An majestetic horse that is always looking for something to pick with its horn.",
        "lose_xp": 2,
        "rarity": 1,
        "ico": """ \\
 =')~
   (¯¯¯¯)~
   //¯¯\\\\"""
    },
    "horny": {
        "name": "Horny",
        "hp": 20,
        "atc": "self.lvl()+5",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "meat_skewer"],
        "miss_chance": 0.2,
        "desc": "A teenaged unicorn in the middle of puberty.",
        "rarity": 1,
        "lose_xp": 2,
        "ico": """  ,
 =')
   (¯¯¯)~
   //¯\\\\"""
    },
    "bushy": {
        "name": "Bushy",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "bark_hardening"],
        "miss_chance": 0,
        "desc": "A bush, and just a bush. But watch out!",
        "lose_xp": 2,
        "rarity": 1,
        "ico": """
    (()
   (()))"""
    },
}

# deciding on wich input to use
if sys.platform == "linux":  # Use another (not on xserver relying) way to read keyboard input, to make this shit work in tty or via ssh, where no xserver is available
    def recogniser():
        import tty, sys, termios
        global ev, old_settings, termios, fd, do_exit

        do_exit=False
        fd=sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        while True:
            char=sys.stdin.read(1)
            if ord(char) == 13:
                ev="Key.enter"
            elif ord(char) == 127:
                ev="Key.backspace"
            elif ord(char) == 32:
                ev="Key.space"
            else:
                ev="'"+char.rstrip()+"'"
            if ord(char) == 3 or do_exit:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                ev="exit"
else:
    from pynput.keyboard import Key, Listener
    def recogniser():
        global ev
        while True:
            with Listener(on_press=on_press) as listener:
                listener.join()

# reading config file
home = str(Path.home())
Path(home+"/.cache/pokete").mkdir(parents=True, exist_ok=True)
Path(home+"/.cache/pokete/pokete.py").touch(exist_ok=True)
# Default test session_info
session_info = {
    "user": "DEFAULT",
    "map": "playmap_1",
    "oldmap": "playmap_1",
    "x": 1,
    "y": 1,
    "pokes": {
        "steini": {"xp": 35, "hp": "SKIP", "ap": ["SKIP", "SKIP"]}
    }
}
with open(home+"/.cache/pokete/pokete.py") as file:
    exec(file.read())


# All playmaps have to have the .trainers array that can also be empty and the .name atribute.
# every trainer Object has to have the:
# .poke = Poke("poundi", 60, player=False)
# .texts = [" < some text to start"]
# .lose_texts = [" < Hahaha!", " < You're a loser!"]
# .win_texts = [" < Your a very good trainer!"]
# .no_poke_texts = [" < I see you don't have a living Pokete"]
# .name = "some name"
# .sx = 30
# .sy = 10
# .will = True
# .gender = "He"
# attributes

# maps
centermap = se.Map(background=" ")
centermap.name = "centermap"
centermap.pretty_name = "Pokete-Center"
playmap_1 = se.Map(background=" ", height=30, width=90)
playmap_1.name = "playmap_1"
playmap_1.pretty_name = "Nice Town"
cave_1 = se.Map(background=" ", height=30, width=90)
cave_1.name = "cave_1"
cave_1.pretty_name = "Nice Town cave"
playmap_2 = se.Map(background=" ", height=30, width=180)
playmap_2.name = "playmap_2"
playmap_2.pretty_name = "Route 1"
playmap_3 = se.Map(background=" ", height=30, width=90)
playmap_3.name = "playmap_3"
playmap_3.pretty_name = "Josi Town"

# movemap
movemap = se.Submap(playmap_1, 0, 0)
figure = se.Object("a")
exclamation = se.Object("!")
multitext = se.Text("")
movemap.underline = se.Square("-", movemap.width, 1)
movemap.deck_label = se.Text("1: Deck")
movemap.exit_label = se.Text("2: Exit")
movemap.code_label = se.Text("")
# adding
movemap.deck_label.add(movemap, 0, movemap.height-1)
movemap.exit_label.add(movemap, 9, movemap.height-1)
movemap.code_label.add(movemap, 0, 0)

# playmap_1
trainer1 = se.Object("a")
trainer1.poke = Poke("poundi", 60, player=False)
trainer1.texts = [" < Wanna fight?"]
trainer1.lose_texts = [" < Hahaha!", " < You're a loser!"]
trainer1.no_poke_texts = [" < I see you don't have a living Pokete"]
trainer1.win_texts = [" < Your a very good trainer!"]
trainer1.name = "Franz"
trainer1.sx = 30
trainer1.sy = 10
trainer1.will = True
trainer1.gender = "He"
playmap_1.trainers = [trainer1]
playmap_1.tree_group_1 = se.Text(""" (()(()((())((()((()
())(())))())))()))(()
 || ||| ||||| |||||
""", ignore=" ")
playmap_1.tree_group_2 = se.Text(""" (()(()((())((()((()
())(())))())))()))(()
 || ||| ||||| |||||
""", ignore=" ")
playmap_1.house = se.Text("""  __________
 /         /\\
/_________/  \\
| # ___ # |  |
|___| |___|__|""", ignore=" ")
playmap_1.meadow2 = se.Text("""    ;;;;;;;;;;;
  ;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;
;;;;;;;;;;;;
 ;;;;;;;;;
""", ignore=" ", ob_class=HightGrass, ob_args={"pokes": ["rato", "hornita", "steini", "voglo", "ostri"], "minlvl": 40, "maxlvl": 128}, state="float")
playmap_1.cave_1_entrance = se.Text("""\  \_/  _____/ \______/
 \_____/""", ignore=" ")
playmap_1.meadow = se.Square(";", 10, 5, state="float", ob_class=HightGrass, ob_args={"pokes": ["rato", "horny", "steini", "vogli", "owol"],"minlvl": 24, "maxlvl": 60})
playmap_1.dor = Dor("#", state="float", arg_proto={"map": centermap, "x": int(centermap.width/2), "y": 7})
playmap_1.dor_cave_1 = Dor(" ", state="float", arg_proto={"map": cave_1, "x": 14, "y": 19})
# adding
trainer1.add(playmap_1, trainer1.sx, trainer1.sy)
playmap_1.meadow2.add(playmap_1, 67, 8)
playmap_1.dor.add(playmap_1, 25, 4)
playmap_1.house.add(playmap_1, 20, 0)
playmap_1.tree_group_1.add(playmap_1, 35, 2)
playmap_1.tree_group_1.add(playmap_1, 25, 14)
playmap_1.cave_1_entrance.add(playmap_1, 60, 0)
playmap_1.meadow.add(playmap_1, 5, 7)
playmap_1.dor_cave_1.add(playmap_1, 74, 0)

# playmap_2
trainer3 = se.Object("a")
trainer3.poke = Poke("ostri", 160, player=False)
trainer3.texts = [" < Isn't that a great day?", " < I traveled here from a far country", " < Do you want to fight against my rare Pokete?"]
trainer3.lose_texts = [" < It is stronger than you might have exspected"]
trainer3.win_texts = [" < Oh, i didn't think you can defeat my Pokete!", " < You are a very good trainer!"]
trainer3.no_poke_texts = [" < I see you don't have a living Pokete"]
trainer3.name = "Wanderer Murrad"
trainer3.sx = 32
trainer3.sy = 12
trainer3.will = True
trainer3.gender = "He"
playmap_2.trainers = [trainer3]
playmap_2.tree_group_1 = se.Text(""" ())
())))
())()
(()))
((())
 |||""", ignore=" ")
playmap_2.tree_group_3 = se.Text(""" ())
())))
())()
(()))
((())
 |||""", ignore=" ")
playmap_2.tree_group_4 = se.Text(""" ())
())))
(()))
())()
())))
(()))
(()))
((())
 |||""", ignore=" ")
playmap_2.tree_group_2 = se.Text("""
                        ())
                       ())))
                       ())())
                      ((())()                                                                              ())
                      (((())                                                                              ()())
                       ())))                                                                              ((())
                       ((())                                                                              (()))
                      ((())))                                                                            (())))
(((()()))))()(((((()))))))()())()()())))()()()))))))(()()()()()()))))))((()))))()(()))))))))(((((())))))))())))
(()())))))(())))))((((())))((((()))((((()()()))))(()()))))()()(()))))))()(()()))))((()))))))))(((()))))))))))()
(()())))))((()()()))()()())))()()))())))))((((()()))))()()()))((((((((()(((((()()()))))(())))))(((())))))))()))
|||||||| |||||| | | | ||| | | |  ||||||| | | ||||||| | | |  |||||| | | |||| | | || |||| ||| ||| ||  |||||| || |""", ignore=" ")
playmap_2.cave_1_entrance = cave_1_entrance = se.Text("""\\
 \\
 |
(
 |
 |
 /
/
""", ignore=" ")
playmap_2.meadow1 = se.Text("""        ;;;;;;
      ;;;;;;;;;;
    ;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;
  ;;;;;; ;;;;;;
 ;;;;;;;;;;;;
 ;;;;;;;;;
  ;;;;;;;""", ignore=" ", ob_class=HightGrass, ob_args={"pokes": ["rato", "hornita", "steini", "voglo"], "minlvl": 60, "maxlvl": 128}, state="float")
playmap_2.meadow2 = se.Text("""      ;;;;;;;
    ;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;
 ;;;;;;;;;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;
     ;;;;;;;;;;;;;
         ;;;;;;""", ignore=" ", ob_class=HightGrass, ob_args={"pokes": ["rato", "hornita", "steini", "voglo"], "minlvl": 60, "maxlvl": 128}, state="float")
playmap_2.dor_cave_1 = Dor(" ", state="float", arg_proto={"map": cave_1, "x": 39, "y": 3})
playmap_2.dor_playmap_3_1 = Dor(" ", state="float", arg_proto={"map": playmap_3, "x": 1, "y": 9})
playmap_2.dor_playmap_3_2 = Dor(" ", state="float", arg_proto={"map": playmap_3, "x": 1, "y": 10})
# adding
trainer3.add(playmap_2, trainer3.sx, trainer3.sy)
playmap_2.tree_group_1.add(playmap_2, 36, 0)
playmap_2.tree_group_3.add(playmap_2, 58, 0)
playmap_2.tree_group_4.add(playmap_2, 106, 0)
playmap_2.tree_group_2.add(playmap_2, 0, 7)
playmap_2.cave_1_entrance.add(playmap_2, 0, 2)
playmap_2.dor_cave_1.add(playmap_2, 1, 5)
playmap_2.dor_playmap_3_1.add(playmap_2, 108, 9)
playmap_2.dor_playmap_3_2.add(playmap_2, 108, 10)
playmap_2.meadow1.add(playmap_2, 10, 0)
playmap_2.meadow2.add(playmap_2, 40, 7)

# cave_1
trainer2 = se.Object("a")
trainer2.poke = Poke("hornita", 128, player=False)
trainer2.texts = [" < Hello noble traveler", " < Are you willing to fight with me?"]
trainer2.lose_texts = [" < Hahaha!", " < Looooser!"]
trainer2.no_poke_texts = [" < I see you don't have a living Pokete"]
trainer2.win_texts = [" < Congratulations!", " < Have a great day!"]
trainer2.name = "Monica"
trainer2.sx = 23
trainer2.sy = 10
trainer2.will = True
trainer2.gender = "She"
cave_1.trainers = [trainer2]
cave_1.innerwalls = se.Text("""+--------+
|        |
|        |                     +-------\_
|        +-----------+         |         )
|                    |         |   +---/¯
|        +--------+  |         |   |
|        |        |  |         |   |
+--------+   +----+  +---------+   |
             |                     |
             |                     |
             |  +-----+ +----------+
      +------+  |     | |
      |         |     +-+
      |  +-+    |
      |  +-+    |
      |         |
      +------+  |
             |  |
             |  |
             |  |""", ignore=" ")
cave_1.inner = se.Text("""##########################################
#         ################################
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
#######         ##########################
#######  ###    ##########################
#######  ###    ##########################
#######         ##########################
##############  ##########################
##############  ##########################
##############  ##########################
##############  ##########################""", ignore="#", ob_class=HightGrass, ob_args={"pokes": ["steini", "bato", "lilstone", "rato"], "minlvl": 40, "maxlvl": 128}, state="float")
cave_1.dor_playmap_1_1 = Dor(" ", state="float", arg_proto={"map": playmap_1, "x": 74, "y": 1})
cave_1.dor_playmap_1_2 = Dor(" ", state="float", arg_proto={"map": playmap_1, "x": 74, "y": 1})
cave_1.dor_playmap_2 = Dor(" ", state="float", arg_proto={"map": playmap_2, "x": 2, "y": 5})
# adding
cave_1.dor_playmap_2.add(cave_1, 40, 3)
trainer2.add(cave_1, trainer2.sx, trainer2.sy)
cave_1.dor_playmap_1_1.add(cave_1, 14, 20)
cave_1.dor_playmap_1_2.add(cave_1, 15, 20)
cave_1.innerwalls.add(cave_1, 0, 0)
cave_1.inner.add(cave_1, 0, 0)

# playmap_3
trainer4 = se.Object("a")
trainer4.poke = Poke("hornita", 200, player=False)
trainer4.texts = [" < Hey!", " < I'm Josi", " < Welcome to Josi Town", " < But first we have to fight!"]
trainer4.lose_texts = [" < Hahaha!", " < Hahaha!", " < You're a fucking loser!"]
trainer4.no_poke_texts = [" < I see you don't have a living Pokete", " < Loooser!"]
trainer4.win_texts = [" < Damn, I lost!"]
trainer4.name = "Josi"
trainer4.sx = 11
trainer4.sy = 5
trainer4.will = True
trainer4.gender = "She"
playmap_3.trainers = [trainer4]
playmap_3.tree_group_1 = se.Text("""())
))()
()))
)()(
))()
()))
()))
(())
|||""", ignore=" ")
playmap_3.tree_group_2 = se.Text("""())
))()
()))
)()(
(())
|||""", ignore=" ")
playmap_3.tree_group_3 = se.Text(""" ())
())()
 |||""", ignore=" ")
playmap_3.house = se.Text("""  __________
 /         /\\
/_________/  \\
| # ___ # |  |
|___| |___|__|""", ignore=" ")
playmap_3.house2 = se.Text("""  ________
 /       /\\
/_______/  \\
|# ___ #|  |
|__| |__|__|""", ignore=" ")
playmap_3.fence1 =  se.Text("""                                   #
  ##################################
  #
  #
  #
  #
  #
  #
###
""", ignore=" ")
playmap_3.fence3 =  se.Text("""###
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  ##################################
                                   #""", ignore=" ")
playmap_3.fence2 =  se.Text("""#
###################################
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
                                  #
###################################
#""", ignore=" ")
playmap_3.dor = Dor("#", state="float", arg_proto={"map": centermap, "x": int(centermap.width/2), "y": 7})
playmap_3.dor_playmap_2_1 = Dor(" ", state="float", arg_proto={"map": playmap_2, "x": 107, "y": 9})
playmap_3.dor_playmap_2_2 = Dor(" ", state="float", arg_proto={"map": playmap_2, "x": 107, "y": 10})
# adding
trainer4.add(playmap_3, trainer4.sx, trainer4.sy)
playmap_3.tree_group_1.add(playmap_3, 0, 0)
playmap_3.tree_group_2.add(playmap_3, 0, 11)
playmap_3.tree_group_3.add(playmap_3, 35, 4)
playmap_3.dor.add(playmap_3, 25, 6)
playmap_3.house.add(playmap_3, 20, 2)
playmap_3.house2.add(playmap_3, 18, 11)
playmap_3.fence1.add(playmap_3, 3, 0)
playmap_3.fence2.add(playmap_3, 45, 0)
playmap_3.fence3.add(playmap_3, 3, 11)
playmap_3.dor_playmap_2_1.add(playmap_3, 0, 9)
playmap_3.dor_playmap_2_2.add(playmap_3, 0, 10)

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


# processing data from save file
figure.pokes = [Poke(poke, session_info["pokes"][poke]["xp"], session_info["pokes"][poke]["hp"]) for poke in session_info["pokes"]]
for poke in figure.pokes:
    for atc, ap in zip(poke.attac_obs, session_info["pokes"][poke.identifier]["ap"]):
        atc.ap = ap if ap != "SKIP" else atc.ap
    for i, atc in enumerate(poke.attac_obs):
        poke.atc_labels[i].rechar(str(i)+": "+atc.name+"-"+str(atc.ap))
figure.name = session_info["user"]
try:
    exec('figure.add('+session_info["map"]+', session_info["x"], session_info["y"])')
except:
    figure.add(playmap_1, 1, 1)
try:
    exec("figure.oldmap = "+session_info["oldmap"])
except:
    figure.oldmap = playmap_1
movemap.name_label = se.Text(figure.name, esccode="\033[1m")
movemap.balls_label = se.Text("", esccode="\033[1m")
movemap.code_label.rechar(figure.map.pretty_name)
balls_label_rechar()
movemap.name_label.add(movemap, 2, movemap.height-2)
movemap.balls_label.add(movemap, 4+len(movemap.name_label.text), movemap.height-2)
movemap.underline.add(movemap, 0, movemap.height-2)

# onjects for detail
detailmap = se.Map(background=" ")
detailmap.name_label = se.Text("Details", esccode="\033[1m")
detailmap.name_attacks = se.Text("Attacks", esccode="\033[1m")
detailmap.line_top = se.Square("_", detailmap.width, 1)
detailmap.line_left = se.Square("|", 1, 16)
detailmap.line_right = se.Square("|", 1, 16)
detailmap.attack_defense = se.Text("Attack:   Defense:")
detailmap.exit_label = se.Text("1: Exit")
detailmap.line_sep1 = se.Square("-", detailmap.width-2, 1)
detailmap.line_sep2 = se.Square("-", detailmap.width-2, 1)
detailmap.line_bottom = se.Square("_", detailmap.width-2, 1)
detailmap.line_middle = se.Square("|", 1, 10)
# adding
detailmap.name_label.add(detailmap, 2, 0)
detailmap.name_attacks.add(detailmap, 2, 6)
detailmap.line_top.add(detailmap, 0, 0)
detailmap.line_left.add(detailmap, 0, 1)
detailmap.line_right.add(detailmap, detailmap.width-1, 1)
detailmap.attack_defense.add(detailmap, 13, 5)
detailmap.exit_label.add(detailmap, 0, detailmap.height-1)
detailmap.line_middle.add(detailmap, round(detailmap.width/2), 7)
detailmap.line_sep1.add(detailmap, 1, 6)
detailmap.line_sep2.add(detailmap, 1, 11)
detailmap.line_bottom.add(detailmap, 1, 16)

# Objects for deckmap
deckmap = se.Map(background=" ")
decksubmap = se.Submap(deckmap, 0, 0)
decksubmap.exit_label = se.Text("1: Exit  ")
decksubmap.move_label = se.Text("2: Move    ")
# adding
decksubmap.exit_label.add(decksubmap, 0, decksubmap.height-1)
decksubmap.move_label.add(decksubmap, 9, decksubmap.height-1)

# objects relevant for fight()
fightmap = se.Map(background=" ")
fightmap.line_left = se.Square("|", 1, fightmap.height-7)
fightmap.line_right = se.Square("|", 1, fightmap.height-7)
fightmap.line_top = se.Square("_", fightmap.width, 1)
fightmap.line_top_text_box = se.Square("-", fightmap.width-2, 1)
fightmap.line_bottom_text_box = se.Square("-", fightmap.width-2, 1)
fightmap.line_middle = se.Square("_", fightmap.width-2, 1)
fightmap.line_l_text_box = se.Text("+\n|\n|\n+")
fightmap.line_r_text_box = se.Text("+\n|\n|\n+")
fightmap.e_underline = se.Text("----------------+")
fightmap.e_sideline = se.Square("|", 1, 3)
fightmap.p_upperline = se.Text("+----------------")
fightmap.p_sideline = se.Square("|", 1, 4)
fightmap.outp = se.Text("")
fightmap.run = se.Text("5: Run!")
fightmap.catch = se.Text("6: Catch")
fightmap.summon = se.Text("7: Deck")
fightmap.shines = [se.Object("\033[1;32m*\033[0m") for i in range(4)]
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
fightmap.line_left.add(fightmap, 0, 1)
fightmap.line_right.add(fightmap, fightmap.width-1, 1)
fightmap.line_top.add(fightmap, 0, 0)
fightmap.line_top_text_box.add(fightmap, 1, fightmap.height-6)
fightmap.line_bottom_text_box.add(fightmap, 1, fightmap.height-3)
fightmap.line_l_text_box.add(fightmap, 0, fightmap.height-6)
fightmap.line_r_text_box.add(fightmap, fightmap.width-1, fightmap.height-6)
fightmap.outp.add(fightmap, 1, fightmap.height-5)
fightmap.e_underline.add(fightmap, 1, 4)
fightmap.e_sideline.add(fightmap, len(fightmap.e_underline.text), 1)
fightmap.p_upperline.add(fightmap, fightmap.width-1-len(fightmap.p_upperline.text), fightmap.height-11)
fightmap.p_sideline.add(fightmap, fightmap.width-1-len(fightmap.p_upperline.text), fightmap.height-10)
fightmap.line_middle.add(fightmap, 1, fightmap.height-7)
fightmap.run.add(fightmap, 38, fightmap.height-2)
fightmap.catch.add(fightmap, 38, fightmap.height-1)
fightmap.summon.add(fightmap, 49, fightmap.height-2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
