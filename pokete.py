#!/usr/bin/env python3
"""This software is licensed under the GPL3
You should have gotten a copy of the GPL3 license anlonside this software
Feel free to contribute what ever you want to this game
New Pokete contributions are especially welcome
For this see the comments in the definations area
You can contribute here: https://github.com/lxgr-linux/pokete
Thanks to MaFeLP for your code review and your great feedback"""


import time
import os
import sys
import threading
import math
import socket
import json
import logging
from pathlib import Path
from datetime import datetime
import scrap_engine as se
import pokete_data as p_data
from pokete_classes import animations
from pokete_classes.pokestats import PokeStats
from pokete_classes.poke import Poke, upgrade_by_one_lvl
from pokete_classes.color import Color
from pokete_classes.ui_elements import Box, ChooseBox, InfoBox, BetterChooseBox, InputBox
from pokete_classes.classes import PlayMap
from pokete_classes.settings import settings, VisSetting, Slider
from pokete_classes.inv_items import invitems, LearnDisc
from pokete_classes.types import types
from pokete_classes.providers import ProtoFigure
from pokete_classes.buy import Buy, InvBox
from pokete_classes.audio import audio
from pokete_classes.tss import tss
from pokete_classes.side_loops import LoadingScreen, About, Help
from pokete_classes.input import text_input, ask_bool, ask_text, ask_ok
from pokete_classes.mods import ModError, ModInfo, DummyMods
from pokete_classes.pokete_care import PoketeCare, DummyFigure
from pokete_classes import deck, detail, game, timer, ob_maps as obmp, \
    movemap as mvp, fightmap as fm
# import pokete_classes.generic_map_handler as gmh
from pokete_classes.landscape import Meadow, Water, Sand, HighGrass, Poketeball, HIGHGRASS_WEIGHT
from pokete_classes.doors import CenterDoor, Door, DoorToCenter, DoorToShop, ChanceDoor
from pokete_classes.learnattack import LearnAttack
from pokete_classes.roadmap import RoadMap
from pokete_classes.npcs import NPC, Trainer
from pokete_classes.notify import notifier
from pokete_classes.achievements import achievements, AchievementOverview
from pokete_classes.event import _ev
from pokete_classes.hotkeys import (
    get_action, Action, ACTION_DIRECTIONS, hotkeys_save, hotkeys_from_save
)
from pokete_classes.dex import Dex
from pokete_classes.loops import std_loop
from pokete_classes.periodic_event_manager import PeriodicEventManager
from pokete_general_use_fns import liner, sort_vers, parse_args

from release import SPEED_OF_TIME
from release import VERSION, CODENAME, SAVEPATH


__t = time.time()


# Class definition
##################

