#!/usr/bin/env python3
"""This software is licensed under the GPL3
You should have gotten an copy of the GPL3 license anlonside this software
Feel free to contribute what ever you want to this game
New Pokete contributions are especially welcome
For this see the comments in the definations area
You can contribute here: https://github.com/lxgr-linux/pokete
Thanks to MaFeLP for your code review and your great feedback"""

import random
import time
import os
import sys
import threading
import math
import socket
import json
import logging
from pathlib import Path
import scrap_engine as se
import pokete_data as p_data
from pokete_classes import animations
from pokete_classes.poke import Poke
from pokete_classes.color import Color
from pokete_classes.ui_elements import StdFrame2, Box, ChooseBox, InfoBox, BetterChooseBox
from pokete_classes.classes import PlayMap
from pokete_classes.settings import settings, VisSetting
from pokete_classes.inv_items import invitems, LearnDisc
from pokete_classes.types import types
from pokete_classes.buy import Buy
from pokete_classes.side_loops import ResizeScreen, LoadingScreen, About, Help
from pokete_classes.input import text_input, ask_bool, ask_text, ask_ok
from pokete_classes.mods import ModError, ModInfo, DummyMods
from pokete_classes.movemap import Movemap
from pokete_classes.fightmap import FightMap, FightItems
from pokete_classes.detail import Informer, Detail
from pokete_classes.learnattack import LearnAttack
from pokete_classes.roadmap import RoadMap
from pokete_classes.npcs import NPC, Trainer
from pokete_classes.notify import notifier
from pokete_classes.achievements import achievements, AchievementOverview
from pokete_classes.event import _ev
from pokete_classes.dex import Dex
from pokete_classes.loops import std_loop
from pokete_general_use_fns import liner, sort_vers, parse_args
from release import VERSION, CODENAME, SAVEPATH


__t = time.time()


# Class definition
##################

class HightGrass(se.Object):
    """Object on the map, that triggers a fight"""

    def action(self, ob):
        """Action triggers the fight
        ARGS:
            ob: The object triggering this action"""
        if random.randint(0, 8) == 0:
            fight(Poke("__fallback__", 0)
                  if len([poke for poke in figure.pokes[:6]
                          if poke.hp > 0]) == 0
                  else [poke for poke in figure.pokes[:6] if poke.hp > 0][0],
                  Poke(random.choices(self.arg_proto["pokes"],
                                      weights=[p_data.pokes[i]["rarity"]
                                               for i in
                                               self.arg_proto["pokes"]])[0],
                       random.choices(list(range(self.arg_proto["minlvl"],
                                                 self.arg_proto["maxlvl"])))[0],
                       player=False, shiny=(random.randint(0, 500) == 0)))
            check_walk_back()


class Meadow(se.Text):
    """Daughter of se.Text to better organize Highgrass
    ARGS:
        string: The character representing the meadow
        poke_args: Dict containing relevant information about Pokes"""
    esccode = Color.green

    def __init__(self, string, poke_args):
        super().__init__(string, ignore=self.esccode + " " + Color.reset,
                         ob_class=HightGrass, ob_args=poke_args,
                         state="float", esccode=self.esccode)


class Water(Meadow):
    """Same as Meadow, but for Water"""
    esccode = Color.blue


class Poketeball(se.Object):
    """Poketeball that can be picked up on the map
    ARGS:
        name: Generic name of the ball"""

    def __init__(self, name):
        self.name = name
        super().__init__(Color.thicc + Color.red + "o" + Color.reset,
                         state="float")

    def action(self, ob):
        """Action triggers the pick up
        ARGS:
            ob: The object triggering this action"""
        amount = random.choices([1, 2, 3],
                                weights=[10, 2, 1], k=1)[0]
        item = random.choices(["poketeball", "hyperball", "superball",
                               "healing_potion"],
                              weights=[10, 1.5, 1, 1],
                              k=1)[0]
        figure.give_item(item, amount)
        self.remove()
        movemap.full_show()
        ask_ok(movemap, f"You found {amount if amount > 1 else 'a'} \
{p_data.items[item]['pretty_name']}{'s' if amount > 1 else ''}!")
        figure.used_npcs.append(self.name)


class NPCActions:
    """This class contains all functions callable by NPCs
    All this methods follow the same pattern:
        ARGS:
            npc: The NPC the method belongs to"""

    @staticmethod
    def swap_poke(npc):
        """Swap_poke wrapper"""
        swap_poke()

    @staticmethod
    def heal(npc):
        """Heal wrapper"""
        heal()

    @staticmethod
    def playmap_17_boy(npc):
        """Interaction with boy"""
        if "choka" in [i.identifier for i in figure.pokes[:6]]:
            npc.text([" < Oh, cool!", " < You have a Choka!",
                      " < I've never seen one before!",
                      " < Here you go, 200$"])
            if ask_bool(movemap,
                        "Young boy gifted you 200$. Do you want to accept it?"):
                figure.add_money(200)
            npc.will = False
            figure.used_npcs.append(npc.name)
        else:
            npc.text([" < In this region lives the würgos Pokete.",
                      f" < At level {p_data.pokes['würgos']['evolve_lvl']} \
it evolves to Choka.",
                      " < I have never seen one before!"])

    @staticmethod
    def playmap_20_trader(npc):
        """Interaction with trader"""
        if ask_bool(movemap, "Do you want to trade a Pokete?"):
            if (index := deck(6, "Your deck", True)) is None:
                return
            figure.add_poke(Poke("ostri", 500), index)
            figure.used_npcs.append(npc.name)
            ask_ok(movemap,
                   f"You received: {figure.pokes[index].name.capitalize()} \
at level {figure.pokes[index].lvl()}.")
            movemap.text(npc.x, npc.y, [" < Cool, huh?"])

    @staticmethod
    def playmap_23_npc_8(npc):
        """Interaction with npc_8"""
        if ask_bool(movemap,
                    "The man gifted you 100$. Do you want to accept it?"):
            npc.will = False
            figure.used_npcs.append(npc.name)
            figure.add_money(100)

    @staticmethod
    def playmap_10_old_man(npc):
        """Interaction with ld_man"""
        npc.give("Old man", "hyperball")

    @staticmethod
    def playmap_29_ld_man(npc):
        """Interaction with ld_man"""
        npc.give("The man", "ld_flying")

    @staticmethod
    def playmap_32_npc_12(npc):
        """Interaction with npc_12"""
        npc.give("Old man", "hyperball")

    @staticmethod
    def playmap_36_npc_14(npc):
        """Interaction with npc_14"""
        npc.give("Old woman", "ap_potion")

    @staticmethod
    def playmap_37_npc_15(npc):
        """Interaction with npc_14"""
        npc.give("Bert the bird", "super_potion")

    @staticmethod
    def chat(npc):
        """Starts a chat"""
        npc.chat()


