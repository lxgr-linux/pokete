"""This file contains all relevant classes for fight"""

import time
import random
import logging
import scrap_engine as se
import pokete_data as p_data
from pokete_classes import animations, ob_maps as obmp, movemap as mvp, \
                           deck, game_map as gm
from .loops import std_loop
from .ui_elements import StdFrame2, ChooseBox
from .classes import OutP
from .input import ask_bool
from .achievements import achievements
from .inv_items import invitems
from .settings import settings
from .event import _ev


class FightMap(gm.GameMap):
    """Wrapper for gm.GameMap
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height, width):
        super().__init__(height, width, name="fightmap")
        self.box = ChooseBox(6, 25, "Attacks", index_x=1)
        self.invbox = ChooseBox(height - 3, 35, "Inventory")
        # icos
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
        self.p_upperline.add(self, self.width - 1 - len(self.p_upperline.text),
                             self.height - 10)
        self.frame_big.add(self, 0, 0)
        self.p_sideline.add(self, self.width - 1 - len(self.p_upperline.text),
                            self.height - 9)
        self.frame_small.add(self, 0, self.height - 5)
        self.label.add(self, 0, self.height - 1)
        self.figure = None

    def clean_up(self, player, enemy):
        """Removes all labels from self
        ARGS:
            player: The player Poke object
            enemy: The enemy Poke object
        that the labels belong to"""
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
        """Adds player labels
        ARGS:
            player: The player Poke object
            enemy: The enemy Poke object
        that the labels belong to"""
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
        """Adds enemy and general labels to self
        ARGS:
            player: The player Poke object
            enemy: The enemy Poke object
        that the labels belong to
            caught_poketes: List of Poke.identifiers of Pokes that have already
                            been caught"""
        for obj, x, y in zip([enemy.tril, enemy.trir,
                              enemy.text_name, enemy.text_lvl,
                              enemy.text_hp, enemy.ico, enemy.hp_bar],
                             [7, 16, 1, 1, 1, self.width - 14, 8],
                             [3, 3, 1, 2, 3, 2, 3]):
            obj.add(self, x, y)
        if enemy.identifier in caught_poketes:
            enemy.pball_small.add(self, len(self.e_underline.text) - 1, 1)
        if player.identifier != "__fallback__":
            self.box.add_c_obs([atc.label for atc in player.attack_obs])
            self.box.set_index(0)
        return [player, enemy]

    def add_2(self, player):
        """Adds player labels with sleeps
        ARGS:
            player: The player Poke object that the labels belong to"""
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
        """Changes fast between a list of texts
        ARGS:
            arr: List of se.Texts that will be changed through
            setob: A reference se.Text with the coordinates the objs in arr
                   will be set to."""
        for _i in range(1, len(arr)):
            arr[_i - 1].remove()
            arr[_i].add(self, setob.x, setob.y)
            self.show()
            time.sleep(0.1)

    def get_attack(self, attack_obs):
        """Inputloop for attack options
        ARGS:
            attack_obs: A list of Attack objects that belong to a Poke"""
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
                std_loop(False)
        return attack

    def get_item(self, items, inv):
        """Inputloop for inv
        ARGS:
            items: List of InvItems that can be choosen from
            inv: The Figures inv"""
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
                std_loop(False)
        self.invbox.remove_c_obs()
        return item

    def fight(self, player, enemy, figure, info):
        """Fight between two Pokes
        ARGS:
            player: The players' used Poke
            enemy: The enemy's used Poke
            figure: Figure object
            info: Dict with information about the fight
                  ({"type": "wild", "player": " "})
        RETURNS:
            Poke object that won the fight"""
        self.figure = figure
        logging.info("[Fight][%s] Started between %s(player) lvl.%d and \
%s(enemy) lvl.%d", info["type"], player.name, player.lvl(), enemy.name,
                     enemy.lvl())
        if settings("animations").val:  # Intro animation
            animations.fight_intro(self.height, self.width)
        players = self.add_1(player, enemy, figure.caught_pokes)
        if info["type"] == "wild":
            self.outp.outp(f"A wild {enemy.name} appeared!")
        elif info["type"] == "duel":
            self.outp.outp(f"{info['player'].name} started a fight!")
            time.sleep(1)
            self.outp.outp(f'{self.outp.text}\n{info["player"].gender} \
used {enemy.name} against you!')
        time.sleep(1)
        self.add_2(player)
        if player.identifier != "__fallback__":
            self.fast_change([player.ico, self.deadico2, self.deadico1,
                              player.ico], player.ico)
            self.outp.outp(f"You used {player.name}")
        self.show()
        time.sleep(0.5)
        if player.identifier == "__fallback__":
            obj, enem = players
        else:
            enem = sorted(zip([i.initiative for i in players],
                              # The [1, 0] array is needed to avoid comparing
                              # two Poke objects
                              [1, 0], players))[0][-1]
            obj = [i for i in players if i != enem][-1]
        for i in players:
            for j in i.effects:
                j.readd()
        while True:
            if obj.player:
                self.outp.append(se.Text(("\n" if "\n" not in self.outp.text
                                          else "") +
                                         "What do you want to do?",
                                         state="float"))
                if obj.identifier == "__fallback__":
                    time.sleep(1)
                    self.outp.outp("You don't have any living poketes left!")
                while True:  # Inputloop for general options
                    if _ev.get() == "'1'":
                        _ev.clear()
                        if player.identifier == "__fallback__":
                            continue
                        attack = self.get_attack(obj.attack_obs)
                        if attack != "":
                            break
                    elif _ev.get() == "'2'":
                        _ev.clear()
                        if ((info["type"] == "duel"
                             and player.identifier != "__fallback__")
                            or not ask_bool(self,
                                            "Do you really want to run away?")):
                            continue
                        if (random.randint(0, 100) < max(5, min(50 - (player.initiative - enemy.initiative), 95))):
                            self.outp.outp("You failed to run away!")
                            time.sleep(1)
                            attack = ""
                            break
                        self.outp.outp("You ran away!")
                        time.sleep(1)
                        self.clean_up(player, enemy)
                        logging.info("[Fight][%s] Ended, ran away",
                                          info["type"])
                        return enem
                    elif _ev.get() == "'3'":
                        _ev.clear()
                        items = [getattr(invitems, i)
                                 for i in figure.inv
                                 if getattr(invitems, i).fn is not None
                                 and figure.inv[i] > 0]
                        if not items:
                            self.outp.outp("You don't have any items left!\n\
 What do you want to do?")
                            continue
                        item = self.get_item(items, figure.inv)
                        if item == "":
                            continue
                        # I hate you python for not having switch statements
                        if (i := getattr(fightitems, item.fn)(obj, enem, info))\
                                == 1:
                            continue
                        elif i == 2:
                            logging.info("[Fight][%s] Ended, fightitem",
                                         info["type"])
                            return obj
                        attack = ""
                        break
                    elif _ev.get() == "'4'":
                        _ev.clear()
                        if obj.identifier == "__fallback__":
                            continue
                        players, player = self.choose_poke(figure, players, player, enemy)
                        attack = ""
                        break
                    std_loop(False)
            else:
                attack = random.choices(obj.attack_obs,
                                        weights=[i.ap * ((1.5
                                                          if enem.type.name in
                                                                i.type.effective
                                                          else 0.5
                                                          if enem.type.name in
                                                                i.type.ineffective
                                                          else 1)
                                                         if info["type"] == "duel"
                                                         else 1)
                                                 for i in obj.attack_obs])[0]
            time.sleep(0.3)
            if attack != "":
                obj.attack(attack, enem, self)
            self.show()
            time.sleep(0.5)
            winner = None
            if any(i.hp <= 0 for i in players):
                winner = [i for i in players if i.hp > 0][0]
            elif all(i.ap == 0 for i in obj.attack_obs):
                winner = [i for i in players if i != obj][0]
                time.sleep(2)
                self.outp.outp(f"{obj.ext_name} has used all its' attacks!")
                time.sleep(3)
            if winner is not None:
                if (obj.identifier != "__fallback__"
                        and not winner.player
                        and any(p.hp > 0 for p in figure.pokes[:6])
                        and ask_bool(self,
                                     "Do you want to choose another Pokete?")):
                    old_player = player
                    players, player = self.choose_poke(figure, players,
                                                       player, enemy)
                    if old_player == player:
                        break
                else:
                    break
            obj = [i for i in players if i != obj][-1]
            enem = [i for i in players if i != obj][-1]
        loser = [obj for obj in players if obj != winner][0]
        _xp = (loser.lose_xp + (1 if loser.lvl() > winner.lvl() else 0))\
                             * (2 if info["type"] == "duel" else 1)
        self.outp.outp(f"{winner.ext_name} won!" + (f'\nXP + {_xp}'
                                                    if winner.player else ''))
        if winner.player and info["type"] == "duel":
            achievements.achieve("first_duel")
        if winner.player and winner.add_xp(_xp):
            time.sleep(1)
            self.outp.outp(f"{winner.name} reached lvl {winner.lvl()}!")
            winner.moves.shine()
            time.sleep(0.5)
            winner.set_vars()
            winner.learn_attack(self)
            winner.evolve(figure, self)
        self.show()
        time.sleep(1)
        ico = [obj for obj in players if obj != winner][0].ico
        self.fast_change([ico, self.deadico1, self.deadico2], ico)
        self.deadico2.remove()
        self.show()
        self.clean_up(player, enemy)
        mvp.movemap.balls_label_rechar(figure.pokes)
        logging.info("[Fight][%s] Ended, %s(%s) won", info["type"],
                     winner.name, "player" if winner.player else "enemy")
        return winner

    def choose_poke(self, figure, players, player, enemy):
        """Lets the player choose another Pokete from their deck
        ARGS:
            figure: Figure object
            players: The list of both player end enemy
            player: The players' used Poke
            enemy: The enemy's used Poke
        RETURNS:
            players: The list of both player end enemy
            player: The players' used Poke"""
        self.clean_up(player, enemy)
        index = deck.deck(6, "Your deck", True)
        player = player if index is None else figure.pokes[index]
        self.add_1(player, enemy, figure.caught_pokes)
        self.box.set_index(0)
        players = self.add_3(player, enemy)
        self.outp.outp(f"You have choosen {player.name}")
        for i in players:
            for j in i.effects:
                time.sleep(1)
                j.readd()
        return players, player