class NPCActions:
    """This class contains all functions callable by NPCs
    All this methods follow the same pattern:
        ARGS:
            npc: The NPC the method belongs to"""

    @staticmethod
    def swap_poke(_):
        """Swap_poke wrapper"""
        swap_poke()

    @staticmethod
    def heal(_):
        """Heal wrapper"""
        figure.heal()

    @staticmethod
    def playmap_13_introductor(npc):
        """Interaction with introductor"""
        if not obmp.ob_maps["playmap_14"].trainers[-1].used:
            npc.text(
                [
                    "To get to the other side of this building, "
                    "you have to win some epic fights against Deepest "
                    "Forests' best trainers!", "This won't be easy!"
                ]
            )
        else:
            npc.text(
                [
                    "It looks like you've been succesfull!",
                    "Congrats!"
                ]
            )
            npc.set_used()

    @staticmethod
    def playmap_17_boy(npc):
        """Interaction with boy"""
        if "choka" in [i.identifier for i in figure.pokes[:6]]:
            npc.text(["Oh, cool!", "You have a Choka!",
                      "I've never seen one before!",
                      "Here you go, have $200!"])
            if ask_bool(
                mvp.movemap,
                "The young boy gifted you $200. Do you want to accept it?",
                mvp.movemap
            ):
                figure.add_money(200)
            npc.set_used()
        else:
            npc.text(["In this region lives the Würgos Pokete.",
                      f"At level {p_data.pokes['würgos']['evolve_lvl']} \
It evolves into Choka.",
                      "I have never seen one before!"])

    @staticmethod
    def playmap_20_trader(npc):
        """Interaction with trader"""
        if ask_bool(mvp.movemap, "Do you want to trade a Pokete?", mvp.movemap):
            if (index := deck.deck(mvp.movemap, 6, "Your deck", True)) is None:
                return
            figure.add_poke(Poke("ostri", 500), index)
            npc.set_used()
            ask_ok(
                mvp.movemap,
                f"You received: {figure.pokes[index].name.capitalize()}"
                f" at level {figure.pokes[index].lvl()}.",
                mvp.movemap
            )
            mvp.movemap.text(npc.x, npc.y, ["Cool, huh?"])

    @staticmethod
    def playmap_50_npc_29(npc):
        """Interaction with npc_28"""
        if pokete_care.poke is None:
            npc.text(["Here you can leave one of your Poketes for some time \
and we will train it."])
            if ask_bool(
                mvp.movemap,
                "Do you want to put a Pokete into the Pokete-Care?",
                mvp.movemap
            ):
                if (index := deck.deck(mvp.movemap, 6, "Your deck", True)) is not None:
                    pokete_care.poke = figure.pokes[index]
                    pokete_care.entry = timer.time.time
                    figure.add_poke(Poke("__fallback__", 0), index)
                    npc.text(["We will take care of it."])
        else:
            add_xp = int((timer.time.time - pokete_care.entry) / 30)
            pokete_care.entry = timer.time.time
            pokete_care.poke.add_xp(add_xp)
            npc.text(["Oh, you're back.", f"Your {pokete_care.poke.name} \
gained {add_xp}xp and reached level {pokete_care.poke.lvl()}!"])
            if ask_bool(mvp.movemap, "Do you want it back?", mvp.movemap):
                dummy = DummyFigure(pokete_care.poke)
                while dummy.pokes[0].evolve(dummy, mvp.movemap):
                    continue
                figure.add_poke(dummy.pokes[0])
                figure.caught_pokes += dummy.caught_pokes
                npc.text(["Here you go!", "Until next time!"])
                pokete_care.poke = None
        npc.text(["See you!"])

    @staticmethod
    def playmap_23_npc_8(npc):
        """Interaction with npc_8"""
        if ask_bool(
            mvp.movemap,
            "The man gifted you $100. Do you want to accept it?", mvp.movemap
        ):
            npc.set_used()
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
    def playmap_39_npc_20(npc):
        """Interaction with npc_20"""
        npc.give("Gerald the farmer", "super_potion")

    @staticmethod
    def playmap_47_npc_26(npc):
        """Interaction with npc_26"""
        npc.give("Poor man", "healing_potion")

    @staticmethod
    def playmap_48_npc_27(npc):
        """Interaction with npc_27"""
        npc.give("Old geezer", "ld_the_old_roots_hit")

    @staticmethod
    def playmap_49_npc_28(npc):
        """Interaction with npc_28"""
        npc.give("Candy man", "treat")

    @staticmethod
    def playmap_42_npc_21(npc):
        """Interaction with npc_21"""
        poke_list = [i for i in figure.pokes[:6]
                     if i.lvl() >= 50 and i.identifier == "mowcow"]
        if len(poke_list) > 0:
            poke = poke_list[0]
            npc.text(["Oh great!", "You're my hero!",
                      f"You brought me a level {poke.lvl()} Mowcow!",
                      "I'm thanking you!",
                      "Now I can still serve the best MowCow-Burgers!",
                      "Can I have it?"])
            if ask_bool(
                mvp.movemap,
                "Do you want to give your Mowcow to the cook?", mvp.movemap
            ):
                figure.pokes[figure.pokes.index(
                    poke)] = Poke("__fallback__", 0)
                npc.text(["Here you go, have $1000!"])
                if ask_bool(
                    mvp.movemap,
                    "The cook gifted you $1000. "
                    "Do you want to accept it?",
                    mvp.movemap
                ):
                    figure.add_money(1000)
                npc.set_used()
        else:
            npc.text(["Ohhh man...", "All of our beef is empty...",
                      "How are we going to serve the best MowCow-Burgers "
                      "without beef?",
                      "If only someone here could bring me a fitting "
                      "Mowcow!?",
                      "But it has to be at least on level 50 to meet our "
                      "high quality standards.",
                      "I will pay a good price!"])

    @staticmethod
    def playmap_39_npc_25(npc):
        """Interaction with npc_25"""
        if not NPC.get("Leader Sebastian").used:
            npc.text(["I can't let you go!",
                      "You first have to defeat our arena leader!"])
            figure.set(figure.x + 1, figure.y)
        else:
            npc.text(["Have a pleasant day."])

    @staticmethod
    def playmap_43_npc_23(npc):
        """Interaction with npc_23"""
        if ask_bool(mvp.movemap, "Do you also want to have one?", mvp.movemap):
            figure.pokes.append(Poke("mowcow", 2000))
            npc.set_used()

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
        mvp.movemap.full_show()
        mvp.movemap.text(
            mvp.movemap.bmap.inner.x - mvp.movemap.x + 8,
            3,
            [
                "Welcome to the Pokete-Center",
                "What do you want to do?",
                "1: See your full deck\n 2: Heal all your Poketes\n 3: Cuddle with the Poketes"
            ]
        )
        while True:
            action = get_action()
            if action.triggers(Action.ACT_1):
                while "__fallback__" in [p.identifier for p in figure.pokes]:
                    figure.pokes.pop([p.identifier for p in
                                      figure.pokes].index("__fallback__"))
                mvp.movemap.balls_label_rechar(figure.pokes)
                deck.deck(mvp.movemap, len(figure.pokes))
                break
            elif action.triggers(Action.ACT_2):
                figure.heal()
                time.sleep(SPEED_OF_TIME * 0.5)
                mvp.movemap.text(
                    mvp.movemap.bmap.inner.x - mvp.movemap.x + 8, 3,
                    ["...", "Your Poketes are now healed!"]
                )
                break
            elif action.triggers(Action.CANCEL, Action.ACT_3):
                break
            std_loop(box=mvp.movemap)
        mvp.movemap.full_show(init=True)


class ShopInteract(se.Object):
    """Triggers a conversation in the shop"""

    def action(self, ob):
        """Triggers an interaction in the shop
        ARGS:
            ob: The object triggering this action"""
        _ev.clear()
        mvp.movemap.full_show()
        mvp.movemap.text(mvp.movemap.bmap.inner.x - mvp.movemap.x + 9, 3,
                         ["Welcome to the Pokete-Shop",
                          "Wanna buy something?"])
        buy()
        mvp.movemap.full_show(init=True)
        mvp.movemap.text(mvp.movemap.bmap.inner.x - mvp.movemap.x + 9, 3,
                         ["Have a great day!"])