class CenterInteract(se.Object):
    """Triggers a conversation in the Pokete center"""

    def action(self, ob):
        """Triggers the interaction in the Pokete center
        ARGS:
            ob: The object triggering this action"""
        _ev.clear()
        movemap.full_show()
        movemap.text(int(movemap.width / 2), 3,
                     [" < Welcome to the Pokete-Center",
                      " < What do you want to do?",
                      " < a: See your full deck\n b: Heal all your Poketes\
\n c: Go"])
        while True:
            if _ev.get() == "'a'":
                _ev.clear()
                while "__fallback__" in [p.identifier for p in figure.pokes]:
                    figure.pokes.pop([p.identifier for p in
                                      figure.pokes].index("__fallback__"))
                movemap.balls_label_rechar(figure.pokes)
                deck(len(figure.pokes))
                break
            elif _ev.get() == "'b'":
                _ev.clear()
                heal()
                time.sleep(0.5)
                movemap.text(int(movemap.width / 2), 3, [" < ...",
                                                         " < Your Poketes are \
now healed!"])
                break
            elif _ev.get() == "'c'":
                _ev.clear()
                break
            std_loop()
            time.sleep(0.05)
        movemap.full_show(init=True)


class ShopInteract(se.Object):
    """Triggers an conversation in the shop"""

    def action(self, ob):
        """Triggers an interaction in the shop
        ARGS:
            ob: The object triggering this action"""
        _ev.clear()
        movemap.full_show()
        movemap.text(int(movemap.width / 2), 3,
                     [" < Welcome to the Pokete-Shop",
                      " < Wanna buy something?"])
        buy()
        movemap.full_show(init=True)
        movemap.text(int(movemap.width / 2), 3, [" < Have a great day!"])


class CenterMap(PlayMap):
    """Contains all relevant objects for centermap
    ARGS:
        _he: The maps height
        _wi: The maps width"""

    def __init__(self, _he, _wi):
        super().__init__(_he, _wi, name="centermap",
                         pretty_name="Pokete-Center")
        self.inner = se.Text(""" ________________
 |______________|
 |     |a |     |
 |     ¯ ¯¯     |
 |              |
 |______  ______|
 |_____|  |_____|""", ignore=" ")

        self.interact = CenterInteract("¯", state="float")
        self.dor_back1 = CenterDor(" ", state="float")
        self.dor_back2 = CenterDor(" ", state="float")
        self.trader = NPC("trader",
                          [" < I'm a trader.",
                           " < Here you can trade one of your Poketes for \
another players' one."],
                          "swap_poke")
        # adding
        self.dor_back1.add(self, int(self.width / 2), 8)
        self.dor_back2.add(self, int(self.width / 2) + 1, 8)
        self.inner.add(self, int(self.width / 2) - 8, 1)
        self.interact.add(self, int(self.width / 2), 4)
        self.trader.add(self, int(self.width / 2) - 6, 3)


class ShopMap(PlayMap):
    """Contains all relevant objects for shopmap
    ARGS:
        _he: The maps height
        _wi: The maps width """

    def __init__(self, _he, _wi):
        super().__init__(_he, _wi, name="shopmap",
                         pretty_name="Pokete-Shop")
        self.inner = se.Text(""" __________________
 |________________|
 |      |a |      |
 |      ¯ ¯¯      |
 |                |
 |_______  _______|
 |______|  |______|""", ignore=" ")
        self.interact = ShopInteract("¯", state="float")
        self.dor_back1 = CenterDor(" ", state="float")
        self.dor_back2 = CenterDor(" ", state="float")
        # adding
        self.dor_back1.add(self, int(self.width / 2), 8)
        self.dor_back2.add(self, int(self.width / 2) + 1, 8)
        self.inner.add(self, int(self.width / 2) - 9, 1)
        self.interact.add(self, int(self.width / 2), 4)


class CenterDor(se.Object):
    """Dor class for the map to enter centers and shops"""

    def action(self, ob):
        """Trigger
        ARGS:
            ob: The object triggering this action"""
        ob.remove()
        i = ob.map.name
        ob.add(ob.oldmap,
               ob.oldmap.dor.x
               if ob.map == centermap
               else ob.oldmap.shopdor.x,
               ob.oldmap.dor.y + 1
               if ob.map == centermap
               else ob.oldmap.shopdor.y + 1)
        ob.oldmap = ob_maps[i]
        game(ob.map)


class Dor(se.Object):
    """Dor class for the map to enter other maps"""

    def action(self, ob):
        """Trigger
        ARGS:
            ob: The object triggering this action"""
        ob.remove()
        i = ob.map.name
        ob.add(ob_maps[self.arg_proto["map"]], self.arg_proto["x"],
               self.arg_proto["y"])
        ob.oldmap = ob_maps[i]
        game(ob_maps[self.arg_proto["map"]])


class DorToCenter(Dor):
    """Dor that leads to the Pokete center"""

    def __init__(self):
        super().__init__("#", state="float",
                         arg_proto={"map": "centermap",
                                    "x": int(centermap.width / 2), "y": 7})

    def action(self, ob):
        """Triggers the dor
        ARGS:
            ob: The object triggering this action"""
        ob.last_center_map = ob.map
        super().action(ob)


class DorToShop(Dor):
    """Dor that leads to the shop"""

    def __init__(self):
        super().__init__("#", state="float",
                         arg_proto={"map": "shopmap",
                                    "x": int(shopmap.width / 2), "y": 7})


class ChanceDor(Dor):
    """Same as dor but with a chance"""

    def action(self, ob):
        """Trigger
        ARGS:
            ob: The object triggering this action"""
        if random.randint(0, self.arg_proto["chance"]) == 0:
            super().action(ob)


