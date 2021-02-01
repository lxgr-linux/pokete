#!/usr/bin/env python3
# This software is licensed under the GPL3

import scrap_engine as se
import random, time, os, sys, threading, math
from pathlib import Path

class Hight_grass(se.Object):
    def action(self, ob):
        if random.randint(0,6) == 0:
            fight([poke for poke in figure.pokes if poke.hp > 0][0], Poke(random.choice([i for i in pokes]), 24, player=False))

class Heal(se.Object):
    def action(self, ob):
        for poke in figure.pokes:
            poke.hp = poke.full_hp
            poke.miss_chance = poke.full_miss_chance
            poke.text_hp.rechar("HP:"+str(poke.hp))
            poke.health_bar_maker(poke.hp)
            for atc in poke.attac_obs:
                atc.ap = atc.max_ap
            poke.label_rechar()

class Poke():
    def __init__(self, poke, xp, _hp="SKIP", player=True):
        self.xp = xp
        self.player = player
        self.identifier = poke
        self.set_vars()
        for name in ["hp", "attacs", "name", "miss_chance"]:
            exec("self."+name+" = pokes[self.identifier][name]")
        self.full_hp = self.hp
        self.full_miss_chance = self.miss_chance
        self.hp_bar = se.Text(8*"#", esccode="\033[32m")
        if _hp != "SKIP":
            self.hp = _hp if _hp <= self.full_hp else self.hp
            self.health_bar_maker(self.hp)
        self.desc = se.Text(liner(pokes[poke]["desc"], movemap.width-34))
        self.ico = se.Text(pokes[poke]["ico"])
        self.text_hp = se.Text("HP:"+str(self.hp))
        self.text_lvl = se.Text("Lvl:"+str(self.lvl()))
        self.text_name = se.Text(str(self.name), esccode="\033[4m")
        self.text_xp = se.Text("XP:"+str(self.xp-(self.lvl()**2-1))+"/"+str(((self.lvl()+1)**2-1)-(self.lvl()**2-1)))
        self.tril = se.Object("<")
        self.trir = se.Object(">")
        self.attac_obs = [Attack(atc) for atc in self.attacs]
        self.atc_labels = [se.Text(str(i)+": "+atc.name+"-"+str(atc.ap)) for i, atc in enumerate(self.attac_obs)]

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
        self.desc = se.Text(self.desc)


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

def fight(player, enemy):
    global ev, attack, fightmap, outp

    outp.rechar("A wild "+enemy.name+" appeared!")

    enemy.tril.add(fightmap, 7, 3)
    enemy.trir.add(fightmap, 16, 3)
    enemy.text_name.add(fightmap, 1, 1)
    enemy.text_lvl.add(fightmap, 1, 2)
    enemy.text_hp.add(fightmap, 1, 3)
    enemy.ico.add(fightmap, fightmap.width-14, 2)
    enemy.hp_bar.add(fightmap, 8, 3)
    player.tril.add(fightmap, fightmap.width-11, fightmap.height-8)
    player.trir.add(fightmap, fightmap.width-2, fightmap.height-8)
    player.text_name.add(fightmap, fightmap.width-17, fightmap.height-10)
    player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-9)
    player.text_hp.add(fightmap, fightmap.width-17, fightmap.height-8)
    player.ico.add(fightmap, 3, fightmap.height-11)
    player.hp_bar.add(fightmap, fightmap.width-10, fightmap.height-8)

    if enemy.name in [ob.name for ob in figure.pokes]:
        pball_small.add(fightmap, len(e_underline.text)-1, 1)

    for ob, x, y in zip(player.atc_labels, [1, 1, 19, 19], [fightmap.height-2, fightmap.height-1, fightmap.height-2, fightmap.height-1]):
        ob.add(fightmap, x, y)

    fightmap.show(init=True)
    time.sleep(1)

    players = [player, enemy]
    while player.hp > 0 and enemy.hp > 0:
        for ob in players:
            enem = [i for i in players if i != ob][0]
            if ob.player:
                outp.rechar(outp.text+("\n" if outp.text != "" else "")+ "What do you want to do?")
                fightmap.show()
                while True:
                    if ev in ["'"+str(i)+"'" for i in range(len(ob.attacs))]:
                        exec("global attack; attack = ob.attac_obs[int("+ev+")]")
                        if attack.ap == 0:
                            continue
                        ev=""
                        break
                    elif ev == "'5'":
                        outp.rechar("You ran away!")
                        fightmap.show()
                        time.sleep(1)
                        fight_clean_up(player, enemy)
                        return
                    elif ev == "'6'":
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
                        ev = ""
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
                enem.text_hp.rechar("HP:0")
                winner = ob
                break
        fightmap.show()
    outp.rechar(winner.name+"("+("you" if winner.player else "enemy")+") won!"+("\nXP + 2" if winner.player else ""))
    winner.xp += 2
    winner.text_xp.rechar("XP:"+str(winner.xp-(winner.lvl()**2-1))+"/"+str(((winner.lvl()+1)**2-1)-(winner.lvl()**2-1)))
    winner.text_lvl.rechar("Lvl:"+str(winner.lvl()))
    winner.set_vars()
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

