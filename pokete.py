#!/usr/bin/env python3
# This software is licensed under the GPL3

import scrap_engine as se
import random, time, os, sys, threading

class Hight_grass(se.Object):
    def action(self, ob):
        if random.randint(0,6) == 0:
            fight([poke for poke in figure.pokes if poke.hp > 0][0], Poke(random.choice([i for i in pokes]), 5, player=False))

class Poke():
    def __init__(self, poke, lvl, player=True):
        self.lvl = lvl
        self.player = player
        for name in ["hp", "atc", "defense"]:
            exec("self."+name+" = int("+pokes[poke][name]+")")
        self.full_hp = self.hp
        self.name = pokes[poke]["name"]
        self.attacs = pokes[poke]["attacs"]
        self.miss_chance = pokes[poke]["miss_chance"]
        self.ico = se.Text(pokes[poke]["ico"])
        self.attac_obs = []
        for atc in self.attacs:
            self.attac_obs.append(Attack(atc))
        if self.player:
            self.atc_labels = []
            for i, atc in enumerate(self.attac_obs):
                self.atc_labels.append(se.Text(str(i)+": "+atc.name+"-"+str(atc.ap)))

    def health_bar_maker(self, oldhp):
        bar_num = round(oldhp*8/self.full_hp)
        if bar_num > 6:
            esccode = "\033[32m"
        elif bar_num > 2:
            esccode = "\033[33m"
        else:
            esccode = "\033[31m"
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
            if self.player:
                for i, atc in enumerate(self.attac_obs):
                    time.sleep(0.1)
                    self.atc_labels[i].rechar(str(i)+": "+atc.name+"-"+str(atc.ap))
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

def exiter():
    global do_exit
    do_exit=True
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

    outp.rechar("")

    enemy.text_name = se.Text(str(enemy.name))
    enemy.text_hp = se.Text("HP:"+str(enemy.hp))
    enemy.text_lvl = se.Text("Lvl:"+str(enemy.lvl))
    enemy.hp_bar = se.Text(8*"#", esccode="\033[32m")
    player.text_hp = se.Text("HP:"+str(player.hp))
    player.text_lvl = se.Text("Lvl:"+str(player.lvl))
    player.text_name = se.Text(str(player.name))
    player.hp_bar = se.Text(8*"#", esccode="\033[32m")
    player.health_bar_maker(player.hp,)

    enemy.text_name.add(fightmap, 1, 1)
    enemy.text_lvl.add(fightmap, 1, 2)
    enemy.text_hp.add(fightmap, 1, 3)
    enemy.ico.add(fightmap, fightmap.width-14, 2)
    enemy.hp_bar.add(fightmap, 8, 3)
    player.text_name.add(fightmap, fightmap.width-17, fightmap.height-10)
    player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-9)
    player.text_hp.add(fightmap, fightmap.width-17, fightmap.height-8)
    player.ico.add(fightmap, 3, fightmap.height-11)
    player.hp_bar.add(fightmap, fightmap.width-10, fightmap.height-8)

    for ob, x, y in zip(player.atc_labels, [1, 1, 19, 19], [fightmap.height-2, fightmap.height-1, fightmap.height-2, fightmap.height-1]):
        ob.add(fightmap, x, y)

    fightmap.show(init=True)

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
                        ev=""
                        break
                    elif ev == "exit":
                        raise KeyboardInterrupt
                    time.sleep(0.1)
            else:
                attack = random.choices([ob for ob in ob.attac_obs], weights=[ob.ap for ob in ob.attac_obs])[0]
            time.sleep(0.3)
            ob.attack(attack, enem)
            ob.text_name.rechar(str(ob.name))
            ob.text_lvl.rechar("Lvl:"+str(ob.lvl))
            ob.text_hp.rechar("HP:"+str(ob.hp))
            fightmap.show()
            time.sleep(0.5)
            if enem.hp <= 0:
                enem.text_hp.rechar("HP:0")
                winner = ob
                break
        fightmap.show()
    outp.rechar(winner.name+"("+("you" if winner.player else "enemy")+") won!")
    fightmap.show()
    time.sleep(1)
    ico = [ob for ob in players if ob != winner][0].ico
    ico.remove()
    deadico1.add(fightmap, ico.x, ico.y)
    fightmap.show()
    time.sleep(0.1)
    deadico1.remove()
    deadico2.add(fightmap, ico.x, ico.y)
    fightmap.show()
    time.sleep(0.1)
    deadico2.remove()
    fightmap.show()

    enemy.text_name.remove()
    enemy.text_lvl.remove()
    enemy.text_hp.remove()
    enemy.ico.remove()
    enemy.hp_bar.remove()
    player.text_name.remove()
    player.text_lvl.remove()
    player.text_hp.remove()
    player.ico.remove()
    player.hp_bar.remove()

    for ob in player.atc_labels:
        ob.remove()

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
        if ev == "'w'":
            figure.direction="t"
            figure.set(figure.x, figure.y-1)
            ev=""
        elif ev == "'a'":
            figure.direction="l"
            figure.set(figure.x-1, figure.y)
            ev=""
        elif ev == "'s'":
            figure.direction="b"
            figure.set(figure.x, figure.y+1)
            ev=""
        elif ev == "'d'":
            figure.direction="r"
            figure.set(figure.x+1, figure.y)
            ev=""
        elif ev == "exit":
            raise KeyboardInterrupt
        time.sleep(0.05)
        if figure.x+5 > movemap.x+movemap.width:
            movemap.set(movemap.x+1, movemap.y)
        if figure.x < movemap.x+5:
            movemap.set(movemap.x-1, movemap.y)
        movemap.remap()
        movemap.show()
    exiter()