class Figure(se.Object):
    """The figure that moves around on the map and represents the player
    ARGS:
        _si: session_info dict"""

    def __init__(self, _si):
        super().__init__("a", state="solid")
        self.__money = _si.get("money", 10)
        self.inv = _si.get("inv", {"poketeballs": 10})
        self.name = _si.get("user", "DEFAULT")
        self.pokes = [Poke((_p := _si["pokes"][poke])["name"], _p["xp"],
                           _p["hp"], _p["ap"], _p.get("attacks", None),
                           _p.get("effects", []),
                           shiny=_p.get("shiny", False))
                      for poke in _si["pokes"]]
        self.caught_pokes = _si.get("caught_poketes", [])
        self.visited_maps = _si.get("visited_maps", ["playmap_1"])
        self.used_npcs = _si.get("used_npcs", [])
        self.last_center_map = ob_maps[_si.get("last_center_map", "playmap_1")]
        self.oldmap = ob_maps[_si.get("oldmap", "playmap_1")]
        self.direction = "t"

    def set_args(self, _si):
        """Processes data from save file
        ARGS:
            _si: session_info dict"""
        try:
            # Looking if figure would be in centermap,
            # so the player may spawn out of the center
            if _si["map"] in ["centermap", "shopmap"]:
                _map = ob_maps[_si["map"]]
                self.add(_map, _map.dor_back1.x, _map.dor_back1.y - 1)
            else:
                if self.add(ob_maps[_si["map"]], _si["x"], _si["y"]) == 1:
                    raise se.CoordinateError(self, ob_maps[_si["map"]],
                                             _si["x"], _si["y"])
        except se.CoordinateError:
            self.add(ob_maps["playmap_1"], 6, 5)
        movemap.name_label.rechar(self.name, esccode=Color.thicc)
        movemap.code_label.rechar(self.map.pretty_name)
        movemap.balls_label_rechar(self.pokes)
        movemap.add_obs()

    def add_money(self, money):
        """Adds money
        ARGS:
            money: Amount of money beeing added"""
        self.set_money(self.__money + money)

    def get_money(self):
        """Getter for __money
        RETURNS:
            The current money"""
        return self.__money

    def set_money(self, money):
        """Sets the money to a certain value
        ARGS:
            money: New value"""
        assert money >= 0, "money has to be positive"
        logging.info("[Figure] Money set to %d$ from %d$",
                     money, self.__money)
        self.__money = money
        for cls in [inv, buy]:
            cls.money_label.rechar(str(self.__money) + "$")
            cls.box.set_ob(cls.money_label,
                           cls.box.width - 2 - len(cls.money_label.text), 0)

    def add_poke(self, poke, idx=None):
        """Adds a Pokete to the players Poketes
        ARGS:
            poke: Poke object beeing added
            idx: Index of the Poke"""
        poke.set_player(True)
        figure.caught_pokes.append(poke.identifier)
        if idx is None:
            self.pokes.append(poke)
        else:
            self.pokes[idx] = poke
        logging.info("[Figure] Added Poke %s", poke.name)

    def give_item(self, item, amount=1):
        """Gives an item to the player"""
        assert amount > 0, "Amounts have to be positive"
        if item not in self.inv:
            self.inv[item] = amount
        else:
            self.inv[item] += amount
        logging.info("[Figure] %d %s(s) given", amount, item)

    def has_item(self, item):
        """Checks if an item is already present
        ARGS:
            item: Generic item name
        RETURNS:
            If the player has this item"""
        return item in self.inv and self.inv[item] > 0

    def remove_item(self, item, amount=1):
        """Removes a certain amount of an item from the inv
        ARGS:
            item: Generic item name
            amount: Amount of items beeing removed"""
        assert amount > 0, "Amounts have to be positive"
        assert item in self.inv, f"Item {item} is not in the inventory"
        assert self.inv[item] - amount >= 0, f"There are not enought {item}s \
in the inventory"
        self.inv[item] -= amount
        logging.info("[Figure] %d %s(s) removed", amount, item)


class Debug:
    """Debug class"""

    @classmethod
    def pos(cls):
        """Prints the figures' position"""
        print(figure.x, figure.y, figure.map.name)