def fight_clean_up(player, enemy):
    for ob in [enemy.text_name, enemy.text_lvl, enemy.text_hp, enemy.ico, enemy.hp_bar, enemy.tril, enemy.trir, player.text_name, player.text_lvl, player.text_hp, player.ico, player.hp_bar, player.tril, player.trir, pball_small]+player.atc_labels:
        ob.remove()

def deck():
    global ev

    for poke, x, y in zip(figure.pokes, [1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1], [1, 1, 6, 6, 11, 11]):
        deck_add(poke, deckmap, x, y)
    deckmap.show(init=True)
    _first_index = ""
    _second_index = ""
    deck_index.index = 0
    deck_index.set(figure.pokes[deck_index.index].text_name.x+len(figure.pokes[deck_index.index].text_name.text)+1, figure.pokes[deck_index.index].text_name.y)
    while True:
        if ev == "'1'":
            ev=""
            for poke in figure.pokes:
                deck_remove(poke)
            return
        elif ev == "'2'":
            ev=""
            if _first_index == "":
                _first_index = deck_index.index
                deck_move_label.rechar("2: Move to?")
            else:
                _second_index = deck_index.index
                _first_item = figure.pokes[_first_index]
                _second_item = figure.pokes[_second_index]
                figure.pokes[_first_index] = _second_item
                figure.pokes[_second_index] = _first_item
                _first_index = ""
                _second_index = ""
                for poke in figure.pokes:
                    deck_remove(poke)
                for poke, x, y in zip(figure.pokes, [1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1], [1, 1, 6, 6, 11, 11]):
                    deck_add(poke, deckmap, x, y)
                deck_index.set(figure.pokes[deck_index.index].text_name.x+len(figure.pokes[deck_index.index].text_name.text)+1, figure.pokes[deck_index.index].text_name.y)
                deck_move_label.rechar("2: Move")
                deckmap.show()
        elif ev == "'a'":
            if deck_index.index != 0:
                deck_index.index -= 1
            else:
                deck_index.index = len(figure.pokes)-1
            deck_index.set(figure.pokes[deck_index.index].text_name.x+len(figure.pokes[deck_index.index].text_name.text)+1, figure.pokes[deck_index.index].text_name.y)
            ev=""
        elif ev == "'d'":
            if deck_index.index != len(figure.pokes)-1:
                deck_index.index += 1
            else:
                deck_index.index = 0
            deck_index.set(figure.pokes[deck_index.index].text_name.x+len(figure.pokes[deck_index.index].text_name.text)+1, figure.pokes[deck_index.index].text_name.y)
            ev=""
        elif ev == "'s'":
            if deck_index.index+2 < len(figure.pokes):
                deck_index.index += 2
            elif deck_index.index+2 == len(figure.pokes):
                deck_index.index = 0
            elif deck_index.index+2 == len(figure.pokes)+1:
                deck_index.index = 1
            deck_index.set(figure.pokes[deck_index.index].text_name.x+len(figure.pokes[deck_index.index].text_name.text)+1, figure.pokes[deck_index.index].text_name.y)
            ev=""
        elif ev == "'w'":
            if deck_index.index-2 >= 0:
                deck_index.index -= 2
            elif deck_index.index-2 == -2:
                deck_index.index = len(figure.pokes)-2
            elif deck_index.index-2 == -1:
                deck_index.index = len(figure.pokes)-1
            else:
                deck_index.index = len(figure.pokes)-1
            deck_index.set(figure.pokes[deck_index.index].text_name.x+len(figure.pokes[deck_index.index].text_name.text)+1, figure.pokes[deck_index.index].text_name.y)
            ev=""
        elif ev == "Key.enter":
            ev=""
            for poke in figure.pokes:
                deck_remove(poke)
            detail(figure.pokes[deck_index.index])
            for poke, x, y in zip(figure.pokes, [1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1, 1, round(deckmap.width/2)+1], [1, 1, 6, 6, 11, 11]):
                deck_add(poke, deckmap, x, y)
            deckmap.show(init=True)
        elif ev == "exit":
            raise KeyboardInterrupt
        time.sleep(0.05)
        deckmap.show()

