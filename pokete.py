#!/usr/bin/env python3
# This software is licensed under the GPL3

import scrap_engine as se
import random, time, os, sys, threading, math
from pathlib import Path

class Hight_grass(se.Object):
    def action(self, ob):
        if random.randint(0,6) == 0:
            if len([poke for poke in figure.pokes[:6] if poke.hp > 0]) > 0:
                fight([poke for poke in figure.pokes[:6] if poke.hp > 0][0], Poke(random.choice([i for i in pokes if i != "__fallback__"]), random.choices(list(range(24, 60)))[0], player=False))
            else:
                fight(Poke("__fallback__", 0), Poke(random.choice([i for i in pokes if i != "__fallback__"]), random.choices(list(range(24, 40)))[0], player=False))

class PC(se.Object):
    def action(self, ob):
        deck(figure.pokes)
        movemap.remap()
        movemap.show(init=True)

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
            time.sleep(0.05)
        multitext.remove()
        movemap.remap()
        movemap.show(init=True)

class Dor(se.Object):
    def __init__(self, char, map_adder, x, y, state="solid"):
        self.char = char
        self.state = state
        self.map_adder = map_adder
        self.added = False
        self.setx = x
        self.sety = y

    def action(self, ob):
        figure.remove()
        figure.add(self.map_adder, self.setx, self.sety)
        game(self.map_adder)

class Heal(se.Object):
    def action(self, ob):
        heal()

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
            outp.rechar(self.name+"("+("you" if self.player else "enemy")+") used "+attac.name+" against "+enem.name+"("+("you" if not self.player else "enemy")+") "+(self.name+" missed!" if n_hp == 0 and attac.factor != 0 else ""))
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
        for i, x, y in zip(shines, [self.ico.x-1, self.ico.x+11, self.ico.x-1, self.ico.x+11], [self.ico.y, self.ico.y, self.ico.y+3, self.ico.y+3]):
            i.add(fightmap, x, y)
            fightmap.show()
            time.sleep(0.2)
        time.sleep(0.2)
        for i in shines:
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

def exiter():
    global do_exit
    do_exit = True
    exit()

def on_press(key):
    global ev
    ev=str(key)

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

def fight(player, enemy, info={"type": "wild", "player": " "}):
    global ev, attack, fightmap, outp

    players = fight_add(player, enemy)

    if info["type"] == "wild":
        outp.rechar("A wild "+enemy.name+" appeared!")
    elif info["type"] == "duel":
        outp.rechar(info["player"]+" started a fight!")
        fightmap.show(init=True)
        time.sleep(2)
        outp.rechar("He used "+enemy.name+" against you!")

    fightmap.show(init=True)
    time.sleep(1)
    fight_running = True

    while fight_running:
        for ob in players:
            enem = [i for i in players if i != ob][0]
            if ob.player:
                outp.rechar(outp.text+("\n" if outp.text != "" else "")+ "What do you want to do?")
                fightmap.show()
                if ob.identifier == "__fallback__":
                    time.sleep(1)
                    outp.rechar("You don't have any living poketes left!")
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
                        outp.rechar("You ran away!")
                        fightmap.show()
                        time.sleep(1)
                        fight_clean_up(player, enemy)
                        return enem
                    elif ev == "'6'":
                        ev = ""
                        if ob.identifier == "__fallback__" or info["type"] == "duel":
                            continue
                        outp.rechar("You threw a poketeball!")
                        arr = [enem.ico, deadico1, deadico2, pball]
                        _i = 1
                        while _i < len(arr):
                            arr[_i-1].remove()
                            arr[_i].add(fightmap, enem.ico.x, enem.ico.y)
                            fightmap.show()
                            time.sleep(0.1)
                            _i += 1
                        time.sleep(random.choice([1,2,3,4]))
                        if random.choices([True, False], weights=[enem.full_hp/enem.hp, enem.full_hp], k=1)[0]:
                            enem.player = True
                            figure.pokes.append(enem)
                            outp.rechar("You catched "+enem.name)
                            fightmap.show()
                            time.sleep(1)
                            pball.remove()
                            fight_clean_up(player, enemy)
                            return
                        else:
                            outp.rechar("You missed!")
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
                        outp.rechar("You have choosen "+player.name)
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
    outp.rechar(winner.name+"("+("you" if winner.player else "enemy")+") won!"+("\nXP + "+str(loser.lose_xp*(2 if info["type"] == "duel" else 1)) if winner.player else ""))
    fightmap.show()
    if winner.player:
        old_lvl = winner.lvl()
        winner.xp += loser.lose_xp*(2 if info["type"] == "duel" else 1)
        winner.text_xp.rechar("XP:"+str(winner.xp-(winner.lvl()**2-1))+"/"+str(((winner.lvl()+1)**2-1)-(winner.lvl()**2-1)))
        winner.text_lvl.rechar("Lvl:"+str(winner.lvl()))
        if old_lvl < winner.lvl():
            time.sleep(1)
            outp.rechar(winner.name+" reached lvl "+str(winner.lvl())+"!")
            winner.move_shine()
            time.sleep(0.5)
    #winner.set_vars()
    fightmap.show()
    time.sleep(1)
    ico = [ob for ob in players if ob != winner][0].ico
    arr = [ico, deadico1, deadico2]
    _i = 1
    while _i < len(arr):
        arr[_i-1].remove()
        arr[_i].add(fightmap, ico.x, ico.y)
        fightmap.show()
        time.sleep(0.1)
        _i += 1
    deadico2.remove()
    fightmap.show()
    fight_clean_up(player, enemy)
    return winner

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
        enemy.pball_small.add(fightmap, len(e_underline.text)-1, 1)

    for ob, x, y in zip(player.atc_labels, [1, 1, 19, 19], [fightmap.height-2, fightmap.height-1, fightmap.height-2, fightmap.height-1]):
        ob.add(fightmap, x, y)

    return [player, enemy]