attacs={
    "tackle": {
        "name": "Tackle",
        "factor": 3/2,
        "action": "",
        "move": "attack",
        "miss_chance": 0.2,
        "ap": 20,
    },
    "earch_quake": {
        "name": "Earch quake",
        "factor": 0,
        "action": "enem.hp -= 4",
        "move": "pound",
        "miss_chance": 0,
        "ap": 5,
    },
    "wing_hit": {
        "name": "Wing hit",
        "factor": 2.5,
        "action": "",
        "move": "attack",
        "miss_chance": 0.5,
        "ap": 5,
    },
    "brooding": {
        "name": "Brooding",
        "factor": 0,
        "action": "self.hp += 2 if self.hp+2 <= self.full_hp else 0",
        "move": "shine",
        "miss_chance": 0,
        "ap": 5,
    },
    "pepple_fire": {
        "name": "Pepple fire",
        "factor": 1,
        "action": "enem.miss_chance += 1",
        "move": "attack",
        "miss_chance": 0,
        "ap": 3,
    },
    "bite": {
        "name": "Bite",
        "factor": 1.75,
        "action": "",
        "move": "attack",
        "miss_chance": 0.1,
        "ap": 20,
    },
    "politure": {
        "name": "Politure",
        "factor": 0,
        "action": "self.defense += 1; self.atc += 1",
        "move": "shine",
        "miss_chance": 0,
        "ap": 10,
    },
    "chocer": {
        "name": "Chocer",
        "factor": 1,
        "action": "enem.atc -= 1",
        "move": "attack",
        "miss_chance": 0.2,
        "ap": 10,
    },
    "poison_bite": {
        "name": "Poison bite",
        "factor": 1,
        "action": "enem.atc -= 1; enem.defense -= 1",
        "move": "attack",
        "miss_chance": 0.3,
        "ap": 5,
    },
    "power_pick": {
        "name": "Power pick",
        "factor": 2,
        "action": "",
        "move": "attack",
        "miss_chance": 0.4,
        "ap": 5,
    },
}