class CenterMap(PlayMap):
    """Contains all relevant objects for centermap
    ARGS:
        _he: The maps height
        _wi: The maps width"""

    def __init__(self, _he, _wi):
        super().__init__(_he, _wi, name="centermap",
                         pretty_name="Pokete-Center", song="Map.mp3")
        self.inner = se.Text(""" ________________
 |______________|
 |     |a |     |
 |     ¯ ¯¯     |
 |              |
 |______  ______|
 |_____|  |_____|""", ignore=" ")

        self.interact = CenterInteract("¯", state="float")
        self.dor_back1 = CenterDoor(" ", state="float")
        self.dor_back2 = CenterDoor(" ", state="float")
        self.trader = NPC("trader",
                          ["I'm a trader.",
                           "Here you can trade one of your Poketes for \
one from another trainer."],
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
                         pretty_name="Pokete-Shop", song="Map.mp3")
        self.inner = se.Text(""" __________________
 |________________|
 |      |a |      |
 |      ¯ ¯¯      |
 |                |
 |_______  _______|
 |______|  |______|""", ignore=" ")
        self.interact = ShopInteract("¯", state="float")
        self.dor_back1 = CenterDoor(" ", state="float")
        self.dor_back2 = CenterDoor(" ", state="float")
        # adding
        self.dor_back1.add(self, int(self.width / 2), 8)
        self.dor_back2.add(self, int(self.width / 2) + 1, 8)
        self.inner.add(self, int(self.width / 2) - 9, 1)
        self.interact.add(self, int(self.width / 2), 4)


class Figure(se.Object, ProtoFigure):
    """The figure that moves around on the map and represents the player
    ARGS:
        _si: session_info dict"""

    def __init__(self, _si):
        r_char = _si.get("represent_char", "a")
        if len(r_char) != 1:
            logging.info(
                "[Figure] '%s' is no valid 'represent_char', resetting", r_char)
            r_char = "a"
        super().__init__(r_char, state="solid")
        ProtoFigure.__init__(
            self,
            [Poke.from_dict(_si["pokes"][poke]) for poke in _si["pokes"]],
            escapable=True,
            xp_multiplier=2
        )
        self.__money = _si.get("money", 10)
        self.inv = _si.get("inv", {"poketeballs": 10})
        self.name = _si.get("user", "DEFAULT")
        self.caught_pokes = _si.get("caught_poketes", [])
        self.visited_maps = _si.get("visited_maps", ["playmap_1"])
        self.used_npcs = _si.get("used_npcs", [])
        self.last_center_map = obmp.ob_maps[_si.get("last_center_map",
                                                    "playmap_1")]
        self.oldmap = obmp.ob_maps[_si.get("oldmap", "playmap_1")]
        self.direction = "t"

    def set_args(self, _si):
        """Processes data from save file
        ARGS:
            _si: session_info dict"""
        try:
            # Looking if figure would be in centermap,
            # so the player may spawn out of the center
            if _si["map"] in ["centermap", "shopmap"]:
                _map = obmp.ob_maps[_si["map"]]
                self.add(_map, _map.dor_back1.x, _map.dor_back1.y - 1)
            else:
                if self.add(obmp.ob_maps[_si["map"]], _si["x"], _si["y"]) == 1:
                    raise se.CoordinateError(self, obmp.ob_maps[_si["map"]],
                                             _si["x"], _si["y"])
        except se.CoordinateError:
            self.add(obmp.ob_maps["playmap_1"], 6, 5)
        mvp.movemap.name_label.rechar(self.name, esccode=Color.thicc)
        mvp.movemap.code_label.rechar(self.map.pretty_name)
        mvp.movemap.balls_label_rechar(self.pokes)
        mvp.movemap.add_obs()

    def add_money(self, money):
        """Adds money
        ARGS:
            money: Amount of money being added"""
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
        assert money >= 0, "Money has to be positive."
        logging.info("[Figure] Money set to $%d from $%d",
                     money, self.__money)
        self.__money = money
        for cls in [inv, buy]:
            cls.money_label.rechar("$" + str(self.__money))
            cls.box.set_ob(cls.money_label,
                           cls.box.width - 2 - len(cls.money_label.text), 0)

    def add_poke(self, poke: Poke, idx=None, caught_with=None):
        """Adds a Pokete to the players Poketes
        ARGS:
            poke: Poke object beeing added
            idx: Index of the Poke
            caught_with: Name of ball which was used"""
        poke.set_player(True)
        poke.set_poke_stats(
            PokeStats(poke.name, datetime.now(), caught_with=caught_with))
        self.caught_pokes.append(poke.identifier)
        if idx is None:
            id_list = [i.identifier for i in self.pokes]
            if "__fallback__" in id_list:
                idx = id_list.index("__fallback__")
                self.pokes[idx] = poke
            else:
                self.pokes.append(poke)
        else:
            self.pokes[idx] = poke
        logging.info("[Figure] Added Poke %s", poke.name)

    def give_item(self, item, amount=1):
        """Gives an item to the player"""
        assert amount > 0, "Amounts have to be positive!"
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
        assert amount > 0, "Amounts have to be positive!"
        assert item in self.inv, f"Item {item} is not in the inventory!"
        assert self.inv[item] - amount >= 0, f"There are not enought {item}s \
in the inventory!"
        self.inv[item] -= amount
        logging.info("[Figure] %d %s(s) removed", amount, item)


class Debug:
    """Debug class"""

    @classmethod
    def pos(cls):
        """Prints the figures' position"""
        print(figure.x, figure.y, figure.map.name)


