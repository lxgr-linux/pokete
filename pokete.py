#!/usr/bin/env python3
"""This software is licensed under the GPL3
You should have gotten an copy of the GPL3 license anlonside this software
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
import release
from pokete_classes.input.recogniser import recogniser
from pokete_classes.map_additions.map_addtions import map_additions
from pokete_classes.multiplayer.communication import com_service
from pokete_classes.multiplayer.modeprovider import modeProvider, Mode
from pokete_classes.multiplayer.pc_manager import pc_manager, NameTag
from pokete_classes.poke import Stats, EvoMap
from pokete_classes.fight import ProtoFigure
from pokete_classes.generate import gen_maps, gen_obs
from pokete_classes import roadmap
# import pokete_classes.generic_map_handler as gmh
from pokete_classes import animations, loops
from pokete_classes.context import Context
from pokete_classes.inv import inv, buy
from pokete_classes.menu import Menu
from pokete_classes.periodic_events import MovingGrassEvent, MovingWaterEvent, \
    TreatNPCEvent, NotifierEvent
from pokete_classes.poke import Poke
from pokete_classes.color import Color
from pokete_classes.pre_game import PreGameMap
from pokete_classes.save import read_save, save
from pokete_classes.input_loops import text_input
from pokete_classes.ui.elements import InfoBox
from pokete_classes.classes import PlayMap
from pokete_classes.settings import settings
from pokete_classes.audio import audio
from pokete_classes.tss import tss
from pokete_classes.side_loops import loading_screen, Help
from pokete_classes.input import _ev
from pokete_classes.mods import try_load_mods, loaded_mods
from pokete_classes.pokete_care import DummyFigure, pokete_care
from pokete_classes import deck, detail, timer, ob_maps as obmp, \
    movemap as mvp
# import pokete_classes.generic_map_handler as gmh
from pokete_classes.landscape import HighGrass, Poketeball, MapInteract
from pokete_classes.doors import Door
from pokete_classes.npcs import NPC, Trainer
from pokete_classes.ui import notifier
from pokete_classes.input_loops import ask_bool, ask_text, ask_ok
from pokete_classes.achievements import achievements
from pokete_classes.input import (
    get_action, Action, ACTION_DIRECTIONS, hotkeys_from_save
)
from pokete_classes.dex import Dex
from pokete_classes.game import (
    PeriodicEventManager, PeriodicEvent, MapChangeExeption
)
from util import liner, sort_vers

from release import SPEED_OF_TIME
from release import VERSION, CODENAME, SAVEPATH
from util.command import RootCommand, Flag

__t = time.time()


# Class definition
##################

class NPCActions:
    """This class contains all functions callable by NPCs
    All this methods follow the same pattern:
        ARGS:
            npc: The NPC the method belongs to"""

    @staticmethod
    def swap_poke(npc):
        """Swap_poke wrapper"""
        swap_poke(npc.ctx)

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
                npc.ctx,
                "The young boy gifted you $200. Do you want to accept it?"
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
        if ask_bool(npc.ctx, "Do you want to trade a Pokete?"):
            if (index := deck.deck(npc.ctx, 6, "Your deck", True)) is None:
                return
            figure.add_poke(Poke("ostri", 500), index)
            npc.set_used()
            ask_ok(
                npc.ctx,
                f"You received: {figure.pokes[index].name.capitalize()}"
                f" at level {figure.pokes[index].lvl()}.",
            )
            mvp.movemap.text(npc.ctx, npc.x, npc.y, ["Cool, huh?"])

    @staticmethod
    def playmap_50_npc_29(npc):
        """Interaction with npc_28"""
        if pokete_care.poke is None:
            npc.text(["Here you can leave one of your Poketes for some time \
and we will train it."])
            if ask_bool(
                npc.ctx,
                "Do you want to put a Pokete into the Pokete-Care?"
            ):
                if (index := deck.deck(npc.ctx, 6, "Your deck",
                                       True)) is not None:
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
            if ask_bool(npc.ctx, "Do you want it back?"):
                dummy = DummyFigure(pokete_care.poke)
                evomap = EvoMap(npc.ctx.map.height, npc.ctx.map.width)
                while evomap(
                    Context(PeriodicEventManager([]), npc.ctx.map,
                            npc.ctx.overview, dummy),
                    dummy.pokes[0]
                ):
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
            npc.ctx,
            "The man gifted you $100. Do you want to accept it?",
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
                npc.ctx,
                "Do you want to give your Mowcow to the cook?"
            ):
                figure.pokes[figure.pokes.index(poke)] = Poke("__fallback__", 0)
                npc.text(["Here you go, have $1000!"])
                if ask_bool(
                    npc.ctx,
                    "The cook gifted you $1000. "
                    "Do you want to accept it?",
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
        if ask_bool(npc.ctx, "Do you also want to have one?"):
            figure.pokes.append(Poke("mowcow", 2000))
            npc.set_used()

    @staticmethod
    def chat(npc):
        """Starts a chat"""
        npc.chat()


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

    def set(self, x, y):
        if super().set(x, y) == 0:
            self.update_server_pos()

    def add(self, _map, x, y):
        if super().add(_map, x, y) == 0:
            self.update_server_pos()

    def update_server_pos(self):
        if modeProvider.mode == Mode.MULTI:
            com_service.pos_update(self.map.name, self.x, self.y)

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
            cls.money_label.rechar("$" + str(self.__money))  # TODO: Remove
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
            Stats(poke.name, datetime.now(), caught_with=caught_with))
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


# General use functions
#######################

def autosave():
    """Autosaves the game every 5 mins"""
    while True:
        time.sleep(SPEED_OF_TIME * 300)
        if settings("autosave").val:
            save(figure)


def exiter():
    """Exit function"""
    recogniser.reset()
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
            save(figure)
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

class Playmap7Event(PeriodicEvent):
    def tick(self, tick: int):
        _map = obmp.ob_maps["playmap_7"]
        for obj in _map.get_obj("inner_walls").obs \
                   + [i.main_ob for i in _map.trainers] \
                   + [obmp.ob_maps["playmap_7"].get_obj(i)
                      for i in p_data.map_data["playmap_7"]["balls"] if
                      "playmap_7." + i not in figure.used_npcs
                      or not save_trainers]:
            if obj.added and math.sqrt((obj.y - figure.y) ** 2
                                       + (obj.x - figure.x) ** 2) <= 3:
                obj.rechar(obj.bchar)
            else:
                obj.rechar(" ")


extra_actions: dict[str, list[PeriodicEvent]] = {
    "playmap_7": [Playmap7Event()]
}


# main functions
################

def teleport(poke):
    """Teleports the player to another towns pokecenter
    ARGS:
        poke: The Poke shown in the animation"""
    if (obj := roadmap.roadmap(
        Context(PeriodicEventManager([]), mvp.movemap, mvp.movemap, figure),
        choose=True)) is None:
        return
    if settings("animations").val:
        animations.transition(mvp.movemap, poke)
    cen_d = p_data.map_data[obj.name]["hard_obs"]["pokecenter"]
    Door("", state="float", arg_proto={
        "map": obj.name,
        "x": cen_d["x"] + 5,
        "y": cen_d["y"] + 6
    }).action(figure)


def swap_poke(ctx: Context):
    """Trading with other players in the local network"""
    if not ask_bool(
        ctx, "Do you want to trade with another trainer?",
    ):
        return
    port = 65432
    save(figure)
    do = ask_bool(ctx, "Do you want to be the host?")
    if (index := deck.deck(ctx, 6, "Your deck", True)) is None:
        return
    if do:
        with InfoBox(f"Hostname: {socket.gethostname()}\nWaiting...",
                     ctx=ctx):
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
                                    {"mods": loaded_mods.mod_info,
                                     "name": figure.name,
                                     "poke": figure.pokes[index].dict()})))
    else:
        host = ""
        while host == "":
            host = ask_text(ctx, "Please type in the hosts hostname",
                            "Host:", "", "Hostname", 30)
            if host in ["localhost", "127.0.0.1", "0.0.0.0",
                        socket.gethostname()]:
                ask_ok(ctx,
                       "You're not allowed trade with your self!\nYou fool!")
                host = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, port))
            except Exception as err:
                ask_ok(ctx, str(err))
                return
            sock.sendall(
                str.encode(
                    json.dumps({"mods": loaded_mods.mod_info,
                                "name": figure.name,
                                "poke": figure.pokes[index].dict()})))
            data = sock.recv(1024)
            decode_data = json.loads(data.decode())
    logging.info("[Swap_poke] Recieved %s", decode_data)
    mod_info = decode_data.get("mods", {})
    if loaded_mods.mod_info != mod_info:
        ask_ok(
            ctx, f"""Conflicting mod versions!