class Deck(Informer):
    """Deck to see Poketes in"""

    def __init__(self):
        self.map = se.Map(height - 1, width, " ")
        self.submap = se.Submap(self.map, 0, 0, height=height - 1, width=width)
        self.exit_label = se.Text("1: Exit  ")
        self.move_label = se.Text("2: Move    ")
        self.move_free = se.Text("3: Free")
        self.index = se.Object("*")
        # adding
        self.exit_label.add(self.submap, 0, self.submap.height - 1)
        self.move_label.add(self.submap, 9, self.submap.height - 1)
        self.move_free.add(self.submap, 20, self.submap.height - 1)

    def rem_pokes(self, pokes):
        """Removes all Poketes from the Deck
        ARGS:
            pokes: List of Pokes beeing removed"""
        for poke in pokes:
            self.remove(poke)

    def __call__(self, p_len, label="Your full deck", in_fight=False):
        """Opens the deck
        ARGS:
            p_len: Number of Pokes beeing included
            label: The displayed label
            in_fight: Whether or not this is called in a fight"""
        _ev.clear()
        pokes = figure.pokes[:p_len]
        ret_action = None
        self.map.resize(5 * int((len(pokes) + 1) / 2) + 2, width,
                        self.map.background)
        # decksubmap.resize(height-1, width)
        se.Text(label, esccode=Color.thicc).add(self.map, 2, 0)
        se.Square("|", 1, self.map.height - 2).add(self.map,
                                                   round(self.map.width / 2),
                                                   1)
        StdFrame2(self.map.height - 1, self.map.width).add(self.map, 0, 0)
        self.move_label.rechar("2: Move    ")
        indici = []
        self.add_all(pokes, True)
        self.index.index = 0
        if len(pokes) > 0:
            self.index.add(self.map,
                           pokes[self.index.index].text_name.x
                            + len(pokes[self.index.index].text_name.text)
                            + 1,
                           pokes[self.index.index].text_name.y)
        self.submap.full_show(init=True)
        while True:
            if _ev.get() in ["'1'", "Key.esc", "'q'"]:
                _ev.clear()
                self.rem_pokes(pokes)
                while len(self.map.obs) > 0:
                    self.map.obs[0].remove()
                self.submap.set(0, 0)
                if ret_action is not None:
                    abb_funcs[ret_action](pokes[self.index.index])
                return None
            elif _ev.get() == "'2'":
                _ev.clear()
                if len(pokes) == 0:
                    continue
                if not indici:
                    indici.append(self.index.index)
                    self.move_label.rechar("2: Move to ")
                else:
                    indici.append(self.index.index)
                    figure.pokes[indici[0]], figure.pokes[indici[1]] = \
                        pokes[indici[1]], pokes[indici[0]]
                    pokes = figure.pokes[:p_len]
                    indici = []
                    self.rem_pokes(pokes)
                    self.index.set(0, self.map.height - 1)
                    self.add_all(pokes)
                    self.index.set(
                        pokes[self.index.index].text_name.x
                         + len(pokes[self.index.index].text_name.text) + 1,
                        pokes[self.index.index].text_name.y)
                    self.move_label.rechar("2: Move    ")
                    self.submap.full_show()
            elif _ev.get() == "'3'":
                _ev.clear()
                if ask_bool(self.submap, f"Do you really want to free \
{figure.pokes[self.index.index].name}?"):
                    self.rem_pokes(pokes)
                    figure.pokes[self.index.index] = Poke("__fallback__", 10, 0)
                    pokes = figure.pokes[:len(pokes)]
                    self.add_all(pokes)
                    self.index.set(
                        pokes[self.index.index].text_name.x
                         + len(pokes[self.index.index].text_name.text)
                         + 1,
                        pokes[self.index.index].text_name.y)
                    movemap.balls_label_rechar(figure.pokes)
            elif _ev.get() in ["'w'", "'a'", "'s'", "'d'"]:
                self.control(pokes, _ev.get())
                _ev.clear()
            elif _ev.get() == "Key.enter":
                _ev.clear()
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
                        _ev.set("'q'")
                        continue
                    self.submap.full_show(init=True)
            std_loop(False)
            if len(pokes) > 0 and\
                    self.index.y - self.submap.y + 6 > self.submap.height:
                self.submap.set(self.submap.x, self.submap.y + 1)
            elif len(pokes) > 0 and self.index.y - 1 < self.submap.y:
                self.submap.set(self.submap.x, self.submap.y - 1)
            time.sleep(0.05)
            self.submap.full_show()

    def add_all(self, pokes, init=False):
        """Adds all Poketes to the deck
        ARGS:
            pokes: List of all Pokes beeing added
            init: Whether or not this happens for the first time"""
        j = 0
        for i, poke in enumerate(pokes):
            self.add(poke, figure, self.map,
                     1 if i % 2 == 0
                     else round(self.map.width / 2) + 1, j * 5 + 1)
            if i % 2 == 0 and init:
                se.Square("-", self.map.width - 2, 1).add(self.map, 1,
                                                          j * 5 + 5)
            if i % 2 == 1:
                j += 1

    def control(self, pokes, inp):
        """Processes inputs
        ARGS:
            pokes: List of all Pokes in deck
            inp: Inputted string"""
        if len(pokes) <= 1:
            return
        for con, stat, fir, sec in zip(["'a'", "'d'", "'s'", "'w'"],
                                       [self.index.index != 0,
                                        self.index.index != len(pokes) - 1,
                                        self.index.index + 2 < len(pokes),
                                        self.index.index - 2 >= 0],
                                       [-1, 1, 2, -2],
                                       [len(pokes) - 1, 0,
                                        self.index.index % 2,
                                        [i for i in range(len(pokes))
                                            if i % 2 ==
                                            self.index.index % 2][-1]]):
            if inp == con:
                if stat:
                    self.index.index += fir
                else:
                    self.index.index = sec
                break
        self.index.set(pokes[self.index.index].text_name.x
                        + len(pokes[self.index.index].text_name.text) + 1,
                       pokes[self.index.index].text_name.y)


class Inv:
    """Inventory to see and manage items in
    ARGS:
        _map: se.Map this will be shown on"""

    def __init__(self, _map):
        self.map = _map
        self.box = ChooseBox(_map.height - 3, 35, "Inventory", "R:remove")
        self.box2 = Box(7, 21)
        self.money_label = se.Text(f"{figure.get_money()}$")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def __call__(self):
        """Opens the inventory"""
        _ev.clear()
        items = self.add()
        with self.box.add(self.map, self.map.width - 35, 0):
            while True:
                if _ev.get() in ["'s'", "'w'"]:
                    self.box.input(_ev.get())
                    _ev.clear()
                elif _ev.get() in ["'4'", "Key.esc", "'q'"]:
                    break
                elif _ev.get() == "Key.enter":
                    obj = items[self.box.index.index]
                    self.box2.name_label.rechar(obj.pretty_name)
                    self.desc_label.rechar(liner(obj.desc, 19))
                    self.box2.add(self.map, self.box.x - 19, 3)
                    _ev.clear()
                    while True:
                        if _ev.get() == "exit":
                            raise KeyboardInterrupt
                        elif _ev.get() in ["Key.enter", "Key.esc", "'q'"]:
                            _ev.clear()
                            self.box2.remove()
                            if type(obj) is LearnDisc:
                                if ask_bool(self.map, f"Do you want to teach '\
{obj.attack_dict['name']}'?"):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck(6, label="Your deck",
                                                     in_fight=True)
                                        if index is None:
                                            ex_cond = False
                                            self.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        if getattr(types,
                                                   obj.attack_dict['types'][0])\
                                                in poke.types:
                                            break
                                        else:
                                            ex_cond = ask_bool(self.map,
                                                               f"You cant't \
teach '{obj.attack_dict['name']}' to '{poke.name}'! \nDo you want to continue?")
                                    if not ex_cond:
                                        break
                                    if LearnAttack(poke, self.map)\
                                            (obj.attack_name):
                                        items = self.rem_item(obj.name, items)
                                        if len(items) == 0:
                                            break
                                    _ev.clear()
                            break
                        time.sleep(0.05)
                        self.map.show()
                elif _ev.get() == "'r'":
                    if ask_bool(self.map,
                                f"Do you really want to throw \
{items[self.box.index.index].pretty_name} away?"):
                        items = self.rem_item(items[self.box.index.index].name,
                                              items)
                        if len(items) == 0:
                            break
                    _ev.clear()
                std_loop()
                time.sleep(0.05)
                self.map.show()
        self.box.remove_c_obs()

    def rem_item(self, name, items):
        """Removes an item from the inv
        ARGS:
            name: Items name
            items: List of Items
        RETURNS:
            List of Items"""
        figure.remove_item(name)
        for obj in self.box.c_obs:
            obj.remove()
        self.box.remove_c_obs()
        items = self.add()
        if not items:
            return items
        if self.box.index.index >= len(items):
            self.box.set_index(len(items) - 1)
        return items

    def add(self):
        """Adds all items to the box
        RETURNS:
            List of Items"""
        items = [getattr(invitems, i) for i in figure.inv if figure.inv[i] > 0]
        self.box.add_c_obs([se.Text(f"{i.pretty_name}s : {figure.inv[i.name]}")
                            for i in items])
        return items


