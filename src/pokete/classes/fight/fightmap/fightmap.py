"""This file contains all relevant classes for fight"""

import time
import scrap_engine as se

from pokete.release import SPEED_OF_TIME
from pokete.base import game_map as gm
from pokete.base.context import Context
from pokete.base.input_loops import ask_bool
from pokete.base.tss import tss
from pokete.base import loops
from pokete.base.ui import Overview
from pokete.base.input import Action, get_action
from pokete.base.ui.elements import StdFrame2
from pokete.classes.items.invitem import InvItem
from pokete.classes.asset_service.service import asset_service
from pokete.classes import animations, deck
from ..fight_decision import FightDecision
from ..providers import ProtoFigure, Provider
from ...classes import OutP
from ...settings import settings
from .attack import AttackBox
from .inv import InvBox


class FightMap(gm.GameMap, Overview):
    """Wrapper for gm.GameMap
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height, width):
        super().__init__(height, width, name="fightmap")
        self.box = AttackBox()
        self.invbox = InvBox(height - 3, 35, "Inventory", overview=self)
        self.providers: list[Provider] = []
        self.overview: Overview
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
        self.e_underline.add(self, 1, 4)
        self.e_sideline.add(self, len(self.e_underline.text), 1)
        self.add_base_boxes()

    def set_overview(self, overview: Overview):
        self.overview = overview

    def add_base_boxes(self):
        """Adds the basic map layout"""
        self.outp.add(self, 1, self.height - 4)
        self.p_upperline.add(self, self.width - 1 - len(self.p_upperline.text),
                             self.height - 10)
        self.frame_big.add(self, 0, 0)
        self.p_sideline.add(self, self.width - 1 - len(self.p_upperline.text),
                            self.height - 9)
        self.frame_small.add(self, 0, self.height - 5)
        self.label.add(self, 0, self.height - 1)

    def resize_view(self):
        """Manages recursive view resizing"""
        player_added = self.providers[0].curr.ico.added
        enem_added = self.providers[1].curr.ico.added
        for obj in [
            self.outp, self.p_upperline, self.providers[1].curr.ico,
            self.frame_big, self.p_sideline, self.frame_small, self.label
        ]:
            obj.remove()
        self.clean_up(self.providers[0], resize=True)

        self.resize(tss.height - 1, tss.width, background=" ")
        self.frame_big.resize(self.height - 5, self.width)
        self.frame_small.resize(4, self.width)
        self.overview.resize_view()

        self.add_base_boxes()
        if player_added:
            self.__add_player(self.providers[0], resize=True)
        if enem_added:
            self.providers[1].curr.ico.add(self, self.width - 14, 2)

    def clean_up(self, *providers, resize=False):
        """Removes all labels from self
        ARGS:
            providers: The Providers to clean up that the labels belong to
            resize: Whether or not the box is beeing resized"""
        for prov in providers:
            for obj in (
                prov.curr.text_name, prov.curr.text_lvl, prov.curr.text_hp,
                prov.curr.ico, prov.curr.hp_bar, prov.curr.tril, prov.curr.trir,
                prov.curr.pball_small
            ):
                obj.remove()
            if not resize:
                if isinstance(prov, ProtoFigure):
                    self.box.box.remove_c_obs()
            for j in prov.curr.effects:
                j.cleanup()

    def __add_player(self, player, resize=False):
        """Adds player labels
        ARGS:
            player: The player provider object
            resize: Whether or not the box is beeing resized"""
        player.curr.text_name.add(self, self.width - 17, self.height - 9)
        player.curr.text_lvl.add(self, self.width - 17, self.height - 8)
        player.curr.tril.add(self, self.width - 11, self.height - 7)
        player.curr.trir.add(self, self.width - 2, self.height - 7)
        player.curr.hp_bar.add(self, self.width - 10, self.height - 7)
        player.curr.text_hp.add(self, self.width - 17, self.height - 7)
        player.curr.ico.add(self, 3, self.height - 10)
        if not resize:
            self.box.box.add_c_obs(
                [atc.label for atc in player.curr.attack_obs])
            self.box.box.set_index(0)

    def __add_1(self, player, enem):
        """Adds enemy and general labels to self
        ARGS:
            player: The player Poke object
            enem: The enemy Poke object that the labels belong to"""
        for obj, _x, _y in zip(
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
            obj.add(self, _x, _y)
        if enem.curr.identifier in player.caught_pokes:
            enem.curr.pball_small.add(self, len(self.e_underline.text) - 1, 1)

    def __add_2(self, player):
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
        self.box.box.add_c_obs([atc.label for atc in player.curr.attack_obs])
        self.box.box.set_index(0)

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

    def get_figure_attack(
        self, ctx: Context, player: Provider, enem: Provider
    ) -> FightDecision:
        """Chooses the players attack
        ARGS:
            player: The players provider
            enem: The enemys provider"""
        quick_attacks = [
                            Action.QUICK_ATC_1, Action.QUICK_ATC_2,
                            Action.QUICK_ATC_3, Action.QUICK_ATC_4
                        ][:len(player.curr.attack_obs)]
        self.outp.append(se.Text(("\n" if "\n" not in self.outp.text
                                  else "") +
                                 "What do you want to do?",
                                 state="float"))
        while True:  # Inputloop for general options
            action = get_action()
            if action.triggers(*quick_attacks):
                attack = player.curr.attack_obs[
                    quick_attacks.index(
                        next(i for i in action if i in quick_attacks)
                    )
                ]
                if attack.ap > 0:
                    return FightDecision.attack(attack)
            elif action.triggers(Action.CHOOSE_ATTACK, Action.ACCEPT):
                attack = self.box(ctx, player.curr.attack_obs)
                if attack != "":
                    return FightDecision.attack(attack)
            elif action.triggers(Action.RUN):
                if (
                    not enem.escapable
                    or not ask_bool(
                    ctx,
                    "Do you really want to run away?",
                )):
                    continue
                return FightDecision.run_away()
            elif action.triggers(Action.CHOOSE_ITEM):
                invitems = asset_service.get_items()
                items: list[InvItem] = [
                    invitems[i]
                    for i in player.inv
                    if invitems[i].func is not None
                       and player.inv[i] > 0]
                if not items:
                    self.outp.outp(
                        "You don't have any items left!\n"
                        "What do you want to do?"
                    )
                    continue
                item = self.invbox(ctx, items, player.inv)
                if item is None:
                    continue

                return FightDecision.item(item)
            elif action.triggers(Action.CHOOSE_POKE):
                if not self.choose_poke(ctx, player):
                    self.show(init=True)
                    continue
                return FightDecision.choose_poke(player.play_index)
            loops.std(ctx)
            self.show()

    def add_providers(self, providers: list[Provider]):
        self.resize_view()
        if settings("animations").val:  # Intro animation
            animations.fight_intro(self.height, self.width)
        self.__add_1(*providers)
        for prov in providers:
            prov.greet(self)
        time.sleep(SPEED_OF_TIME * 1)
        self.__add_2(providers[0])
        self.fast_change(
            [providers[0].curr.ico, self.deadico2, self.deadico1,
             providers[0].curr.ico], providers[0].curr.ico)
        self.outp.outp(f"You used {providers[0].curr.name}")
        self.show()
        time.sleep(SPEED_OF_TIME * 0.5)

    def add_enemy_after_choosing(self, winner, enem):
        self.__add_1(winner, enem)
        ico = enem.curr.ico
        self.fast_change(
            [ico, self.deadico2, self.deadico1, ico],
            ico
        )
        self.outp.outp(f"{enem.name} used {enem.curr.name}!")
        self.show()
        time.sleep(SPEED_OF_TIME * 2)

    def choose_poke(self, ctx: Context, player, allow_exit=True):
        """Lets the player choose another Pokete from their deck
        ARGS:
            player: The players' used Poke
            allow_exit: Whether or not it's allowed to exit without choosing
        RETURNS:
            bool whether or not a Pokete was choosen"""
        self.clean_up(player)
        index = None
        while index is None:
            index = deck.deck(ctx, 6, "Your deck", True)
            if allow_exit:
                break
        if index is not None:
            player.play_index = index
        self.__add_player(player)
        self.outp.outp(f"You have choosen {player.curr.name}")
        for j in player.curr.effects:
            time.sleep(SPEED_OF_TIME * 1)
            j.readd()
        if index is None:
            return False
        return True

    def death_animation(self, loser: Provider):
        ico = loser.curr.ico
        self.show()
        time.sleep(SPEED_OF_TIME * 1)
        self.fast_change([ico, self.deadico1, self.deadico2], ico)
        self.deadico2.remove()
        self.show()
        self.clean_up(loser)

    def win_animation(self, winner: Provider):
        time.sleep(SPEED_OF_TIME * 1)
        self.outp.outp(
            f"{winner.curr.name} reached lvl {winner.curr.lvl()}!"
        )
        winner.curr.moves.shine()
        time.sleep(SPEED_OF_TIME * 0.5)

    def declare_winner(self, winner: Provider, xp: int):
        time.sleep(SPEED_OF_TIME * 1)
        self.outp.outp(
            f"{winner.curr.ext_name} won!" +
            (f'\nXP + {xp}' if winner.curr.player else '')
        )

    def show_used_all_attacks(self, player: Provider):
        time.sleep(SPEED_OF_TIME * 2)
        self.outp.outp(
            f"{player.curr.ext_name} has used all its' attacks!")
        time.sleep(SPEED_OF_TIME * 3)

    def show_death(self, loser: Provider):
        self.outp.outp(f"{loser.curr.ext_name} is dead!")

    def failed_to_escape(self):
        self.outp.outp("You failed to run away!")
        time.sleep(SPEED_OF_TIME * 1)

    def ran_away(self, *providers):
        self.outp.outp("You ran away!")
        time.sleep(SPEED_OF_TIME * 2)
        self.clean_up(*providers)

    def show_effectivity(self, eff: int, n_hp: int, random_factor: int,
                         attacker, attack):
        eff_text = {
            eff < 1: "\nThat was not effective! ",
            eff > 1: "\nThat was very effective! ",
            eff == 1 or n_hp == 0: "",
            random_factor == 0: f"{attacker.name} missed!"}[True]
        self.outp.outp(
            f'{attacker.ext_name} used {attack.name}! {eff_text}')

    def show_weather(self, weather):
        self.outp.outp(weather.info)
        time.sleep(SPEED_OF_TIME * 1.5)

    def set_providers(self, providers: list[Provider]):
        self.providers = providers

    def show_hurt_it_self(self, attacker):
        time.sleep(SPEED_OF_TIME * 1)
        self.outp.outp(f'{attacker.ext_name} hurt itself!')


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