def deck_add(poke, map, x, y):
    for ob, _x, _y in zip([poke.ico, poke.text_name, poke.text_lvl, poke.text_hp, poke.tril, poke.trir, poke.hp_bar, poke.text_xp], [0, 12, 12, 12, 18, 27, 19, 12], [0, 0, 1, 2, 2, 2, 2, 3]):
        ob.add(map, x+_x, y+_y)

def deck_remove(poke):
    for ob in [poke.ico, poke.text_name, poke.text_lvl, poke.text_hp, poke.tril, poke.trir, poke.hp_bar, poke.text_xp]:
        ob.remove()

def detail(poke):
    global ev
    deck_add(poke, detailmap, 1, 1)
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

def main():
    global ev
    ev=""
    os.system("")
    recognising=threading.Thread(target=recogniser)
    recognising.daemon=True
    recognising.start()

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
            deck()
            movemap.show(init=True)
        elif ev == "'2'":
            ev=""
            save()
            exiter()
        elif ev == "exit":
            raise KeyboardInterrupt
        time.sleep(0.05)
        if figure.x+5 > movemap.x+movemap.width:
            movemap.set(movemap.x+1, movemap.y)
        if figure.x < movemap.x+5:
            movemap.set(movemap.x-1, movemap.y)
        movemap.remap()
        movemap.show()

def save():
    session_info={
        "user": figure.name,
        "x": figure.x,
        "y": figure.y,
        "pokes": {
        }
    }

    for poke in figure.pokes:
        session_info["pokes"][poke.identifier] = [poke.xp, poke.hp, [atc.ap for atc in poke.attac_obs]]

    with open(home+"/.cache/pokete/pokete.py", "w+") as file:
        file.write("session_info="+str(session_info))