class Menu:
    """Menu to manage settings and other stuff in
    ARGS:
        _map: se.Map this will be shown on"""

    def __init__(self, _map):
        self.map = _map
        self.box = ChooseBox(_map.height - 3, 35, "Menu")
        self.playername_label = se.Text("Playername: ", state="float")
        self.mods_label = se.Text("Mods", state="float")
        self.ach_label = se.Text("Achievements", state="float")
        self.about_label = se.Text("About", state="float")
        self.save_label = se.Text("Save", state="float")
        self.exit_label = se.Text("Exit", state="float")
        self.realname_label = se.Text(session_info["user"], state="float")
        self.box.add_c_obs([self.playername_label,
                            VisSetting("Autosave", "autosave",
                                       {True: "On", False: "Off"}),
                            VisSetting("Animations", "animations",
                                       {True: "On", False: "Off"}),
                            VisSetting("Save trainers", "save_trainers",
                                       {True: "On", False: "Off"}),
                            VisSetting("Load mods", "load_mods",
                                       {True: "On", False: "Off"}),
                            self.mods_label, self.ach_label,
                            self.about_label, self.save_label,
                            self.exit_label])
        # adding
        self.box.add_ob(self.realname_label,
                        self.playername_label.rx
                        + len(self.playername_label.text),
                        self.playername_label.ry)

    def __call__(self):
        """Opens the menu"""
        _ev.clear()
        self.realname_label.rechar(figure.name)
        with self.box.add(self.map, self.map.width - self.box.width, 0):
            while True:
                if _ev.get() == "Key.enter":
                    _ev.clear()
                    # Fuck python for not having case statements
                    if (i := self.box.c_obs[self.box.index.index]) ==\
                            self.playername_label:
                        figure.name = text_input(self.realname_label,
                                                 self.map,
                                                 figure.name, 18, 17)
                        self.map.name_label_rechar(figure.name)
                    elif i == self.mods_label:
                        ModInfo(movemap, mods.mod_info)()
                    elif i == self.save_label:
                        # When will python3.10 come out?
                        with InfoBox("Saving....", info="", _map=self.map):
                            # Shows a box displaying "Saving...." while saving
                            save()
                            time.sleep(1.5)
                    elif i == self.exit_label:
                        save()
                        exiter()
                    elif i == self.about_label:
                        about()
                    elif i == self.ach_label:
                        AchievementOverview()(movemap)
                    else:
                        i.change()
                elif _ev.get() in ["'s'", "'w'"]:
                    self.box.input(_ev.get())
                    _ev.clear()
                elif _ev.get() in ["'e'", "Key.esc", "'q'"]:
                    _ev.clear()
                    break
                std_loop()
                time.sleep(0.05)
                self.map.show()


# General use functions
#######################

def check_walk_back(self=None):
    """Check whether the figure has to be walked back to the last Poketecenter
       or not"""
    if all(i.hp <= 0 for i in figure.pokes[:6]):
        amount = round(figure.get_money() / 3)
        figure.add_money(-amount)
        heal()
        ask_ok(movemap, f"""All your Poketes have died and you ran
back to the last Pokecenter you visited, to heal them!
On the way there {amount}$ fell out of your pocket!""")
        figure.remove()
        figure.map = figure.last_center_map
        logging.info("[Figure] Lost all Poketes and ran away")
        DorToCenter().action(figure)


def heal():
    """Heals all poketes"""
    for poke in figure.pokes:
        poke.hp = poke.full_hp
        poke.effects = []
        poke.miss_chance = poke.full_miss_chance
        poke.text_hp.rechar(f"HP:{poke.hp}")
        poke.set_vars()
        poke.hp_bar.make(poke.hp)
        movemap.balls_label_rechar(figure.pokes)


def autosave():
    """Autosaves the game every 5 mins"""
    while True:
        time.sleep(300)
        if settings("autosave").val:
            save()


def save():
    """Saves all relevant data to savefile"""
    _si = {
        "user": figure.name,
        "ver": VERSION,
        "map": figure.map.name,
        "oldmap": figure.oldmap.name,
        "last_center_map": figure.last_center_map.name,
        "x": figure.x,
        "y": figure.y,
        "achievements": achievements.achieved,
        "pokes": {i: poke.dict() for i, poke in enumerate(figure.pokes)},
        "inv": figure.inv,
        "money": figure.get_money(),
        "settings": settings.to_dict(),
        "caught_poketes": list(dict.fromkeys(figure.caught_pokes
                                             + [i.identifier
                                                for i in figure.pokes])),
        "visited_maps": figure.visited_maps,
        "startup_time": __t,
        # filters doublicates from figure.used_npcs
        "used_npcs": list(dict.fromkeys(figure.used_npcs))
    }
    with open(HOME + SAVEPATH + "/pokete.json", "w+") as file:
        # writes the data to the save file in a nice format
        json.dump(_si, file, indent=4)
    logging.info("[General] Saved")


def read_save():
    """Reads form savefile
    RETURNS:
        session_info dict"""
    Path(HOME + SAVEPATH).mkdir(parents=True, exist_ok=True)
    # Default test session_info
    _si = {
        "user": "DEFAULT",
        "ver": VERSION,
        "map": "intromap",
        "oldmap": "playmap_1",
        "last_center_map": "playmap_1",
        "x": 4,
        "y": 5,
        "achievements": [],
        "pokes": {
            "0": {"name": "steini", "xp": 50, "hp": "SKIP",
                  "ap": ["SKIP", "SKIP"]}
        },
        "inv": {"poketeball": 15, "healing_potion": 1},
        "settings": {
            "load_mods": False},
        "figure.caught_pokes": ["steini"],
        "visited_maps": ["playmap_1"],
        "startup_time": 0,
        "used_npcs": []
    }

    if (not os.path.exists(HOME + SAVEPATH + "/pokete.json")
        and os.path.exists(HOME + SAVEPATH + "/pokete.py")):
        l_dict = {}
        with open(HOME + SAVEPATH + "/pokete.py", "r") as _file:
            exec(_file.read(), {"session_info": _si}, l_dict)
        _si = json.loads(json.dumps(l_dict["session_info"]))
    elif os.path.exists(HOME + SAVEPATH + "/pokete.json"):
        with open(HOME + SAVEPATH + "/pokete.json") as _file:
            _si = json.load(_file)
    return _si


def on_press(key):
    """Sets the _ev variable
    ARGS:
        key: Key object _ev is set from"""
    _ev.set(str(key))


