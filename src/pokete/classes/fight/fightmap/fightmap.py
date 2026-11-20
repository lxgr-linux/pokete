"""This file contains all relevant classes for fight"""

import random
import time
from typing import override

import scrap_engine as se
from scrap_engine.addable.area import Area

from pokete.base import game_map as gm
from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input import Action, get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.input_loops import ask_bool
from pokete.base.mouse import MouseInteractor
from pokete.base.tss import tss
from pokete.base.ui import Overview
from pokete.base.ui.elements import StdFrame2
from pokete.base.ui.elements.text import HightlightableText
from pokete.classes import animations
from pokete.classes.asset_service.service import asset_service
from pokete.classes.deck import Deck
from pokete.classes.effects import Effect
from pokete.classes.fight.fightmap.moves import moves
from pokete.classes.i import IEffect
from pokete.classes.items.invitem import InvItem
from pokete.classes.poke.poke.poke import Poke
from pokete.classes.poke.ui import PokeLabels
from pokete.classes.weather import Weather
from pokete.release import SPEED_OF_TIME

from ...settings import settings
from ..fight_decision import FightDecision
from ..providers import Provider
from .attack import AttackBox
from .inv import InvBox


class FightMap(gm.GameMapWithOutp, Overview, MouseInteractor):
    """Wrapper for gm.GameMap
    ARGS:
        height: The height of the map
        width: The width of the map"""

    def __init__(self, height: int, width: int) -> None:
        super().__init__(height, width, name="fightmap")
        self.mouse_choosen = -1
        self.box = AttackBox()
        self.invbox = InvBox()
        self.providers: list[Provider] = []
        self.poke_labels: list[PokeLabels] = []
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
        self.frame_big = StdFrame2(self.height - 5, self.width, state="float")
        self.frame_small = se.Frame(height=4, width=self.width, state="float")
        self.e_underline = se.Text("----------------+", state="float")
        self.e_sideline = se.Square("|", 1, 3, state="float")
        self.p_upperline = se.Text("+----------------", state="float")
        self.p_sideline = se.Square("|", 1, 4, state="float")
        self.label_attack = HightlightableText(
            f"{Action.CHOOSE_ATTACK.mapping}: Attack", state="float"
        )
        self.label_run = HightlightableText(
            f"{Action.RUN.mapping}: Run!", state="float"
        )
        self.label_inv = HightlightableText(
            f"{Action.CHOOSE_ITEM.mapping}: Inv", state="float"
        )
        self.label_deck = HightlightableText(
            f"{Action.CHOOSE_POKE.mapping}: Deck", state="float"
        )
        self.labels: list[HightlightableText] = [
            self.label_attack,
            self.label_run,
            self.label_inv,
            self.label_deck,
        ]

        # adding
        self.e_underline.add(self, 1, 4)
        self.e_sideline.add(self, len(self.e_underline.text), 1)
        self.add_base_boxes()

    def provider_index(self, provider: Provider) -> None:
        return self.providers.index(provider)

    def provider_labels(self, provider: Provider) -> PokeLabels:
        return self.poke_labels[self.provider_index(provider)]

    @override
    def get_interaction_areas(self) -> list[Area]:
        return [i.get_area() for i in self.labels]

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent) -> None:
        if area_idx >= 0:
            match event.type:
                case MouseEventType.MOVE:
                    for label in self.labels:
                        label.un_highlight()
                    self.labels[area_idx].highlight()
                case MouseEventType.LEFT:
                    if event.pressed:
                        self.mouse_choosen = area_idx
        else:
            for label in self.labels:
                label.un_highlight()
            # self.mouse_choosen = -1

    def set_overview(self, overview: Overview) -> None:
        self.overview = overview

    def add_base_boxes(self) -> None:
        """Adds the basic map layout"""
        self.outp.add(self, 1, self.height - 4)
        self.p_upperline.add(
            self, self.width - 1 - len(self.p_upperline.text), self.height - 10
        )
        self.frame_big.add(self, 0, 0)
        self.p_sideline.add(
            self, self.width - 1 - len(self.p_upperline.text), self.height - 9
        )
        self.frame_small.add(self, 0, self.height - 5)
        x = 0
        for label in self.labels:
            label.add(self, x, self.height - 1)
            x += label.width + 2

    @override
    def resize_view(self) -> None:
        """Manages recursive view resizing"""
        player_added = self.poke_labels[0].ico.added
        enem_added = self.poke_labels[1].ico.added
        for obj in [
            self.outp,
            self.p_upperline,
            self.poke_labels[1].ico,
            self.frame_big,
            self.p_sideline,
            self.frame_small,
        ] + self.labels:
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

    def clean_up(self, *providers: Provider, resize=False) -> None:
        """Removes all labels from self
        ARGS:
            providers: The Providers to clean up that the labels belong to
            resize: Whether or not the box is beeing resized"""
        for prov in providers:
            labels = self.provider_labels(prov)
            for obj in (
                labels.text_name,
                labels.text_lvl,
                labels.hp_bar,
                labels.ico,
                labels.effects,
                prov.curr.pball_small,
            ):
                obj.remove()
            # if not resize:
            #    if isinstance(prov, ProtoFigure):
            #        self.box.box.remove_c_obs()
            # for j in prov.curr.effects:
            #    j.cleanup()

    def __add_player(self, player: Provider, resize=False) -> None:
        """Adds player labels
        ARGS:
            player: The player provider object
            resize: Whether or not the box is beeing resized"""
        labels = self.provider_labels(player)
        labels.text_name.add(self, self.width - 17, self.height - 9)
        labels.text_lvl.add(self, self.width - 17, self.height - 8)
        labels.hp_bar.add(self, self.width - 17, self.height - 7)
        labels.ico.add(self, 3, self.height - 10)
        labels.effects.add(self, self.width - 10, self.height - 8, failsafe=True)
        # if not resize:
        #    self.box.box.add_c_obs(
        #        [atc.label for atc in player.curr.attack_obs]
        #    )
        #    self.box.box.set_index(0)

    def __add_1(self, player: Provider, enem: Provider) -> None:
        """Adds enemy and general labels to self
        ARGS:
            player: The player Poke object
            enem: The enemy Poke object that the labels belong to"""
        labels = self.provider_labels(enem)
        for obj, _x, _y in zip(
            (
                labels.text_name,
                labels.text_lvl,
                labels.hp_bar,
                labels.ico,
                labels.effects,
            ),
            (1, 1, 1, self.width - 14, 8),
            (1, 2, 3, 2, 2),
        ):
            obj.add(self, _x, _y)
        if enem.curr.identifier in player.caught_pokes:
            enem.curr.pball_small.add(self, len(self.e_underline.text) - 1, 1)

    def __add_2(self, player: Provider) -> None:
        """Adds player labels with sleeps
        ARGS:
            player: The player Poke object that the labels belong to"""
        labels = self.provider_labels(player)
        labels.text_name.add(self, self.width - 17, self.height - 9)
        time.sleep(SPEED_OF_TIME * 0.05)
        self.show()
        labels.text_lvl.add(self, self.width - 17, self.height - 8)
        labels.effects.add(self, self.width - 10, self.height - 8, failsafe=True)
        time.sleep(SPEED_OF_TIME * 0.05)
        self.show()
        labels.hp_bar.add(self, self.width - 17, self.height - 7)
        time.sleep(SPEED_OF_TIME * 0.05)
        self.show()
        labels.ico.add(self, 3, self.height - 10)
        # self.box.box.add_c_obs([atc.label for atc in player.curr.attack_obs])
        # self.box.box.set_index(0)

    def fast_change(self, arr, setob) -> None:
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
            Action.QUICK_ATC_1,
            Action.QUICK_ATC_2,
            Action.QUICK_ATC_3,
            Action.QUICK_ATC_4,
        ][: len(player.curr.attack_obs)]
        self.outp.append(
            se.Text(
                ("\n" if "\n" not in self.outp.text else "")
                + "What do you want to do?",
                state="float",
            )
        )
        while True:  # Inputloop for general options
            action, _ = get_action()
            mouse_choosen = -1
            if self.mouse_choosen >= 0:
                mouse_choosen = self.mouse_choosen
                self.mouse_choosen = -1
            if action.triggers(*quick_attacks):
                attack = player.curr.attack_obs[
                    quick_attacks.index(next(i for i in action if i in quick_attacks))
                ]
                if attack.ap > 0:
                    return FightDecision.attack(attack)
            elif (
                action.triggers(Action.CHOOSE_ATTACK, Action.ACCEPT)
                or mouse_choosen == 0
            ):
                attack = self.box(ctx, player.curr.attack_obs)
                if attack is not None:
                    return FightDecision.attack(attack)
            elif action.triggers(Action.RUN) or mouse_choosen == 1:
                if not enem.escapable or not ask_bool(
                    ctx,
                    "Do you really want to run away?",
                ):
                    continue
                return FightDecision.run_away()
            elif action.triggers(Action.CHOOSE_ITEM) or mouse_choosen == 2:
                invitems = asset_service.get_items()
                items: list[InvItem] = [
                    invitems[i]
                    for i in player.get_inv()
                    if invitems[i].func is not None and player.get_inv()[i] > 0
                ]
                if not items:
                    self.outp.outp(
                        "You don't have any items left!\nWhat do you want to do?"
                    )
                    continue
                item = self.invbox(ctx, items, player.get_inv())
                if item is None:
                    continue

                return FightDecision.item(item)
            elif action.triggers(Action.CHOOSE_POKE) or mouse_choosen == 3:
                if not self.choose_poke(ctx, player):
                    self.show(init=True)
                    continue
                return FightDecision.choose_poke(player.play_index)
            ctx = change_ctx(ctx, self)
            loops.std(ctx)
            self.show()

    def add_providers(self, providers: list[Provider]) -> None:
        self.resize_view()
        if settings("animations").val:  # Intro animation
            animations.fight_intro(self.height, self.width)
        self.__add_1(*providers)
        for prov in providers:
            prov.greet(self)
        time.sleep(SPEED_OF_TIME * 1)
        self.__add_2(providers[0])
        ico = self.provider_labels(providers[0]).ico
        self.fast_change([ico, self.deadico2, self.deadico1, ico], ico)
        self.outp.outp(f"You used {providers[0].curr.name}")
        self.show()
        time.sleep(SPEED_OF_TIME * 0.5)

    def add_enemy_after_choosing(self, winner: Provider, enem: Provider) -> None:
        self.__add_1(winner, enem)
        ico = self.provider_labels(enem).ico
        self.fast_change([ico, self.deadico2, self.deadico1, ico], ico)
        self.outp.outp(f"{enem.name} used {enem.curr.name}!")
        self.show()
        time.sleep(SPEED_OF_TIME * 2)

    def choose_poke(
        self, ctx: Context, player: Provider, allow_exit: bool = True
    ) -> None:
        """Lets the player choose another Pokete from their deck
        ARGS:
            player: The players' used Poke
            allow_exit: Whether or not it's allowed to exit without choosing
        RETURNS:
            bool whether or not a Pokete was choosen"""
        index = None
        while index is None:
            index = Deck()(ctx, 6, "Your deck", True)
            if allow_exit:
                break
        if index is not None:
            player.play_index = index
            self.clean_up(player)
            self.poke_labels[self.provider_index(player)] = PokeLabels(player.curr)
            self.__add_player(player)
            self.outp.outp(f"You have choosen {player.curr.name}")
            for j in player.curr.effects:
                time.sleep(SPEED_OF_TIME * 1)
                self.readd_effect(j, player)
        return index is not None

    def death_animation(self, loser: Provider) -> None:
        ico = self.provider_labels(loser).ico
        self.show()
        time.sleep(SPEED_OF_TIME * 1)
        self.fast_change([ico, self.deadico1, self.deadico2], ico)
        self.deadico2.remove()
        self.show()
        self.clean_up(loser)

    def win_animation(self, winner: Provider) -> None:
        time.sleep(SPEED_OF_TIME * 1)
        self.outp.outp(f"{winner.curr.name} reached lvl {winner.curr.lvl()}!")
        winner.curr.moves.shine()
        time.sleep(SPEED_OF_TIME * 0.5)

    def declare_winner(self, winner: Provider, xp: int) -> None:
        time.sleep(SPEED_OF_TIME * 1)
        self.outp.outp(
            f"{winner.curr.ext_name} won!"
            + (f"\nXP + {xp}" if winner.curr.player else "")
        )

    def show_used_all_attacks(self, player: Provider) -> None:
        time.sleep(SPEED_OF_TIME * 2)
        self.outp.outp(f"{player.curr.ext_name} has used all its' attacks!")
        time.sleep(SPEED_OF_TIME * 3)

    def show_death(self, loser: Provider) -> None:
        self.outp.outp(f"{loser.curr.ext_name} is dead!")

    def failed_to_escape(self) -> None:
        self.outp.outp("You failed to run away!")
        time.sleep(SPEED_OF_TIME * 1)

    def ran_away(self, *providers: Provider) -> None:
        self.outp.outp("You ran away!")
        time.sleep(SPEED_OF_TIME * 2)
        self.clean_up(*providers)

    def show_effectivity(
        self, eff: int, n_hp: int, random_factor: int, attacker, attack
    ) -> None:
        eff_text = {
            eff < 1: "\nThat was not effective! ",
            eff > 1: "\nThat was very effective! ",
            eff == 1 or n_hp == 0: "",
            random_factor == 0: f"{attacker.name} missed!",
        }[True]
        self.outp.outp(f"{attacker.ext_name} used {attack.name}! {eff_text}")

    def show_weather(self, weather: Weather) -> None:
        self.outp.outp(weather.info)
        time.sleep(SPEED_OF_TIME * 1.5)

    def set_providers(self, providers: list[Provider]) -> None:
        self.providers = providers
        self.poke_labels = [PokeLabels(p.curr) for p in providers]

    def show_hurt_it_self(self, attacker) -> None:
        time.sleep(SPEED_OF_TIME * 1)
        self.outp.outp(f"{attacker.ext_name} hurt itself!")

    def show_attack_move(self, attack: str, is_player: bool) -> None:
        moves[attack].move(
            *(self.poke_labels if is_player else reversed(self.poke_labels)),
            is_player=is_player,
        )

    def add_effect(self, effect: Effect, poke: Poke, provider: Provider) -> None:
        """Adds the effect to a Pokete
        ARGS:
            obj: The Poke the effect is added to"""
        if poke.type.name in effect.exclude:
            self.outp.rechar(f"{poke.ext_name} is not affected by ")
            self.outp.append(
                se.Text(effect.name, esccode=effect.str_esccode, state="float"),
                se.Text("!", state="float"),
            )
        elif all(type(i) is not type(effect) for i in poke.effects):
            poke.effects.append(effect)
            self.provider_labels(provider).effects.update()
            self.outp.rechar(f"{poke.ext_name} is now ")
            self.outp.append(
                se.Text(effect.name, esccode=effect.str_esccode, state="float"),
                se.Text("!", state="float"),
            )
            effect.log.info("[Effect][%s] Added to %s", effect.name, poke.name)
        else:
            self.outp.rechar(f"{poke.ext_name} is already ")
            self.outp.append(
                se.Text(effect.name, esccode=effect.str_esccode, state="float"),
                se.Text("!", state="float"),
            )
        time.sleep(SPEED_OF_TIME * 2)

    def remove_effect(self, effect: Effect, poke: Poke, provider: Provider) -> None:
        """Removes itself from the current pokete with a certain chance"""
        if random.randint(0, effect.rem_chance) == 0:
            self.outp.outp(f"{poke.ext_name} isn't ")
            self.outp.append(
                se.Text(effect.name, esccode=effect.str_esccode, state="float"),
                se.Text(" anymore!", state="float"),
            )
            i = poke.effects.index(effect)
            del poke.effects[i]
            self.provider_labels(provider).effects.update()
            effect.log.info(
                "[Effect][%s] Removed from  %s", self.name, provider.curr.name
            )
            time.sleep(SPEED_OF_TIME * 2)

    def readd_effect(self, effect: IEffect, provider: Provider) -> None:
        """Readds label and shows text"""
        self.outp.outp(f"{provider.curr.ext_name} is still ")
        self.outp.append(
            se.Text(effect.name, esccode=effect.str_esccode, state="float"),
            se.Text("!", state="float"),
        )
        self.show()
        time.sleep(SPEED_OF_TIME * 2)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