attacs={
    "tackle": {
        "name": "Tackle",
        "factor": 3/2,
        "action": "",
        "move": "attack",
        "miss_chance": 0.2,
        "desc": "Tackles the enemy very hard",
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
    "sucker": {
        "name": "Sucker",
        "factor": 0,
        "action": "enem.hp -=2; self.hp +=2 if self.hp+2 <= self.full_hp else 0",
        "move": "attack",
        "miss_chance": 0,
        "desc": "Sucks 2 HP from the enemy and adds it to it's own",
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
}

pokes={
    "steini": {
        "name": "Steini",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+4",
        "attacs": ["tackle", "politure"],
        "miss_chance": 0,
        "desc": "A squared stone that can casually be found on the ground",
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
      "attacs": ["sucker"],
      "miss_chance": 0,
      "desc": "A plant Pokete, that's often mistaken for a normal flower",
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
      "attacs": ["tackle"],
      "miss_chance": 0,
      "desc": "A scary ghost Pokete that lives in caves and old houses",
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
        "ico": """  >'({{{
  }}}}}}}
 {{{{{{{{{
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
        "steini": [35, "SKIP", ["SKIP", "SKIP"]]
    }
}
with open(home+"/.cache/pokete/pokete.py") as file:
    exec(file.read())

# objects for main()
playmap_1 = se.Map(background=" ", height=1000, width=1000)
movemap = se.Submap(playmap_1, 0, 0)
figure = se.Object("a")
figure.pokes = [Poke(poke, session_info["pokes"][poke][0], session_info["pokes"][poke][1]) for poke in session_info["pokes"]]
for poke in figure.pokes:
    for atc, ap in zip(poke.attac_obs, session_info["pokes"][poke.identifier][2]):
        atc.ap = ap if ap != "SKIP" else atc.ap
    for i, atc in enumerate(poke.attac_obs):
        poke.atc_labels[i].rechar(str(i)+": "+atc.name+"-"+str(atc.ap))
figure.name = session_info["user"]
meadow = se.Square(";", 10, 5, state="float", ob_class=Hight_grass)
center = Heal("+", state="float")
try:
    figure.add(playmap_1, session_info["x"], session_info["y"])
except:
    figure.add(playmap_1, 1, 1)
meadow.add(playmap_1, 5, 5)
center.add(playmap_1, 10, 4)

# objects for movemap
movemap_underline = se.Square("-", movemap.width, 1)
name_label = se.Text(figure.name, esccode="\033[1m")
move_deck_label = se.Text("1: Deck")
move_exit_label = se.Text("2: Exit")
name_label.add(movemap, 2, movemap.height-2)
move_deck_label.add(movemap, 0, movemap.height-1)
move_exit_label.add(movemap, 9, movemap.height-1)
movemap_underline.add(movemap, 0, movemap.height-2)

# objects for deck
deckmap = se.Map(background=" ")
deck_name = se.Text("Your deck", esccode="\033[1m")
deck_line_top = se.Square("_", deckmap.width, 1)
deck_line_sep1 = se.Square("-", deckmap.width-2, 1)
deck_line_sep2 = se.Square("-", deckmap.width-2, 1)
deck_line_left = se.Square("|", 1, 15)
deck_line_right = se.Square("|", 1, 15)
deck_line_middle = se.Square("|", 1, 15)
deck_line_bottom = se.Square("_", deckmap.width-2, 1)
deck_exit_label = se.Text("1: Exit")
deck_move_label = se.Text("2: Move")
deck_index = se.Object("*")
deck_name.add(deckmap, 2, 0)
deck_line_left.add(deckmap, 0, 1)
deck_line_right.add(deckmap, deckmap.width-1, 1)
deck_line_middle.add(deckmap, round(deckmap.width/2), 1)
deck_line_top.add(deckmap, 0, 0)
deck_line_sep1.add(deckmap, 1, 5)
deck_line_sep2.add(deckmap, 1, 10)
deck_line_bottom.add(deckmap, 1, 15)
deck_exit_label.add(deckmap, 0, deckmap.height-1)
deck_move_label.add(deckmap, 9, deckmap.height-1)
deck_index.add(deckmap, 8, deckmap.height-1)

# onjects for detail
detailmap = se.Map(background=" ")
detail_name = se.Text("Details", esccode="\033[1m")
detail_name_attacks = se.Text("Attacks", esccode="\033[1m")
detail_line_top = se.Square("_", detailmap.width, 1)
detail_line_left = se.Square("|", 1, 16)
detail_line_right = se.Square("|", 1, 16)
detail_attack_defense = se.Text("Attack:   Defense:")
detail_exit_label = se.Text("1: Exit")
detail_line_sep1 = se.Square("-", deckmap.width-2, 1)
detail_line_sep2 = se.Square("-", deckmap.width-2, 1)
detail_line_bottom = se.Square("_", deckmap.width-2, 1)
detail_line_middle = se.Square("|", 1, 10)
detail_name.add(detailmap, 2, 0)
detail_name_attacks.add(detailmap, 2, 6)
detail_line_top.add(detailmap, 0, 0)
detail_line_left.add(detailmap, 0, 1)
detail_line_right.add(detailmap, detailmap.width-1, 1)
detail_attack_defense.add(detailmap, 13, 5)
detail_exit_label.add(detailmap, 0, detailmap.height-1)
detail_line_middle.add(detailmap, round(deckmap.width/2), 7)
detail_line_sep1.add(detailmap, 1, 6)
detail_line_sep2.add(detailmap, 1, 11)
detail_line_bottom.add(detailmap, 1, 16)

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
shines = [se.Object("\033[1;32m*\033[0m") for i in range(4)]
pball_small = se.Object("o")
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