class Inv:
    """Inventory to see and manage items in
    ARGS:
        _map: se.Map this will be shown on"""

    def __init__(self, _map):
        self.map = _map
        self.box = ChooseBox(_map.height - 3, 35, "Inventory",
                             f"{Action.REMOVE.mapping}:remove")
        self.box2 = InvBox(7, 21, overview=self)
        self.money_label = se.Text(f"${figure.get_money()}")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.box.remove()
        self.map.resize_view()
        self.box.resize(self.map.height - 3, 35)
        self.box.add(self.map, self.map.width - self.box.width, 0)
        mvp.movemap.full_show()

    def __call__(self):
        """Opens the inventory"""
        _ev.clear()
        items = self.add()
        self.box.resize(self.map.height - 3, 35)
        with self.box.add(self.map, self.map.width - 35, 0):
            while True:
                action = get_action()
                if action.triggers(Action.UP, Action.DOWN):
                    self.box.input(action)
                elif action.triggers(Action.CANCEL):
                    break
                elif action.triggers(Action.ACCEPT):
                    obj = items[self.box.index.index]
                    self.box2.name_label.rechar(obj.pretty_name)
                    self.desc_label.rechar(liner(obj.desc, 19))
                    self.box2.add(self.map, self.box.x - 19, 3)
                    while True:
                        action = get_action()
                        if (
                            action.triggers(Action.CANCEL)
                            or action.triggers(Action.ACCEPT)
                        ):
                            self.box2.remove()
                            if obj.name == "treat":
                                if ask_bool(
                                    self.map,
                                    "Do you want to upgrade one of "
                                    "your Poketes by a level?",
                                    self
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            mvp.movemap, 6, label="Your deck",
                                            in_fight=True
                                        )
                                        if index is None:
                                            ex_cond = False
                                            self.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        break
                                    if not ex_cond:
                                        break
                                    upgrade_by_one_lvl(poke, figure, self.map)
                                    items = self.rem_item(obj.name, items)
                                    ask_ok(
                                        self.map,
                                        f"{poke.name} reached level "
                                        f"{poke.lvl()}!",
                                        self
                                    )
                            elif isinstance(obj, LearnDisc):
                                if ask_bool(
                                    self.map,
                                    f"Do you want to teach "
                                    f"'{obj.attack_dict['name']}'?",
                                    self
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            mvp.movemap, 6, label="Your deck",
                                            in_fight=True
                                        )
                                        if index is None:
                                            ex_cond = False
                                            self.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        if getattr(types,
                                                   obj.attack_dict['types'][0])\
                                                in poke.types:
                                            break
                                        ex_cond = ask_bool(
                                            self.map,
                                            "You can't teach "
                                            f"'{obj.attack_dict['name']}' to "
                                            f"'{poke.name}'! \n"
                                            "Do you want to continue?",
                                            self
                                        )
                                    if not ex_cond:
                                        break
                                    if LearnAttack(poke, self.map, self)(obj.attack_name):
                                        items = self.rem_item(obj.name, items)
                                        if len(items) == 0:
                                            break
                            break
                        std_loop(box=self.box2)
                        self.map.show()
                elif action.triggers(Action.REMOVE):
                    if ask_bool(
                        self.map,
                        "Do you really want to throw "
                        f"{items[self.box.index.index].pretty_name} away?",
                        self
                    ):
                        items = self.rem_item(items[self.box.index.index].name,
                                              items)
                        if len(items) == 0:
                            break
                std_loop(box=self)
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
        self.box.add_c_obs(
            [
                se.Text(
                    f"{i.pretty_name}s : {figure.inv[i.name]}",
                    state="float"
                )
                for i in items
            ]
        )
        return items


class Menu:
    """Menu to manage settings and other stuff in
    ARGS:
        _map: se.Map this will be shown on"""

    def __init__(self, _map):
        self.map = _map
        self.box = ChooseBox(_map.height - 3, 35, "Menu", overview=_map)
        self.playername_label = se.Text("Playername: ", state="float")
        self.represent_char_label = se.Text("Char: ", state="float")
        self.mods_label = se.Text("Mods", state="float")
        self.ach_label = se.Text("Achievements", state="float")
        self.about_label = se.Text("About", state="float")
        self.save_label = se.Text("Save", state="float")
        self.exit_label = se.Text("Exit", state="float")
        self.realname_label = se.Text(session_info["user"], state="float")
        self.char_label = se.Text(figure.char, state="float")
        self.box.add_c_obs([self.playername_label,
                            self.represent_char_label,
                            VisSetting("Autosave", "autosave",
                                       {True: "On", False: "Off"}),
                            VisSetting("Animations", "animations",
                                       {True: "On", False: "Off"}),
                            VisSetting("Save trainers", "save_trainers",
                                       {True: "On", False: "Off"}),
                            VisSetting("Audio", "audio",
                                       {True: "On", False: "Off"}),
                            Slider("Volume", "volume"),
                            VisSetting("Load mods", "load_mods",
                                       {True: "On", False: "Off"}),
                            self.mods_label, self.ach_label,
                            self.about_label, self.save_label,
                            self.exit_label])
        # adding
        self.box.add_ob(self.realname_label,
                        self.playername_label.rx + self.playername_label.width,
                        self.playername_label.ry)
        self.box.add_ob(self.char_label,
                        self.represent_char_label.rx
                        + self.represent_char_label.width,
                        self.represent_char_label.ry)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.box.remove()
        self.box.overview.resize_view()
        self.box.resize(self.map.height - 3, 35)
        self.box.add(self.map, self.map.width - self.box.width, 0)

    def __call__(self, pevm):
        """Opens the menu"""
        self.box.resize(self.map.height - 3, 35)
        self.realname_label.rechar(figure.name)
        self.char_label.rechar(figure.char)
        audio_before = settings("audio").val
        volume_before = settings("volume").val
        with self.box.add(self.map, self.map.width - self.box.width, 0):
            _ev.clear()
            while True:
                action = get_action()
                i = self.box.c_obs[self.box.index.index]
                if (strength := action.get_x_strength()) != 0:
                    if isinstance(i, Slider):
                        i.change(strength)
                elif action.triggers(Action.ACCEPT):
                    # Fuck python for not having case statements - lxgr
                    #     but it does lmao - Magnus
                    if i == self.playername_label:
                        figure.name = text_input(self.realname_label, self.map,
                                                 figure.name, 18, 17)
                        self.map.name_label_rechar(figure.name)
                    elif i == self.represent_char_label:
                        inp = text_input(self.char_label, self.map,
                                         figure.char, 18, 1)
                        # excludes bad unicode:
                        if (
                            len(inp.encode("utf-8")) != 1
                            and inp not in ["ä", "ö", "ü", "ß"]
                        ):
                            inp = "a"
                            self.char_label.rechar(inp)
                            notifier.notify("Error", "Bad character",
                                            "The chosen character has to be a \
valid single-space character!")
                        figure.rechar(inp)
                    elif i == self.mods_label:
                        ModInfo(mvp.movemap, mods.mod_info)()
                    elif i == self.save_label:
                        # When will python3.10 come out?
                        with InfoBox("Saving....", info="", _map=self.map):
                            # Shows a box displaying "Saving...." while saving
                            save()
                            time.sleep(SPEED_OF_TIME * 1.5)
                    elif i == self.exit_label:
                        save()
                        sys.exit()
                    elif i == self.about_label:
                        about()
                    elif i == self.ach_label:
                        AchievementOverview()(mvp.movemap)
                    elif isinstance(i, VisSetting):
                        i.change()
                if (
                    audio_before != settings("audio").val
                    or volume_before != settings("volume").val
                ):
                    audio.switch(figure.map.song)
                    audio_before = settings("audio").val
                    volume_before = settings("volume").val
                elif action.triggers(Action.UP, Action.DOWN):
                    self.box.input(action)
                elif action.triggers(Action.CANCEL, Action.MENU):
                    break
                std_loop(pevm=pevm, box=self)
                self.map.full_show()


