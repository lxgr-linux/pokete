#!/usr/bin/env python3

import scrap_engine as se
import random, time

pokes={
    "steini": {
        "ap": "self.lvl+20",
        "name": "Steini",
        "hp": "self.lvl*2",
        "atc": "self.lvl+5",
        "defense": "1+self.lvl/3",
        "ico": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
    }
}

class Poke():
    def __init__(self, poke, lvl):
        self.lvl = lvl
        for name in ["ap", "hp", "atc", "defense"]:
            exec("self."+name+" = "+pokes[poke][name])
        self.name = pokes[poke]["name"]
        self.ico = se.Text(pokes[poke]["ico"])


fightmap = se.Map(background=" ")
line_left = se.Square("|", 1, fightmap.height-7)
line_right = se.Square("|", 1, fightmap.height-7)
line_top = se.Square("_", fightmap.width, 1)
line_middle = se.Square("_", fightmap.width-2, 1)

e_underline = se.Text("----------------+")
e_sideline = se.Square("|", 1, 3)
e_ap = se.Text("AP: ")
e_hp = se.Text("HP: ")
e_lvl = se.Text("Lvl: ")
e_name = se.Text("")

p_upperline = se.Text("+----------------")
p_sideline = se.Square("|", 1, 4)
line_left.add(fightmap, 0, 1)
line_right.add(fightmap, fightmap.width-1, 1)
line_top.add(fightmap, 0, 0)

e_underline.add(fightmap, 1, 4)
e_sideline.add(fightmap, len(e_underline.text), 1)
e_name.add(fightmap, 1, 1)
e_lvl.add(fightmap, 1, 2)
e_ap.add(fightmap, 1, 3)
e_hp.add(fightmap, 10, 3)

p_upperline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-11)
p_sideline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-10)
line_middle.add(fightmap, 1, fightmap.height-7)
fightmap.show(init=True)

enemy = Poke("steini", 5)
e_name.rechar(str(enemy.name))
e_lvl.rechar("Lvl:"+str(enemy.lvl))
e_ap.rechar("AP:"+str(enemy.ap))
e_hp.rechar("HP:"+str(enemy.hp))
enemy.ico.add(fightmap, fightmap.width-14, 2)

fightmap.show()

time.sleep(1)
