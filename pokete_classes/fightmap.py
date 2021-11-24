"""This file contains all relevant classes for fight"""

import time
import random
import scrap_engine as se
from .ui_elements import StdFrame2, ChooseBox
from .classes import OutP
from pokete_general_use_fns import std_loop


class FightMap(se.Map):
    """Wrapper for se.Map"""

    def __init__(self, height, width):
        super().__init__(height, width, " ")
        self.box = ChooseBox(6, 25, "Attacks", index_x=1)
        self.invbox = ChooseBox(height - 3, 35, "Inventory")
        # visual obs
        self.deadico1 = se.Text(r"""
    \ /
     o
    / \ """)
        self.deadico2 = se.Text("""

     o""")
        self.pball = se.Text(r"""   _____
  /_____\
  |__O__|
  \_____/""")
        # visual objects
        self.frame_big = StdFrame2(self.height - 5, self.width,
                                       state="float")
        self.frame_small = se.Frame(height=4, width=self.width,
                                                  state="float")
        self.e_underline = se.Text("----------------+", state="float")
        self.e_sideline = se.Square("|", 1, 3, state="float")
        self.p_upperline = se.Text("+----------------", state="float")
        self.p_sideline = se.Square("|", 1, 4, state="float")
        self.outp = OutP("", state="float")
        self.label = se.Text("1: Attack  2: Run!  3: Inv.  4: Deck")
        # adding
        self.outp.add(self, 1, self.height - 4)
        self.e_underline.add(self, 1, 4)
        self.e_sideline.add(self, len(self.e_underline.text), 1)
        self.p_upperline.add(self,
                                 self.width - 1 - len(self.p_upperline.text),
                                 self.height - 10)
        self.frame_big.add(self, 0, 0)
        self.p_sideline.add(self,
                                self.width - 1 - len(self.p_upperline.text),
                                self.height - 9)
        self.frame_small.add(self, 0, self.height - 5)
        self.label.add(self, 0, self.height - 1)

    def clean_up(self, player, enemy):
        """Removes all labels from self"""
        for obj in [enemy.text_name, enemy.text_lvl, enemy.text_hp, enemy.ico,
                    enemy.hp_bar, enemy.tril, enemy.trir, player.text_name,
                    player.text_lvl, player.text_hp, player.ico, player.hp_bar,
                    player.tril, player.trir, enemy.pball_small]:
            obj.remove()
        self.box.remove_c_obs()
        for i in [player, enemy]:
            for j in i.effects:
                j.cleanup()

    def add_3(self, player, enemy):
        """Adds player labels"""
        if player.identifier != "__fallback__":
            player.text_name.add(self, self.width - 17, self.height - 9)
            player.text_lvl.add(self, self.width - 17, self.height - 8)
            player.tril.add(self, self.width - 11, self.height - 7)
            player.trir.add(self, self.width - 2, self.height - 7)
            player.hp_bar.add(self, self.width - 10, self.height - 7)
            player.text_hp.add(self, self.width - 17, self.height - 7)
            player.ico.add(self, 3, self.height - 10)
        return [player, enemy]

    def add_1(self, player, enemy, caught_poketes):
        """Adds enemy and general labels to self"""
        for obj, x, y in zip([enemy.tril, enemy.trir,
                              enemy.text_name, enemy.text_lvl,
                              enemy.text_hp, enemy.ico, enemy.hp_bar],
                             [7, 16, 1, 1, 1, self.width - 14, 8],
                             [3, 3, 1, 2, 3, 2, 3]):
            obj.add(self, x, y)
        if enemy.identifier in caught_poketes:
            enemy.pball_small.add(self, len(self.e_underline.text) - 1, 1)
        if player.identifier != "__fallback__":
            self.box.add_c_obs(player.atc_labels)
            self.box.set_index(0)
        return [player, enemy]

    def add_2(self, player):
        """Adds player labels with sleeps"""
        if player.identifier != "__fallback__":
            player.text_name.add(self, self.width - 17, self.height - 9)
            time.sleep(0.05)
            self.show()
            player.text_lvl.add(self, self.width - 17, self.height - 8)
            time.sleep(0.05)
            self.show()
            player.tril.add(self, self.width - 11, self.height - 7)
            player.trir.add(self, self.width - 2, self.height - 7)
            player.hp_bar.add(self, self.width - 10, self.height - 7)
            player.text_hp.add(self, self.width - 17, self.height - 7)
            time.sleep(0.05)
            self.show()
            player.ico.add(self, 3, self.height - 10)

    def fast_change(self, arr, setob):
        """Changes fast between a list of texts"""
        for _i in range(1, len(arr)):
            arr[_i - 1].remove()
            arr[_i].add(self, setob.x, setob.y)
            self.show()
            time.sleep(0.1)

    def get_attack(self, _ev, attack_obs):
        """Inputloop for attack options"""
        with self.box.add(self, 1, self.height - 7):
            while True:
                if _ev.get() in ["'s'", "'w'"]:
                    self.box.input(_ev.get())
                    self.show()
                    _ev.clear()
                elif _ev.get() in [f"'{i + 1}'" for i in
                                   range(len(attack_obs))] + ["Key.enter"]:
                    attack = attack_obs[self.box.index.index
                                        if _ev.get() == "Key.enter"
                                        else int(_ev.get().strip("'")) - 1]
                    _ev.clear()
                    if attack.ap == 0:
                        continue
                    break
                elif _ev.get() in ["Key.esc", "'q'"]:
                    _ev.clear()
                    attack = ""
                    break
                std_loop(_ev)
                time.sleep(0.05)
        return attack

    def get_item(self, _ev, items, inv):
        """Inputloop for inv"""
        self.invbox.add_c_obs([se.Text(f"{i.pretty_name}s : {inv[i.name]}")
                               for i in items])
        self.invbox.set_index(0)
        with self.invbox.add(self, self.width - 35, 0):
            while True:
                if _ev.get() in ["'s'", "'w'"]:
                    self.invbox.input(_ev.get())
                    self.show()
                    _ev.clear()
                elif _ev.get() in ["Key.esc", "'q'"]:
                    item = ""
                    break
                elif _ev.get() == "Key.enter":
                    item = items[self.invbox.index.index]
                    break
                std_loop(_ev)
                time.sleep(0.05)
        self.invbox.remove_c_obs()
        return item


