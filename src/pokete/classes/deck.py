from typing import override

import scrap_engine as se

from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.input import Action, ActionList
from pokete.base.ui.elements.labels import GenericActionLabel
from pokete.base.ui.views.better_choose_box import BetterChooseBoxView
from pokete.classes.detail import Detail
from pokete.classes.poke.poke import Poke
from pokete.classes.poke.ui import PokeLabels


class MoveActionLabel(GenericActionLabel):
    def __init__(self) -> None:
        super().__init__(Action.MOVE_POKETE, "move")

    def set_esccode(self, esccode: str):
        self.default_esccode = esccode
        self.un_highlight()


class DeckItem(se.Box):
    def __init__(self, poke: Poke) -> None:
        super().__init__(4, 28)
        self.__labels = PokeLabels(poke)
        self.add_ob(self.__labels.text_name, 12, 0)
        if poke.identifier != "__fallback__":
            for obj, _x, _y in zip(
                [
                    self.__labels.ico,
                    self.__labels.text_lvl,
                    self.__labels.hp_bar,
                    self.__labels.text_xp,
                    self.__labels.effects,
                ],
                [0, 12, 12, 12, 19],
                [0, 1, 2, 3, 1],
            ):
                self.add_ob(obj, _x, _y)


class Deck(BetterChooseBoxView[int]):
    default_label = "Your Deck"

    def __init__(self) -> None:
        super().__init__(2, 3, [se.Text(" ")], self.default_label)
        self.pokes: list[Poke]
        self.in_fight = False
        self.__move_action_label = MoveActionLabel()
        self.info_labels.append(self.__move_action_label)
        self.__move_idx: int | None = None
        self.__p_len = 0

    @override
    def choose(self, ctx: Context, idx: int) -> int | None:
        if self.in_fight:
            return idx
        Detail()(ctx, self.pokes[(self.page * self.rows * self.columns) + idx])
        return None

    @property
    def pointing_poke_idx(self) -> int:
        return (
            (self.page * self.rows * self.columns)
            + self.index[0] * self.columns
            + self.index[1]
        )

    @override
    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool:
        if action.triggers(Action.MOVE_POKETE):
            if self.__move_idx is None:
                self.__move_idx = self.pointing_poke_idx

                self.__move_action_label.set_esccode(Color.blue)
            else:
                page = self.page
                idx = self.index[0] * self.columns + self.index[1]

                poke1 = ctx.figure.pokes[self.__move_idx]
                poke2 = ctx.figure.pokes[self.pointing_poke_idx]
                ctx.figure.pokes[self.__move_idx] = poke2
                ctx.figure.pokes[self.pointing_poke_idx] = poke1

                self.pokes = ctx.figure.pokes[: self.__p_len]
                self.__set_elements()
                self.__move_action_label.set_esccode("")
                self.change_page(page, idx)

                self.__move_idx = None
        return False

    def __set_elements(self):
        self.set_elems(2, 3, [DeckItem(poke) for poke in self.pokes])

    @override
    def __call__(
        self, ctx: Context, p_len: int, label: str = "", in_fight: bool = False
    ) -> int | None:
        self.__p_len = p_len
        self.pokes = ctx.figure.pokes[:p_len]
        self.in_fight = in_fight

        self.name_label.rechar(label if label else self.default_label)
        self.__set_elements()

        return super().__call__(ctx)