# General use functions
#######################

def autosave():
    """Autosaves the game every 5 mins"""
    while True:
        time.sleep(SPEED_OF_TIME * 300)
        if settings("autosave").val:
            save()


def save():
    """Saves all relevant data to savefile"""
    _si = {
        "user": figure.name,
        "represent_char": figure.char,
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
        "hotkeys": hotkeys_save(),
        # filters doublicates from figure.used_npcs
        "used_npcs": list(dict.fromkeys(figure.used_npcs)),
        "pokete_care": pokete_care.dict(),
        "time": timer.time.time,
    }
    with open(SAVEPATH / "pokete.json", "w+") as file:
        # writes the data to the save file in a nice format
        json.dump(_si, file, indent=4)
    logging.info("[General] Saved")


def read_save():
    """Reads from savefile
    RETURNS:
        session_info dict"""
    Path(SAVEPATH).mkdir(parents=True, exist_ok=True)
    # Default test session_info
    _si = {
        "user": "DEFAULT",
        "represent_char": "a",
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
        "used_npcs": [],
        "hotkeys": {},
        "pokete_care": {
            "entry": 0,
            "poke": None,
        },
        "time": 0
    }

    if os.path.exists(SAVEPATH / "pokete.json"):
        with open(SAVEPATH / "pokete.json") as _file:
            _si = json.load(_file)
    elif os.path.exists(HOME / ".cache" / "pokete" / "pokete.json"):
        with open(HOME / ".cache" / "pokete" / "pokete.json") as _file:
            _si = json.load(_file)
    elif os.path.exists(HOME / ".cache" / "pokete" / "pokete.py"):
        l_dict = {}
        with open(HOME / ".cache" / "pokete" / "pokete.py", "r") as _file:
            exec(_file.read(), {"session_info": _si}, l_dict)
        _si = json.loads(json.dumps(l_dict["session_info"]))
    return _si


def reset_terminal():
    """Resets the terminals state"""
    if sys.platform == "linux":
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def exiter():
    """Exit function"""
    reset_terminal()
    logging.info("[General] Exiting...")
    print("\033[?1049l\033[1A")
    if audio.curr is not None:
        audio.kill()


# Functions needed for mvp.movemap
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
            sys.exit()


# Playmap extra action functions
# Those are adding additional actions to playmaps
#################################################

class ExtraActions:
    """Extra actions class to keep track of extra actions"""

    @staticmethod
    def playmap_7():
        """Cave animation"""
        _map = obmp.ob_maps["playmap_7"]
        for obj in _map.get_obj("inner_walls").obs\
                + [i.main_ob for i in _map.trainers]\
                + [obmp.ob_maps["playmap_7"].get_obj(i)
                    for i in p_data.map_data["playmap_7"]["balls"] if
                    "playmap_7." + i not in figure.used_npcs
                    or not save_trainers]:
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
                         "Test", _map=mvp.movemap) as a:
        while True:
            action = get_action()
            if action.triggers(*ACTION_DIRECTIONS):
                a.input(action)
            elif action.triggers(Action.CANCEL):
                break
            elif action.triggers(Action.ACCEPT):
                a.remove()
                a.set_items(3, [se.Text(i, state="float") for i in ["test",
                                                                    "test", "123", "fuckthesystem"]])
                a.center_add(a.map)
            std_loop()
            a.map.show()


def teleport(poke):
    """Teleports the player to another towns pokecenter
    ARGS:
        poke: The Poke shown in the animation"""
    if (obj := roadmap(mvp.movemap, choose=True)) is None:
        return
    if settings("animations").val:
        animations.transition(mvp.movemap, poke)
    cen_d = p_data.map_data[obj.name]["hard_obs"]["pokecenter"]
    Door("", state="float", arg_proto={
        "map": obj.name,
        "x": cen_d["x"] + 5,
        "y": cen_d["y"] + 6
    }).action(figure)