class FightItems:
    """Contains all fns callable by an item in fight
    ARGS:
        figure: Figure object

    The methods that can actually be called in fight follow the following pattern:
        ARGS:
            obj: The players Poke object
            enem: The enemys Poke object
            info: The info dict
        RETURNS:
            1: To continue the attack round
            2: To win the game
            None: To let the enemy attack"""

    def __init__(self, figure):
        self.fig = figure

    def throw(self, obj, enem, info, chance, name):
        """Throws a *ball
        ARGS:
            obj: The players Poke object
            enem: The enemys Poke object
            info: The info dict
            chance: The balls catch chance
            name: The balls name
        RETURNS:
            1: The continue the attack round
            2: The win the game
            None: To let the enemy attack"""

        if obj.identifier == "__fallback__" or info["type"] == "duel":
            return 1
        fightmap.outp.rechar(f"You threw a {name.capitalize()}!")
        fightmap.fast_change([enem.ico, fightmap.deadico1, fightmap.deadico2,
                             fightmap.pball], enem.ico)
        time.sleep(random.choice([1, 2, 3, 4]))
        self.fig.remove_item(name)
        catch_chance = 20 if self.fig.map == obmp.ob_maps["playmap_1"] else 0
        for effect in enem.effects:
            catch_chance += effect.catch_chance
        if random.choices([True, False],
                          weights=[(enem.full_hp / enem.hp)
                                   * chance + catch_chance,
                                   enem.full_hp], k=1)[0]:
            self.fig.add_poke(enem)
            fightmap.outp.outp(f"You caught {enem.name}!")
            time.sleep(2)
            fightmap.pball.remove()
            fightmap.clean_up(obj, enem)
            mvp.movemap.balls_label_rechar(self.fig.pokes)
            logging.info("[Fighitem][%s] Caught %s", name, enem.name)
            achievements.achieve("first_poke")
            if all(poke in self.fig.caught_pokes for poke in p_data.pokes):
                achievements.achieve("catch_em_all")
            return 2
        fightmap.outp.outp("You missed!")
        fightmap.show()
        fightmap.pball.remove()
        enem.ico.add(fightmap, enem.ico.x, enem.ico.y)
        fightmap.show()
        logging.info("[Fighitem][%s] Missed", name)
        return None

    def potion(self, obj, enem, info, hp, name):
        """Potion function
        ARGS:
            obj: The players Poke object
            enem: The enemys Poke object
            info: The info dict
            hp: The hp that will be given to the Poke
            name: The potions name"""

        self.fig.remove_item(name)
        obj.oldhp = obj.hp
        if obj.hp + hp > obj.full_hp:
            obj.hp = obj.full_hp
        else:
            obj.hp += hp
        obj.hp_bar.update(obj.oldhp)
        logging.info("[Fighitem][%s] Used", name)

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
        for atc in obj.attack_obs:
            atc.set_ap(atc.max_ap)
        logging.info("[Fighitem][ap_potion] Used")


class Fight:
    """Wrapper for fightmap.fight
    ARGS:
        figure: The Figure object"""
    def __init__(self, figure):
        self.figure = figure

    def __call__(self, player, enemy, info=None):
        """Wrapper for fightmap.fight
        ARGS:
            player: The players Poke
            enemy: The enemys Poke
            info: Dict containing info about the fight"""
        if info is None:
            info = {"type": "wild", "player": " "}
        return fightmap.fight(player, enemy, self.figure, info)


fight = None
fightitems = None
fightmap = None


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