Your mods: {', '.join(i + '-' + loaded_mods.mod_info[i] for i in loaded_mods.mod_info)}
Your partners mods: {', '.join(i + '-' + mod_info[i] for i in mod_info)}"""
        )
        return
    figure.add_poke(Poke(decode_data["poke"]["name"],
                         decode_data["poke"]["xp"],
                         decode_data["poke"]["hp"]), index)
    figure.pokes[index].set_ap(decode_data["poke"]["ap"])
    save(figure)  # to avoid duping
    ask_ok(ctx,
           f"You received: {figure.pokes[index].name.capitalize()} at level \
{figure.pokes[index].lvl()} from {decode_data['name']}.")


def _game(_map: PlayMap):
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
    mvp.movemap.resize_view()
    mvp.movemap.set(0, 0)
    mvp.movemap.bmap = _map
    pc_manager.movemap_move()
    mvp.movemap.full_show()
    pevm = PeriodicEventManager(
        [
            MovingGrassEvent(_map),
            MovingWaterEvent(_map),
            TreatNPCEvent(),
            NotifierEvent()
        ] + _map.extra_actions())
    ctx = Context(pevm, mvp.movemap, mvp.movemap, figure)
    MapInteract.set_ctx(ctx)  # Npcs need thois global context
    inp_dict = {
        Action.DECK: [deck.deck, (ctx, 6, "Your deck")],
        Action.MAP: [roadmap.roadmap, (ctx,)],
        Action.INVENTORY: [inv, (ctx,)],
        Action.POKEDEX: [Dex(), (ctx,)],
        Action.CLOCK: [timer.clock, (ctx,)],
        Action.MENU: [Menu(), (ctx,)],
        Action.HELP: [Help(), (ctx,)]
    }
    if _map.weather is not None:
        notifier.notify("Weather", "Info", _map.weather.info)
    while True:
        # Directions are not being used yet
        action = get_action()
        if action.triggers(*ACTION_DIRECTIONS):
            figure.direction = ''
            figure.set(
                figure.x + action.get_x_strength(),
                figure.y + action.get_y_strength()
            )
        elif action.triggers(*inp_dict):
            for key, option in inp_dict.items():
                if action.triggers(key):
                    option[0](*option[1])
            _ev.clear()
            mvp.movemap.show(init=True)
        elif action.triggers(Action.CANCEL, Action.EXIT_GAME):
            if ask_bool(ctx, "Do you really wish to exit?"):
                save(figure)
                sys.exit()
        elif action.triggers(Action.CONSOLE):
            inp = text_input(ctx, mvp.movemap.code_label, ":",
                             mvp.movemap.width,
                             (mvp.movemap.width - 2)
                             * mvp.movemap.height - 1)[1:]
            mvp.movemap.code_label.outp(figure.map.pretty_name)
            codes(inp)
            _ev.clear()

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
                pc_manager.movemap_move()
        loops.std(ctx)


def intro(ctx: Context):
    """Intro to Pokete"""
    mvp.movemap.set(0, 0)
    mvp.movemap.bmap = obmp.ob_maps["intromap"]
    mvp.movemap.full_show()
    while figure.name in ["DEFAULT", ""]:
        figure.name = ask_text(
            ctx,
            "Welcome to Pokete!\nPlease choose your name!\n",
            "Name:", "", "Name", 17
        )
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
    PreGameMap()(figure)
    game_map = figure.map
    if figure.name == "DEFAULT":
        intro(
            Context(PeriodicEventManager([]), mvp.movemap, mvp.movemap, figure)
        )
        game_map = obmp.ob_maps["intromap"]
    while True:
        try:
            _game(game_map)
        except MapChangeExeption as err:
            game_map = err.map


# Actual code execution
#######################
if __name__ == "__main__":
    log_flag = Flag(["--log"], "Enables logging")
    mods_flag = Flag(["--no_mods"], "Disables mods")
    audio_flag = Flag(["--no_audio"], "Disables audio")

    do_logging = False
    load_mods = True
    audio.use_audio = True


    def root_fn(ex: str, options: list[str],
                flags: dict[str, list[str]]):
        global do_logging, load_mods
        for flag in flags:
            if log_flag.is_flag(flag):
                do_logging = True
            elif mods_flag.is_flag(flag):
                load_mods = False
            elif audio_flag.is_flag(flag):
                audio.use_audio = False


    c = RootCommand(
        "Pokete", f"{release.CODENAME} v{release.VERSION}", root_fn,
        flags=[log_flag, mods_flag, audio_flag],
        additional_info=f"""All save and logfiles are located in ~{release.SAVEPATH}/