def swap_poke():
    """Trading with other players in the local network"""
    if not ask_bool(
        mvp.movemap, "Do you want to trade with another trainer?",
        mvp.movemap
    ):
        return
    port = 65432
    save()
    do = ask_bool(mvp.movemap, "Do you want to be the host?", mvp.movemap)
    if (index := deck.deck(mvp.movemap, 6, "Your deck", True)) is None:
        return
    if do:
        with InfoBox(f"Hostname: {socket.gethostname()}\nWaiting...",
                     _map=mvp.movemap):
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
            host = ask_text(mvp.movemap, "Please type in the hosts hostname",
                            "Host:", "", "Hostname", 30, mvp.movemap)
            if host in ["localhost", "127.0.0.1", "0.0.0.0",
                        socket.gethostname()]:
                ask_ok(mvp.movemap,
                       "You're not allowed trade with your self!\nYou fool!",
                       mvp.movemap)
                host = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, port))
            except Exception as err:
                ask_ok(mvp.movemap, str(err), mvp.movemap)
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
        ask_ok(
            mvp.movemap, f"""Conflicting mod versions!
Your mods: {', '.join(i + '-' + mods.mod_info[i] for i in mods.mod_info)}
Your partners mods: {', '.join(i + '-' + mod_info[i] for i in mod_info)}""",
            mvp.movemap
        )
        return
    figure.add_poke(Poke(decode_data["poke"]["name"],
                         decode_data["poke"]["xp"],
                         decode_data["poke"]["hp"]), index)
    figure.pokes[index].set_ap(decode_data["poke"]["ap"])
    save()  # to avoid duping
    ask_ok(mvp.movemap,
           f"You received: {figure.pokes[index].name.capitalize()} at level \
{figure.pokes[index].lvl()} from {decode_data['name']}.", mvp.movemap)


def _game(_map):
    """Game function
    ARGS:
        _map: The map that will be shown"""
    _ev.clear()
    print("\033]0;Pokete - " + _map.pretty_name + "\a", end="")
    if _map.name not in figure.visited_maps:
        figure.visited_maps.append(_map.name)

    if audio.curr is None:
        audio.start(_map.song)
    else:
        audio.switch(_map.song)

    mvp.movemap.code_label.rechar(figure.map.pretty_name)
    mvp.movemap.set(0, 0)
    mvp.movemap.bmap = _map
    mvp.movemap.full_show()
    pevm = PeriodicEventManager(_map)
    inp_dict = {
        Action.DECK: [deck.deck, (mvp.movemap, 6, "Your deck")],
        Action.MAP: [roadmap, (mvp.movemap,)],
        Action.INVENTORY: [inv, ()],
        Action.POKEDEX: [pokete_dex, ()],
        Action.CLOCK: [timer.clock, (mvp.movemap,)],
        Action.MENU: [mvp.movemap.menu, (pevm,)],
        Action.HELP: [help_page, ()]
    }
    if _map.weather is not None:
        notifier.notify("Weather", "Info", _map.weather.info)
    figure.fightWeight = HIGHGRASS_WEIGHT
    while True:
        # Directions are not being used yet
        action = get_action()
        if action.triggers(*ACTION_DIRECTIONS):
            figure.npc = None
            figure.direction = ''
            figure.set(
                figure.x + action.get_x_strength(),
                figure.y + action.get_y_strength()
            )
        elif action.triggers(Action.ACCEPT) and figure.npc != None:
            figure.npc.reaction()
        elif action.triggers(*inp_dict):
            for key, option in inp_dict.items():
                if action.triggers(key):
                    option[0](*option[1])
            _ev.clear()
            mvp.movemap.show(init=True)
        elif action.triggers(Action.CANCEL, Action.EXIT_GAME):
            if ask_bool(
                mvp.movemap, "Do you really wish to exit?",
                mvp.movemap
            ):
                save()
                sys.exit()
        elif action.triggers(Action.CONSOLE):
            inp = text_input(mvp.movemap.code_label, mvp.movemap, ":",
                             mvp.movemap.width,
                             (mvp.movemap.width - 2)
                             * mvp.movemap.height - 1)[1:]
            mvp.movemap.code_label.outp(figure.map.pretty_name)
            codes(inp)
            _ev.clear()
        std_loop(pevm=pevm, box=mvp.movemap)
        for statement, x, y in zip(
            [
                figure.x + 6 > mvp.movemap.x + mvp.movemap.width,
                figure.x < mvp.movemap.x + 6,
                figure.y + 6 > mvp.movemap.y + mvp.movemap.height,
                figure.y < mvp.movemap.y + 6
            ],
            [1, -1, 0, 0],
            [0, 0, 1, -1]
        ):
            if statement:
                mvp.movemap.set(mvp.movemap.x + x, mvp.movemap.y + y)
        mvp.movemap.full_show()


def intro():
    """Intro to Pokete"""
    mvp.movemap.set(0, 0)
    mvp.movemap.bmap = obmp.ob_maps["intromap"]
    mvp.movemap.full_show()
    while figure.name in ["DEFAULT", ""]:
        figure.name = ask_text(
            mvp.movemap,
            "Welcome to Pokete!\nPlease choose your name!\n",
            "Name:", "", "Name", 17, mvp.movemap
        )
    figure.char = figure.name[0]
    mvp.movemap.name_label_rechar(figure.name)
    mvp.movemap.text(4, 3, ["Hello, my child.",
                            "You're now ten years old.",
                            "I think it's now time for you to travel \
the world and be a Pokete-trainer.",
                            "Therefore, I give you this powerful 'Steini', \
15 'Poketeballs' to catch Poketes, and a "
                            "'Healing potion'.",
                            "You will be the best Pokete-Trainer in Nice \
town.",
                            "Now go out and become the best!"])


def parse_obj(_map, name, obj, _dict):
    """Parses an object to a maps attribute and adds it
    ARGS:
        _map: The given PlayMap
        name: Name of the attribute
        obj: Object beeing set
        _dict: Dict containing info"""
    _map.register_obj(name, obj)
    obj.add(_map, _dict["x"], _dict["y"])