def reset_terminal():
    """Resets the terminals state"""
    if sys.platform == "linux":
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def exiter():
    """Exit function"""
    reset_terminal()
    logging.info("[General] Exiting...")
    sys.exit()


# Functions needed for movemap
##############################

def codes(string):
    """Cheats"""
    for i in string:
        if i == "w":
            save()
        elif i == "!":
            exec(string[string.index("!") + 2:])
            return
        elif i == "e":
            try:
                exec(string[string.index("e") + 2:])
            except Exception as exc:
                print(exc)
            return
        elif i == "q":
            exiter()


# Playmap extra action functions
# Those are adding additional actions to playmaps
#################################################

class ExtraActions:
    """Extra actions class to keep track of extra actions"""

    @staticmethod
    def water(obs):
        """Water animation
        ARGS:
            obs: List of se.Objects that represent the water"""
        if settings("animations").val:
            for obj in obs:
                if random.randint(0, 9) == 0:
                    if " " not in obj.char:
                        obj.rechar([i for i in
                                    [Color.lightblue + "~" + Color.reset,
                                     Color.blue + "~" + Color.reset]
                                    if i != obj.char][0])
                        if obj.x == figure.x and obj.y == figure.y:
                            figure.redraw()

    @staticmethod
    def playmap_4():
        """Water animation"""
        ExtraActions.water(ob_maps["playmap_4"].lake_1.obs)

    @staticmethod
    def playmap_11():
        """Water animation"""
        ExtraActions.water(ob_maps["playmap_11"].lake_1.obs)

    @staticmethod
    def playmap_18():
        """Water animation"""
        ExtraActions.water(ob_maps["playmap_18"].lake_1.obs)

    @staticmethod
    def playmap_21():
        """Water animation"""
        ExtraActions.water(ob_maps["playmap_21"].lake_1.obs)

    @staticmethod
    def playmap_7():
        """Cave animation"""
        for obj in ob_maps["playmap_7"].inner_walls.obs\
                   + [i.main_ob for i in ob_maps["playmap_7"].trainers]\
                   + [getattr(ob_maps["playmap_7"], i)
                    for i in p_data.map_data["playmap_7"]["balls"] if
                        "playmap_7." + i not in figure.used_npcs or not save_trainers]:
            if obj.added and math.sqrt((obj.y - figure.y) ** 2
                                       + (obj.x - figure.x) ** 2) <= 3:
                obj.rechar(obj.bchar)
            else:
                obj.rechar(" ")


# main functions
################

def test():
    """test/demo for BetterChooseBox, until BetterChooseBox is actively used
       this will remain"""
    with BetterChooseBox(3, [se.Text(i, state="float") for i in ["Hallo",
        "Welt", "Wie", "Gehts", "Dir", "So", "Du"]],
        "Test", _map=movemap) as a:
        while True:
            if _ev.get() in ["'w'", "'s'", "'a'", "'d'"]:
                a.input(_ev.get())
                _ev.clear()
            elif _ev.get() in ["'q'", "Key.esc"]:
                _ev.clear()
                break
            elif _ev.get() == "'t'":
                _ev.clear()
                a.remove()
                a.set_items(3, [se.Text(i, state="float") for i in ["test",
                    "test", "123", "fuckthesystem"]])
                a.center_add(a.map)
            std_loop()
            time.sleep(0.05)
            a.map.show()


def teleport(poke):
    """Teleports the player to another towns pokecenter
    ARGS:
        poke: The Poke shown in the animation"""
    if (obj := roadmap(movemap, choose=True)) is None:
        return
    else:
        if settings("animations").val:
            animations.transition(movemap, poke)
        cen_d = p_data.map_data[obj.name]["hard_obs"]["pokecenter"]
        Dor("", state="float", arg_proto={"map": obj.name,
                                          "x": cen_d["x"] + 5,
                                          "y": cen_d["y"] + 6}).action(figure)


def swap_poke():
    """Trading with other players in the local network"""
    if not ask_bool(movemap, "Do you want to trade with another trainer?"):
        return
    port = 65432
    save()
    do = ask_bool(movemap, "Do you want to be the host?")
    if (index := deck(6, "Your deck", True)) is None:
        return
    if do:
        with InfoBox(f"Hostname: {socket.gethostname()}\nWaiting...",
                     _map=movemap):
            host = ''
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((host, port))
                sock.listen()
                conn = sock.accept()[0]
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        decode_data = json.loads(data.decode())
                        conn.sendall(
                                str.encode(
                                    json.dumps(
                                        {"mods": mods.mod_info,
                                         "name": figure.name,
                                         "poke": figure.pokes[index].dict()})))
    else:
        host = ""
        while host == "":
            host = ask_text(movemap, "Please type in the hosts hostname",
                            "Host:", "", "Hostname", 30)
            if host in ["localhost", "127.0.0.1", "0.0.0.0",
                        socket.gethostname()]:
                ask_ok(movemap,
                       "You're not allowed trade with your self!\nYou fool!")
                host = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, port))
            except Exception as err:
                ask_ok(movemap, str(err))
                return
            sock.sendall(
                    str.encode(
                        json.dumps({"mods": mods.mod_info,
                                    "name": figure.name,
                                    "poke": figure.pokes[index].dict()})))
            data = sock.recv(1024)
            decode_data = json.loads(data.decode())
    logging.info("[Swap_poke] Recieved %s", decode_data)
    mod_info = decode_data.get("mods", {})
    if mods.mod_info != mod_info:
        ask_ok(movemap, f"""Conflicting mod versions!
Your mods: {', '.join(i + '-' + mods.mod_info[i] for i in mods.mod_info)}
Your partners mods: {', '.join(i + '-' + mod_info[i] for i in mod_info)}""")
        return
    figure.add_poke(Poke(decode_data["poke"]["name"],
                         decode_data["poke"]["xp"],
                         decode_data["poke"]["hp"]), index)
    figure.pokes[index].set_ap(decode_data["poke"]["ap"])
    save()  # to avoid duping
    ask_ok(movemap,
           f"You received: {figure.pokes[index].name.capitalize()} at level \
{figure.pokes[index].lvl()} from {decode_data['name']}.")


def fight(player, enemy, info=None):
    """Wrapper for fightmap.fight
    ARGS:
        player: The players Poke
        enemy: The enemys Poke
        info: Dict containing info about the fight"""
    if info is None:
        info = {"type": "wild", "player": " "}
    return fightmap.fight(player, enemy, figure, fightitems, deck, info)