Feel free to contribute.
See README.md for more information.
This software is licensed under the GPLv3, you should have gotten a
copy of it alongside this software.""",
        usage=""
    )

    c.exec()

    print("\033[?1049h")

    # resizing screen
    tss()
    loading_screen()

    # Home global
    HOME = Path.home()

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
    try_load_mods(loading_screen.map)

    # Definiton of the playmaps
    # Most of the objects are generated from map_data,
    # but can be extended via map_additions()
    ############################################################

    obmp.ob_maps = gen_maps(p_data.maps, extra_actions)

    # Figure
    figure = Figure(session_info)
    NameTag.set_args(figure)

    # gen_obs(p_data.map_data, p_data.npcs, p_data.trainers, figure)
    # map_additions(figure)

    # Definiton of all additionaly needed obs and maps
    #############################################################

    mvp.movemap = mvp.Movemap(tss.height - 1, tss.width)

    # A dict that contains all world action functions for Attacks
    abb_funcs = {"teleport": teleport}

    # side fn definitions
    detail.detail = detail.Detail(tss.height - 1, tss.width)
    deck.deck = deck.Deck(tss.height - 1, tss.width, figure, abb_funcs)
    pokete_care.from_dict(session_info.get("pokete_care", {
        "entry": 0,
        "poke": None,
    }))
    timer.time = timer.Time(session_info.get("time", 0))
    timer.clock = timer.Clock(timer.time)
    HighGrass.figure = figure
    Poketeball.figure = figure
    _ev.set_emit_fn(timer.time.emit_input)

    # Achievements
    achievements.set_achieved(session_info.get("achievements", []))
    for identifier, achievement_args in p_data.achievements.items():
        achievements.add(identifier, **achievement_args)

    for _i in [NPC, Trainer]:
        _i.set_vars(NPCActions)
    notifier.set_vars(mvp.movemap)
    figure.set_args(session_info)

    __t = time.time() - __t
    logging.info("[General] Startup took %fs", __t)

    try:
        main()
    except KeyboardInterrupt:
        print("\033[?1049l\033[1A\nKeyboardInterrupt")
    finally:
        exiter()