def gen_obs():
    """Generates all objects on the maps"""
    map_data = p_data.map_data
    npcs = p_data.npcs
    trainers = p_data.trainers

    # adding all trainer to map
    for i, trainer_list in trainers.items():
        _map = obmp.ob_maps[i]
        for j in trainer_list:
            args = j["args"]
            trainer = Trainer([Poke.wild(*p) for p in j["pokes"]], *args[:-2])
            trainer.add(_map, args[-2], args[-1])
            _map.trainers.append(trainer)

    # generating objects from map_data
    for ob_map, single_map in map_data.items():
        _map = obmp.ob_maps[ob_map]
        for hard_ob, single_hard_ob in single_map["hard_obs"].items():
            parse_obj(_map, hard_ob,
                      se.Text(single_hard_ob["txt"],
                              ignore=" "),
                      single_hard_ob)
        for soft_ob, single_soft_ob in single_map["soft_obs"].items():
            cls = {
                "sand": Sand,
                "meadow": Meadow,
                "water": Water,
            }[single_soft_ob.get("cls", "meadow")]
            parse_obj(_map, soft_ob,
                      cls(single_soft_ob["txt"],
                          _map.poke_args
                          if cls != Water else _map.w_poke_args),
                      single_soft_ob)
        for door, single_door in single_map["dors"].items():
            parse_obj(_map, door,
                      Door(" ", state="float",
                           arg_proto=single_door["args"]),
                      single_door)
        for ball, single_ball in single_map["balls"].items():
            if f'{ob_map}.{ball}' not in figure.used_npcs or not \
                    settings("save_trainers").val:
                parse_obj(_map, ball,
                          Poketeball(f"{ob_map}.{ball}"),
                          single_ball)
    # NPCs
    for npc, _npc in npcs.items():
        NPC(npc, _npc["texts"], _fn=_npc["fn"],
            chat=_npc.get("chat", None)).add(obmp.ob_maps[_npc["map"]],
                                             _npc["x"], _npc["y"])


def gen_maps():
    """Generates all maps
    RETURNS:
        Dict of all PlayMaps"""
    maps = {}
    for ob_map, args in p_data.maps.items():
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
        return False
    ver = sinfo["ver"]
    if VERSION != ver and sort_vers([VERSION, ver])[-1] == ver:
        if not ask_bool(loading_screen.map,
                        liner(f"The save file was created \
on version '{ver}', the current version is '{VERSION}', \
such a downgrade may result in data loss! \
Do you want to continue?", int(tss.width * 2 / 3))):
            sys.exit()
    return VERSION != ver


def main():
    """Main function"""
    os.system("")
    timing = threading.Thread(target=timer.time_threat, daemon=True)
    recognising = threading.Thread(target=recogniser, daemon=True)
    autosaving = threading.Thread(target=autosave, daemon=True)

    timing.start()
    recognising.start()
    autosaving.start()

    ver_change = check_version(session_info)
    # hotkeys
    hotkeys_from_save(session_info.get("hotkeys", {}),
                      loading_screen.map, ver_change)
    game_map = figure.map
    if figure.name == "DEFAULT":
        intro()
        game_map = obmp.ob_maps["intromap"]
    while True:
        try:
            _game(game_map)
        except game.MapChangeExeption as err:
            game_map = err.map


def map_additions():
    """Applies additions to the maps"""

    # playmap_1
    _map = obmp.ob_maps["playmap_1"]
    _map.dor = DoorToCenter()
    # adding
    _map.dor.add(_map, 25, 4)

    # cave_1
    _map = obmp.ob_maps["cave_1"]
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
                         ob_class=HighGrass,
                         ob_args=_map.poke_args,
                         state="float")
    # adding
    _map.inner.add(_map, 0, 0)

    # playmap_3
    _map = obmp.ob_maps["playmap_3"]
    _map.dor = DoorToCenter()
    _map.shopdor = DoorToShop()
    # adding
    _map.dor.add(_map, 25, 6)
    _map.shopdor.add(_map, 61, 6)

    # playmap_4
    _map = obmp.ob_maps["playmap_4"]
    _map.dor_playmap_5 = ChanceDoor("~", state="float",
                                    arg_proto={"chance": 6,
                                               "map": "playmap_5",
                                               "x": 17, "y": 16})
    # adding
    _map.dor_playmap_5.add(_map, 56, 1)

    # playmap_5
    _map = obmp.ob_maps["playmap_5"]
    _map.inner = se.Square(" ", 11, 11, state="float", ob_class=HighGrass,
                           ob_args=_map.poke_args)
    # adding
    _map.inner.add(_map, 26, 1)

    # playmap_7
    _map = obmp.ob_maps["playmap_7"]
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
##############################""", ignore="#", ob_class=HighGrass,
                         ob_args=_map.poke_args, state="float")
    for ob in (_map.get_obj("inner_walls").obs + [i.main_ob for i in _map.trainers] +
               [_map.get_obj(i) for i in p_data.map_data["playmap_7"]["balls"]
                if "playmap_7." + i not in figure.used_npcs
                   or not settings("save_trainers").val]):
        ob.bchar = ob.char
        ob.rechar(" ")
    # adding
    _map.inner.add(_map, 0, 0)

    # playmap_9
    _map = obmp.ob_maps["playmap_9"]
    _map.inner = se.Text("""
#########################
#########################
###       #  #         ##
#         ####          #
#                       #
##                      #
#               #########
############ ############
#########################""", ignore="#", ob_class=HighGrass,
                         ob_args=_map.poke_args, state="float")
    # adding
    _map.inner.add(_map, 2, 1)

    # playmap_13
    _map = obmp.ob_maps["playmap_13"]
    _map.dor = DoorToCenter()
    _map.shopdor = DoorToShop()
    # adding
    _map.dor.add(_map, 14, 29)
    _map.shopdor.add(_map, 52, 29)

    # playmap_19
    _map = obmp.ob_maps["playmap_19"]
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
            ###""", ignore="#", ob_class=HighGrass,
                         ob_args=_map.poke_args, state="float")
    # adding
    _map.inner.add(_map, 0, 0)

    # playmap_21
    _map = obmp.ob_maps["playmap_21"]
    _map.dor_playmap_19 = Door("_", state="float",
                               arg_proto={"map": "playmap_19",
                                          "x": 26, "y": 1})
    _map.dor = DoorToCenter()
    _map.shopdor = DoorToShop()
    # adding
    _map.dor_playmap_19.add(_map, 5, 26)
    _map.dor.add(_map, 10, 7)
    _map.shopdor.add(_map, 34, 7)

    # playmap_30
    _map = obmp.ob_maps["playmap_30"]
    _map.dor = DoorToCenter()
    _map.shopdor = DoorToShop()
    # adding
    _map.dor.add(_map, 13, 7)
    _map.shopdor.add(_map, 30, 7)

    # playmap_39
    _map = obmp.ob_maps["playmap_39"]
    _map.dor = DoorToCenter()
    _map.shopdor = DoorToShop()
    # adding
    _map.dor.add(_map, 44, 52)
    _map.shopdor.add(_map, 122, 64)