def deck(pokes, label="Your full deck", in_fight=False):
    global ev

    deckmap.resize(5*int((len(pokes)+1)/2)+2, deckmap.width, deckmap.background)
    se.Text(label, esccode="\033[1m").add(deckmap, 2, 0)
    se.Square("_", deckmap.width, 1).add(deckmap, 0, 0)
    se.Square("|", 1, deckmap.height-2).add(deckmap, 0, 1)
    se.Square("|", 1, deckmap.height-2).add(deckmap, deckmap.width-1, 1)
    se.Square("|", 1, deckmap.height-2).add(deckmap, round(deckmap.width/2), 1)
    se.Square("_", deckmap.width-2, 1).add(deckmap, 1, deckmap.height-2)
    deck_move_label.rechar("2: Move    ")
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
                deck_move_label.rechar("2: Move to?")
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
                deck_move_label.rechar("2: Move    ")
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

def deck_add(poke, map, x, y, in_deck=True):
    for ob, _x, _y in zip([poke.ico, poke.text_name, poke.text_lvl, poke.text_hp, poke.tril, poke.trir, poke.hp_bar, poke.text_xp], [0, 12, 12, 12, 18, 27, 19, 12], [0, 0, 1, 2, 2, 2, 2, 3]):
        ob.add(map, x+_x, y+_y)
    if figure.pokes.index(poke) < 6 and in_deck:
        poke.pball_small.add(map, round(deckmap.width/2)-1 if figure.pokes.index(poke) % 2 == 0 else deckmap.width-2, y)

def deck_remove(poke):
    for ob in [poke.ico, poke.text_name, poke.text_lvl, poke.text_hp, poke.tril, poke.trir, poke.hp_bar, poke.text_xp, poke.pball_small]:
        ob.remove()

def detail(poke):
    global ev
    deck_add(poke, detailmap, 1, 1, False)
    detail_attack_defense.rechar("Attack:"+str(poke.atc)+(4-len(str(poke.atc)))*" "+"Defense:"+str(poke.defense))
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
    os.system("")
    recognising=threading.Thread(target=recogniser)
    recognising.daemon=True
    recognising.start()
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
            move_code_label.rechar(":"+exec_string+"█")
            movemap.show()
            while True:
                if ev == "Key.enter":
                    move_code_label.rechar("")
                    movemap.show()
                    codes(exec_string)
                    break
                elif ev == "exit":
                    move_code_label.rechar("")
                    movemap.show()
                    break
                elif ev == "Key.backspace":
                    if len(exec_string) == 0:
                        move_code_label.rechar("")
                        movemap.show()
                        break
                    exec_string = exec_string[:-1]
                    move_code_label.rechar(":"+exec_string+"█")
                    movemap.show()
                    ev = ""
                elif ev not in ["", "Key.enter", "exit", "Key.backspace", "Key.shift"]:
                    if ev == "Key.space":
                        ev = "' '"
                    exec("global exec_string; exec_string += str("+ev+")")
                    move_code_label.rechar(":"+exec_string+"█")
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
                movemap_text(trainer.x, trainer.y, trainer.texts)
                if len([poke for poke in figure.pokes[:6] if poke.hp > 0]) > 0:
                    winner = fight([poke for poke in figure.pokes[:6] if poke.hp > 0][0], trainer.poke, info={"type": "duel", "player": trainer.name})
                else:
                    winner = fight(Poke("__fallback__", 0), trainer.poke, info={"type": "duel", "player": trainer.name})
                if winner == trainer.poke:
                    movemap_text(trainer.x, trainer.y, trainer.lose_texts)
                else:
                    movemap_text(trainer.x, trainer.y, trainer.win_texts)
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
            if ev != "":
                ev = ""
                break
        multitext.rechar(t)
        movemap.show()
        while True:
            if ev != "":
                break
            time.sleep(0.05)