pokes={
    "steini": {
        "name": "Steini",
        "hp": "25",
        "atc": "self.lvl+2",
        "defense": "self.lvl+4",
        "attacs": ["tackle", "politure"],
        "miss_chance": 0,
        "ico": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
    },
    "poundi": {
        "name": "Poundi",
        "hp": "25",
        "atc": "self.lvl+2",
        "defense": "self.lvl+3",
        "attacs": ["tackle", "politure", "earch_quake"],
        "miss_chance": 0,
        "ico": """   A-A-A
  < o o >
  < --- >
   VvVvV""",
   },
   "lilstone": {
       "name": "Lilstone",
       "hp": "20",
       "atc": "self.lvl+1",
       "defense": "self.lvl+2",
       "attacs": ["tackle", "politure", "pepple_fire"],
       "miss_chance": 0,
       "ico": """
   _____
   |'ᵕ'|
   ‾‾‾‾‾
""",
  },
  "gobost": {
      "name": "Gobost",
      "hp": "20",
      "atc": "self.lvl+2",
      "defense": "self.lvl+1",
      "attacs": ["tackle"],
      "miss_chance": 0,
      "ico": """ .░░░░░░░.
 ░░o░░░o░░
 ░░░░░░░░░
 ░ ░ ░ ░ ░""",
  },
    "vogli": {
        "name": "Vogli",
        "hp": "20",
        "atc": "self.lvl+6",
        "defense": "self.lvl+1",
        "attacs": ["tackle", "power_pick"],
        "miss_chance": 0,
        "ico":"""    A
   <')
    www*
    ||     """
    },
    "voglo": {
        "name": "Voglo",
        "hp": "20",
        "atc": "self.lvl+7",
        "defense": "self.lvl+1",
        "attacs": ["tackle", "power_pick", "wing_hit", "brooding"],
        "miss_chance": 0,
        "ico":"""    ?
   >´)
    www*
    ||     """
    },
    "karpi": {
        "name": "Karpi",
        "hp": "15",
        "atc": "self.lvl",
        "defense": "self.lvl/2",
        "attacs": ["tackle"],
        "miss_chance": 0,
        "ico":"""

  <°))))><
           """
    },
    "würgos": {
        "name": "Würgos",
        "hp": "20",
        "atc": "self.lvl+3",
        "defense": "self.lvl",
        "attacs": ["chocer", "bite", "poison_bite"],
        "miss_chance": 0,
        "ico": """  >'({{{
  }}}}}}}
 {{{{{{{{{
           """
    },
}

playmap_1 = se.Map(background=" ", height=1000, width=1000)
movemap = se.Submap(playmap_1, 0, 0)
figure = se.Object("a")
figure.pokes = []
figure.pokes.append(Poke("voglo", 6))
figure.pokes.append(Poke("poundi", 6))
meadow = se.Square(";", 10, 5, state="float", ob_class=Hight_grass)
figure.add(playmap_1, 1, 1)
meadow.add(playmap_1, 5, 5)

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
e_tril = se.Object("<")
e_trir = se.Object(">")
p_upperline = se.Text("+----------------")
p_sideline = se.Square("|", 1, 4)
p_tril = se.Object("<")
p_trir = se.Object(">")
outp = se.Text("")
shines = [se.Object("\033[1;32m*\033[0m") for i in range(4)]
deadico1 = se.Text("""
    \ /
     o
    / \\
""")
deadico2 = se.Text("""

     o

""")
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
e_tril.add(fightmap, 7, 3)
e_trir.add(fightmap, 16, 3)
p_upperline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-11)
p_sideline.add(fightmap, fightmap.width-1-len(p_upperline.text), fightmap.height-10)
e_tril.add(fightmap, fightmap.width-11, fightmap.height-8)
e_trir.add(fightmap, fightmap.width-2, fightmap.height-8)
line_middle.add(fightmap, 1, fightmap.height-7)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
