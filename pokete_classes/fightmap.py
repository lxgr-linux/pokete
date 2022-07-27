"""This file contains all relevant classes for fight"""

import time
import random
import logging
import scrap_engine as se
import pokete_data as p_data
from pokete_general_use_fns import liner
from pokete_classes import animations, ob_maps as obmp, movemap as mvp, \
                           deck, game_map as gm
from .hotkeys import ACTION_UP_DOWN, Action, get_action
from .audio import audio
from .loops import std_loop
from .npcs import Trainer
from .providers import NatureProvider, ProtoFigure
from .ui_elements import StdFrame2, ChooseBox, LabelBox
from .classes import OutP
from .input import ask_bool
from .achievements import achievements
from .inv_items import invitems
from .settings import settings
from release import SPEED_OF_TIME


class FightMap(gm.GameMap):
    """Wrapper for gm.GameMap
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height, width):
        super().__init__(height, width, name="fightmap")
        self.box = ChooseBox(6, 25, "Attacks",
                             f"{Action.INFO.mapping}:Info", index_x=1)
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
        self.label = se.Text(
            f"{Action.CHOOSE_ATTACK.mapping}: Attack  "
            f"{Action.RUN.mapping}: Run!  "
            f"{Action.CHOOSE_ITEM.mapping}: Inv.  "
            f"{Action.CHOOSE_POKE.mapping}: Deck"
        )
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
        # Attack info box
        self.atk_info_box = LabelBox(se.Text(""), "Attack Info")
        self.show_atk_info_box = False

    def clean_up(self, *providers):
        """Removes all labels from self
        ARGS:
            providers: The Providers to clean up
        that the labels belong to"""
        for prov in providers:
            for obj in (
                prov.curr.text_name, prov.curr.text_lvl, prov.curr.text_hp,
                prov.curr.ico, prov.curr.hp_bar, prov.curr.tril, prov.curr.trir,
                prov.curr.pball_small
            ):
                obj.remove()
            if isinstance(prov, ProtoFigure):
                self.box.remove_c_obs()
            for j in prov.curr.effects:
                j.cleanup()

    def add_player(self, player):
        """Adds player labels
        ARGS:
            player: The player Poke object"""
        player.curr.text_name.add(self, self.width - 17, self.height - 9)
        player.curr.text_lvl.add(self, self.width - 17, self.height - 8)
        player.curr.tril.add(self, self.width - 11, self.height - 7)
        player.curr.trir.add(self, self.width - 2, self.height - 7)
        player.curr.hp_bar.add(self, self.width - 10, self.height - 7)
        player.curr.text_hp.add(self, self.width - 17, self.height - 7)
        player.curr.ico.add(self, 3, self.height - 10)
        self.box.add_c_obs([atc.label for atc in player.curr.attack_obs])
        self.box.set_index(0)

    def add_1(self, player, enem):
        """Adds enemy and general labels to self
        ARGS:
            player: The player Poke object
            enemy: The enemy Poke object that the labels belong to"""
        for obj, x, y in zip(
            (
                enem.curr.tril,
                enem.curr.trir,
                enem.curr.text_name,
                enem.curr.text_lvl,
                enem.curr.text_hp,
                enem.curr.ico,
                enem.curr.hp_bar
            ),
            (7, 16, 1, 1, 1, self.width - 14, 8),
            (3, 3, 1, 2, 3, 2, 3)
        ):
            obj.add(self, x, y)
        if enem.curr.identifier in player.caught_pokes:
            enem.curr.pball_small.add(self, len(self.e_underline.text) - 1, 1)


    def add_2(self, player):
        """Adds player labels with sleeps
        ARGS:
            player: The player Poke object that the labels belong to"""
        player.curr.text_name.add(self, self.width - 17, self.height - 9)
        time.sleep(SPEED_OF_TIME * 0.05)
        self.show()
        player.curr.text_lvl.add(self, self.width - 17, self.height - 8)
        time.sleep(SPEED_OF_TIME * 0.05)
        self.show()
        player.curr.tril.add(self, self.width - 11, self.height - 7)
        player.curr.trir.add(self, self.width - 2, self.height - 7)
        player.curr.hp_bar.add(self, self.width - 10, self.height - 7)
        player.curr.text_hp.add(self, self.width - 17, self.height - 7)
        time.sleep(SPEED_OF_TIME * 0.05)
        self.show()
        player.curr.ico.add(self, 3, self.height - 10)
        self.box.add_c_obs([atc.label for atc in player.curr.attack_obs])
        self.box.set_index(0)

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
            time.sleep(SPEED_OF_TIME * 0.1)

    def rechar_atk_info_box(self, attack_obs):
        self.atk_info_box.label.rechar(
            liner(attack_obs[self.box.index.index].desc, 37)
        )
        self.atk_info_box.resize(
            self.atk_info_box.label.height + 2,
            self.atk_info_box.label.width + 4
        )

    def get_attack(self, attack_obs):
        """Inputloop for attack options
        ARGS:
            attack_obs: A list of Attack objects that belong to a Poke"""
        with self.box.add(self, 1, self.height - 7):
            self.rechar_atk_info_box(attack_obs)
            if self.show_atk_info_box:
                self.atk_info_box.add(self, 27, self.height - 7)
            self.show()
            while True:#158
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.box.input(action)
                    self.rechar_atk_info_box(attack_obs)
                    self.show()
                elif action.triggers(Action.ACCEPT) or (0 <= action.get_number()
                        < len(attack_obs)):
                    attack = attack_obs[
                        self.box.index.index if action.triggers(Action.ACCEPT)
                        else action.get_number()
                    ]
                    if attack.ap == 0:
                        continue
                    break
                elif action.triggers(Action.INFO):
                    self.show_atk_info_box = not self.show_atk_info_box
                    if self.show_atk_info_box:
                        self.atk_info_box.add(self, 27, self.height - 7)
                    else:
                        self.atk_info_box.remove()
                    self.show()
                    continue
                elif action.triggers(Action.CANCEL):
                    attack = ""
                    break
                std_loop(False)
            self.atk_info_box.remove()
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
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.invbox.input(action)
                    self.show()
                elif action.triggers(Action.CANCEL):
                    item = ""
                    break
                elif action.triggers(Action.ACCEPT):
                    item = items[self.invbox.index.index]
                    break
                std_loop(False)
        self.invbox.remove_c_obs()
        return item

    def get_figure_attack(self, figure, enem):
        """Chooses the players attack
        ARGS:
            figure: The players provider
            enem: The enemys provider"""
        quick_attacks = [
            Action.QUICK_ATC_1, Action.QUICK_ATC_2,
            Action.QUICK_ATC_3, Action.QUICK_ATC_4
        ][:len(figure.curr.attack_obs)]
        self.outp.append(se.Text(("\n" if "\n" not in self.outp.text
                                          else "") +
                                         "What do you want to do?",
                                         state="float"))
        while True:  # Inputloop for general options
            action = get_action()
            if action.triggers(*quick_attacks):
                attack = figure.curr.attack_obs[
                    quick_attacks.index(
                        next(i for i in action if i in quick_attacks)
                    )
                ]
                if attack.ap > 0:
                    return attack
            elif action.triggers(Action.CHOOSE_ATTACK, Action.ACCEPT):
                attack = self.get_attack(figure.curr.attack_obs)
                if attack != "":
                    return attack
            elif action.triggers(Action.RUN):
                if (
                    type(enem) is Trainer
                    or not ask_bool(self, "Do you really want to run away?")
                ):
                    continue
                if (random.randint(0, 100) < max(5, min(50 - (figure.curr.initiative - enem.curr.initiative), 95))):
                    self.outp.outp("You failed to run away!")
                    time.sleep(SPEED_OF_TIME * 1)
                    return ""
                audio.switch("xDeviruchi - Decisive Battle (End).mp3")
                self.outp.outp("You ran away!")
                time.sleep(SPEED_OF_TIME * 2)
                self.clean_up(figure, enem)
                logging.info("[Fight] Ended, ran away")
                audio.switch(figure.map.song)
                return "won"
            elif action.triggers(Action.CHOOSE_ITEM):
                items = [getattr(invitems, i)
                            for i in figure.inv
                            if getattr(invitems, i).fn is not None
                            and figure.inv[i] > 0]
                if not items:
                    self.outp.outp(
                        "You don't have any items left!\n"
                        "What do you want to do?"
                    )
                    continue
                item = self.get_item(items, figure.inv)
                if item == "":
                    continue
                # I hate you python for not having switch statements
                if (i := getattr(fightitems, item.fn)(figure, enem)) == 1:
                    continue
                elif i == 2:
                    logging.info("[Fight] Ended, fightitem")
                    time.sleep(SPEED_OF_TIME * 2)
                    audio.switch(figure.map.song)
                    return "won"
                return ""
            elif action.triggers(Action.CHOOSE_POKE):
                if not self.choose_poke(figure):
                    self.show(init=True)
                    continue
                return ""
            std_loop(False)

    def fight(self, providers):
        """Fight between two Pokes
        ARGS:
            providers
        RETURNS:
            Provider that won the fight"""
        audio.switch("xDeviruchi - Decisive Battle (Loop).mp3")
        index = 0
        logging.info(
            "[Fight] Started between %s",
            "and ".join(
                f"{prov.curr.name} ({type(prov)}) lvl. {prov.curr.lvl()}"
                    for prov in providers
            )
        )
        weather = providers[0].map.weather
        for prov in providers:
            prov.index_conf()
        if settings("animations").val:  # Intro animation
            animations.fight_intro(self.height, self.width)
        self.add_1(*providers)
        for prov in providers:
            if type(prov) is NatureProvider:
                self.outp.outp(f"A wild {prov.curr.name} appeared!")
            elif type(prov) is Trainer:
                self.outp.outp(f"{prov.name} started a fight!")
                time.sleep(SPEED_OF_TIME * 1)
                self.outp.outp(
                    f'{self.outp.text}\n{prov.gender} used {prov.curr.name} '
                    'against you!'
                )
        time.sleep(SPEED_OF_TIME * 1)
        self.add_2(providers[0])
        self.fast_change([providers[0].curr.ico, self.deadico2, self.deadico1,
                          providers[0].curr.ico], providers[0].curr.ico)
        self.outp.outp(f"You used {providers[0].curr.name}")
        self.show()
        time.sleep(SPEED_OF_TIME * 0.5)
        index = providers.index(
            max(providers, key=lambda i: i.curr.initiative)
        )
        for prov in providers:
            i = prov.curr
            for j in i.effects:
                j.readd()
        while True:
            player = providers[index % 2]
            enem = providers[(index + 1) % 2]

            attack = player.get_attack(self, enem)
            time.sleep(SPEED_OF_TIME * 0.3)
            if attack == "won":
                return player
            elif attack != "":
                player.curr.attack(attack, enem.curr, self, weather)
            self.show()
            time.sleep(SPEED_OF_TIME * 0.5)
            winner = None
            loser = None
            for i, prov in enumerate(providers):
                if prov.curr.hp <= 0:
                    loser = prov
                    winner = providers[(i + 1) % 2]
            if winner is not None:
                self.outp.outp(f"{loser.curr.ext_name} is dead!")
            elif all(i.ap == 0 for i in player.curr.attack_obs):
                winner = providers[(index + 1) % 2]
                loser = player
                time.sleep(SPEED_OF_TIME * 2)
                self.outp.outp(f"{player.curr.ext_name} has used all its' attacks!")
                time.sleep(SPEED_OF_TIME * 3)
            if winner is not None:
                if (
                    type(winner) is Trainer
                    and any(p.hp > 0 for p in loser.pokes[:6])
                ):
                    time.sleep(2)
                    self.choose_poke(loser, False)
                elif (
                    loser.curr.player
                    and any(p.hp > 0 for p in loser.pokes[:6])
                    and ask_bool(self, "Do you want to choose another Pokete?")
                ):
                    success = self.choose_poke(loser)
                    if not success:
                        break
                elif (
                    isinstance(loser, Trainer)
                    and winner.curr.player
                    and any(p.hp > 0 for p in loser.pokes)
                ):
                    time.sleep(SPEED_OF_TIME * 1)
                    ico = loser.curr.ico
                    self.fast_change([ico, self.deadico1, self.deadico2], ico)
                    self.deadico2.remove()
                    self.show()
                    self.clean_up(loser)
                    loser.play_index += 1
                    self.add_1(*providers)
                    ico = loser.curr.ico
                    self.fast_change(
                        [ico, self.deadico2, self.deadico1, ico], ico
                    )
                    self.outp.outp(f"{loser.name} used {loser.curr.name}!")
                    self.show()
                    time.sleep(SPEED_OF_TIME * 2)
                else:
                    break
            index += 1
        audio.switch("xDeviruchi - Decisive Battle (End).mp3")
        time.sleep(SPEED_OF_TIME * 1)
        _xp = sum(
            poke.lose_xp + max(0, poke.lvl() - winner.curr.lvl())
            for poke in loser.pokes
        ) * (2 if not isinstance(loser, NatureProvider) else 1)
        self.outp.outp(
            f"{winner.curr.ext_name} won!" +
            (f'\nXP + {_xp}' if winner.curr.player else '')
        )
        if winner.curr.player and isinstance(loser, Trainer):
            achievements.achieve("first_duel")
        if winner.curr.player and winner.curr.add_xp(_xp):
            time.sleep(SPEED_OF_TIME * 1)
            self.outp.outp(
                f"{winner.curr.name} reached lvl {winner.curr.lvl()}!"
            )
            winner.curr.moves.shine()
            time.sleep(SPEED_OF_TIME * 0.5)
            winner.curr.set_vars()
            winner.curr.learn_attack(self)
            winner.curr.evolve(winner, self)
        self.show()
        time.sleep(SPEED_OF_TIME * 1)
        ico = loser.curr.ico
        self.fast_change([ico, self.deadico1, self.deadico2], ico)
        self.deadico2.remove()
        self.show()
        self.clean_up(*providers)
        mvp.movemap.balls_label_rechar(winner.pokes)
        logging.info(
            "[Fight] Ended, %s(%s) won",
            winner.curr.name, "player" if winner.curr.player else "enemy"
        )
        audio.switch(providers[0].map.song)
        return winner

    def choose_poke(self, player, allow_exit=True):
        """Lets the player choose another Pokete from their deck
        ARGS:
            player: The players' used Poke
            allow_exit: Whether or not it's allowed to exit without choosing
        RETURNS:
            bool whether or not a Pokete was choosen"""
        self.clean_up(player)
        index = None
        while index is None:
            index = deck.deck(6, "Your deck", True)
            if allow_exit:
                break
        if index is not None:
            player.play_index = index
        self.add_player(player)
        self.outp.outp(f"You have choosen {player.curr.name}")
        for j in player.curr.effects:
            time.sleep(SPEED_OF_TIME * 1)
            j.readd()
        if index is None:
            return False
        return True


class FightItems:
    """Contains all fns callable by an item in fight
    The methods that can actually be called in fight follow the following pattern:
        ARGS:
            obj: The players Provider
            enem: The enemys Provider
        RETURNS:
            1: To continue the attack round
            2: To win the game
            None: To let the enemy attack"""

    def throw(self, obj, enem, chance, name):
        """Throws a ball
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

        if not isinstance(enem, NatureProvider):
            fightmap.outp.outp("You can't do that in a duel!")
            return 1
        fightmap.outp.rechar(f"You threw a {name.capitalize()}!")
        fightmap.fast_change([enem.curr.ico, fightmap.deadico1, fightmap.deadico2,
                             fightmap.pball], enem.curr.ico)
        time.sleep(SPEED_OF_TIME * random.choice([1, 2, 3, 4]))
        obj.remove_item(name)
        catch_chance = 20 if obj.map == obmp.ob_maps["playmap_1"] else 0
        for effect in enem.curr.effects:
            catch_chance += effect.catch_chance
        if random.choices([True, False],
                          weights=[(enem.curr.full_hp / enem.curr.hp)
                                   * chance + catch_chance,
                                   enem.curr.full_hp], k=1)[0]:
            audio.switch("xDeviruchi - Decisive Battle (End).mp3")
            obj.add_poke(enem.curr)
            fightmap.outp.outp(f"You caught {enem.curr.name}!")
            time.sleep(SPEED_OF_TIME * 2)
            fightmap.pball.remove()
            fightmap.clean_up(obj, enem)
            mvp.movemap.balls_label_rechar(obj.pokes)
            logging.info("[Fighitem][%s] Caught %s", name, enem.curr.name)
            achievements.achieve("first_poke")
            if all(poke in obj.caught_pokes for poke in p_data.pokes):
                achievements.achieve("catch_em_all")
            return 2
        fightmap.outp.outp("You missed!")
        fightmap.show()
        fightmap.pball.remove()
        enem.curr.ico.add(fightmap, enem.curr.ico.x, enem.curr.ico.y)
        fightmap.show()
        logging.info("[Fighitem][%s] Missed", name)
        return None

    def potion(self, obj, enem, hp, name):
        """Potion function
        ARGS:
            obj: The players Poke object
            enem: The enemys Poke object
            hp: The hp that will be given to the Poke
            name: The potions name"""

        obj.remove_item(name)
        obj.curr.oldhp = obj.curr.hp
        obj.curr.hp = min(obj.curr.full_hp, obj.curr.hp + hp)
        obj.curr.hp_bar.update(obj.curr.oldhp)
        logging.info("[Fighitem][%s] Used", name)

    def heal_potion(self, obj, enem):
        """Healing potion function"""
        return self.potion(obj, enem, 5, "healing_potion")

    def super_potion(self, obj, enem):
        """Super potion function"""
        return self.potion(obj, enem, 15, "super_potion")

    def poketeball(self, obj, enem):
        """Poketeball function"""
        return self.throw(obj, enem, 1, "poketeball")

    def superball(self, obj, enem):
        """Superball function"""
        return self.throw(obj, enem, 6, "superball")

    def hyperball(self, obj, enem):
        """Hyperball function"""
        return self.throw(obj, enem, 1000, "hyperball")

    def ap_potion(self, obj, enem):
        """AP potion function"""
        obj.remove_item("ap_potion")
        for atc in obj.curr.attack_obs:
            atc.set_ap(atc.max_ap)
        logging.info("[Fighitem][ap_potion] Used")


fightitems = FightItems()
fightmap = None


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
