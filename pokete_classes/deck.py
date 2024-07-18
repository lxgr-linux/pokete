"""The Deck shows all Poketes a player owns"""

import scrap_engine as se
from pokete_classes import detail
import pokete_classes.game_map as gm
from .input import (
    ACTION_DIRECTIONS, Action, get_action, _ev
)
import pokete_classes.movemap as mvp
from .input_loops import ask_bool, ask_ok
from .color import Color
from .poke import Poke
from .ui.elements import StdFrame2
from .tss import tss
from . import loops


class Deck(detail.Informer):
    """Deck to see Poketes in"""

    def __init__(self, height, width, figure, abb_funcs):
        self.map = gm.GameMap(height, width, name="deck")
        self.submap = gm.GameSubmap(self.map, 0, 0, height, width, "decksubmap")
        self.exit_label = se.Text(f"{Action.DECK.mapping}: Exit  ")
        self.move_label = se.Text(f"{Action.MOVE_POKETE.mapping}: Move    ")
        self.move_free = se.Text(f"{Action.FREE_POKETE.mapping}: Free")
        self.index = se.Object("*")
        self.figure = figure
        self.abb_funcs = abb_funcs
        self.pokes = []
        self.label = ""
        self.overview = None
        # adding
        self.exit_label.add(self.submap, 0, self.submap.height - 1)
        self.move_label.add(self.submap, 9, self.submap.height - 1)
        self.move_free.add(self.submap, 20, self.submap.height - 1)

    def rem_pokes(self):
        """Removes all Poketes from the Deck"""
        for poke in self.pokes:
            self.remove(poke)

    def resize_view(self):
        """Manages recursive view resizing"""
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
        self.map.resize(5 * int((len(self.pokes) + 1) / 2) + 2, tss.width,
                        self.map.background)
        self.overview.resize_view()
        se.Text(self.label, esccode=Color.thicc).add(self.map, 2, 0)
        se.Square("|", 1, self.map.height - 2).add(self.map,
                                                   round(self.map.width / 2),
                                                   1)
        StdFrame2(self.map.height - 1, self.map.width).add(self.map, 0, 0)
        self.add_all(True, not all(i.ico.map == self.map for i in self.pokes))
        self.index.add(
            self.map,
            self.pokes[self.index.index].text_name.x
            + len(self.pokes[self.index.index].text_name.text) + 1,
            self.pokes[self.index.index].text_name.y
        )

    def __call__(self, overview, p_len, label="Your full deck", in_fight=False):
        """Opens the deck
        ARGS:
            overview: Overview
            p_len: Number of Pokes being included
            label: The displayed label
            in_fight: Whether or not this is called in a fight"""
        self.overview = overview
        self.pokes = self.figure.pokes[:p_len]
        ret_action = None

        self.exit_label.remove()
        self.move_label.remove()
        self.move_free.remove()
        self.submap.resize(tss.height - 1, tss.width)
        self.exit_label.add(self.submap, 0, self.submap.height - 1)
        self.move_label.add(self.submap, 9, self.submap.height - 1)
        self.move_free.add(self.submap, 20, self.submap.height - 1)
        self.map.resize(5 * int((len(self.pokes) + 1) / 2) + 2, tss.width,
                        self.map.background)

        self.label = label
        se.Text(label, esccode=Color.thicc).add(self.map, 2, 0)
        se.Square("|", 1, self.map.height - 2).add(self.map,
                                                   round(self.map.width / 2),
                                                   1)
        StdFrame2(self.map.height - 1, self.map.width).add(self.map, 0, 0)
        self.move_label.rechar(f"{Action.MOVE_POKETE.mapping}: Move    ")
        indici = []
        self.add_all(True)
        self.index.index = 0
        if len(self.pokes) > 0:
            self.index.add(self.map,
                           self.pokes[self.index.index].text_name.x
                           + len(self.pokes[self.index.index].text_name.text)
                           + 1,
                           self.pokes[self.index.index].text_name.y)
        self.submap.full_show(init=True)
        while True:
            action = get_action()
            if action.triggers(*ACTION_DIRECTIONS):
                self.control(action)
            elif action.triggers(Action.DECK, Action.CANCEL):
                self.rem_pokes()
                while len(self.map.obs) > 0:
                    self.map.obs[0].remove()
                self.submap.set(0, 0)
                if ret_action is not None:
                    self.abb_funcs[ret_action](self.pokes[self.index.index])
                return None
            elif action.triggers(Action.MOVE_POKETE):
                if len(self.pokes) == 0:
                    continue
                if not indici:
                    indici.append(self.index.index)
                    self.move_label.rechar(
                        f"{Action.MOVE_POKETE.mapping}: Move to "
                    )
                else:
                    indici.append(self.index.index)
                    self.figure.pokes[indici[0]], self.figure.pokes[indici[1]] = \
                        self.pokes[indici[1]], self.pokes[indici[0]]
                    self.pokes = self.figure.pokes[:p_len]
                    indici = []
                    self.rem_pokes()
                    self.index.set(0, self.map.height - 1)
                    self.add_all()
                    self.index.set(
                        self.pokes[self.index.index].text_name.x
                        + len(self.pokes[self.index.index].text_name.text) + 1,
                        self.pokes[self.index.index].text_name.y)
                    self.move_label.rechar(
                        f"{Action.MOVE_POKETE.mapping}: Move    "
                    )
                    self.submap.full_show()
            elif action.triggers(Action.FREE_POKETE):
                if self.pokes[self.index.index].identifier == "__fallback__":
                    pass
                elif len(
                    [
                        poke for poke in self.pokes
                        if poke.identifier != "__fallback__"
                    ]
                ) <= 1:
                    ask_ok(self.submap, "You can't free all your Poketes", self)
                elif ask_bool(self.submap, f"Do you really want to free \
{self.figure.pokes[self.index.index].name}?", self):
                    self.rem_pokes()
                    self.figure.pokes[self.index.index] = Poke("__fallback__",
                                                               10, 0)
                    self.pokes = self.figure.pokes[:len(self.pokes)]
                    self.add_all()
                    self.index.set(
                        self.pokes[self.index.index].text_name.x
                        + len(self.pokes[self.index.index].text_name.text)
                        + 1,
                        self.pokes[self.index.index].text_name.y)
                    mvp.movemap.balls_label_rechar(self.figure.pokes)
            elif action.triggers(Action.ACCEPT):
                if len(self.pokes) == 0 or \
                    self.pokes[self.index.index].identifier == "__fallback__":
                    continue
                if in_fight:
                    if self.pokes[self.index.index].hp > 0:
                        self.rem_pokes()
                        while len(self.map.obs) > 0:
                            self.map.obs[0].remove()
                        self.submap.set(0, 0)
                        return self.index.index
                else:
                    self.rem_pokes()
                    ret_action = detail.detail(
                        self.pokes[self.index.index],
                        overview=self
                    )
                    self.add_all()
                    self.index.set(
                        self.pokes[self.index.index].text_name.x
                        + len(self.pokes[self.index.index].text_name.text) + 1,
                        self.pokes[self.index.index].text_name.y)
                    if ret_action is not None:
                        _ev.set(Action.CANCEL.mapping)
                        continue
                    self.submap.full_show(init=True)
            loops.std(False, box=self)
            if len(self.pokes) > 0 and \
                self.index.y - self.submap.y + 6 > self.submap.height:
                self.submap.set(self.submap.x, self.submap.y + 1)
            elif len(self.pokes) > 0 and self.index.y - 1 < self.submap.y:
                self.submap.set(self.submap.x, self.submap.y - 1)
            self.submap.full_show()

    def add_all(self, init=False, no_poke=False):
        """Adds all Poketes to the deck
        ARGS:
            init: Whether or not this happens for the first time
            no_poke: Whether or not pokes should be added"""
        j = 0
        for i, poke in enumerate(self.pokes):
            if not no_poke:
                self.add(poke, self.figure, self.map,
                         1 if i % 2 == 0
                         else round(self.map.width / 2) + 1, j * 5 + 1)
            if i % 2 == 0 and init:
                se.Square("-", self.map.width - 2, 1).add(self.map, 1,
                                                          j * 5 + 5)
            if i % 2 == 1:
                j += 1

    def control(self, inp):
        """Processes inputs
        ARGS:
            inp: Inputted string"""
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
                [
                    i for i in range(len(self.pokes))
                    if i % 2 == self.index.index % 2
                ][-1]
            ]
        ):
            if inp == direction:
                if not_out_of_bounds:
                    self.index.index += index_delta
                else:
                    self.index.index = out_of_bounds_pos
                break
        self.index.set(
            self.pokes[self.index.index].text_name.x
            + len(self.pokes[self.index.index].text_name.text) + 1,
            self.pokes[self.index.index].text_name.y
        )


deck = None
