"""The Deck shows all Poketes a player owns"""

import scrap_engine as se
from typing import Optional

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.exception_propagation import (
    exception_propagating_periodic_event,
)
from pokete.base.game_map import GameMap, GameSubmap
from pokete.base.input import ACTION_DIRECTIONS, Action, get_action
from pokete.base.input_loops import ask_bool, ask_ok
from pokete.base.periodic_event_manager import PeriodicEventManager
from pokete.base.tss import tss
from pokete.base.ui import Overview
from pokete.base.ui.elements import StdFrame2
from pokete.classes import detail

from pokete.base.ui.views.better_choose_box import BetterChooseBoxView

from .poke import Poke

"""
class Index(se.Object):
    def __init__(self):
        super().__init__("*")
        self.index = 0
"""


class Deck(BetterChooseBoxView):
    """Deck to see Poketes in"""

    def __init__(self):
        super().__init__(2, [se.Text("  ")], name="Your full deck")
        self.pokes = []
        self.figure = None
        self.in_fight = False
        self.indici = []

    def choose(self, ctx: Context, idx: int) -> Optional[int]:
        if not self.pokes or self.pokes[idx].identifier == "__fallback__":
            return None
        if self.in_fight:
            if self.pokes[idx].hp > 0:
                return idx
            return None
        else:
            detail.detail(ctx, self.pokes[idx])
            return None

    """
    def rem_pokes(self):
        #Removes all Poketes from the Deck
        for poke in self.pokes:
            self.remove(poke)

    def resize_view(self):
        #Manages recursive view resizing
        self.exit_label.remove()
        self.move_label.remove()
        self.move_free.remove()

        self.submap.resize(tss.height - 1, tss.width)

        self.exit_label.add(self.submap, 0, self.submap.height - 1)
        self.move_label.add(self.submap, 9, self.submap.height - 1)
        self.move_free.add(self.submap, 20, self.submap.height - 1)

        if all(i.ico.map == self.map for i in self.pokes):
            self.rem_pokes()

        while len(self.map.obs) > 0:
            self.map.obs[0].remove()
        self.map.resize(
            5 * int((len(self.pokes) + 1) / 2) + 2,
            tss.width,
            self.map.background,
        )
        self.overview.resize_view()
        se.Text(self.label, esccode=Color.thicc).add(self.map, 2, 0)
        se.Square("|", 1, self.map.height - 2).add(
            self.map, round(self.map.width / 2), 1
        )
        StdFrame2(self.map.height - 1, self.map.width).add(self.map, 0, 0)
        self.add_all(True, not all(i.ico.map == self.map for i in self.pokes))
        self.index.add(
            self.map,
            self.pokes[self.index.index].text_name.x
            + len(self.pokes[self.index.index].text_name.text)
            + 1,
            self.pokes[self.index.index].text_name.y,
        )
    """

    def __call__(self, ctx: Context, p_len, in_fight=False):
        self.figure = ctx.figure
        self.pokes = ctx.figure.pokes[:p_len]
        self.in_fight = in_fight
        self.indici = []
        self.set_items(2, [se.Text(p.name, state="float") for p in self.pokes])
        self.p_len = p_len
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        with self:
            while True:
                action, _ = get_action()
                if action.triggers(*ACTION_DIRECTIONS):
                    self.input(action)
                elif action.triggers(Action.MOVE_POKETE):
                    if len(self.pokes) == 0:
                        continue
                    if not self.indici:
                        self.indici.append(
                            self.index[0] * self.columns + self.index[1])
                    else:
                        self.indici.append(
                            self.index[0] * self.columns + self.index[1])
                        (
                            self.figure.pokes[self.indici[0]],
                            self.figure.pokes[self.indici[1]],
                        ) = self.pokes[self.indici[1]], self.pokes[
                            self.indici[0]]
                        self.pokes = self.figure.pokes[:p_len]
                        self.indici = []
                        self.set_items(2,
                                       [se.Text(p.name, state="float") for p in
                                        self.pokes])
                elif action.triggers(Action.FREE_POKETE):
                    if self.pokes[
                        self.index[0] * self.columns + self.index[
                            1]].identifier == "__fallback__":
                        pass
                    elif (
                        len(
                            [
                                poke
                                for poke in self.pokes
                                if poke.identifier != "__fallback__"
                            ]
                        )
                        <= 1
                    ):
                        ask_ok(ctx, "You can't free all your Poketes")
                    elif ask_bool(
                        ctx,
                        f"Do you really want to free \
                    {self.figure.pokes[self.index[0] * self.columns +
                                       self.index[1]].name}?",
                    ):
                        self.figure.pokes[
                            self.index[0] * self.columns + self.index[
                                1]] = Poke(
                            "__fallback__", 10, 0
                        )
                        self.pokes = self.figure.pokes[: len(self.pokes)]
                        self.set_items(2,
                                       [se.Text(p.name, state="float") for p in
                                        self.pokes])
                        self.figure.balls_label_rechar()
                else:
                    if action.triggers(Action.CANCEL):
                        break
                    if action.triggers(Action.ACCEPT):
                        res = self.choose(
                            ctx, self.index[1] + self.index[0] * self.columns
                        )
                        ctx = change_ctx(ctx, self)
                        if res is not None:
                            return res
                loops.std(ctx)
        return None

    """
    def add_all(self, init=False, no_poke=False):
        #Adds all Poketes to the deck
        #ARGS:
        #    init: Whether or not this happens for the first time
        #    no_poke: Whether or not pokes should be added
        j = 0
        for i, poke in enumerate(self.pokes):
            if not no_poke:
                self.add(
                    poke,
                    self.figure,
                    self.map,
                    1 if i % 2 == 0 else round(self.map.width / 2) + 1,
                    j * 5 + 1,
                )
            if i % 2 == 0 and init:
                se.Square("-", self.map.width - 2, 1).add(self.map, 1, j * 5 + 5)
            if i % 2 == 1:
                j += 1
    """
    """
    def control(self, inp):
        #Processes inputs
        #ARGS:
        #    inp: Inputted string
        if len(self.pokes) <= 1:
            return
        for action in inp:
            if action in ACTION_DIRECTIONS:
                inp = action
                break
        for direction, not_out_of_bounds, index_delta, out_of_bounds_pos in zip(
            [Action.LEFT, Action.RIGHT, Action.DOWN, Action.UP],
            [
                self.index.index != 0,
                self.index.index != len(self.pokes) - 1,
                self.index.index + 2 < len(self.pokes),
                self.index.index - 2 >= 0,
            ],
            [-1, 1, 2, -2],
            [
                len(self.pokes) - 1,
                0,
                self.index.index % 2,
                [i for i in range(len(self.pokes)) if i % 2 == self.index.index % 2][
                    -1
                ],
            ],
        ):
            if inp == direction:
                if not_out_of_bounds:
                    self.index.index += index_delta
                else:
                    self.index.index = out_of_bounds_pos
                break
        self.index.set(
            self.pokes[self.index.index].text_name.x
            + len(self.pokes[self.index.index].text_name.text)
            + 1,
            self.pokes[self.index.index].text_name.y,
        )
    """


deck: Deck = Deck()
