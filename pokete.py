#!/usr/bin/env python3
# This software is licensed under the GPL3

import scrap_engine as se
import random, time

attacs={
    "tackle": {
        "atcname": "Tackle",
        "atcfactor": 3/2,
        "defbetter": 0,
        "atcbetter": 0,
        "atcap": 5,
    },
    "politure": {
        "atcname": "Politure",
        "atcfactor": 0,
        "defbetter": 5,
        "atcbetter": 5,
        "atcap": 5,
    },
}

pokes={
    "steini": {
        "ap": "self.lvl+20",
        "name": "Steini",
        "hp": "self.lvl*2",
        "atc": "self.lvl+5",
        "defense": "1+self.lvl/3",
        "attacs": ["tackle", "politure"],
        "ico": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
    }
}


class Poke():
    def __init__(self, poke, lvl, player=True):
        self.lvl = lvl
        self.player = player
        for name in ["ap", "hp", "atc", "defense"]:
            exec("self."+name+" = "+pokes[poke][name])
        self.name = pokes[poke]["name"]
        self.attacs = pokes[poke]["attacs"]
        self.ico = se.Text(pokes[poke]["ico"])

    def attack(self, attac, enemy):
        if self.ap > 0:
            enemy.hp = round(enemy.hp - self.atc * attacs[attac]["atcfactor"] / enemy.defense)
            self.defense += attacs[attac]["defbetter"]
            self.atc += attacs[attac]["atcbetter"]
            self.ap -= attacs[attac]["atcap"]


enemy = Poke("steini", 5, player=False)
player = Poke("steini", 5)

fightmap = se.Map(background=" ")
line_left = se.Square("|", 1, fightmap.height-7)
line_right = se.Square("|", 1, fightmap.height-7)
line_top = se.Square("_", fightmap.width, 1)
line_middle = se.Square("_", fightmap.width-2, 1)

e_underline = se.Text("----------------+")
e_sideline = se.Square("|", 1, 3)
enemy.text_ap = se.Text("AP: ")
enemy.text_hp = se.Text("HP: ")
enemy.text_lvl = se.Text("Lvl: ")
enemy.text_name = se.Text("")
player.text_ap = se.Text("AP: ")
player.text_hp = se.Text("HP: ")
player.text_lvl = se.Text("Lvl: ")
player.text_name = se.Text("")

p_upperline = se.Text("+----------------")
p_sideline = se.Square("|", 1, 4)
line_left.add(fightmap, 0, 1)
line_right.add(fightmap, fightmap.width-1, 1)
line_top.add(fightmap, 0, 0)

e_underline.add(fightmap, 1, 4)
e_sideline.add(fightmap, len(e_underline.text), 1)
enemy.text_name.add(fightmap, 1, 1)
enemy.text_lvl.add(fightmap, 1, 2)
enemy.text_ap.add(fightmap, 1, 3)
enemy.text_hp.add(fightmap, 10, 3)

p_upperline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-11)
p_sideline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-10)
player.text_name.add(fightmap, fightmap.width-17, fightmap.height-10)
player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-9)
player.text_ap.add(fightmap, fightmap.width-17, fightmap.height-8)
player.text_hp.add(fightmap, fightmap.width-8, fightmap.height-8)

line_middle.add(fightmap, 1, fightmap.height-7)
fightmap.show(init=True)

enemy.text_name.rechar(str(enemy.name))
enemy.text_lvl.rechar("Lvl:"+str(enemy.lvl))
enemy.text_ap.rechar("AP:"+str(enemy.ap))
enemy.text_hp.rechar("HP:"+str(enemy.hp))
enemy.ico.add(fightmap, fightmap.width-14, 2)

player.text_name.rechar(str(player.name))
player.text_lvl.rechar("Lvl:"+str(player.lvl))
player.text_ap.rechar("AP:"+str(player.ap))
player.text_hp.rechar("HP:"+str(player.hp))
player.ico.add(fightmap, 3, fightmap.height-11)

fightmap.show()

players = [player, enemy]
while player.hp > 0 and enemy.hp > 0:
    for ob in players:
        if ob.hp <= 0:
            ob.text_hp.rechar("HP:0")
            break
        ob.attack("tackle", [i for i in players if i != ob][0])
        ob.text_name.rechar(str(ob.name))
        ob.text_lvl.rechar("Lvl:"+str(ob.lvl))
        ob.text_ap.rechar("AP:"+str(ob.ap))
        ob.text_hp.rechar("HP:"+str(ob.hp))
        fightmap.show()
        time.sleep(0.5)
    fightmap.show()

time.sleep(1)