def game(_map):
    """Game function
    ARGS:
        _map: The map that will be shown"""
    global width, height
    _ev.clear()
    print("\033]0;Pokete - " + _map.pretty_name + "\a", end="")
    if _map.name not in figure.visited_maps:
        figure.visited_maps.append(_map.name)
    movemap.code_label.rechar(figure.map.pretty_name)
    movemap.set(0, 0)
    movemap.bmap = _map
    movemap.full_show()
    inp_dict = {"'1'": [deck, (6, "Your deck")],
                "'3'": [roadmap, (movemap,)],
                "'4'": [inv, ()],
                "'5'": [pokete_dex, ()],
                "'e'": [menu, ()],
                "'?'": [help_page, ()]}
    if _map.weather is not None:
        notifier.notify("Weather", "Info", _map.weather.info)
    while True:
        # Directions are not beening used yet
        for name, _dir, x, y in zip(["'w'", "'a'", "'s'", "'d'"],
                                    ["t", "l", "b", "r"],
                                    [0, -1, 0, 1], [-1, 0, 1, 0]):
            if _ev.get() == name:
                figure.direction = _dir
                figure.set(figure.x + x, figure.y + y)
                _ev.clear()
                break
        else:
            if _ev.get() in inp_dict:
                inp_dict[_ev.get()][0](*inp_dict[_ev.get()][1])
                _ev.clear()
                movemap.show(init=True)
            elif _ev.get() == "'2'":
                _ev.clear()
                if ask_bool(movemap, "Do you realy want to exit?"):
                    save()
                    exiter()
            elif _ev.get() == "':'":
                _ev.clear()
                inp = text_input(movemap.code_label, movemap, ":",
                                 movemap.width,
                                 (movemap.width - 2) * movemap.height - 1)[1:]
                movemap.code_label.outp(figure.map.pretty_name)
                codes(inp)
                _ev.clear()
        std_loop()
        _map.extra_actions()
        time.sleep(0.05)
        for statement, x, y in zip([figure.x + 6 > movemap.x + movemap.width,
                                    figure.x < movemap.x + 6,
                                    figure.y + 6 > movemap.y + movemap.height,
                                    figure.y < movemap.y + 6],
                                   [1, -1, 0, 0], [0, 0, 1, -1]):
            if statement:
                movemap.set(movemap.x + x, movemap.y + y)
        # checking for resizing
        width, height = os.get_terminal_size()
        if movemap.width != width or movemap.height != height - 1:
            movemap.resize(height - 1, width, " ")
        movemap.full_show()


def intro():
    """Intro to Pokete"""
    movemap.set(0, 0)
    movemap.bmap = ob_maps["intromap"]
    movemap.full_show()
    while figure.name in ["DEFAULT", ""]:
        figure.name = ask_text(movemap,
                               "Welcome to Pokete!\nPlease choose your name!\n",
                               "Name:", "", "Name", 17)
    movemap.name_label_rechar(figure.name)
    movemap.text(4, 3, [" < Hello my child.",
                        " < You're now ten years old.",
                        " < And I think it's now time for you to travel the \
world and be a Pokete-trainer.",
                        " < Therefore I give you this powerfull 'Steini', \
15 'Poketeballs' to catch Poketes and a "
                        "'Healing potion'.",
                        " < You will be the best Pokete-Trainer in Nice town.",
                        " < Now go out and become the best!"])
    game(ob_maps["intromap"])


def parse_obj(_map, name, obj, _dict):
    """Parses an object to a maps attribute and adds it
    ARGS:
        _map: The given PlayMap
        name: Name of the attribute
        obj: Object beeing set
        _dict: Dict containing info"""
    setattr(_map, name, obj)
    obj.add(_map, _dict["x"], _dict["y"])


def gen_obs():
    """Genrates all objests on the maps"""
    map_data = p_data.map_data
    npcs = p_data.npcs
    trainers = p_data.trainers

    # adding all trainer to map
    for i in trainers:
        _map = ob_maps[i]
        for j in trainers[i]:
            args = j["args"]
            trainer = Trainer(Poke(*j["poke"], player=False),
                              *args[:-2], fight)
            trainer.add(_map, args[-2], args[-1])
            _map.trainers.append(trainer)

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
                      Meadow(map_data[ob_map]["soft_obs"][soft_ob]["txt"],
                             _map.poke_args),
                      map_data[ob_map]["soft_obs"][soft_ob])
        for dor in map_data[ob_map]["dors"]:
            parse_obj(_map, dor,
                      Dor(" ", state="float",
                          arg_proto=map_data[ob_map]["dors"][dor]["args"]),
                      map_data[ob_map]["dors"][dor])
        for ball in map_data[ob_map]["balls"]:
            if f'{ob_map}.{ball}' not in figure.used_npcs or not \
            settings("save_trainers").val:
                parse_obj(_map, ball,
                          Poketeball(f"{ob_map}.{ball}"),
                          map_data[ob_map]["balls"][ball])
    # NPCs
    for npc in npcs:
        parse_obj(ob_maps[npcs[npc]["map"]], npc,
                  NPC(npc, npcs[npc]["texts"], fn=npcs[npc]["fn"],
                      chat=npcs[npc].get("chat", None)),
                  npcs[npc])


def gen_maps():
    """Generates all maps
    RETURNS:
        Dict of all PlayMaps"""
    maps = {}
    for ob_map in p_data.maps:
        args = p_data.maps[ob_map]
        args["extra_actions"] = (getattr(ExtraActions, args["extra_actions"],
                                         None)
                                 if args["extra_actions"] is not None
                                 else None)
        maps[ob_map] = PlayMap(name=ob_map, **args)
    return maps


def check_version(sinfo):
    """Checks if version in save file is the same as current version
    ARGS:
        sinfo: session_info dict"""
    if "ver" not in sinfo:
        return
    else:
        ver = sinfo["ver"]
    if VERSION != ver and sort_vers([VERSION, ver])[-1] == ver:
        if not ask_bool(loading_screen.map,
                        liner(f"The save file was created \
on version '{ver}', the current version is '{VERSION}', \
such a downgrade may result in data loss! \
Do you want to continue?", int(width * 2 / 3))):
            exiter()


def main():
    """Main function"""
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