class FightItems:
    """Contains all fns callable by an item in fight"""

    def __init__(self, _map, movemap, figure, ob_maps):
        self.map = _map
        self.mvmap = movemap
        self.fig = figure
        self.ob_maps = ob_maps

    def throw(self, obj, enem, info, chance, name):
        """Throws a Poketeball"""
        if obj.identifier == "__fallback__" or info["type"] == "duel":
            return 1
        self.map.outp.rechar(f"You threw a {name.capitalize()}!")
        self.map.fast_change([enem.ico, self.map.deadico1, self.map.deadico2,
            self.map.pball], enem.ico)
        time.sleep(random.choice([1, 2, 3, 4]))
        self.fig.remove_item(name)
        catch_chance = 20 if self.fig.map == self.ob_maps["playmap_1"] else 0
        for effect in enem.effects:
            catch_chance += effect.catch_chance
        if random.choices([True, False],
                          weights=[(enem.full_hp / enem.hp) * chance + catch_chance,
                                   enem.full_hp], k=1)[0]:
            self.fig.add_poke(enem)
            self.map.outp.outp(f"You catched {enem.name}")
            time.sleep(2)
            self.map.pball.remove()
            self.map.clean_up(obj, enem)
            self.mvmap.balls_label_rechar(self.fig.pokes)
            return 2
        else:
            self.map.outp.outp("You missed!")
            self.map.show()
            self.map.pball.remove()
            enem.ico.add(self.map, enem.ico.x, enem.ico.y)
            self.map.show()
            return None

    def potion(self, obj, enem, info, hp, name):
        """Potion function"""
        self.fig.remove_item(name)
        obj.oldhp = obj.hp
        if obj.hp + hp > obj.full_hp:
            obj.hp = obj.full_hp
        else:
            obj.hp += hp
        obj.hp_bar.update(obj.oldhp)

    def heal_potion(self, obj, enem, info):
        """Healing potion function"""
        return self.potion(obj, enem, info, 5, "healing_potion")

    def super_potion(self, obj, enem, info):
        """Super potion function"""
        return self.potion(obj, enem, info, 15, "super_potion")

    def poketeball(self, obj, enem, info):
        """Poketeball function"""
        return self.throw(obj, enem, info, 1, "poketeball")

    def superball(self, obj, enem, info):
        """Superball function"""
        return self.throw(obj, enem, info, 6, "superball")

    def hyperball(self, obj, enem, info):
        """Hyperball function"""
        return self.throw(obj, enem, info, 1000, "hyperball")

    def ap_potion(self, obj, enem, info):
        """AP potion function"""
        self.fig.remove_item("ap_potion")
        for atc in obj.attac_obs:
            atc.ap = atc.max_ap
        obj.label_rechar()
