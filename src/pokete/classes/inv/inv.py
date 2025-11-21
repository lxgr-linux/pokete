from typing import Never, Optional

import scrap_engine as se

from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input import Action
from pokete.base.input.hotkeys import ActionList
from pokete.base.input_loops import ask_bool, ask_ok
from pokete.base.ui.elements.text import HightlightableText
from pokete.classes.asset_service.service import asset_service
from pokete.classes.items.invitem import InvItem
from pokete.classes.items.learndisc import LearnDisc
from pokete.classes.poke.poke import Poke
from pokete.figure.inv import Inventory

from .. import deck
from ..learnattack import LearnAttack
from ..poke import upgrade_by_one_lvl
from ..types import types
from .base_inv import BaseInv


class Inv(BaseInv):
    """Inventory to see and manage items in"""

    def __init__(self):
        super().__init__(
            "Inventory", [HightlightableText(f"{Action.REMOVE.mapping}:remove")]
        )
        self.items: list[InvItem] = []

    def choose(self, ctx: Context, idx: int) -> Optional[Never]:
        obj = self.items[self.index.index]
        do_interact = self.invbox(ctx, obj)
        ctx = change_ctx(ctx, self)
        if not do_interact:
            return
        poke: Optional[Poke] = None
        if obj.name == "treat":
            if ask_bool(
                ctx,
                "Do you want to upgrade one of your Poketes by a level?",
            ):
                while True:
                    index = deck.deck(
                        ctx,
                        6,
                        label="Your deck",
                        in_fight=True,
                    )
                    if index is None:
                        ctx.map.show(init=True)
                        break
                    poke = ctx.figure.pokes[index]
                    break
                if poke is None:
                    return
                upgrade_by_one_lvl(ctx, poke)
                self.rem_item(ctx.figure, obj.name)
                ask_ok(
                    ctx,
                    f"{poke.name} reached level {poke.lvl()}!",
                )
        elif isinstance(obj, LearnDisc):
            if ask_bool(
                ctx,
                f"Do you want to teach '{obj.attack.name}'?",
            ):
                while True:
                    index = deck.deck(
                        ctx,
                        6,
                        label="Your deck",
                        in_fight=True,
                    )
                    if index is None:
                        ctx.map.show(init=True)
                        break
                    poke = ctx.figure.pokes[index]
                    if getattr(types, obj.attack.types[0]) in poke.types:
                        break
                    if not ask_bool(
                        ctx,
                        "You can't teach "
                        f"'{obj.attack.name}' to "
                        f"'{poke.name}'! \n"
                        "Do you want to continue?",
                    ):
                        poke = None
                if poke is None:
                    return
                if LearnAttack(poke)(ctx.with_overview(self), obj.attack_name):
                    self.rem_item(ctx.figure, obj.name)
                    if len(self.items) == 0:
                        return None

    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool:
        if action.triggers(Action.REMOVE):
            if ask_bool(
                ctx,
                "Do you really want to throw "
                f"{self.items[self.index.index].pretty_name} away?",
            ):
                self.rem_item(ctx.figure, self.items[self.index.index].name)
                if len(self.items) == 0:
                    return True
        elif action.triggers(Action.INVENTORY):
            return True
        return False

    def __call__(self, ctx: Context[Inventory]):
        self.resize(ctx.map.height - 3, 35)
        self.set_money(ctx.figure)
        self.add_items(ctx.figure)
        with self.add(ctx.map, ctx.map.width - self.width, 0):
            super().__call__(ctx)

    def rem_item(self, figure, name):
        """Removes an item from the inv
        ARGS:
            name: Items name
            items: List of Items
        RETURNS:
            List of Items"""
        figure.remove_item(name)
        self.rem_elems()
        self.add_items(figure)
        if self.items:
            if self.index.index >= len(self.items):
                self.set_index(len(self.items) - 1)

    def add_items(self, figure: Inventory):
        """Adds all items to the box
        RETURNS:
            List of Items"""
        inv = figure.get_inv()
        self.items = [asset_service.get_items()[i] for i in inv if inv[i] > 0]
        self.elems = [
            se.Text(f"{i.pretty_name}s : {inv[i.name]}", state="float")
            for i in self.items
        ]
        self.add_elems()


inv = Inv()