def map_additions():
    """Applies additions to the maps"""

    # playmap_1
    _map = ob_maps["playmap_1"]
    _map.dor = DorToCenter()
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
                         ob_args=_map.poke_args,
                         state="float")
    # adding
    _map.inner.add(_map, 0, 0)

    # playmap_3
    _map = ob_maps["playmap_3"]
    _map.dor = DorToCenter()
    _map.shopdor = DorToShop()
    # adding
    _map.dor.add(_map, 25, 6)
    _map.shopdor.add(_map, 61, 6)

    # playmap_4
    _map = ob_maps["playmap_4"]
    _map.dor_playmap_5 = ChanceDor("~", state="float",
                                   arg_proto={"chance": 6,
                                              "map": "playmap_5",
                                              "x": 17, "y": 16})
    _map.lake_1 = Water(
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~         ~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~                 ~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~                    ~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~                                ~~~~~~~~~~~~~~
~~~~~~~~~                                           ~~~~~~~~
~~~""", _map.w_poke_args)
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
    for ob in (_map.inner_walls.obs + [i.main_ob for i in _map.trainers] +
               [getattr(_map, i) for i in p_data.map_data["playmap_7"]["balls"]
                if "playmap_7." + i not in figure.used_npcs
                   or not settings("save_trainers").val]):
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
    _map.lake_1 = Water(
"""~~~~~                                                 ~~~~~~
~~~~~~~~~~~~                                 ~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~                       ~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~                   ~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~          ~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""",
_map.w_poke_args)
    # adding
    _map.lake_1.add(_map, 0, 12)

    # playmap_13
    _map = ob_maps["playmap_13"]
    _map.dor = DorToCenter()
    _map.shopdor = DorToShop()
    # adding
    _map.dor.add(_map, 14, 29)
    _map.shopdor.add(_map, 52, 29)

    # playmap_18
    _map = ob_maps["playmap_18"]
    _map.lake_1 = Water("""  ~~
 ~~~~
~~~~~~~
~~~~~~~~
~~~~~~~~
~~~~~~~~
~~~~~~
 ~~~~
 ~~""", _map.w_poke_args)
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
                              arg_proto={"map": "playmap_19",
                                         "x": 26, "y": 1})
    _map.dor = DorToCenter()
    _map.shopdor = DorToShop()
    _map.lake_1 = Water("""       ~~~~~~~~~~~
   ~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~
 ~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~
       ~~~~~~~~""", _map.w_poke_args)
    # adding
    _map.dor_playmap_19.add(_map, 5, 26)
    _map.dor.add(_map, 10, 7)
    _map.shopdor.add(_map, 34, 7)
    _map.lake_1.add(_map, 65, 10)

    # playmap_30
    _map = ob_maps["playmap_30"]
    _map.dor = DorToCenter()
    _map.shopdor = DorToShop()
    # adding
    _map.dor.add(_map, 13, 7)
    _map.shopdor.add(_map, 30, 7)


# Actual code execution
#######################
if __name__ == "__main__":
    # deciding on wich input to use
    if sys.platform == "linux":
        import tty
        import termios


        def recogniser():
            """Use another (not on xserver relying) way to read keyboard input,
                to make this shit work in tty or via ssh,
                where no xserver is available"""
            global fd, old_settings

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                _ev.set({ord(char): f"'{char.rstrip()}'", 13: "Key.enter",
                        127: "Key.backspace", 32: "Key.space",
                        27: "Key.esc"}[ord(char)])
                if ord(char) == 3:
                    reset_terminal()
                    _ev.set("exit")
    else:
        from pynput.keyboard import Listener


        def recogniser():
            """Gets keyboard input from pynput"""
            while True:
                with Listener(on_press=on_press) as listener:
                    listener.join()

    do_logging, load_mods = parse_args(sys.argv)

    # resizing screen
    tss = ResizeScreen()
    width, height = tss()

    # Home global
    HOME = str(Path.home())

    # loading screen
    loading_screen = LoadingScreen(VERSION, CODENAME)
    loading_screen()

    # logging config
    log_file = f"{HOME}{SAVEPATH}/pokete.log" if do_logging else None
    logging.basicConfig(filename=log_file,
                        encoding='utf-8',
                        format='[%(asctime)s][%(levelname)s]: %(message)s',
                        level=logging.DEBUG if do_logging else logging.ERROR)
    logging.info("=== Startup Pokete %s v%s ===", CODENAME, VERSION)

    # reading save file
    session_info = read_save()

    settings.from_dict(session_info.get("settings", {}))

    save_trainers = settings("save_trainers").val

    if not load_mods:
        settings("load_mods").val = False

    # Loading mods
    if settings("load_mods").val:
        try:
            import mods
        except ModError as err:
            error_box = InfoBox(str(err), "Mod-loading Error")
            error_box.center_add(loading_screen.map)
            loading_screen.map.show()
            sys.exit(1)

        for mod in mods.mod_obs:
            mod.mod_p_data(p_data)
    else:
        mods = DummyMods()
    logging.info("[General] %d mods are loaded: (%s)",
                 len(mods.mod_obs), ', '.join(mods.mod_names))

    # validating data
    p_data.validate()

    # Definiton of the playmaps
    # Most of the objects are generated from map_data,
    # but can be extended via map_additions()
    ############################################################

    ob_maps = gen_maps()
    # Those two maps cant to sourced out, because `height` and `width`
    # are global variables exclusive to pokete.py
    centermap = CenterMap(height - 1, width)
    shopmap = ShopMap(height - 1, width)
    ob_maps["centermap"] = centermap
    ob_maps["shopmap"] = shopmap

    # Figure
    figure = Figure(session_info)

    gen_obs()
    map_additions()

    # Definiton of all additionaly needed obs and maps
    #############################################################
    movemap = Movemap(ob_maps, height - 1, width)

    # side fn definitions
    detail = Detail(height - 1, width)
    pokete_dex = Dex(movemap, figure)
    help_page = Help(movemap)
    roadmap = RoadMap(ob_maps, figure)
    deck = Deck()
    menu = Menu(movemap)
    about = About(VERSION, CODENAME, movemap)
    inv = Inv(movemap)
    buy = Buy(figure, movemap)

    # Achievements
    achievements.set_achieved(session_info.get("achievements", []))
    for identifier, args in p_data.achievements.items():
        achievements.add(identifier, **args)

    # A dict that contains all world action functions for Attacks
    abb_funcs = {"teleport": teleport}

    # objects relevant for fight()
    fightmap = FightMap(height - 1, width)
    fightitems = FightItems(fightmap, movemap, figure, ob_maps)

    for _i in [NPC, Trainer]:
        _i.set_vars(movemap, figure, NPCActions, check_walk_back)
    notifier.set_vars(movemap)
    figure.set_args(session_info)

    __t = time.time() - __t
    logging.info("[General] Startup took %fs", __t)

    fd = None
    old_settings = None

    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