# Actual code execution
#######################
if __name__ == "__main__":
    do_logging, load_mods, audio.use_audio = parse_args(sys.argv)
    # deciding on wich input to use
    if sys.platform == "win32":
        import msvcrt

        def recogniser():
            """Gets keyboard input from msvcrt, the Microsoft Visual C++ Runtime"""
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getwch()
                    _ev.set(
                        {
                            ord(char): f"{char.rstrip()}",
                            13: "Key.enter",
                            127: "Key.backspace",
                            8: "Key.backspace",
                            32: "Key.space",
                            27: "Key.esc",
                            3: "exit",
                        }[ord(char)]
                    )

    else:
        import tty
        import termios
        import select

        def recogniser():
            """Use another (not on xserver relying) way to read keyboard input,
                to make this shit work in tty or via ssh,
                where no xserver is available"""
            global fd, old_settings

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            time.sleep(SPEED_OF_TIME * 0.1)
            while True:
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                if rlist:
                    char = sys.stdin.read(1)
                    _ev.set(
                        {
                            ord(char): f"{char.rstrip()}",
                            13: "Key.enter",
                            127: "Key.backspace",
                            32: "Key.space",
                            27: "Key.esc",
                            3: "exit",
                        }[ord(char)]
                    )
                    if ord(char) == 3:
                        reset_terminal()

    print("\033[?1049h")

    # resizing screen
    tss()

    # Home global
    HOME = Path.home()

    # loading screen
    loading_screen = LoadingScreen(VERSION, CODENAME)
    loading_screen()

    # readinf savefile
    session_info = read_save()

    # logging config
    log_file = (SAVEPATH / "pokete.log") if do_logging else None
    logging.basicConfig(filename=log_file,
                        format='[%(asctime)s][%(levelname)s]: %(message)s',
                        level=logging.DEBUG if do_logging else logging.ERROR)
    logging.info("=== Startup Pokete %s v%s ===", CODENAME, VERSION)

    # settings
    settings.from_dict(session_info.get("settings", {}))
    save_trainers = settings("save_trainers").val

    if not load_mods:
        settings("load_mods").val = False

    # Loading mods
    if settings("load_mods").val:
        try:
            import mods
        except ModError as mod_err:
            error_box = InfoBox(str(mod_err), "Mod-loading Error")
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

    obmp.ob_maps = gen_maps()
    # Those two maps cant to sourced out, because `height` and `width`
    # are global variables exclusive to pokete.py
    centermap = CenterMap(tss.height - 1, tss.width)
    shopmap = ShopMap(tss.height - 1, tss.width)
    obmp.ob_maps["centermap"] = centermap
    obmp.ob_maps["shopmap"] = shopmap

    # Figure
    figure = Figure(session_info)

    gen_obs()
    map_additions()

    # Definiton of all additionaly needed obs and maps
    #############################################################

    mvp.movemap = mvp.Movemap(tss.height - 1, tss.width, Menu)

    # A dict that contains all world action functions for Attacks
    abb_funcs = {"teleport": teleport}

    # side fn definitions
    detail.detail = detail.Detail(tss.height - 1, tss.width)
    pokete_dex = Dex(figure)
    help_page = Help(mvp.movemap)
    RoadMap.check_maps()
    roadmap = RoadMap(figure)
    deck.deck = deck.Deck(tss.height - 1, tss.width, figure, abb_funcs)
    about = About(VERSION, CODENAME, mvp.movemap)
    inv = Inv(mvp.movemap)
    buy = Buy(figure, mvp.movemap)
    pokete_care = PoketeCare.from_dict(session_info.get("pokete_care", {
        "entry": 0,
        "poke": None,
    }))
    timer.time = timer.Time(session_info.get("time", 0))
    timer.clock = timer.Clock(timer.time, mvp.movemap)
    HighGrass.figure = figure
    Poketeball.figure = figure
    _ev.set_emit_fn(timer.time.emit_input)

    # Achievements
    achievements.set_achieved(session_info.get("achievements", []))
    for identifier, achievement_args in p_data.achievements.items():
        achievements.add(identifier, **achievement_args)

    # objects relevant for fm.fight()
    fm.fightmap = fm.FightMap(tss.height - 1, tss.width)

    for _i in [NPC, Trainer]:
        _i.set_vars(figure, NPCActions)
    notifier.set_vars(mvp.movemap)
    figure.set_args(session_info)

    __t = time.time() - __t
    logging.info("[General] Startup took %fs", __t)

    fd = None
    old_settings = None

    try:
        main()
    except KeyboardInterrupt:
        print("\033[?1049l\033[1A\nKeyboardInterrupt")
    finally:
        exiter()
