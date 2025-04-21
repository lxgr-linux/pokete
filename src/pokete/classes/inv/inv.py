import logging
import scrap_engine as se

from pokete.classes.asset_service.service import asset_service
from pokete.figure.inv import Inventory
from pokete.util import liner
from pokete.base import loops
from pokete.base.context import Context
from pokete.base.input import Action, get_action, _ev
from pokete.base.input_loops import ask_bool, ask_ok
from pokete.classes.items.learndisc import LearnDisc
from .. import deck
from ..learnattack import LearnAttack
from ..types import types
from ..poke import upgrade_by_one_lvl
from .base_inv import BaseInv


class Inv(BaseInv):
    """Inventory to see and manage items in"""

    def __init__(self):
        super().__init__(
            "Inventory",
            f"{Action.REMOVE.mapping}:remove"
        )

    def __call__(self, ctx: Context[Inventory]):
        """Opens the inventory"""
        self.box.set_ctx(ctx)
        figure = ctx.figure
        _ev.clear()
        items = self.add(figure)
        self.box.resize(ctx.map.height - 3, 35)
        self.set_money(figure)
        with self.box.add(ctx.map, ctx.map.width - 35, 0):
            while True:
                action = get_action()
                if action.triggers(Action.UP, Action.DOWN):
                    self.box.input(action)
                elif action.triggers(Action.CANCEL):
                    break
                elif action.triggers(Action.ACCEPT):
                    obj = items[self.box.index.index]
                    self.invbox.name_label.rechar(obj.pretty_name)
                    self.desc_label.rechar(liner(obj.desc, 19))
                    self.invbox.add(ctx.map, self.box.x - 19, 3)
                    while True:
                        action = get_action()
                        if (
                            action.triggers(Action.CANCEL)
                            or action.triggers(Action.ACCEPT)
                        ):
                            self.invbox.remove()
                            if obj.name == "treat":
                                if ask_bool(
                                    ctx.with_overview(self),
                                    "Do you want to upgrade one of "
                                    "your Poketes by a level?",
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            ctx.with_overview(self), 6,
                                            label="Your deck",
                                            in_fight=True
                                        )
                                        if index is None:
                                            ex_cond = False
                                            ctx.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        break
                                    if not ex_cond:
                                        break
                                    upgrade_by_one_lvl(
                                        ctx.with_overview(self),
                                        poke
                                    )
                                    items = self.rem_item(figure, obj.name,
                                                          items)
                                    ask_ok(
                                        ctx.with_overview(self),
                                        f"{poke.name} reached level "
                                        f"{poke.lvl()}!",

                                    )
                            elif isinstance(obj, LearnDisc):
                                if ask_bool(
                                    ctx.with_overview(self),
                                    f"Do you want to teach "
                                    f"'{obj.attack['name']}'?",
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            ctx.with_overview(self), 6,
                                            label="Your deck",
                                            in_fight=True
                                        )
                                        if index is None:
                                            ex_cond = False
                                            ctx.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        if getattr(types,
                                                   obj.attack['types'][0]) \
                                            in poke.types:
                                            break
                                        ex_cond = ask_bool(
                                            ctx.with_overview(self),
                                            "You can't teach "
                                            f"'{obj.attack['name']}' to "
                                            f"'{poke.name}'! \n"
                                            "Do you want to continue?",
                                        )
                                    if not ex_cond:
                                        break
                                    if LearnAttack(poke)(
                                        ctx.with_overview(self),
                                        obj.attack_name
                                    ):
                                        items = self.rem_item(figure, obj.name,
                                                              items)
                                        if len(items) == 0:
                                            break
                            break
                        loops.std(ctx=ctx.with_overview(self.invbox))
                elif action.triggers(Action.REMOVE):
                    if ask_bool(
                        ctx.with_overview(self),
                        "Do you really want to throw "
                        f"{items[self.box.index.index].pretty_name} away?"
                    ):
                        items = self.rem_item(
                            figure, items[self.box.index.index].name,
                            items
                        )
                        if len(items) == 0:
                            break
                loops.std(ctx=ctx.with_overview(self))
        self.box.remove_c_obs()

    def rem_item(self, figure, name, items):
        """Removes an item from the inv
        ARGS:
            name: Items name
            items: List of Items
        RETURNS:
            List of Items"""
        figure.remove_item(name)
        for obj in self.box.c_obs:
            obj.remove()
        self.box.remove_c_obs()
        items = self.add(figure)
        if not items:
            return items
        if self.box.index.index >= len(items):
            self.box.set_index(len(items) - 1)
        return items

    def add(self, figure:Inventory):
        """Adds all items to the box
        RETURNS:
            List of Items"""
        inv = figure.get_inv()
        items = [asset_service.get_items()[i] for i in inv if inv[i] > 0]
        self.box.add_c_obs(
            [
                se.Text(
                    f"{i.pretty_name}s : {inv[i.name]}",
                    state="float"
                )
                for i in items
            ]
        )
        return items


inv = Inv()
