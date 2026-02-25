from typing import Optional, override

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.ui.views.better_choose_box import BetterChooseBoxView
from pokete.classes.poke.poke import Poke


class DeckItem(se.Box):
    def __init__(self, poke: Poke):
        super().__init__(4, 28)
        self.add_ob(poke.text_name, 12, 0)
        if poke.identifier != "__fallback__":
            for obj, _x, _y in zip(
                [
                    poke.ico,
                    poke.text_lvl,
                    poke.text_hp,
                    poke.tril,
                    poke.trir,
                    poke.hp_bar,
                    poke.text_xp,
                ],
                [0, 12, 12, 18, 27, 19, 12],
                [0, 1, 2, 2, 2, 2, 3],
            ):
                self.add_ob(obj, _x, _y)


class NewDeck(BetterChooseBoxView[int]):
    def __init__(self):
        super().__init__(2, [se.Text(" ")], "Your Deck")
        self.pokes: list[Poke]

    def choose(self, ctx: Context, idx: int) -> Optional[int]:
        return idx

    @override
    def __call__(
        self, ctx: Context, p_len: int, in_fight=False
    ) -> Optional[int]:
        self.pokes = ctx.figure.pokes[:p_len]

        self.set_items(2, [DeckItem(poke) for poke in self.pokes])

        return super().__call__(ctx)