def main():
    game(playmap_1)

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
        "x": figure.x,
        "y": figure.y,
        "pokes": {poke.identifier: {"xp": poke.xp, "hp": poke.hp, "ap": [atc.ap for atc in poke.attac_obs]} for poke in figure.pokes}
    }
    with open(home+"/.cache/pokete/pokete.py", "w+") as file:
        file.write("session_info="+str(session_info))

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
}

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
        "ico": """   ^---^
   \o o/
   >\./<
"""
    },
}


# reading config file
home = str(Path.home())
Path(home+"/.cache/pokete").mkdir(parents=True, exist_ok=True)
Path(home+"/.cache/pokete/pokete.py").touch(exist_ok=True)
# Default test session_info
session_info = {
    "user": "DEFAULT",
    "x": 1,
    "y": 1,
    "pokes": {
        "steini": {"xp": 35, "hp": "SKIP", "ap": ["SKIP", "SKIP"]}
    }
}
with open(home+"/.cache/pokete/pokete.py") as file:
    exec(file.read())

# objects for main()
playmap_1 = se.Map(background=" ", height=1000, width=1000)
movemap = se.Submap(playmap_1, 0, 0)
figure = se.Object("a")
trainer1 = se.Object("a")
trainer1.poke = Poke("poundi", 60, player=False)
trainer1.texts = [" < Wanna fight?"]
trainer1.lose_texts = [" < Hahaha!", " < You're a loser!"]
trainer1.win_texts = [" < Your a very good trainer!"]
trainer1.name = "Franz"
trainer1.sx = 30
trainer1.sy = 10
trainer1.will = True
playmap_1.trainers = [trainer1]
centermap = se.Map(background=" ")
centermap.trainers = []
exclamation = se.Object("!")
tree_group_1 = se.Text(""" (()(()((())((()((()
())(())))())))()))(()
 || ||| ||||| |||||
""", ignore=" ")
tree_group_2 = se.Text(""" (()(()((())((()((()
())(())))())))()))(()
 || ||| ||||| |||||
""", ignore=" ")
house = se.Text("""  __________
 /         /\\
/_________/  \\
| # ___ # |  |
|___| |___|__|""", ignore=" ")
inner_center = se.Text(""" ________________
 |______________|
 |     |a |     |
 |     ¯ ¯¯     |
 |              |
 |______  ______|
 |_____|  |_____|""", ignore=" ")
multitext = se.Text("")
figure.pokes = [Poke(poke, session_info["pokes"][poke]["xp"], session_info["pokes"][poke]["hp"]) for poke in session_info["pokes"]]
for poke in figure.pokes:
    for atc, ap in zip(poke.attac_obs, session_info["pokes"][poke.identifier]["ap"]):
        atc.ap = ap if ap != "SKIP" else atc.ap
    for i, atc in enumerate(poke.attac_obs):
        poke.atc_labels[i].rechar(str(i)+": "+atc.name+"-"+str(atc.ap))
figure.name = session_info["user"]
meadow = se.Square(";", 10, 5, state="float", ob_class=Hight_grass)
center = Heal("+", state="float")
dor = Dor("#", centermap, int(centermap.width/2), 7, state="float")
dor_back1 = Dor(" ", playmap_1, 25, 5, state="float")
dor_back2 = Dor(" ", playmap_1, 25, 5, state="float")
interact = CenterInteract("¯", state="float")
pc = PC("#", state="float")
center.add(playmap_1, 10, 4)
pc.add(playmap_1, 9, 4)
trainer1.add(playmap_1, trainer1.sx, trainer1.sy)
house.add(playmap_1, 20, 0)
dor.add(playmap_1, 25, 4)
tree_group_1.add(playmap_1, 25, 14)
tree_group_1.add(playmap_1, 35, 2)
meadow.add(playmap_1, 5, 7)
inner_center.add(centermap, int(centermap.width/2)-8, 1)
dor_back1.add(centermap, int(centermap.width/2), 8)
dor_back1.add(centermap, int(centermap.width/2)+1, 8)
interact.add(centermap, int(centermap.width/2), 4)
try:
    figure.add(playmap_1, session_info["x"], session_info["y"])
