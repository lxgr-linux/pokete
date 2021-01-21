#!/usr/bin/env python3
# This software is licensed under the GPL3

import scrap_engine as se
import random, time, os, sys, threading

class Poke():
    def __init__(self, poke, lvl, player=True):
        self.lvl = lvl
        self.player = player
        for name in ["ap", "hp", "atc", "defense"]:
            exec("self."+name+" = int("+pokes[poke][name]+")")
        self.name = pokes[poke]["name"]
        self.attacs = pokes[poke]["attacs"]
        self.ico = se.Text(pokes[poke]["ico"])

    def attack(self, attac, enem):
        if self.ap > 0:
            time.sleep(0.4)
            self.ico.move(3 if self.player else -3, -2 if self.player else 2)
            fightmap.show()
            time.sleep(0.3)
            self.ico.move(-3 if self.player else 3, 2 if self.player else -2)
            fightmap.show()
            oldhp = enem.hp
            oldap = self.ap
            enem.hp = round(enem.hp - (self.atc * attac.factor / enem.defense)*random.choice([0.75, 1, 1.26]))
            self.defense += attac.defbetter
            self.atc += attac.atcbetter
            self.ap -= attac.ap
            outp.rechar(self.name+"("+("you" if self.player else "enemy")+") used "+attac.name+" against "+enem.name+"("+("you" if not self.player else "enemy")+")")
            while oldhp > enem.hp and oldhp > 0:
                oldhp-=1
                enem.text_hp.rechar("HP:"+str(oldhp), esccode="\033[33m")
                time.sleep(0.1)
                fightmap.show()
            enem.text_hp.rechar("HP:"+str(oldhp))
            while oldap > self.ap and oldap > 0:
                oldap-=1
                self.text_ap.rechar("AP:"+str(oldap))
                time.sleep(0.1)
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

attacs={
    "tackle": {
        "name": "Tackle",
        "factor": 3/2,
        "defbetter": 0,
        "atcbetter": 0,
        "ap": 5,
    },
    "politure": {
        "name": "Politure",
        "factor": 0,
        "defbetter": 5,
        "atcbetter": 5,
        "ap": 5,
    },
}

for attac in attacs:
    exec(attac+"=Attack(attac)")

pokes={
    "steini": {
        "ap": "self.lvl+20",
        "name": "Steini",
        "hp": "self.lvl*2",
        "atc": "self.lvl+2",
        "defense": "4+self.lvl/3",
        "attacs": [tackle, politure],
        "ico": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
    },
    "vogli": {
        "ap": "self.lvl+20",
        "name": "Vogli",
        "hp": "self.lvl*2",
        "atc": "self.lvl+6",
        "defense": "self.lvl/3",
        "attacs": [tackle],
        "ico":"""    A
   <')
    www*
    ||     """
    },
    "karpi": {
        "ap": "self.lvl+5",
        "name": "Karpi",
        "hp": "self.lvl*3/2",
        "atc": "self.lvl",
        "defense": "self.lvl/4",
        "attacs": [tackle],
        "ico":"""

  <°))))><
           """
    },
    "würgos": {
        "ap": "self.lvl+5",
        "name": "Würgos",
        "hp": "self.lvl*3/2",
        "atc": "self.lvl",
        "defense": "self.lvl/4",
        "attacs": [tackle],
        "ico": """ {{{{{{{{{
  }}}}}}}
  >'({{{
           """
    },
}


ev=""
os.system("")
recognising=threading.Thread(target=recogniser)
recognising.daemon=True
recognising.start()

def fight():
    global ev, attack, fightmap, outp

    enemy = Poke(random.choice([i for i in pokes]), 5, player=False)
    player = Poke(random.choice([i for i in pokes]), 6)

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

    enemy.text_ap = se.Text("AP: ")
    enemy.text_hp = se.Text("HP: ")
    enemy.text_lvl = se.Text("Lvl: ")
    enemy.text_name = se.Text("")
    player.text_ap = se.Text("AP: ")
    player.text_hp = se.Text("HP: ")
    player.text_lvl = se.Text("Lvl: ")
    player.text_name = se.Text("")

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

    enemy.text_name.add(fightmap, 1, 1)
    enemy.text_lvl.add(fightmap, 1, 2)
    enemy.text_ap.add(fightmap, 1, 3)
    enemy.text_hp.add(fightmap, 10, 3)

    player.text_name.add(fightmap, fightmap.width-17, fightmap.height-10)
    player.text_lvl.add(fightmap, fightmap.width-17, fightmap.height-9)
    player.text_ap.add(fightmap, fightmap.width-17, fightmap.height-8)
    player.text_hp.add(fightmap, fightmap.width-8, fightmap.height-8)

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

    player.atc_labels = []

    for i, atc in enumerate(player.attacs):
        player.atc_labels.append(se.Text(str(i)+": "+atc.name))

    for ob, x, y in zip(player.atc_labels, [1, 1, 7, 7], [fightmap.height-2, fightmap.height-1, fightmap.height-2, fightmap.height-1]):
        ob.add(fightmap, x, y)

    fightmap.show()

    players = [player, enemy]
    while player.hp > 0 and enemy.hp > 0:
        for ob in players:
            enem = [i for i in players if i != ob][0]
            if ob.player:
                outp.rechar(outp.text+("\n" if outp.text != "" else "")+ "What do you want to do?")
                fightmap.show()
                while True:
                    if ev in ["'"+str(i)+"'" for i in range(len(ob.attacs))]:
                        exec("global attack; attack = ob.attacs[int("+ev+")]")
                        ev=""
                        break
                    elif ev == "exit":
                        raise KeyboardInterrupt
            else:
                attack = random.choice(ob.attacs)
            time.sleep(0.3)
            ob.attack(attack, enem)
            ob.text_name.rechar(str(ob.name))
            ob.text_lvl.rechar("Lvl:"+str(ob.lvl))
            ob.text_ap.rechar("AP:"+str(ob.ap if ob.ap > 0 else 0))
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

def main():
    fight()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exiter()