except:
    figure.add(playmap_1, 1, 1)

# objects for movemap
movemap_underline = se.Square("-", movemap.width, 1)
name_label = se.Text(figure.name, esccode="\033[1m")
move_deck_label = se.Text("1: Deck")
move_exit_label = se.Text("2: Exit")
move_code_label = se.Text("")
name_label.add(movemap, 2, movemap.height-2)
move_deck_label.add(movemap, 0, movemap.height-1)
move_exit_label.add(movemap, 9, movemap.height-1)
movemap_underline.add(movemap, 0, movemap.height-2)
move_code_label.add(movemap, 0, 0)

# onjects for detail
detailmap = se.Map(background=" ")
detail_name = se.Text("Details", esccode="\033[1m")
detail_name_attacks = se.Text("Attacks", esccode="\033[1m")
detail_line_top = se.Square("_", detailmap.width, 1)
detail_line_left = se.Square("|", 1, 16)
detail_line_right = se.Square("|", 1, 16)
detail_attack_defense = se.Text("Attack:   Defense:")
detail_exit_label = se.Text("1: Exit")
detail_line_sep1 = se.Square("-", detailmap.width-2, 1)
detail_line_sep2 = se.Square("-", detailmap.width-2, 1)
detail_line_bottom = se.Square("_", detailmap.width-2, 1)
detail_line_middle = se.Square("|", 1, 10)
detail_name.add(detailmap, 2, 0)
detail_name_attacks.add(detailmap, 2, 6)
detail_line_top.add(detailmap, 0, 0)
detail_line_left.add(detailmap, 0, 1)
detail_line_right.add(detailmap, detailmap.width-1, 1)
detail_attack_defense.add(detailmap, 13, 5)
detail_exit_label.add(detailmap, 0, detailmap.height-1)
detail_line_middle.add(detailmap, round(detailmap.width/2), 7)
detail_line_sep1.add(detailmap, 1, 6)
detail_line_sep2.add(detailmap, 1, 11)
detail_line_bottom.add(detailmap, 1, 16)

# Objects for deckmap
deckmap = se.Map(background=" ")
decksubmap = se.Submap(deckmap, 0, 0)
deck_exit_label = se.Text("1: Exit  ")
deck_move_label = se.Text("2: Move    ")
deck_exit_label.add(decksubmap, 0, decksubmap.height-1)
deck_move_label.add(decksubmap, 9, decksubmap.height-1)

# objects relevant for fight()
fightmap = se.Map(background=" ")
line_left = se.Square("|", 1, fightmap.height-7)
line_right = se.Square("|", 1, fightmap.height-7)
line_top = se.Square("_", fightmap.width, 1)
line_top_text_box = se.Square("-", fightmap.width-2, 1)
line_bottom_text_box = se.Square("-", fightmap.width-2, 1)
line_middle = se.Square("_", fightmap.width-2, 1)
line_l_text_box = se.Text("+\n|\n|\n+")
line_r_text_box = se.Text("+\n|\n|\n+")
e_underline = se.Text("----------------+")
e_sideline = se.Square("|", 1, 3)
p_upperline = se.Text("+----------------")
p_sideline = se.Square("|", 1, 4)
outp = se.Text("")
run = se.Text("5: Run!")
catch = se.Text("6: Catch")
summon = se.Text("7: Deck")
shines = [se.Object("\033[1;32m*\033[0m") for i in range(4)]
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
line_left.add(fightmap, 0, 1)
line_right.add(fightmap, fightmap.width-1, 1)
line_top.add(fightmap, 0, 0)
line_top_text_box.add(fightmap, 1, fightmap.height-6)
line_bottom_text_box.add(fightmap, 1, fightmap.height-3)
line_l_text_box.add(fightmap, 0, fightmap.height-6)
line_r_text_box.add(fightmap, fightmap.width-1, fightmap.height-6)
outp.add(fightmap, 1, fightmap.height-5)
e_underline.add(fightmap, 1, 4)
e_sideline.add(fightmap, len(e_underline.text), 1)
p_upperline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-11)
p_sideline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-10)
line_middle.add(fightmap, 1, fightmap.height-7)
run.add(fightmap, 38, fightmap.height-2)
catch.add(fightmap, 38, fightmap.height-1)
summon.add(fightmap, 49, fightmap.height-2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
